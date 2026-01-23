from fastapi import FastAPI, HTTPException
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("outputs/model.pkl")



NAME = "Abhishek Akash"
ROLL_NO = "2022BCS0002"


@app.get("/predict")
@app.post("/predict")
def predict(
    fixed_acidity: float,
    volatile_acidity: float,
    citric_acid: float,
    residual_sugar: float,
    chlorides: float,
    free_sulfur_dioxide: float,
    total_sulfur_dioxide: float,
    density: float,
    pH: float,
    sulphates: float,
    alcohol: float
):
    try:
        features = np.array([[
            fixed_acidity,
            volatile_acidity,
            citric_acid,
            residual_sugar,
            chlorides,
            free_sulfur_dioxide,
            total_sulfur_dioxide,
            density,
            pH,
            sulphates,
            alcohol
        ]])

        prediction = model.predict(features)
        wine_quality = int(prediction.flatten()[0])

        return {
            "name": NAME,
            "roll_no": ROLL_NO,
            "wine_quality": wine_quality
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
