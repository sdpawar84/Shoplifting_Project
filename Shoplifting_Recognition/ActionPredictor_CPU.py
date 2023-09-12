import numpy as np
from tensorflow.keras.models import load_model
from config import *

class ActionPredictor():
    def __init__(self):
        self.model = load_model(model_path)

    def getPredictedLabel(self, frames_list):
        # Passing the pre-processed frames to the model and get the predicted probabilities.
        predicted_labels_probabilities = self.model.predict(np.expand_dims(frames_list, axis=0))[0]

        # Get the index of class with highest probability.
        predicted_label = np.argmax(predicted_labels_probabilities)

        # Get the class name using the retrieved index.
        predicted_class_name = CLASSES_LIST[predicted_label]

        print(f'Action Predicted: {predicted_class_name}\nConfidence: {predicted_labels_probabilities[predicted_label]}')

        return predicted_class_name