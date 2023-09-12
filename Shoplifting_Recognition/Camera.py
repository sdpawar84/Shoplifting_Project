import uuid

import cv2
from config import *
import logging
import numpy as np
from ActionPredictor_CPU import ActionPredictor


logger = logging.getLogger(__name__)


def compose_video(output_file, frames_list, frame_width, frame_height, frame_rate):
    # Get the codec for the video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # Create a VideoWriter object
    video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (frame_width, frame_height))

    # Write each frame to the video file
    for frame in frames_list:
        cv2.putText(frame, output_file.split("__")[0], (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()


class Camera:
    def __init__(self, cam_url):
        self.cam_url = cam_url

        self.stream_disconnect_counter = 0
        self.frame_count = 0
        self.predictor = ActionPredictor()

        self.read_stream()

    def read_stream(self):
        """
        read the stream & it'll keep on trying untill we get the stream
        :return: None
        """
        while True:
            self.video_reader = cv2.VideoCapture(self.cam_url)
            print("RTSP Connecting...")

            try:
                self.video_reader.isOpened()
            except:
                logger.error("Exception occurred at **** Camera / read_stream **** \n", exc_info=True)
                self.video_reader = cv2.VideoCapture(self.cam_url)

            if self.video_reader.isOpened():
                _, frame = self.video_reader.read()
                print('RTSP Connected')
                self.stream_disconnect_counter = 0
                break

    def monitor_stream(self):
        """

        :return:
        """
        self.frame_count = 0
        frames_list = []
        predicted_class_name = ''
        buffer_array = []

        while True:

            # Read the Frame from a Stream
            try:
                _, frame = self.video_reader.read()
            except:
                logger.error("Exception occurred at **** camera / monitor_stream **** \n", exc_info=True)
                frame = None

            # To Check if Frame is None & if stream_disconnect_counter > 1000
            # it'll try to read Frame until we get stream
            if frame is None:
                self.stream_disconnect_counter += 1
                # print('stream_disconnect_counter', self.stream_disconnect_counter, )

                if self.stream_disconnect_counter > 1000:
                    self.read_stream()
                    self.stream_disconnect_counter = 0

                    # initialize it again
                    self.frame_count = 0
                    frames_list = []
                    predicted_class_name = ''
                    buffer_array = []

                # continue
                break
            else:
                self.stream_disconnect_counter = 0

            # To compose a Video
            resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
            buffer_array.append(resized_frame)

            # skip the frames
            if self.frame_count % skip_frame_for_box != 0:
                self.frame_count += 1
                continue

            # ----------------- pre-process the frame ------------------
            # resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
            # Normalize the resized frame by dividing it with 255
            # so that each pixel value then lies between 0 and 1.
            normalized_frame = resized_frame / 255
            frames_list.append(normalized_frame)

            # Checking if we have enough frames for prediction.
            if len(frames_list) == SEQUENCE_LENGTH:
                predicted_class_name = self.predictor.getPredictedLabel(frames_list)
                frames_list.clear()

            if len(frames_list) == 0:
                # compose_video(predicted_class_name,buffer_array)
                if predicted_class_name:
                    compose_video(f"{predicted_class_name}__{uuid.uuid4()}.avi", buffer_array, IMAGE_WIDTH, IMAGE_HEIGHT, 20)
                buffer_array.clear()
                pass

            self.frame_count += 1
