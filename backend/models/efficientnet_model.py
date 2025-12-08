import torch
import time
from torchvision import models, transforms
from PIL import Image
import warnings
import torch.nn as nn
from backend.utils.util import read_json
from backend.utils.logger import logger


class Model:
    def __init__(
        self,
        model_path: str = "model/efficientnet_b0_waste_classifier.pth",
        class_path: str = "model/class_labels.json",
    ):
        warnings.filterwarnings("ignore", category=UserWarning)

        # Load class labels
        try:
            self.classes = read_json(class_path)
            self.class_size = len(self.classes)
            logger.info(f"Loaded {self.class_size} classes from {class_path}")
        except Exception as e:
            logger.error(f"Failed to load class labels from {class_path}: {e}")
            self.classes = {}
            self.class_size = 0

        # Set device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

        # Load model
        try:
            self.model = models.efficientnet_b0(pretrained=False)
            self.model.classifier[1] = nn.Linear(
                self.model.classifier[1].in_features, self.class_size
            )
            self.model.load_state_dict(
                torch.load(model_path, map_location=torch.device(self.device))
            )
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None

    def _preprocess(self, img: Image):
        try:
            transform = transforms.Compose(
                [
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225],
                    ),
                ]
            )
            tensor = transform(img).unsqueeze(0).to(self.device)
            logger.info("Image preprocessed successfully.")
            return tensor
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            return None

    def predict(self, img: Image) -> str:
        if self.model is None:
            logger.error("Prediction failed — model not loaded.")
            return "Model not loaded"
        start = time.time()
        try:
            tensor = self._preprocess(img)
            if tensor is None:
                return "Invalid image"

            with torch.no_grad():
                output = self.model(tensor)
                _, predicted = torch.max(output, 1)

            predicted_class = self.classes.get(str(int(predicted)), "Unknown")
            inference_time = time.time() - start
            logger.info(f"Prediction successful: {predicted_class}, inference: {inference_time}", extra={"prediction":predicted_class, "inference_time_ms":round(inference_time * 1000, 2)})
            return predicted_class
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return "Prediction failed"
