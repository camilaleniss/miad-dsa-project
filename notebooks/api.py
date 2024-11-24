from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
import joblib
from typing import List

# Cargar el modelo previamente entrenado y serializado
try:
    model = joblib.load('best_random_forest_model.pkl')
except FileNotFoundError:
    raise RuntimeError("El modelo 'best_random_forest_model.pkl' no se encuentra en el directorio.")

# Crear la aplicación FastAPI
app = FastAPI(title="Crime Prediction API", version="1.0.0")

# Definir los datos de entrada esperados por la API
class InputData(BaseModel):
    AREA: float
    Rpt_Dist_No: float
    Crm_Cd: float
    Vict_Age: float
    Premis_Cd: float
    Status: float
    Status_Desc: float
    Crm_Cd_1: float
    LAT: float
    LON: float

class MultipleInputs(BaseModel):
    inputs: List[InputData]

@app.post("/predict", summary="Realiza predicciones usando el modelo Random Forest")
async def predict(data: MultipleInputs):
    """
    Recibe múltiples conjuntos de características y devuelve las predicciones.
    """
    try:
        # Convertir los datos al formato esperado por el modelo
        features = [
            [
                entry.AREA,
                entry.Rpt_Dist_No,
                entry.Crm_Cd,
                entry.Vict_Age,
                entry.Premis_Cd,
                entry.Status,
                entry.Status_Desc,
                entry.Crm_Cd_1,
                entry.LAT,
                entry.LON,
            ]
            for entry in data.inputs
        ]

        # Realizar predicciones
        predictions = model.predict(features)

        # Retornar las predicciones como respuesta
        return {"predictions": predictions.tolist()}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Error en la validación de datos: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/", summary="Verifica el estado de la API")
async def root():
    """
    Endpoint raíz para verificar si la API está funcionando correctamente.
    """
    return {"message": "API de predicción funcionando correctamente"}

@app.get("/health", summary="Verifica la salud del sistema")
async def health():
    """
    Devuelve el estado de la API y la carga del modelo.
    """
    return {"status": "ok", "model_loaded": True, "model_name": "best_random_forest_model.pkl"}
