## Enter into the Docker File by exec cmd

## Convert the Model from Tensorflow to Tensort gpu acceleration
1) go inside TF_TRT folder
2) modify keras2tf.py 
- change path_to_.h5_file

3) python keras2tf.py
4) python TF_TRT_convertor.py

you will get the output in /mnt/TRT_output folder

## RUN
OPTIONAL 

then you can run like shoplifting_detection.py
for ex - 
python3 /app/object_falling_recognition.py --redis_host {redis_host} --redis_port {redis_port}  some_node_id
