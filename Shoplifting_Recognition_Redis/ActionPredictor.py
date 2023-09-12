import numpy as np
import tensorflow as tf
from config import *
import os

# Set the 'TF_GPU_ALLOCATOR' environment variable to 'cuda_malloc_async'
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'


class ActionPredictor():
    # def __init__(self):
    #     # Load the TensorRT-optimized model instead of the standard TensorFlow model
    #     self.model = self.load_trt_model()
    def __init__(self, gpu_memory_limit=None):
        # Set GPU memory growth to limit GPU usage
        if gpu_memory_limit is not None:
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                    if gpu_memory_limit > 0:
                        tf.config.experimental.set_virtual_device_configuration(
                            gpu,
                            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=gpu_memory_limit)])

        # Load the TensorRT-optimized model instead of the standard TensorFlow model
        self.model = self.load_trt_model()

    def load_trt_model(self):
        # Load the TensorRT-optimized model using the TF-TRT converter
        trt_model_path = "/mnt/TRT_output/"  # Path to the TensorRT-optimized model saved earlier
        return tf.saved_model.load(trt_model_path, tags=[tf.saved_model.SERVING])

    def getPredictedLabel(self, frames_list):

        infer = self.model.signatures["serving_default"]
        frames_list = np.array(frames_list, dtype=np.float32)
        output = infer(conv_lstm2d_input=tf.constant(np.expand_dims(frames_list, axis=0)))

        # Get the predicted class probabilities (example assumes a classification model)
        predicted_probabilities = output["dense"].numpy()

        # Get the predicted class index with the highest probability
        predicted_class_index = tf.argmax(predicted_probabilities, axis=-1).numpy()[0]

        # Assuming you have a list of class names, get the predicted class name
        predicted_class_name = CLASSES_LIST[predicted_class_index]

        print(f"Predicted Class: {predicted_class_name}")
        print(f"Predicted Probabilities: {predicted_probabilities}")

        return predicted_class_name