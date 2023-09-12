from tensorflow.python.compiler.tensorrt import trt_convert as trt

SAVED_MODEL_DIR = ""
OUTPUT_SAVED_MODEL_DIR = ""

# Instantiate the TF-TRT converter
# Here saved model directory is the path to the saved model
# You can customise precision mode to FP32 FP16 or INT8

converter = trt.TrtGraphConverterV2(
    input_saved_model_dir=SAVED_MODEL_DIR,
    precision_mode=trt.TrtPrecisionMode.FP32
)

# Convert the model into TRT compatible segments
trt_func = converter.convert()
converter.summary()

# save the model by specifying output dir path
converter.save(output_saved_model_dir=OUTPUT_SAVED_MODEL_DIR)