import joblib


class DigitPredictor:
    def __init__(self, model_path="model.joblib"):
        self.model_path = model_path
        self.model = joblib.load(model_path)

    def reload_model(self):
        self.model = joblib.load(self.model_path)

    def predict(self, flat_input):
        return self.model.predict([flat_input])[0]

    def predict_with_confidence(self, flat_input):
        prediction = self.predict(flat_input)
        probabilities = self.model.predict_proba([flat_input])[0]
        confidence = max(probabilities) * 100
        return prediction, confidence
