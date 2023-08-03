import whisper
import ssl
import numpy as np

def whisperer(audio, sample_rate):
    # Ignore SSL certificate verification (not recommended for production use)
    ssl._create_default_https_context = ssl._create_default_https_context = ssl._create_unverified_context

    model = whisper.load_model("tiny")

    # Pad/trim the audio to fit 30 seconds
    audio = whisper.pad_or_trim(audio, sample_rate, desired_length=30)

    # Convert to Float
    audio = audio.astype(np.float32)

    # Print the length of the audio data
    print(f"Length of audio data: {len(audio)}")

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # Decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # Print the recognized text
    print(result.text)

    return result.text

