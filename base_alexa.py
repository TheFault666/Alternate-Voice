import os
import speech_recognition as sr
import pyttsx3 as pt
import webbrowser as app
from datetime import datetime


# Initialize text-to-speech engine
def init_tts(voice_index=1, rate=150):
    engine = pt.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print("Invalid voice index, using default voice.")
    return engine


# Log recognized text to a file with a timestamp
def log_text(text, file_name="log.txt"):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(file_name, "a") as logfile:
        logfile.write(f"{timestamp} {text}\n")


# Process recognized voice commands
def process_command(command, tts_engine):
    if "alexa play " in command:
        url = command[11:]
        song = f"https://www.youtube.com/results?search_query={url}"
        app.open(song)
        tts_engine.say(f"Playing {url} on YouTube")
        tts_engine.runAndWait()

    elif command.startswith("alexa what ") or command.startswith("alexa who ") or command.startswith("alexa where "):
        query = command[6:]
        app.open(f"https://www.google.com/search?q={query}")
        tts_engine.say(f"Here are the results for {query}")
        tts_engine.runAndWait()

    elif "alexa stop" in command:
        tts_engine.say("Goodbye")
        tts_engine.runAndWait()
        return False

    else:
        print("Sorry, I didn't understand that.")
        # tts_engine.say("Sorry, I didn't understand that.")
        tts_engine.runAndWait()

    return True


# Automatically select a microphone
def auto_select_microphone():
    microphones = sr.Microphone.list_microphone_names()
    if not microphones:
        raise RuntimeError("No microphones detected.")

    print("Available microphones:")
    for i, mic_name in enumerate(microphones):
        print(f"{i}: {mic_name}")

    # Attempt to find a preferred microphone
    preferred_keywords = ["microphone", "mic", "input"]
    for i, mic_name in enumerate(microphones):
        if any(keyword.lower() in mic_name.lower() for keyword in preferred_keywords):
            print(f"Automatically selected preferred microphone: {mic_name}")
            return sr.Microphone(device_index=i)

    # Fall back to the first available microphone
    print("No preferred microphone found. Using the default microphone.")
    return sr.Microphone()


# Main program
def main():
    recognizer = sr.Recognizer()
    tts_engine = init_tts()

    mic = auto_select_microphone()
    print("Trigger phrase is 'Alexa/Okay Google'")

    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print("Listening...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                
                log_text(command)
                if not process_command(command, tts_engine):
                    break

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error making the request: {e}")

    print("Exiting...")


if __name__ == "__main__":
    main()
