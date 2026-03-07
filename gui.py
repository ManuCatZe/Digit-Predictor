import tkinter as tk

from canvas_processor import CanvasProcessor
from feedback_manager import FeedbackManager
from predictor import DigitPredictor
from retrainer import ModelRetrainer


class DigitApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digit Predictor")
        self.root.geometry("820x580")

        self.last_x = None
        self.last_y = None
        self.last_input = None
        self.last_prediction = None
        self.feedback_choice = None

        self.processor = CanvasProcessor(280, 8)
        self.predictor = DigitPredictor("model.joblib")
        self.feedback_manager = FeedbackManager("feedback_data.json")
        self.retrainer = ModelRetrainer(
            dataset_file="base_dataset.joblib",
            feedback_file="feedback_data.json",
            model_file="model.joblib",
        )

        self.empty_preview = self._build_empty_preview()

        self.build_ui()

    def _build_empty_preview(self):
        rows = []

        for _ in range(8):
            rows.append("0 0 0 0 0 0 0 0")

        return "\n".join(rows)

    def build_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=280, height=280, bg="white")
        self.canvas.pack(side="left", padx=10)
        self.canvas.bind("<Button-1>", self.save_position)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.reset_line)

        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.pack(side="left", padx=20, anchor="n")

        self.prediction_label = tk.Label(
            self.info_frame,
            text="Prediction: None",
            font=("Arial", 16),
        )
        self.prediction_label.pack(pady=10)

        self.confidence_label = tk.Label(
            self.info_frame,
            text="Confidence: None",
            font=("Arial", 14),
        )
        self.confidence_label.pack(pady=10)

        self.status_label = tk.Label(
            self.info_frame,
            text="Status: Waiting",
            font=("Arial", 12),
        )
        self.status_label.pack(pady=10)

        self.feedback_label = tk.Label(
            self.info_frame,
            text="Feedback choice: None",
            font=("Arial", 12),
        )
        self.feedback_label.pack(pady=5)

        self.grid_title_label = tk.Label(
            self.info_frame,
            text="8x8 Preview",
            font=("Arial", 14, "bold"),
        )
        self.grid_title_label.pack(pady=(20, 5))

        self.grid_preview_label = tk.Label(
            self.info_frame,
            text=self.empty_preview,
            font=("Courier New", 12),
            justify="left",
            anchor="w",
        )
        self.grid_preview_label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_canvas,
            width=12,
        )
        self.clear_button.pack(side="left", padx=5)

        self.predict_button = tk.Button(
            self.button_frame,
            text="Predict",
            command=self.predict_digit,
            width=12,
        )
        self.predict_button.pack(side="left", padx=5)

        self.feedback_frame = tk.Frame(self.root)
        self.feedback_frame.pack(pady=15)

        self.yes_button = tk.Button(
            self.feedback_frame,
            text="Yes",
            command=self.choose_yes,
            width=12,
        )
        self.yes_button.pack(side="left", padx=5)

        self.no_button = tk.Button(
            self.feedback_frame,
            text="No",
            command=self.choose_no,
            width=12,
        )
        self.no_button.pack(side="left", padx=5)

        self.commit_button = tk.Button(
            self.feedback_frame,
            text="Commit feedback",
            command=self.commit_feedback,
            width=16,
        )
        self.commit_button.pack(side="left", padx=10)

        self.correct_digit_label = tk.Label(
            self.feedback_frame,
            text="Correct digit:",
            font=("Arial", 12),
        )
        self.correct_digit_label.pack(side="left", padx=(15, 5))

        self.correct_digit_entry = tk.Entry(self.feedback_frame, width=5)
        self.correct_digit_entry.pack(side="left", padx=5)

    def reset_line(self, _event):
        self.last_x = None
        self.last_y = None

    def save_position(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.processor.add_point(event.x, event.y)

    def draw_line(self, event):
        if self.last_x is None or self.last_y is None:
            self.save_position(event)
            return

        self.canvas.create_line(
            self.last_x,
            self.last_y,
            event.x,
            event.y,
            fill="black",
            width=8,
            capstyle=tk.ROUND,
            smooth=True,
        )

        self.last_x = event.x
        self.last_y = event.y
        self.processor.add_point(event.x, event.y)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.processor.clear_points()

        self.last_x = None
        self.last_y = None
        self.last_input = None
        self.last_prediction = None
        self.feedback_choice = None

        self.prediction_label.config(text="Prediction: None")
        self.confidence_label.config(text="Confidence: None")
        self.status_label.config(text="Status: Waiting")
        self.feedback_label.config(text="Feedback choice: None")
        self.grid_preview_label.config(text=self.empty_preview)
        self.correct_digit_entry.delete(0, tk.END)

    def update_grid_preview(self, grid):
        rows = []

        for row in grid:
            values = []
            for value in row:
                values.append(f"{value:2}")
            rows.append(" ".join(values))

        self.grid_preview_label.config(text="\n".join(rows))

    def predict_digit(self):
        grid = self.processor.get_grid()
        self.update_grid_preview(grid)

        flat_input = self.processor.get_flattened_input()
        prediction, confidence = self.predictor.predict_with_confidence(flat_input)

        self.last_input = flat_input
        self.last_prediction = prediction
        self.feedback_choice = None

        self.prediction_label.config(text=f"Prediction: {prediction}")
        self.confidence_label.config(text=f"Confidence: {confidence:.2f}%")
        self.feedback_label.config(text="Feedback choice: None")
        self.status_label.config(text="Status: Choose Yes/No, then Commit")

    def choose_yes(self):
        if self.last_input is None:
            self.status_label.config(text="Status: Predict first")
            return

        self.feedback_choice = "yes"
        self.feedback_label.config(text="Feedback choice: Yes")
        self.status_label.config(text="Status: Press Commit feedback")

    def choose_no(self):
        if self.last_input is None:
            self.status_label.config(text="Status: Predict first")
            return

        self.feedback_choice = "no"
        self.feedback_label.config(text="Feedback choice: No")
        self.status_label.config(text="Status: Enter correct digit, then Commit")

    def _get_correct_digit(self):
        text = self.correct_digit_entry.get().strip()

        if text == "":
            self.status_label.config(text="Status: Enter correct digit")
            return None

        if not text.isdigit():
            self.status_label.config(text="Status: Correct digit must be 0-9")
            return None

        digit = int(text)

        if digit < 0 or digit > 9:
            self.status_label.config(text="Status: Correct digit must be 0-9")
            return None

        return digit

    def commit_feedback(self):
        if self.last_input is None or self.last_prediction is None:
            self.status_label.config(text="Status: Predict first")
            return

        if self.feedback_choice is None:
            self.status_label.config(text="Status: Choose Yes or No first")
            return

        if self.feedback_choice == "yes":
            self.status_label.config(text="Status: Saving YES feedback...")
            self.feedback_manager.save_feedback(
                flat_input=self.last_input,
                predicted=self.last_prediction,
                correct=self.last_prediction,
                was_correct=True,
            )
        else:
            correct_digit = self._get_correct_digit()
            if correct_digit is None:
                return

            self.status_label.config(text=f"Status: Saving NO feedback ({correct_digit})...")
            self.feedback_manager.save_feedback(
                flat_input=self.last_input,
                predicted=self.last_prediction,
                correct=correct_digit,
                was_correct=False,
            )

        # после фидбека модель перечитываем, чтобы новое поведение было сразу видно
        self.retrainer.retrain_model()
        self.predictor.reload_model()

        self.clear_canvas()
        self.status_label.config(text="Status: Feedback committed, model updated")

    def start(self):
        self.root.mainloop()
