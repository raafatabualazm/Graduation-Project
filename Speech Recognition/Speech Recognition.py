import math
from array import array
import pyaudio
import speech_recognition
import wave
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

stri = '''{
  "type": "service_account",
  "project_id": "true-study-250623",
  "private_key_id": "c9dc9ba7a79076a879e4470519167cd7ac22be19",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCvy3Dcv+IUacbj\nXkSqFzZ5e9imsDXWxb071klSfITCGTTkIozgw7HI9Kt/xi9zFDR0Z5uBt1i0VPl5\nZ5l94MpbX3w87gTrenRRudpSOvXCCRX47nzJJJmDx7ze899G8JE1jvAmhS9jTSjS\njaXqSGk6ypBydtSMEN+OqzXgPn4HcVB1RS7fF9JObcpOR6MTVIx4HaeCZI1hmz2c\n0FbxsC2R2tket3Ljdun4og5CCZX6vxBEuCbtoavBQKUQofKtNvj2TZ0auJzoErEX\n1QawGYm1AeCt2xhAyyafRP1+UwBZp5lF29/D3jusAfmbanXdaNSTQkLzZgLgVN89\n0ZUOmTx/AgMBAAECggEABr8E5sPKVkQ06LbOZcScR480Ijly53oRKAGyMKMsqRI0\nkGivBVUdNnwFNNMTMRReavUq55B0q/7yz/Dk2ArPWTBR4Ti1IaBCZHyAX1V55udY\nW4Qzb7ii14bLvbaYI+3JdMe2eZP03JeycFoVOudqemIZpvrebz2ahqwVVjSvu3NS\nYX0w4B4dnVPyaNhUh1YHOQApKMU46F3M/6ZwDB073B2XnaU/Wa1YeXS4Z/TZsYHf\nhM761g3BIhQGBj0sxq0YOFcqXPqKtDS1G/E1kYfJRZkQ6xTMaJraVH4LY2zTiEsT\nYGZ2bb6cCXVLgAzkX+las/erEwfYnULTuwI5mIxYEQKBgQDuZN5an1dZ2A/JLoCs\nzovQk6U+TPjDspUnM89jcj05yJ2ExMGxarag+BH34OS1HIMSkJOfB+tB/jRoCjSW\nD0K8srpoqzobqrj7Ta0hgvZzKpgsDwZ6htIiPoWoDcKoUCqEMGvEymCCqCtuPiAa\niRYpJcONKHCEofx0sW72oPm0SQKBgQC8xw4iMC3Rycb50QTP04mrZlB+STsqUtUW\n+ZoSsOPW16XK6WUdFvZr76VgG5iL8H+toMCCF4d4IZgWHWlJ5ydYHCSxHNnXlScW\nuoy3ZcwuHd8EGlRp3+nbbGpABCLsvS/BkW8AyyxQRFaziTk2gGzeZDHA0RMMVJeg\n0ZtBAj3ahwKBgDBnpMprzjW87D+iRJhR/Aum3weOY3iA+04RdAuyN4JTHMDHnrii\nfWCj3iohrO6lUmvjlUXWOsuUjRmO8OyDPr7H35e/JLZXbOYB+KR0TgxGWs2fY2Zf\nl61CWqsr2BmK5YcfudIkcYI2GVNyI9yfdzN1qoYv7uDPb05WdLx5JRqZAoGAabOr\nnkkL3uP0nf0DjLsN4wMvHwcyMcifuHWaZ8zURoAJPUziaR9qa5WMK/xHtlO7qiTQ\npgc2u3VUC038nnzn8tYPVXyqHaROdtON50MAyPHA5jM4APB3qX1TIPUv+Q8VpnUg\nink5HtilE3JKrtHKI9xGX4ix+b2ECXBUVlpC+BECgYEA3G1jWBptKz08Ach6xTl9\nsbq0dDEDyj9Xra5wcIkP8nzVPjIAJJK301bzW74qfcIWoQbNGdFp/RysxWq+fH4+\niwbarRaFgpfUiTEPVz0HFgts/25QGB0r4VsdCIThOI/9ZdQZKJGA2dKlqit+20iy\ng3vgsJqrAtkKSdMfmlsJR5o=\n-----END PRIVATE KEY-----\n",
  "client_email": "recognizer@true-study-250623.iam.gserviceaccount.com",
  "client_id": "107155020698383311571",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/recognizer%40true-study-250623.iam.gserviceaccount.com"
}'''


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
    text = r.recognize_google(audio)
    print(text)
    print(type(text))
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