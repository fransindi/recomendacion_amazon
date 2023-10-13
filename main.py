from fastapi import FastAPI
import pandas as pd
from fastapi import HTTPException

#instanciamos la api
app = FastAPI()

all_beauty = pd.read_csv('resultados/dataset_ml/recomendaciones_all_beauty.csv')
digital_music = pd.read_csv('resultados/dataset_ml/recomendaciones_digital_music.csv')
pet_supplies = pd.read_csv('resultados/dataset_ml/recomendaciones_pet_supplies.csv')
toys = pd.read_csv('resultados/dataset_ml/recomendaciones_toys_and_games.csv')

def buscar_recomendacion(palabra_clave, dataframe):
    """
    Esta funcion itera sobre un dataframe y busca las recomendaciones
    segun la palabra clave ingresada
    ------
    parametros: palabra_clave. una palabra en minuscula del tipo str.
    """
    result = dataframe[dataframe['PalabraClave'] == palabra_clave]['Recomendaciones'].values
    if len(result) > 0:
        return result[0]
    else:
        return None


@app.get("/recomendacion_all_beauty/")
async def all_beauty_recomendacion(palabra_clave: str):
    """
    Esta funcion itera sobre una base de datos y devuelve las recomendaciones
    segun la palabra clave buscada
    ----
    parametros: palabra_clave. una palabra en minuscula del tipo str
    ----
    salida: un array con 5 recomendaciones con NombreProducto y PrecioProducto.
    """
    palabra_clave = palabra_clave.strip()  # Eliminar espacios en blanco al comienzo y al final

    if not palabra_clave:
        raise HTTPException(status_code=400, detail="Palabra clave no proporcionada")

    recomendacion = buscar_recomendacion(palabra_clave, all_beauty)

    if recomendacion is not None:
        return {"recomendacion": recomendacion}
    else:
        raise HTTPException(status_code=404, detail="Palabra clave no encontrada")
    

@app.get("/recomendacion_digital_music/")
async def digital_music_recomendacion(palabra_clave: str):
    # Buscar la recomendación basada en la palabra clave
    """
    Esta funcion itera sobre una base de datos y devuelve las recomendaciones
    segun la palabra clave buscada
    ----
    parametros: palabra_clave. una palabra en minuscula del tipo str
    ----
    salida: un array con 5 recomendaciones con NombreProducto y PrecioProducto.
    """
    palabra_clave = palabra_clave.strip()  # Eliminar espacios en blanco al comienzo y al final

    if not palabra_clave:
        raise HTTPException(status_code=400, detail="Palabra clave no proporcionada")

    recomendacion = buscar_recomendacion(palabra_clave, digital_music)

    if recomendacion is not None:
        return {"recomendacion": recomendacion}
    else:
        raise HTTPException(status_code=404, detail="Palabra clave no encontrada")

@app.get("/recomendacion_pet_supplies/")
async def pet_supplies_recomendacion(palabra_clave: str):
    # Buscar la recomendación basada en la palabra clave
    """
    Esta funcion itera sobre una base de datos y devuelve las recomendaciones
    segun la palabra clave buscada
    ----
    parametros: palabra_clave. una palabra en minuscula del tipo str
    ----
    salida: un array con 5 recomendaciones con NombreProducto y PrecioProducto.
    """
    palabra_clave = palabra_clave.strip()  # Eliminar espacios en blanco al comienzo y al final

    if not palabra_clave:
        raise HTTPException(status_code=400, detail="Palabra clave no proporcionada")

    recomendacion = buscar_recomendacion(palabra_clave, pet_supplies)

    if recomendacion is not None:
        return {"recomendacion": recomendacion}
    else:
        raise HTTPException(status_code=404, detail="Palabra clave no encontrada")



@app.get("/recomendacion_toys/")
async def toys_recomendacion(palabra_clave: str):
    """
    Esta funcion itera sobre una base de datos y devuelve las recomendaciones
    segun la palabra clave buscada
    ----
    parametros: palabra_clave. una palabra en minuscula del tipo str
    ----
    salida: un array con 5 recomendaciones con NombreProducto y PrecioProducto.
    """
    # Buscar la recomendación basada en la palabra clave
    palabra_clave = palabra_clave.strip()  # Eliminar espacios en blanco al comienzo y al final

    if not palabra_clave:
        raise HTTPException(status_code=400, detail="Palabra clave no proporcionada")

    recomendacion = buscar_recomendacion(palabra_clave, toys)

    if recomendacion is not None:
        return {"recomendacion": recomendacion}
    else:
        raise HTTPException(status_code=404, detail="Palabra clave no encontrada")