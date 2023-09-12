import tensorflow as tf
from tensorflow.keras.models import load_model
import os

try:
    os.mkdir("/mnt/model")
except Exception as e:
    print(e)

try:
    os.mkdir("/mnt/TRT_output")
except Exception as e:
    print(e)


# path_to_.h5_file
keras_model = load_model('/app/TF_TRT/convlstm_model___Date_Time_2023_08_28__12_43_19___Loss_0.5779551863670349___Accuracy_0.782608687877655.h5',compile=False)

tf.keras.models.save_model(keras_model, '/mnt/model')