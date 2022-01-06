import spacy

import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel


# pip install spacy
# python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")
# nlp = spacy.load("en_core_web_md")


doc1 = nlp(u"the person wear red T-shirt")
doc2 = nlp(u"this person is walking")
doc3 = nlp(u"the boy wear red T-shirt")


print(doc1.similarity(doc2))
print(doc1.similarity(doc3))
print(doc2.similarity(doc3))


##-------------------------------------------------------------
class Word:
    """A class representing a word from the JSON format for vosk speech recognition API"""

    def __init__(self, dict):
        """
        Parameters:
          dict (dict) dictionary from JSON, containing:p
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        """

        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]

    def to_string(self):
        """Returns a string describing this instance"""
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
            self.word, self.start, self.end, self.conf * 100
        )
    
    def give_word(self):
        return self.word

model_path = "vosk-model-en-us-0.22"
audio_filename = "test_question.wav"
#audio_filename = "URVtest.wav"
#audio_filename = "personal_audio.wav"

model = Model(model_path)
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

# convert list of JSON dictionaries to list of 'Word' objects
list_of_words = []
for sentence in results:
    if len(sentence) == 1:
        # sometimes there are bugs in recognition
        # and it returns an empty dictionary
        # {'text': ''}
        continue
    for obj in sentence["result"]:
        w = Word(obj)  # create custom Word object
        list_of_words.append(w)  # and add it to list

wf.close()  # close audiofile

output = []
# output to the screen
for word in list_of_words:
    print(word.to_string())
    output.append(word.give_word())

#print(list_of_words)
print(output)
output1_string = " ".join(map(str, output))

print(output1_string)
