import base64
import os
import tempfile
from io import BytesIO

import torch
import whisper
from pydub import AudioSegment


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
    initial_prompt = model_inputs.get("initial_prompt", None)
    audio_bytes_str = model_inputs.get("audio_bytes_str", None)
    audio_format = model_inputs.get(
        "audio_format", None
    )  # Expected to be something like mp3 or m4a
    num_speakers = model_inputs.get("num_speakers", None)

    if audio_bytes_str is None or audio_format is None:
        return {"message": "Missing audio_bytes_str or audio_format"}

    # Convert audio to mp3
    audio_bytes = BytesIO(base64.b64decode(audio_bytes_str.encode("ISO-8859-1")))
    audio_segment_input = AudioSegment.from_file(audio_bytes, format=audio_format)

    t_file = tempfile.NamedTemporaryFile(suffix=".mp3")
    audio_segment_input.export(t_file.name, format="mp3")

    # Run the model
    result = model.transcribe(t_file.name, initial_prompt=initial_prompt)

    t_file.close()

    # Return the results as a dictionary
    return result
