import logging
import requests
import azure.functions as func

from skills.models.cognitive_skill import CognitiveSkill
from skills.models.cognitive_search import CognitiveSearch

# Azure Search settings
endpoint = ""
admin_key = ""
api_version = ""

# Blob storage settings
connection_string = ""
container = ""

def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    
    skillset = create_skillset('myskillsetsample')
    index = create_index('myindexsample')
    data_source = create_data_source('mydatasourcesample')
    indexer = create_indexer('myindexersample', 'mydatasourcesample', 'myindexsample', 'myskillsetsample')

    return func.HttpResponse("OK")

def create_skillset(skillset_name: str):
    uri = f"{endpoint}/skillsets/{skillset_name}?api-version={api_version}"
    headers = create_headers()
    data = create_skillset_data()

    return requests.put(uri, headers=headers, data=data)

def create_headers():
    return {
        'Content-Type': 'application/json', 
        'api-key': admin_key 
    }

def create_skillset_data():
    description = "OCR for extracting text from PDF files and custom skills for data anonymization"
    skills = create_skills()

    return CognitiveSearch.skillset_schema(description, skills)

def create_skills():
    skills = []
    ocr_skill = CognitiveSkill.create_schema(language='pt', detect_orientation=True)

    skills.append(ocr_skill)

    return skills

def create_index(index_name: str):
    uri = f"{endpoint}/indexes/{index_name}?api-version={api_version}"
    headers = create_headers()
    data = CognitiveSearch.index_schema('pt-br.lucene')

    return requests.put(uri, headers=headers, data=data)

def create_data_source(datasource_name: str ):
    uri = f"{endpoint}/datasources/{datasource_name}?api-version={api_version}"
    headers = create_headers()
    data = CognitiveSearch.datasource_schema(datasource_name, connection_string, container)
    
    return requests.put(uri, headers=headers, data=data)

def create_indexer(indexer_name: str, datasource_name: str, index_name: str, skillset_name: str):
    uri = f"{endpoint}/indexers/{indexer_name}?api-version={api_version}"
    headers = create_headers()
    data = CognitiveSearch.indexer_schema(indexer_name, datasource_name, index_name, skillset_name)
    
    return requests.put(uri, headers=headers, data=data)
