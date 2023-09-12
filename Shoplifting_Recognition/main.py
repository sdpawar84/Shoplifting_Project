import logging
import sys
from config import *
from Camera import Camera
import os

# log_filename = '/app/images/Box_falling.log'
# log_filename = 'Box_falling.log'
# sys.stdout = open(log_filename, 'a')
# sys.stderr = sys.stdout
#
# FORMAT = "\n\n %(asctime)s -- %(name)s -- %(funcName)s --  %(message)s"
# logging.basicConfig(stream=sys.stderr, format=FORMAT, datefmt="%d-%b-%y %H:%M:%S", level=eval(logging_level))


def main():
    path = "/home/inqedge/Desktop/INQEDGE_BACKUP/shop_lifting_Project/Shoplifting Dataset (2022) - CV Laboratory MNNIT Allahabad/Dataset/Shoplifting/"
    cam_url = path + "Shoplifting (1).mp4"
    # cam_url = "/home/inqedge/Downloads/shoplift_vid.mp4"
    print(os.path.isfile(cam_url))
    # exit()
    cam_obj = Camera(cam_url=cam_url)
    cam_obj.monitor_stream()

if __name__ == "__main__":
    main()