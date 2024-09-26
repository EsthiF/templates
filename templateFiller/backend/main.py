from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .processor import WordTemplateProcessor

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Route for the template selection page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to display form based on the selected template
@app.get("/form/{template_name}", response_class=HTMLResponse)
async def get_form(request: Request, template_name: str):
    # Serve a predefined form for each template
    return templates.TemplateResponse(f"{template_name}_form.html", {
        "request": request, 
        "template_name": template_name
    })

# Route to handle form submission and document generation
@app.post("/form/{template_name}", response_class=HTMLResponse)
async def submit_form(request: Request, template_name: str, name: str = Form(...), date: str = Form(...), address: str = Form(...)):
    # Create a dictionary to map answers to placeholders
    placeholder_dict = {
        "{{NAME}}": name,
        "{{DATE}}": date,
        "{{ADDRESS}}": address
    }
    
    # Process and fill the Word template
    processor = WordTemplateProcessor(template_name)
    processor.load_template()
    processor.replace_placeholders(placeholder_dict)
    processor.save_document(f'../output/{template_name}_filled.docx')
    
    return f"{template_name} document filled and saved successfully!"
