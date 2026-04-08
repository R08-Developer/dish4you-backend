from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ImportRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Dish4You backend draait"}

@app.post("/import-recipe")
def import_recipe(data: ImportRequest):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Analyseer deze tekst.

1. Bepaal of dit een maaltijdrecept is.
2. Extraheer titel, ingrediënten en stappen.
3. Geef aan wat ontbreekt.
4. Geef waarschuwingen indien nodig.

BELANGRIJK:
- Verzín geen ontbrekende informatie
- Als iets ontbreekt → leeg laten
- Titel mag je voorzichtig afleiden indien duidelijk

Tekst:
{data.text}
""",
        text={
            "format": {
                "type": "json_schema",
                "name": "recipe_import",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "isRecipe": {"type": "boolean"},
                        "confidence": {"type": "number"},
                        "title": {"type": "string"},
                        "ingredients": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "missingFields": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "warnings": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "isRecipe",
                        "confidence",
                        "title",
                        "ingredients",
                        "steps",
                        "missingFields",
                        "warnings"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    return {"result": response.output_text}
