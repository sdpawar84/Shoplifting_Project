# Use the NVIDIA TensorFlow base image
FROM nvcr.io/nvidia/tensorflow:22.01-tf2-py3

# Set the working directory
WORKDIR /app

# Copy your application files to the container
COPY . /app

# Install any additional dependencies, if required
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

## Parameter
#ENV redis_host some_val
#ENV redis_port some_val
#
## Specify the command to run your application
#ENTRYPOINT python3 /app/object_falling_recognition.py --redis_host ${redis_host} --redis_port ${redis_port}
# CMD while true;do echo 'hello';done