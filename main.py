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
2. De invoer kan Nederlands, Duits of Engels zijn.
3. Extraheer titel, porties, ingrediënten en stappen.
4. Geef ALLE output volledig in het Nederlands terug.
5. Vertaal ook losse ingrediënten, kooktermen en stapbeschrijvingen volledig naar het Nederlands.
6. Haal hoeveelheden, eenheden, bereidingstijd en wachttijd eruit als die expliciet of heel duidelijk in de tekst staan.
7. Geef aan wat ontbreekt.
8. Geef waarschuwingen indien nodig.

BELANGRIJK:
- Ondersteun alleen Nederlands, Duits en Engels. Als de tekst een andere taal is, geef dit aan in warnings.
- ALLE tekstvelden in de output moeten volledig Nederlands zijn.
- Laat geen Duitse of Engelse woorden staan in title, ingredients, steps, missingFields of warnings, behalve bij originele eenheden die niet goed vertaald kunnen worden.
- Verzín geen ontbrekende informatie.
- Als iets ontbreekt: laat leeg of gebruik null.
- Gebruik alleen tijden die echt in de tekst staan of duidelijk direct uit de tekst volgen.
- actionMinutes = actieve tijd voor die stap.
- waitMinutes = wachttijd / oven / rijzen / rusten / marineren enz.
- title mag je voorzichtig afleiden indien duidelijk.
- servings mag alleen ingevuld worden als het expliciet genoemd wordt.
- Engelse of buitenlandse eenheden mogen behouden blijven, maar geef een waarschuwing als ze mogelijk onduidelijk zijn (bijvoorbeeld 'cup', 'ounce').
Tekst:
{data.text}""",
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
                        "servings": {"type": ["integer", "null"]},
                        "ingredients": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": ["string", "null"]}
                                },
                                "required": ["name", "amount", "unit"],
                                "additionalProperties": False
                            }
                        },
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "actionMinutes": {"type": ["integer", "null"]},
                                    "waitMinutes": {"type": ["integer", "null"]}
                                },
                                "required": ["text", "actionMinutes", "waitMinutes"],
                                "additionalProperties": False
                            }
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
                        "servings",
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
