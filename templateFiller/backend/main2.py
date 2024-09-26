import os
import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.processor import WordTemplateProcessor
from backend.assessor_names import AssessorNames

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="backend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{template_name}_form", response_class=HTMLResponse)
async def serve_form(request: Request, template_name: str):
    years = list(range(2020, 2051))  # Years dropdown from 2020 to 2050
    template_file = f"{template_name}_form.html"
    return templates.TemplateResponse(template_file, {"request": request, "assessors": AssessorNames, "years": years})

def format_date(date_string):
    if date_string:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").strftime("%d/%m/%Y")
    return None

# Generic route to process any form submission (POST request)
@app.post("/process_form", response_class=HTMLResponse)
async def process_form(
    request: Request, 
    template_name: str = Form(...), 
    company_name: str = Form(None),
    company_name_1: str = Form(None), 
    company_name_2: str = Form(None), 
    company_name_3: str = Form(None),       
    date_1: str = Form(None),  
    date_2: str = Form(None),  
    date_3: str = Form(None),    
    date_4: str = Form(None),  
    date_5: str = Form(None),  
    sum: str = Form(None),   
    pakid_shuma: str = Form(None),    
    pakid_shuma_1: str = Form(None),    
    address_pkid_shuma: str = Form(None),  
    address: str = Form(None),
    city: str = Form(None),           
    c_r_number: str = Form(None),   
    c_r_number_1: str = Form(None),  
    c_r_number_2: str = Form(None),      
    year: str = Form(None),
    year_1: str = Form(None),  
    total_amount: str = Form(None), 
    total_amount_1: str = Form(None), 
    amount_1: str = Form(None),
    n_amount: str = Form(None),
    n_amount_1: str = Form(None),
    amount_2: str = Form(None),
    m_amount: str = Form(None),
    m_amount_1: str = Form(None),
    l_amount: str = Form(None), 
    l_amount_1: str = Form(None), 
    amount_3: str = Form(None),
    amount_4: str = Form(None),
    amount_5: str = Form(None),
    amount_6: str = Form(None),
    name: str = Form(None),
    name_2: str = Form(None),
    country_code: str = Form(None),
    phone_number: str = Form(None),
    email: str = Form(None),
    asset_1: str = Form(None),
    asset_2: str = Form(None),
    sum_1: str = Form(None),
    sum_2: str = Form(None),
    value: str = Form(None),

):  
    formatted_date_1 = format_date(date_1)
    formatted_date_2 = format_date(date_2)
    formatted_date_3 = format_date(date_3)
    formatted_date_4 = format_date(date_4)
    formatted_date_5 = format_date(date_5)

   
    formatted_total_amount = None
    if total_amount:
        try:
            clean_amount = total_amount.replace(",", "")
            formatted_total_amount = "{:,.2f}".format(float(clean_amount))
        except ValueError:
            formatted_total_amount = total_amount

    formatted_phone_number = None
    if country_code and phone_number:
        formatted_phone_number = f"{country_code}{phone_number}"

    placeholder_dict = {
    "{{COMPANY_NAME}}": company_name,
    "{{COMPANY_NAME_1}}": company_name_1,
    "{{COMPANY_NAME_2}}": company_name_2,
    "{{COMPANY_NAME_3}}": company_name_3,
    "{{DATE_1}}": formatted_date_1,
    "{{DATE_2}}": formatted_date_2,
    "{{DATE_3}}": formatted_date_3,
    "{{DATE_4}}": formatted_date_4,
    "{{DATE_5}}": formatted_date_5,
    "{{PAKID_SHUMA}}": pakid_shuma,
    "{{PAKID_SHUMA_1}}": pakid_shuma_1,
    "{{ADDRESS_PKID_SHUMA}}": address_pkid_shuma,
    "{{ADDRESS}}": address,
    "{{CITY}}": city,
    "{{C_R_NUMBER}}": c_r_number,
    "{{C_R_NUMBER_1}}": c_r_number_1,
    "{{C_R_NUMBER_2}}": c_r_number_2,
    "{{YEAR}}": year,
    "{{YEAR_1}}": year_1,
    "{{TOTAL_AMOUNT}}": formatted_total_amount,
    "{{TOTAL_AMOUNT_1}}": total_amount_1,
    "{{AMOUNT_1}}": amount_1,
    "{{N_AMOUNT}}": n_amount,
    "{{N_AMOUNT_1}}": n_amount_1,
    "{{M_AMOUNT}}": m_amount,
    "{{M_AMOUNT_1}}": m_amount_1,
    "{{L_AMOUNT}}": l_amount,
    "{{L_AMOUNT_1}}": l_amount_1,
    "{{AMOUNT_2}}": amount_2,
    "{{AMOUNT_3}}": amount_3,
    "{{AMOUNT_4}}": amount_4,
    "{{AMOUNT_5}}": amount_5,
    "{{AMOUNT_6}}": amount_6,
    "{{NAME}}": name,
    "{{NAME_2}}": name_2,
    "{{EMAIL}}": email,
    "{{PHONE_NUMBER}}": formatted_phone_number,
    "{{ASSET_1}}": asset_1,
    "{{ASSET_2}}": asset_2,
    "{{SUM_1}}": sum_1, 
    "{{SUM_2}}": sum_2,
    "{{VALUE}}": value,
}

    # Filter out None values from the placeholder dictionary
    placeholder_dict = {k: v for k, v in placeholder_dict.items() if v is not None}

    print(f"Filtered placeholder_dict: {placeholder_dict}")

    # Load the appropriate Word template based on the form submission
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the current directory
    template_path = os.path.join(base_dir, 'assets', f'{template_name}.docx')  # Construct the path dynamically

    processor = WordTemplateProcessor(template_path)  # Pass the correct path
    processor.load_template()
    processor.replace_placeholders(placeholder_dict)

    # Define the output file path where the filled Word document will be saved
    output_dir = os.path.join(base_dir, 'output')  # Create the output path
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    output_file = os.path.join(output_dir, f"{template_name}_filled.docx")  # Define output file path
    
    # Save the document
    processor.save_document(output_file)

    # Return the filled Word document to the user for download
    return FileResponse(output_file, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"{template_name}_filled.docx")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
