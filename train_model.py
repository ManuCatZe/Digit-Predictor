import joblib
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


def main():
    digits = load_digits()
    x_data = digits.data
    y_data = digits.target

    base_dataset = {"X": x_data, "y": y_data}
    joblib.dump(base_dataset, "base_dataset.joblib")
    print("Base dataset saved to base_dataset.joblib")

    x_train, x_test, y_train, y_test = train_test_split(
        x_data,
        y_data,
        test_size=0.2,
        random_state=42,
    )

    model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    # оставил простой вывод, чтобы сразу было видно что модель вообще обучилась
    print("Accuracy:", accuracy)

    joblib.dump(model, "model.joblib")
    print("Model saved to model.joblib")


if __name__ == "__main__":
    main()
