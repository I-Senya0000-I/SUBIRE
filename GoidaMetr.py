import speech_recognition as speech_r
import pyaudio
import wave
import soundfile as sf   #   pip install pysoundfile
from pydub import AudioSegment
import librosa


GoidaWords = ["путин", "гойда", "ленин", "ссср", "хорошо", "отлично", "бедность", "россия"]
GoidaRates = {"путин": 100.0, "гойда": 10.0, "ленин": 10.0, "ссср": 90.0, "хорошо": 5.0, "отлично": 9.0, "бедность": -50.0, "россия": 100.0}


from fuzzywuzzy import fuzz
from fuzzywuzzy import process



def get_duration_pydub(file_path):
   #f = sf.SoundFile('output.wav')
   return librosa.get_duration(path='/home/senya0000/Documents/pyprojects/SUBIRE/output.wav')


def goidaRate(words):
    words = words.split()
    final = 0
    for word in words:
        rate = process.extractOne(word, GoidaWords)
        final += rate[1] / 100 * GoidaRates[rate[0]]
    
    final = final / len(words)

    

    return final

def convertor(filename):
    
    data, samplerate = sf.read('/home/senya0000/Documents/pyprojects/SUBIRE/audio/'+filename)
    sf.write('output.wav', data, samplerate)
    
    '''
    sound = AudioSegment.from_mp3('/home/senya0000/Documents/pyprojects/SUBIRE/audio/'+filename)
    sound.export("output.wav", format="wav")
    '''
    return 'output.wav'


import speech_recognition as sr
r = sr.Recognizer()

def analyze(filename):
    file = convertor(filename)
    harvard = sr.AudioFile(file)
    with harvard as source:
        audio = r.record(source)
    try:
        result = (r.recognize_google(audio, language="ru-RU")).lower()
        rate = goidaRate(result)
        print(result, rate)
        
        length = get_duration_pydub(filename)

        goidaspeed = rate/length
        return [result, rate, goidaspeed] 
    except speech_r.exceptions.UnknownValueError:
        print("No words!")
        return ["", 0]
    #print(result)

    



#print(analyze("audio_2024-11-26_18-35-21.ogg"))