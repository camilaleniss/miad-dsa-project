from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Cargar el modelo previamente entrenado y serializado
model = joblib.load('best_random_forest_model.pkl')

# Crear la aplicación FastAPI
app = FastAPI()

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

@app.post("/predict")
async def predict(data: InputData):
    # Convertir los datos en el formato que el modelo espera
    features = [[
        data.AREA,
        data.Rpt_Dist_No,
        data.Crm_Cd,
        data.Vict_Age,
        data.Premis_Cd,
        data.Status,
        data.Status_Desc,
        data.Crm_Cd_1,
        data.LAT,
        data.LON
    ]]

    # Hacer la predicción
    prediction = model.predict(features)

    # Retornar la predicción como respuesta
    return {"prediction": int(prediction[0])}

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}

# NOTA: ^Para que funcione esta API de prueba se debe ejecutar "uvicorn app:app --reload" en la 
# carpeta donde se guarde este archivo. Adicional se debe instalar: pip install fastapi uvicorn joblib scikit-learn
