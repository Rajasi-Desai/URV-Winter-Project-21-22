import wave
import json
import os
from vosk import Model, KaldiRecognizer, SetLogLevel

# To download the model
# curl -LO http://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
# and unzip the file
model_path = os.path.join(os.path.dirname(__file__), "vosk-model-en-us-0.22")

model = Model(model_path)


def parse(audio_filename):
    wf = wave.open(audio_filename, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    return results
