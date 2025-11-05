from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from backend.models.efficientnet_model import Model
from backend.utils.logger import logger

app = FastAPI(title="Waste Management ML API", version="1.0")

# Initialize model
try:
    model_instance = Model()
    logger.info("✅ Model initialized successfully.")
except Exception as e:
    logger.error(f"❌ Model initialization failed: {e}")
    model_instance = None


@app.get("/", tags=["Health"])
async def health_check():
    logger.info("Health check called.")
    return {"status": "running"}


@app.post("/predict", tags=["Prediction"])
async def predict(file: UploadFile = File(...)):
    if not file.filename:
        logger.error("No file uploaded.")
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        img = Image.open(file.file).convert("RGB")
        logger.info(f"File '{file.filename}' opened successfully.")
    except Exception as e:
        logger.error(f"Invalid image file: {e}")
        raise HTTPException(status_code=400, detail="Invalid image file")

    if model_instance is None:
        logger.error("Model instance unavailable for prediction.")
        raise HTTPException(status_code=500, detail="Model not initialized")

    try:
        prediction = model_instance.predict(img)
        logger.info(f"Prediction successful: {prediction}")
        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
