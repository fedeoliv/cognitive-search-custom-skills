import logging
import requests
import json
import azure.functions as func

# Azure Search settings
endpoint = ""
admin_key = ""
api_version = ""

def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    
    create_skillset('myskillsetsample')
    create_index('myheadersample')

    return func.HttpResponse("OK")

def create_skillset(skillset_name: str):
    uri = f"{endpoint}/skillsets/{skillset_name}?api-version={api_version}"
    headers = create_headers()
    data = create_skillset_data()

    response = requests.put(uri, headers=headers, data=data)

def create_headers():
    return {
        'Content-Type': 'application/json', 
        'api-key': admin_key 
    }

def create_skillset_data():
    description = "OCR for extracting text from PDF files and custom skills for data anonymization"
    skills = create_skills()

    return json.dumps({
        "description": description,
        "skills": skills
    })

def create_skills():
    skills = []

    skills.append(create_ocr_skill())

    return skills

def create_ocr_skill():
    return {
        "description": "Extracts text (plain and structured) from PDF.",
        "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
        "context": "/document/normalized_images/*",
        "defaultLanguageCode": "pt",
        "detectOrientation": "true",
        "inputs": [
            {
                "name": "image",
                "source": "/document/normalized_images/*"
            }
        ],
        "outputs": [
            {
                "name": "text",
                "targetName": "myText"
            },
            {
                "name": "layoutText",
                "targetName": "myLayoutText"
            }
        ]
    }

def create_index(index_name: str):
    uri = f"{endpoint}/indexes/{index_name}?api-version={api_version}"
    headers = create_headers()

    response = requests.put(uri, headers=headers)
