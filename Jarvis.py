import os  
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import requests
import schedule
import time
from datetime import datetime
from pptx import Presentation
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import threading

# Initialize Firebase
cred = credentials.Certificate("D:\Download\chatbot-by-amit-firebase-adminsdk-fbsvc-bc076f45a2.json")  # Replace with your Firebase JSON key path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 600  
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            store_command(command)  # Store command in Firebase
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.") 
        except sr.RequestError:
            speak("Internet connection error.")
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
        return ""

def store_command(command):
    doc_ref = db.collection("commands").document()
    doc_ref.set({
        "command": command,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def system_commands(command):
    if "shutdown" in command:
        speak("Are you sure you want to shut down the system? Say yes to confirm.")
        if "yes" in listen():
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")
        else:
            speak("Shutdown canceled.")
    elif "restart" in command:
        speak("Are you sure you want to restart the system? Say yes to confirm.")
        if "yes" in listen():
            speak("Restarting the system.")
            os.system("shutdown /r /t 1")
        else:
            speak("Restart canceled.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open file explorer" in command:
        os.system("explorer.exe")
        speak("File Manager is now open.")
    elif "open notepad" in command:
        os.system("notepad.exe")
        speak("Notepad is now open.")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web.")
    elif "open google chrome" in command:
        os.system("start chrome")
        speak("Google Chrome is now open.")
    elif "open microsoft edge" in command:
        os.system("start msedge")
        speak("Microsoft Edge is now open.")
    else:
        speak(f"I couldn't recognize the application {command}.")

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Your query is ambiguous. Suggestions: {e.options[:5]}"
    except wikipedia.PageError:
        return "I couldn't find anything about that on Wikipedia."
    except Exception as e:
        return f"An error occurred: {e}"

def main_jarvis():
    schedule.run_pending()
    speak("Hello, I am Jeevan. How can I assist you today?")
    while True:
        command = listen()
        if not command:
            continue
        if "date" in command:
            today = datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today's date is {today}.")
        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}.")
        elif "shutdown" in command or "restart" in command or "open" in command:
            system_commands(command)
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            if topic:
                result = search_wikipedia(topic)
                speak(result)
            else:
                speak("Please specify a topic to search on Wikipedia.")
        elif "exit" in command:
            speak("Goodbye!")
            break
        time.sleep(1)

def run_gui():
    st.set_page_config(page_title="JARVIS AI Assistant", page_icon="🤖", layout="centered")
    st.markdown(
        """
        <style>
        .stApp {background: linear-gradient(45deg, #1a1a1a, #2c3e50); color: white;}
        div.stButton > button:first-child {
            border-radius: 50% !important;
            width: 120px !important;
            height: 120px !important;
            padding: 0 !important;
            margin: 2rem auto;
            display: block !important;
            font-size: 3rem !important;
            background: #2ecc71 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("JARVIS AI Assistant")
    st.markdown("---")
    if "mic_active" not in st.session_state:
        st.session_state.mic_active = False
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn = st.button("🎙️" if not st.session_state.mic_active else "🔴", key="mic_button")
    if btn:
        st.session_state.mic_active = not st.session_state.mic_active
        st.rerun()
    status_text = "🎤 Listening..." if st.session_state.mic_active else "🌟 Ready"
    st.markdown(f"<div class='status-box'><h3>{status_text}</h3></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    threading.Thread(target=main_jarvis, daemon=True).start()
    run_gui()
