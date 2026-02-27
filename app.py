from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load trained model
model = joblib.load("outputs/model.pkl")

NAME = "Abhishek Akash"
ROLL_NO = "2022BCS0002"


class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/predict")
def predict(data: WineInput):
    try:
        features = np.array([[
            data.fixed_acidity,
            data.volatile_acidity,
            data.citric_acid,
            data.residual_sugar,
            data.chlorides,
            data.free_sulfur_dioxide,
            data.total_sulfur_dioxide,
            data.density,
            data.pH,
            data.sulphates,
            data.alcohol
        ]])

        prediction = model.predict(features)
        result = int(prediction[0])

        return {
            "name": NAME,
            "roll_no": ROLL_NO,
            "prediction": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))