# In this file, we define download_model
# It runs during container build time to get model weights built into the container

# In this example: A Huggingface BERT model

import torch
import whisper


def download_model():
    model = whisper.load_model("large-v2")


if __name__ == "__main__":
    download_model()
