import math
from array import array
import pyaudio
import speech_recognition
import wave
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types



chunk = 1024  # Create a 1024-byte chunk of data to be read at once.
Format = pyaudio.paInt16  # Use PCM-16 in the recording.
Channels = 1  # Number of audio channels, this is mono.
Rate = 44100  # Sampling rate of the audio file.
rec_sec = 5  # The length of each individual recording.
p = pyaudio.PyAudio()  # The PyAudio object that will do the recording.
r = speech_recognition.Recognizer()  # The Speech Recognition object.
# Open a recording stream
stream = p.open(format=Format, channels=Channels, rate=Rate, frames_per_buffer=chunk, input=True, output=True)
fh = open('recognised_text.txt','w')
rec = []
for i in range(math.ceil(Rate/chunk*rec_sec)):
    data = stream.read(chunk)
    rec.append(data)
    data_chunk = array('h', data)
wavfile=wave.open('sound.wav','wb')
wavfile.setnchannels(Channels)
wavfile.setsampwidth(p.get_sample_size(Format))
wavfile.setframerate(Rate)
wavfile.writeframes(b''.join(rec))#append frames recorded to file
wavfile.close()

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

try:
    with speech_recognition.AudioFile('sound.wav') as source:
        audio = r.record(source)
    text = r.recognize_google_cloud(audio, language='en-us')
    print(text)
    fh.write(text)
except:
    print('Whatever you said was gibberish to me!')


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