import base64
import os
from io import BytesIO

import torch
import whisper


# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model
    assert torch.cuda.is_available()
    model = whisper.load_model("large-v2")


# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs: dict) -> dict:
    global model

    # Parse out your arguments
    mp3BytesString = model_inputs.get("mp3BytesString", None)
    initial_prompt = model_inputs.get("initial_prompt", None)

    if mp3BytesString == None:
        return {"message": "No input provided"}

    mp3Bytes = BytesIO(base64.b64decode(mp3BytesString.encode("ISO-8859-1")))
    with open("input.mp3", "wb") as file:
        file.write(mp3Bytes.getbuffer())

    # Run the model
    result = model.transcribe("input.mp3", initial_prompt=initial_prompt)
    os.remove("input.mp3")
    # Return the results as a dictionary
    return result
