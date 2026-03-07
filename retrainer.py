import joblib
from sklearn.neural_network import MLPClassifier

from feedback_manager import FeedbackManager


class ModelRetrainer:
    def __init__(
        self,
        dataset_file="base_dataset.joblib",
        feedback_file="feedback_data.json",
        model_file="model.joblib",
    ):
        self.dataset_file = dataset_file
        self.feedback_file = feedback_file
        self.model_file = model_file

    def retrain_model(self):
        dataset = joblib.load(self.dataset_file)
        x_data = list(dataset["X"])
        y_data = list(dataset["y"])

        feedback_manager = FeedbackManager(self.feedback_file)
        feedback_list = feedback_manager.load_feedback()

        for item in feedback_list:
            x_data.append(item["input"])
            y_data.append(item["correct"])

        model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
        model.fit(x_data, y_data)
        joblib.dump(model, self.model_file)
