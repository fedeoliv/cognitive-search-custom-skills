import requests

admin_key = ""

class HttpRequest:
    
    @staticmethod
    def put(uri, data):
        headers = {
            'Content-Type': 'application/json', 
            'api-key': admin_key 
        }

        return requests.put(uri, headers=headers, data=data)

