import logging
import requests
import json
import azure.functions as func

# Azure Search settings
endpoint = ""
admin_key = ""
api_version = ""

# Blob storage settings
connection_string = ""
container = ""

def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    
    create_skillset('myskillsetsample')
    create_index('myindexsample')
    create_data_source('mydatasourcesample')
    create_indexer('myindexersample', 'mydatasourcesample', 'myindexsample', 'myskillsetsample')

    return func.HttpResponse("OK")

def create_skillset(skillset_name: str):
    uri = f"{endpoint}/skillsets/{skillset_name}?api-version={api_version}"
    headers = create_headers()
    data = create_skillset_data()

    response = requests.put(uri, headers=headers, data=data)

    print(response.content)

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
    data = create_index_data()

    response = requests.put(uri, headers=headers, data=data)

    print(response.content)

def create_index_data():
    data = {
        "fields": [
            { 
                "name": "id", 
                "type": "Edm.String", 
                "key": "true", 
                "searchable": "false" 
            },
            {
                "name": "content",
                "type": "Edm.String",
                "facetable": "false",
                "filterable": "false",
                "key": "false",
                "retrievable": "true",
                "searchable": "true",
                "sortable": "false",
                "analyzer": "pt-br.lucene",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "metadata_storage_content_type",
                "type": "Edm.String",
                "facetable": "false",
                "filterable": "false",
                "key": "false",
                "retrievable": "false",
                "searchable": "false",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "metadata_storage_size",
                "type": "Edm.Int64",
                "facetable": "false",
                "filterable": "false",
                "retrievable": "false",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "metadata_storage_last_modified",
                "type": "Edm.DateTimeOffset",
                "facetable": "false",
                "filterable": "false",
                "retrievable": "false",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "metadata_storage_name",
                "type": "Edm.String",
                "facetable": "false",
                "filterable": "false",
                "key": "false",
                "retrievable": "false",
                "searchable": "false",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name":"metadata_storage_path",
                "type":"Edm.String",
                "facetable":"false",
                "filterable":"false",
                "key":"false",
                "retrievable":"true",
                "searchable":"false",
                "sortable":"false",
                "synonymMaps":[],
                "fields":[]
            },
            {
                "name": "metadata_content_type",
                "type": "Edm.String",
                "facetable": "false",
                "filterable": "false",
                "key": "false",
                "retrievable": "false",
                "searchable": "false",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "metadata_language",
                "type": "Edm.String",
                "facetable": "false",
                "filterable": "false",
                "key": "false",
                "retrievable": "false",
                "searchable": "false",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "merged_content",
                "type": "Edm.String",
                "facetable": "false",
                "filterable": "false",
                "key": "false",
                "retrievable": "true",
                "searchable": "true",
                "sortable": "false",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "text",
                "type": "Collection(Edm.String)",
                "facetable": "false",
                "filterable": "false",
                "retrievable": "true",
                "searchable": "true",
                "analyzer": "pt-br.lucene",
                "synonymMaps": [],
                "fields": []
            },
            {
                "name": "layoutText",
                "type": "Collection(Edm.String)",
                "facetable": "false",
                "filterable": "false",
                "retrievable": "true",
                "searchable": "true",
                "analyzer": "pt-br.lucene",
                "synonymMaps": [],
                "fields": []
            }
        ],
        "suggesters": [],
        "scoringProfiles": [],
        "defaultScoringProfile": "",
        "corsOptions": {  
            "allowedOrigins": ["*"]
        },
        "analyzers": [],
        "charFilters": [],
        "tokenFilters": [],
        "tokenizers": []
    }

    return json.dumps(data)

def create_data_source(data_source_name: str ):
    uri = f"{endpoint}/datasources/{data_source_name}?api-version={api_version}"
    headers = create_headers()
    data = create_datasource_data(data_source_name)
    
    response = requests.put(uri, headers=headers, data=data)

    print(response.content)

def create_datasource_data(data_source_name: str):
    return json.dumps({   
        "name" : data_source_name,  
        "description" : "Blob storage data source",  
        "type" : "azureblob",
        "credentials" : { "connectionString" : connection_string },  
        "container" : { "name" : container }
    })

def create_indexer(indexer_name: str, datasource_name: str, index_name: str, skillset_name: str):
    uri = f"{endpoint}/indexers/{indexer_name}?api-version={api_version}"
    headers = create_headers()
    data = create_indexer_data(indexer_name, datasource_name, index_name, skillset_name)
    
    response = requests.put(uri, headers=headers, data=data)

    print(response.content)

def create_indexer_data(indexer_name: str, datasource_name: str, index_name: str, skillset_name: str):
    return json.dumps({   
        "name" : indexer_name,  
        "description" : "Indexer sample",  
        "dataSourceName" : datasource_name,  
        "targetIndexName" : index_name,  
        "skillsetName" : skillset_name
    })
