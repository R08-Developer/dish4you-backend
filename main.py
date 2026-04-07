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
        input=f"Zet deze recepttekst om naar een gestructureerd recept.\n\n{data.text}",
        text={
            "format": {
                "type": "json_schema",
                "name": "recipe_import",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "ingredients": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["title", "ingredients", "steps"],
                    "additionalProperties": False
                }
            }
        }
    )
    return {"result": response.output_text}
