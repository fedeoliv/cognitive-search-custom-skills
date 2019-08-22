import logging
import requests
import json
import azure.functions as func

# Azure Search settings
endpoint = ""
admin_key = ""

def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    
    create_skillset('myskillsetsample')

    return func.HttpResponse("OK")

def create_skillset(skillset_name: str):
    uri = f"{endpoint}/skillsets/{skillset_name}?api-version=2019-05-06"

    headers = {
        'Content-Type': 'application/json', 
        'api-key': admin_key 
    }

    data = create_skillset_data()
    response = requests.put(uri, headers=headers, data=json.dumps(data))

def create_skillset_data():
    description = "OCR for extracting text from PDF files and custom skills for data anonymization"
    skills = create_skills()
    
    return {
        "description": description,
        "skills": skills
    }

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
