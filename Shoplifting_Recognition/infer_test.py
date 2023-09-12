import tensorflow as tf
import cv2
from config import *

# Load the TensorRT-optimized model using TensorFlow's SavedModel format
trt_model_path = "/mnt/TRT_output/"  # Path to the TensorRT-optimized model saved earlier
loaded_model = tf.saved_model.load(trt_model_path, tags=[tf.saved_model.SERVING])

# Create a function to perform inference with the loaded model
infer = loaded_model.signatures["serving_default"]

path = ""
frame = cv2.imread(path)
# Input data for inference (example assumes an image with appropriate preprocessing)
resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))

input_data = ...  # Provide your input data here

# Perform inference on the input data
output = infer(tf.constant(input_data))

# Get the predicted class probabilities (example assumes a classification model)
predicted_probabilities = output["output"].numpy()

# Get the predicted class index with the highest probability
predicted_class_index = tf.argmax(predicted_probabilities, axis=-1).numpy()

# Assuming you have a list of class names, get the predicted class name
class_names = [...]  # Replace with your list of class names
predicted_class_name = class_names[predicted_class_index]

print(f"Predicted Class: {predicted_class_name}")
print(f"Predicted Probabilities: {predicted_probabilities}")
