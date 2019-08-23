import logging
import os
import requests
import azure.functions as func
import skills.utils.analyzer as analyzer

from skills.models.cognitive_skill import CognitiveSkill
from skills.models.cognitive_search import CognitiveSearch
from skills.utils.http_requests import HttpRequest

# Azure Search settings
endpoint = os.environ['AzureSearchEndpoint']
api_version = os.environ['AzureSearchApiVersion']

# Blob storage settings
connection_string = os.environ['AzureBlobConnectionString']
container = os.environ['AzureBlobContainer']

def main(req: func.HttpRequest):
    logging.info('Cognitive Search HTTP trigger function processed a request.')
    
    skillset = create_skillset('myskillsetsample')
    index = create_index('myindexsample')
    data_source = create_data_source('mydatasourcesample')
    indexer = create_indexer('myindexersample', 'mydatasourcesample', 'myindexsample', 'myskillsetsample')

    return func.HttpResponse("OK")

def create_skillset(skillset_name: str):
    uri = f"{endpoint}/skillsets/{skillset_name}?api-version={api_version}"
    data = create_skillset_data()

    return HttpRequest.put(uri, data)

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
    data = CognitiveSearch.index_schema(analyzer.MICROSOFT_PT_BR)

    return HttpRequest.put(uri, data)

def create_data_source(datasource_name: str ):
    uri = f"{endpoint}/datasources/{datasource_name}?api-version={api_version}"
    data = CognitiveSearch.datasource_schema(datasource_name, connection_string, container)
    
    return HttpRequest.put(uri, data)

def create_indexer(indexer_name: str, datasource_name: str, index_name: str, skillset_name: str):
    uri = f"{endpoint}/indexers/{indexer_name}?api-version={api_version}"
    data = CognitiveSearch.indexer_schema(indexer_name, datasource_name, index_name, skillset_name)
    
    return HttpRequest.put(uri, data)
