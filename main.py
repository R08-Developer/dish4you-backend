@app.post("/import-recipe")
def import_recipe(data: ImportRequest):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Analyseer deze tekst.

1. Bepaal of dit een maaltijdrecept is.
2. Extraheer titel, porties, ingrediënten en stappen.
3. Haal hoeveelheden, eenheden, bereidingstijd en wachttijd eruit als die expliciet of heel duidelijk in de tekst staan.
4. Geef aan wat ontbreekt.
5. Geef waarschuwingen indien nodig.

BELANGRIJK:
- Verzín geen ontbrekende informatie.
- Als iets ontbreekt: laat leeg of gebruik null.
- Gebruik alleen tijden die echt in de tekst staan of duidelijk direct uit de tekst volgen.
- actionMinutes = actieve tijd voor die stap.
- waitMinutes = wachttijd / oven / rijzen / rusten / marineren enz.
- title mag je voorzichtig afleiden indien duidelijk.
- servings mag alleen ingevuld worden als het expliciet genoemd wordt.

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
                        "servings": {
                            "type": ["integer", "null"]
                        },
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

    return {"result": response.output_text}        text={
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
