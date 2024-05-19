import pyttsx3
import openai
import speech_recognition as sr
import time

#Key de API de la openAI
openai.api_key = ""

#Init la TTS engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

def generate_response(prompt):
    response = openai.completions.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop =  None,
        temperature = 0.7,
    )
    return response['choices'][0]['text']
    
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #Asteptam hello 
        print("Say hello to start the question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    #Inregistram audio
                    filename = "input.wav"
                    print("Tell me your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    #Transcriem audio
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"{text}")

                        #Generam raspuns
                        response = generate_response(text)
                        print(f"{response}")

                        #Spunem raspunsul
                        speak_text(response)
            except Exception as e:
                print("I didn't understand that, error occured: {}".format(e))

if __name__ == "__main__":
    main()