from xhtml2pdf import pisa
import io

def compile_pdf(worksheet_data):
    # 1. Initialize empty HTML structural blocks
    html_problems = ""
    html_answers = ""
    
    # 2. Loop through your saved session memory to build the document body text
    for i, item in enumerate(worksheet_data):
        # Clean up LaTeX characters that PDF readers can't read natively
        clean_eq = item["equation"].replace("\\quad", " ").replace("=", " = ")
        clean_sol = item["solution"].replace("\\quad", "   ").replace("\\", "")
        
        # Build the HTML string for the student sheet
        html_problems += f"""
        <div class="problem-container">
            <p class="problem-num">Exercise {i+1}:</p>
            <p class="math-text">{clean_eq}</p>
        </div>
        """
        
        # Build the HTML string for the tutor answer key
        html_answers += f"""
        <div class="answer-container">
            <p><b>Solution {i+1}:</b> <span class="math-text">{clean_sol}</span></p>
        </div>
        <hr/>
        """
        
    # 3. The Master Page Template (The CSS style code lives here)
    master_template = f"""
    <html>
    <head>
        <style>
            @page {{ 
                size: letter; 
                margin: 25mm 20mm 25mm 20mm; 
            }}
            body {{ 
                font-family: Helvetica, Arial, sans-serif; 
                color: #2c3e50; 
            }}
            h1 {{ text-align: center; color: #2c3e50; }}
            .section-title {{ font-size: 16pt; font-weight: bold; margin-top: 20px; border-bottom: 2px solid #bdc3c7; padding-bottom: 5px; }}
            .problem-container {{ margin-bottom: 40px; }}
            .problem-num {{ font-weight: bold; margin-bottom: 5px; color: #34495e; }}
            .math-text {{ font-family: 'Times New Roman', Times, serif; font-style: italic; font-size: 16pt; margin-left: 20px; }}
            .page-break {{ page-break-before: always; }}
        </style>
    </head>
    <body>
        <h1>Quadratic Equations Worksheet</h1>
        <div class="section-title">Student Copy</div>
        <br/><br/>
        
        {html_problems}
        
        <div class="page-break"></div>
        
        <h1>Answer Key</h1>
        <div class="section-title">Tutor Reference Copy</div>
        <br/><br/>
        
        {html_answers}
    </body>
    </html>
    """
    
    # 4. Run the data through the digital RAM pipeline factory
    pdf_buffer = io.BytesIO()
    pisa.CreatePDF(io.StringIO(master_template), dest=pdf_buffer)
    
    # 5. Return the raw 1s and 0s back to the main program
    return pdf_buffer.getvalue()