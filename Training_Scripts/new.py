# -*- coding: utf-8 -*-
"""CNN_with_LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Owwg1K6eaQKC9WKuQLCijoinUdq3JEd
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import cv2
# import pafy
import math
import random
import numpy as np
import datetime as dt
import tensorflow as tf
from collections import deque
import matplotlib.pyplot as plt

# from moviepy.editor import *
# %matplotlib inline

from sklearn.model_selection import train_test_split

from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.set_visible_devices(physical_devices[0], 'GPU')
else:
    print("No GPU devices found. Running on CPU.")

"""Pre-Process the Dataset"""

IMAGE_HEIGHT, IMAGE_WIDTH = 320, 420

# Specify the number of frames of a video that will be fed to the model as one sequence.
SEQUENCE_LENGTH = 20

# Specify the directory containing the dataset.
DATASET_DIR = "/home/ubuntu/SAT_PROJECTS/Shoplifiting_Project/Dataset"

# Specify the list containing the names of the classes used for training.
CLASSES_LIST = ["shoplifting", "normal"]


def frames_extraction(video_path):
    '''
    This function will extract the required frames from a video after resizing and normalizing them.
    Args:
        video_path: The path of the video in the disk, whose frames are to be extracted.
    Returns:
        frames_list: A list containing the resized and normalized frames of the video.
    '''

    # Declare a list to store video frames.
    frames_list = []

    # Read the Video File using the VideoCapture object.
    video_reader = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video.
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count / SEQUENCE_LENGTH), 1)

    # Iterate through the Video Frames.
    for frame_counter in range(SEQUENCE_LENGTH):

        # Set the current frame position of the video.
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

        # Reading the frame from the video.
        success, frame = video_reader.read()

        # Check if Video frame is not successfully read then break the loop
        if not success:
            break

        # Resize the Frame to fixed height and width.
        resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))

        # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1
        normalized_frame = resized_frame / 255

        # Append the normalized frame into the frames list
        frames_list.append(normalized_frame)

    # Release the VideoCapture object.
    video_reader.release()

    # Return the frames list.
    return frames_list


def create_dataset():
    """
    create a video file paths
    :return:
    """
    # Declared Empty Lists to store the features, labels and video file path values.
    labels = []
    video_files_paths = []

    # Iterating through all the classes mentioned in the classes list
    for class_index, class_name in enumerate(CLASSES_LIST):

        # Display the name of the class whose data is being extracted.
        print(f'Extracting Data of Class: {class_name}')

        # Get the list of video files present in the specific class name directory.
        files_list = os.listdir(os.path.join(DATASET_DIR, class_name))

        # Iterate through all the files present in the files list.
        for file_name in files_list:
            # Get the complete video path.
            video_file_path = os.path.join(DATASET_DIR, class_name, file_name)
            video_files_paths.append(video_file_path)
            labels.append(class_index)

    return video_files_paths, labels


def data_generator(video_paths, labels, batch_size=32):
    while True:
        # Shuffle the data
        data = list(zip(video_paths, labels))
        random.shuffle(data)

        for i in range(0, len(data), batch_size):
            print(f"Batch Data  {i}:{i + batch_size}")
            batch_data = data[i:i + batch_size]
            batch_frames = []
            batch_labels = []

            for video_path, label in batch_data:
                frames = frames_extraction(video_path)
                if len(frames) == SEQUENCE_LENGTH:
                    batch_frames.append(frames)
                    batch_labels.append(label)

            # Convert the batch of frames and labels to NumPy arrays
            batch_frames = np.asarray(batch_frames)
            batch_labels = np.asarray(batch_labels)

            # Using Keras's to_categorical method to convert labels into one-hot-encoded vectors
            one_hot_encoded_labels = to_categorical(batch_labels)

            # Yield the batch of frames and labels
            yield batch_frames, one_hot_encoded_labels
        return


# Create the dataset.
video_files_paths, labels = create_dataset()
batch_size = 24
train_data_generator = data_generator(video_files_paths, labels, batch_size)

print("Data Genrator")
# for x,y in train_data_generator:
#     print(len(x),len(y))
# exit()


"""Split the Data Set into training & testing"""
def split_data_generator(data_generator, test_size=0.25):
    """
    Splits a data generator into train and test generators.

    Args:
        data_generator: A data generator yielding (X, y) tuples.
        test_size: The proportion of data to include in the test split.

    Returns:
        train_generator: A data generator for the training set.
        test_generator: A data generator for the test set.
    """
    data = list(data_generator)  # Convert the generator to a list
    num_samples = len(data)
    num_test_samples = int(test_size * num_samples)

    # Split the data
    test_data = data[:num_test_samples]
    train_data = data[num_test_samples:]

    # Create new generators for train and test data
    train_generator = (item for item in train_data)
    test_generator = (item for item in test_data)

    return train_generator, test_generator


# Split the data generator into train and test generators
train_data_generator, test_data_generator = split_data_generator(train_data_generator, test_size=0.25)

# Now you can use train_data_generator and test_data_generator for training and testing.

print("IMAGE_WIDTH,IMAGE_HEIGHT", IMAGE_WIDTH, IMAGE_HEIGHT)


def create_LRCN_model():
    '''
    This function will construct the required LRCN model.
    Returns:
        model: It is the required constructed LRCN model.
    '''

    # We will use a Sequential model for model construction.
    model = Sequential()

    # Define the Model Architecture.
    ########################################################################################################################

    model.add(TimeDistributed(Conv2D(16, (3, 3), padding='same', activation='relu'),
                              input_shape=(SEQUENCE_LENGTH, IMAGE_HEIGHT, IMAGE_WIDTH, 3)))

    model.add(TimeDistributed(MaxPooling2D((4, 4))))
    model.add(TimeDistributed(Dropout(0.25)))

    model.add(TimeDistributed(Conv2D(32, (3, 3), padding='same', activation='relu')))
    model.add(TimeDistributed(MaxPooling2D((4, 4))))
    model.add(TimeDistributed(Dropout(0.25)))

    model.add(TimeDistributed(Conv2D(64, (3, 3), padding='same', activation='relu')))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    model.add(TimeDistributed(Dropout(0.25)))

    model.add(TimeDistributed(Conv2D(64, (3, 3), padding='same', activation='relu')))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    # model.add(TimeDistributed(Dropout(0.25)))

    model.add(TimeDistributed(Flatten()))

    model.add(LSTM(32))

    model.add(Dense(len(CLASSES_LIST), activation='softmax'))

    ########################################################################################################################

    # Display the models summary.
    model.summary()

    # Return the constructed LRCN model.
    return model


# Construct the required LRCN model.
LRCN_model = create_LRCN_model()

# Display the success message.
print("Model Created Successfully!")

# Plot the structure of the contructed LRCN model.
plot_model(LRCN_model, to_file='LRCN_model_structure_plot.png', show_shapes=True, show_layer_names=True)

""" Compile & Train the Model """
# Define your model (LRCN_model) here

# Create an Instance of Early Stopping Callback.
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=15, mode='min', restore_best_weights=True)

# Compile the model and specify loss function, optimizer, and metrics.
LRCN_model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=["accuracy"])

# Specify the number of training steps per epoch and testing steps per epoch based on batch size and data size.
train_steps_per_epoch = len(video_files_paths) // batch_size
test_steps_per_epoch = len(video_files_paths) // batch_size  # You can adjust this if you have a separate test set

# Start training the model using fit_generator.
LRCN_model_training_history = LRCN_model.fit(train_data_generator,
                                                       steps_per_epoch=train_steps_per_epoch,
                                                       epochs=70,
                                                       validation_data=test_data_generator,
                                                       validation_steps=test_steps_per_epoch,
                                                       callbacks=[early_stopping_callback])

# You can access training history, including loss and accuracy, from LRCN_model_training_history.

print("Evaluation "*5)
""" Evaluating the trained Model """
# Evaluate the trained model using evaluate_generator.
model_evaluation_history = LRCN_model.evaluate(test_data_generator,
                                                        steps=test_steps_per_epoch)

""" Save the model """
# Get the loss and accuracy from model_evaluation_history.
model_evaluation_loss, model_evaluation_accuracy = model_evaluation_history

# Define the string date format.
# Get the current Date and Time in a DateTime Object.
# Convert the DateTime object to string according to the style mentioned in date_time_format string.
date_time_format = '%Y_%m_%d__%H_%M_%S'
current_date_time_dt = dt.datetime.now()
current_date_time_string = dt.datetime.strftime(current_date_time_dt, date_time_format)

# Define a useful name for our model to make it easy for us while navigating through multiple saved models.
model_file_name = f'LRCN_model___Date_Time_{current_date_time_string}___Loss_{model_evaluation_loss}___Accuracy_{model_evaluation_accuracy}.h5'

# Save the Model.
LRCN_model.save(model_file_name)


"""**Plot Model’s Loss & Accuracy Curves**"""

def plot_metric(model_training_history, metric_name_1, metric_name_2, plot_name):
    '''
    This function will plot the metrics passed to it in a graph.
    Args:
        model_training_history: A history object containing a record of training and validation
                                loss values and metrics values at successive epochs
        metric_name_1:          The name of the first metric that needs to be plotted in the graph.
        metric_name_2:          The name of the second metric that needs to be plotted in the graph.
        plot_name:              The title of the graph.
    '''

    # Get metric values using metric names as identifiers.
    metric_value_1 = model_training_history.history[metric_name_1]
    metric_value_2 = model_training_history.history[metric_name_2]

    # Construct a range object which will be used as x-axis (horizontal plane) of the graph.
    epochs = range(len(metric_value_1))

    # Plot the Graph.
    plt.plot(epochs, metric_value_1, 'blue', label=metric_name_1)
    plt.plot(epochs, metric_value_2, 'red', label=metric_name_2)

    # Add title to the plot.
    plt.title(str(plot_name))

    # Add legend to the plot.
    plt.legend()

    plt.savefig(f"{plot_name}.png")


# Visualize the training and validation loss metrices.
plot_metric(LRCN_model_training_history, 'loss', 'val_loss', 'Total Loss vs Total Validation Loss')

# Visualize the training and validation accuracy metrices.
plot_metric(LRCN_model_training_history, 'accuracy', 'val_accuracy', 'Total Accuracy vs Total Validation Accuracy')
