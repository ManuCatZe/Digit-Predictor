import json
import os


class FeedbackManager:
    def __init__(self, feedback_file="feedback_data.json"):
        self.feedback_file = feedback_file

    def load_feedback(self):
        if not os.path.exists(self.feedback_file):
            return []

        with open(self.feedback_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_feedback(self, flat_input, predicted, correct, was_correct):
        feedback_list = self.load_feedback()

        feedback_list.append(
            {
                "input": flat_input,
                "predicted": int(predicted),
                "correct": int(correct),
                "was_correct": bool(was_correct),
            }
        )

        with open(self.feedback_file, "w", encoding="utf-8") as file:
            json.dump(feedback_list, file, ensure_ascii=False, indent=2)
