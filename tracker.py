import uuid
from datetime import datetime, timezone

import streamlit as st
from supabase import Client, create_client

try:
    from streamlit_cookies_manager import EncryptedCookieManager
    COOKIES_AVAILABLE = True
except ImportError:
    COOKIES_AVAILABLE = False

COOKIE_PASSWORD = st.secrets["COOKIE_PASSWORD"]

# Supabase client

@st.cache_resource
def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_resource
def get_admin_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    service_key = st.secrets["SUPABASE_SERVICE_KEY"]
    return create_client(url, service_key)

# Visitor identity (persistent across sessions via cookie)

def get_visitor_id() -> str:
    if not COOKIES_AVAILABLE:
        if "visitor_id" not in st.session_state:
            st.session_state.visitor_id = str(uuid.uuid4())
        return st.session_state.visitor_id

    cookies = EncryptedCookieManager(prefix="mathgen/", password=COOKIE_PASSWORD)
    if not cookies.ready():
        st.stop() 

    if cookies.get("visitor_id") is None:
        cookies["visitor_id"] = str(uuid.uuid4())
        cookies.save()

    return cookies["visitor_id"]


# ---------------------------------------------------------------------------
# Event logging
# ---------------------------------------------------------------------------

def log_event(visitor_id: str, event_type: str, meta: dict | None = None):
    client = get_client()
    client.table("events").insert({
        "visitor_id": visitor_id,
        "event_type": event_type,
        "meta": meta or {},
        "ts": datetime.now(timezone.utc).isoformat(),
    }, returning="minimal").execute()


# Admin dashboard — call this behind a query param / password, not publicly

def show_admin_dashboard():
    import pandas as pd

    client = get_admin_client()
    response = client.table("events").select("*").order("ts", desc=True).limit(10000).execute()
    df = pd.DataFrame(response.data)

    st.header("📊 Analytics")

    if df.empty:
        st.info("No events logged yet.")
        return

    
    df["ts"] = pd.to_datetime(df["ts"], format="ISO8601")
    df["date"] = df["ts"].dt.date

    distinct_visitors = df["visitor_id"].nunique()

    visits_per_visitor = df.groupby("visitor_id")["date"].nunique()
    repeat_visitors = (visits_per_visitor >= 2).sum()

    generations = (df["event_type"] == "worksheet_generated").sum()
    downloads = (df["event_type"] == "pdf_downloaded").sum()
    visitors_who_generated = df[df["event_type"] == "worksheet_generated"]["visitor_id"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Distinct visitors", distinct_visitors)
    col2.metric("Repeat visitors (2+ days)", repeat_visitors)
    col3.metric("Repeat rate", f"{repeat_visitors / distinct_visitors:.0%}" if distinct_visitors else "—")

    col4, col5, col6 = st.columns(3)
    col4.metric("Worksheets generated", int(generations))
    col5.metric("PDFs downloaded", int(downloads))
    col6.metric("Visitors who generated ≥1", visitors_who_generated)

    st.subheader("Events by day")
    daily = df.groupby(["date", "event_type"]).size().reset_index(name="count")
    daily["date"] = daily["date"].astype(str)
 
    import plotly.express as px
 
    fig = px.bar(
        daily,
        x="date",
        y="count",
        color="event_type",
        barmode="group",  # side-by-side bars instead of stacked
    )
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Event breakdown")
    st.dataframe(df["event_type"].value_counts().rename("count"))

    st.subheader("Raw event log")
    st.dataframe(df.head(200))

    st.download_button(
        "Download full event log as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="analytics_export.csv",
        mime="text/csv",
    )