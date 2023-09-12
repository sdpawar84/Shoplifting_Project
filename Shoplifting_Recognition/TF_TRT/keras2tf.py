import tensorflow as tf
from tensorflow.keras.models import load_model

keras_model = load_model('path_to_.h5_file',compile=False)

tf.keras.models.save_model(keras_model, '/mnt/TRT_output')
# tf.saved_model.save(keras_model, 'saved_model_dir')