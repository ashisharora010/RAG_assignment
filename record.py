import pyaudio
import wave
import assemblyai as aai
from gtts import gTTS
import simpleaudio as sa
import sounddevice as sd
import soundfile as sf



def read_audio(file_name, apikey):
    # Your API token is already set here
    aai.settings.api_key = apikey
    # Create a transcriber object.
    transcriber = aai.Transcriber()
    # If you have a local audio file, you can transcribe it using the code below.
    # Make sure to replace the filename with the path to your local audio file.
    transcript = transcriber.transcribe(file_name)

    return transcript.text

def record_audio(file_name):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 48000  # Record at 44100 samples per second
    seconds = 10
    filename = file_name

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    stream = p.open(format=sample_format,
                    input_device_index = 0,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return 


def play_audio(text): 
    # The text that you want to convert to audio
    
    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("temp.wav")
    filename = 'temp.wav'
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    sd.wait()  # Wait until file is done playing
    return