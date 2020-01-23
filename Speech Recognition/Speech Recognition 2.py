import math
from array import array
import pyaudio
import speech_recognition
import wave
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import multitimer
import nltk
#nltk.download('punkt')
chunk = 1024  # Create a 1024-byte chunk of data to be read at once.
Format = pyaudio.paInt16  # Use PCM-16 in the recording.
Channels = 1  # Number of audio channels, this is mono.
Rate = 44100  # Sampling rate of the audio file.
rec_sec = 10  # The length of each individual recording.
p = pyaudio.PyAudio()  # The PyAudio object that will do the recording.
r = speech_recognition.Recognizer()  # The Speech Recognition object.
# Open a recording stream
stream = p.open(format=Format, channels=Channels, rate=Rate, frames_per_buffer=chunk, input=True, output=True)
rec = []
total_words = []
counter = 0

def analysis_input_text(all_words_in_two_min):
    print(all_words_in_two_min)
    min_threshold = 100
    max_threshold = 200
    number_of_words = len(all_words_in_two_min)
    if min_threshold <= number_of_words <= max_threshold:
        print("Good rate")
    elif number_of_words > max_threshold:
        print("You should slow down")
    else:
        print("You are too slow")


def save_and_recognize(recording):
    global counter
    global total_words
    counter += 1
    fh = open('recognised_text.txt', 'r+')
    record = recording.copy()
    wavfile = wave.open('sound.wav', 'wb')
    wavfile.setnchannels(Channels)
    wavfile.setsampwidth(p.get_sample_size(Format))
    wavfile.setframerate(Rate)
    wavfile.writeframes(b''.join(recording))  # append frames recorded to file
    wavfile.close()

    try:
        with speech_recognition.AudioFile('sound.wav') as source:
            audio = r.record(source)
        text = r.recognize_google_cloud(audio, language='en-us')
        print(text)
        words = text.split()  # Why didn't you use split?
        for word in words:
            total_words.append(word)
        if counter == 12:
            analysis_input_text(total_words)
            total_words.clear()
            counter = 0
        fh.write(text)
        fh.close()
    except:
        print('Whatever you said was gibberish to me!')


t = multitimer.MultiTimer(rec_sec-0.01, function=save_and_recognize, kwargs={'recording': rec}, runonstart=False)
#t2 = multitimer.MultiTimer(120, function=analysis_input_text, kwargs={'all_words_in_two_min': total_words}, runonstart=False)
t.start()
#t2.start()


while True:
    for i in range(math.ceil(Rate/chunk*rec_sec)):
        data = stream.read(chunk)
        rec.append(data)
    rec.clear()

'''
try:
    with speech_recognition.AudioFile('sound.wav') as source:
        audio = r.record(source)
    text = r.recognize_wit(audio, key="HTDCCKGTKR5P6WTEG7MEFQ4NSE36KKBU")
    print(text)
    print(type(text))
    fh.write(text)
except:
    print('Whatever you said was gibberish to me!')
'''
'''
try:
    with speech_recognition.AudioFile('sound.wav') as source:
        audio = r.record(source)
    text = r.recognize_google_cloud(audio, language='en-us')
    print(text)
    fh.write(text)
except:
    print('Whatever you said was gibberish to me!')
'''

'''
client = speech.SpeechClient()

with open('sound.wav', 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='en-US')
response = client.recognize(config, audio)
for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))

print('Whatever you said was gibberish to me!')
'''
