# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import base64
from io import BytesIO

import banana_dev as banana
import requests

INPUT_TEST_FILE = "test_data/test.m4a"


with open(INPUT_TEST_FILE, "rb") as f_:
    audio_bytes = io.BytesIO(f_.read())

audio_bytes_str = base64.b64encode(audio_bytes.getvalue()).decode("ISO-8859-1")

model_payload = {
    "audio_bytes_str": audio_bytes_str,
    "audio_format": "m4a",
}

# use following to call deployed model on banana, model_payload is same as above
out = banana.run("apikey", "modelkey", model_payload)

print(out)
