from fastapi import FastAPI
import pandas as pd
import json

#instanciamos la api
app = FastAPI()

all_beauty = pd.read_csv('../resultados/dataset_ml/recomendaciones_all_beauty.csv')
digital_music = pd.read_csv('../resultados/dataset_ml/recomendaciones_digital_music.csv')
pet_supplies = pd.read_csv('../resultados/dataset_ml/recomendaciones_pet_supplies.csv')
toys = pd.read_csv('../resultados/dataset_ml/recomendaciones_toys_and_games.csv')

@app.get("/recomendacion_all_beauty/")
async def all_beauty_recomendacion(palabra_clave: str):
    # Buscar la recomendación basada en la palabra clave
    result = all_beauty[all_beauty['PalabraClave'] == palabra_clave]['Recomendaciones'].values
    if len(result) > 0:
        recomendaciones = json.loads(result[0])
        return {"recomendacion": recomendaciones}
    else:
        return {"recomendacion": "Palabra clave no encontrada"}
    

@app.get("/recomendacion_digital_music/")
async def digital_music_recomendacion(palabra_clave: str):
    # Buscar la recomendación basada en la palabra clave
    result = digital_music[digital_music['PalabraClave'] == palabra_clave]['Recomendaciones'].values
    if len(result) > 0:
        recomendaciones = json.loads(result[0])
        return {"recomendacion": recomendaciones}
    else:
        return {"recomendacion": "Palabra clave no encontrada"}
    
@app.get("/recomendacion_pet_supplies/")
async def pet_supplies_recomendacion(palabra_clave: str):
    # Buscar la recomendación basada en la palabra clave
    result = pet_supplies[pet_supplies['PalabraClave'] == palabra_clave]['Recomendaciones'].values
    if len(result) > 0:
        recomendaciones = json.loads(result[0])
        return {"recomendacion": recomendaciones}
    else:
        return {"recomendacion": "Palabra clave no encontrada"}

@app.get("/recomendacion_toys/")
async def toys_recomendacion(palabra_clave: str):
    # Buscar la recomendación basada en la palabra clave
    result = toys[toys['PalabraClave'] == palabra_clave]['Recomendaciones'].values
    if len(result) > 0:
        recomendaciones = json.loads(result[0])
        return {"recomendacion": recomendaciones}
    else:
        return {"recomendacion": "Palabra clave no encontrada"}