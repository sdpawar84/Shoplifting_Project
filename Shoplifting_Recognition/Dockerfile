# Use the NVIDIA TensorFlow base image
FROM nvcr.io/nvidia/tensorflow:22.01-tf2-py3

# Set the working directory
WORKDIR /app

# Copy your application files to the container
COPY . /app

# Install any additional dependencies, if required
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

# Specify the command to run your application
CMD ["python", "main.py"]
# CMD while true;do echo 'hello';done
