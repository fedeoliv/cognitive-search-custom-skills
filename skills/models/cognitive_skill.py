class CognitiveSkill:
    @staticmethod
    def create_schema(language: str, detect_orientation: bool):
        return {
            "description": "Extracts text (plain and structured) from PDF.",
            "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
            "context": "/document/normalized_images/*",
            "defaultLanguageCode": language,
            "detectOrientation": detect_orientation,
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
