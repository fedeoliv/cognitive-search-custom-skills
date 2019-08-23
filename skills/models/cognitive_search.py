import json

class CognitiveSearch:
    @staticmethod
    def index_schema(analyzer: str):
        schema = {
            "fields": [
                {
                    "name": "content",
                    "type": "Edm.String",
                    "facetable": "false",
                    "filterable": "false",
                    "key": "false",
                    "retrievable": "true",
                    "searchable": "true",
                    "sortable": "false",
                    "analyzer": analyzer,
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
                    "name": "metadata_storage_path",
                    "type": "Edm.String",
                    "facetable": "false",
                    "filterable": "false",
                    "key": True,
                    "retrievable": "true",
                    "searchable": "false",
                    "sortable": "false",
                    "synonymMaps": [],
                    "fields": []
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
                    "analyzer": analyzer,
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
                    "analyzer": analyzer,
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

        return json.dumps(schema)

    @staticmethod
    def skillset_schema(description: str, skills: list):

        return json.dumps({
            "description": description,
            "skills": skills
        })

    @staticmethod
    def datasource_schema(datasource_name: str, connection_string: str, container: str):

        return json.dumps({   
            "name" : datasource_name,  
            "description" : "Blob storage data source",  
            "type" : "azureblob",
            "credentials" : { "connectionString" : connection_string },  
            "container" : { "name" : container }
        })

    @staticmethod
    def indexer_schema(indexer_name: str, datasource_name: str, index_name: str, skillset_name: str):
        return json.dumps({   
            "name" : indexer_name,  
            "description" : "Indexer sample",  
            "dataSourceName" : datasource_name,  
            "targetIndexName" : index_name,  
            "skillsetName" : skillset_name,
            "fieldMappings" : [
                { 
                    "sourceFieldName" : "metadata_storage_path", 
                    "mappingFunction" : {
                        "name" : "base64Encode"
                    }
                }
            ]
        })
