from lib_init import *
from lib_redis import *
from lib_cv2 import *
import time
import os
import multiprocessing
from lib_aws import *
from ActionPredictor import *
from config import *

RECORDERQ = "record"
FO = "action_recognition_q"

def generate_notify(ret_val, data, ai_type):
    ret_val["time"] = data["time"]
    ret_val["frameid"] = data["frameid"]
    ret_val["ai_type"] = ai_type
    if "notify" in data["cam_config"]:
        ret_val["notify"] = data["cam_config"]["notify"]
    if "notify_token" in data["cam_config"]:
        ret_val["notify_token"] = data["cam_config"]["notify_token"]
    ret_val["camid"] = data["cam_config"]["camid"]
    return ret_val

def record(camid, json_detect):
    cam_url = json_detect["cam_config"]["url"]
    video_feed = cv2.VideoCapture(cam_url, cv2.CAP_FFMPEG)
    # recording_fps = 10
    # Set the duration of the clip (in seconds)
    clip_duration = 3

    # Set the codec for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Set the frame rate of the output video
    fps = int(video_feed.get(cv2.CAP_PROP_FPS))
    print(cam_url)
    frame_height = int(video_feed.get(4))
    frame_width = int(video_feed.get(3))
    frame_size = (frame_width, frame_height)
    notify_type = json_detect["ai_type"]
    time2 = int(json_detect["time"])
    camid = camid
    path = "/recordings/" + notify_type + "/" + camid + "/"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    # Initialize variables
    frame_count = 0
    clip_count = 0
    frames_in_clip = clip_duration * fps
    out = None

    # Initialize variables for ActionPredictor
    frame_list = []
    predictor = ActionPredictor(gpu_memory_limit=gpu_memory_limit)

    # Read the video frame by frame
    while True:
        success, frame = video_feed.read()
        if not success:
            break

        # If this is the first frame or the end of a clip, start a new clip
        if frame_count % frames_in_clip == 0:
            if out is not None:
                out.release()
            clip_count += 1
            file_name = "/recordings/" + notify_type + "/" + str(camid) + "/" + str(time2) + ".mp4"
            out = cv2.VideoWriter(file_name, fourcc, fps, (frame_width, frame_height))

        # Write the frame to the current clip
        out.write(frame)

        # skip the frames for frame_list only
        if frame_count % skip_frame_for_box == 0:
            # pre-process the frame
            resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
            normalized_frame = resized_frame / 255
            frame_list.append(normalized_frame)

        # If we have written enough frames for the current clip, stop writing
        if frame_count % frames_in_clip == frames_in_clip - 1:
            out.release()
            try:
                ret_val = {}
                ret_val[camid] = {}
                notify = {}
                value = ""

                # Checking if we have enough frames for prediction.
                if len(frame_list) == SEQUENCE_LENGTH:
                    value = predictor.getPredictedLabel(frame_list)
                    frame_list.clear()

                # value = predict(video=file_name)
                # print(value)

                if value == "shoplifting":
                    notify["shoplifting"] = "True"
                    ret_val[camid]["notify"] = notify
                    # jpg = cv2.imencode('.jpg', send_frame)[1].tobytes()
                    # img_r = base64.b64encode(jpg).decode()
                    # ret_val[camid]["image"] = img_r
                    time_v = json_detect["time"]
                    ai_type = "shoplifting"
                    videov = S3_BASE + ai_type + "/" + camid + "/" + str(time_v) + ".mp4"
                    client.upload_file(file_name, NOTIFY_BUCKET, ai_type + "/" + camid + "/" + str(time_v) + ".mp4")
                    ret_val[camid]["video_url"] = videov
                    os.remove(file_name)
                    return ret_val
            except Exception as ex:
                print("Issue")
                os.remove(file_name)
                return False

        frame_count += 1

    # Release the video capture and output video objects
    video_feed.release()
    if out is not None:
        out.release()

    # print(file_name + " written")


def send_notify(data, key1, r):
    ct = time.time()
    ret_val = record(data["cam_config"]["camid"], data)
    dt = time.time()
    print(str(dt - ct))
    if ret_val:
        print("Generating Notifications " + str(key1[2]))
        ret_val = generate_notify(ret_val, data, "shoplifting")
        writeq(key1[1], NOTIFYQ, key1[2], ret_val, r, 1000)


def get_notifications():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    while True:
        for i in list_keys("*" + FO + "*", r):
            i = i.decode('ascii')
            key1 = i.split("/")
            data = readq(key1[0], key1[1], key1[2], r)
            if data:
                print(list_keys("*" + FO + "*", r))
                p = multiprocessing.Process(target=send_notify, args=(data, key1, r))
                p.start()

############### Notification Engine ###################
if __name__ == "__main__":
    get_notifications()