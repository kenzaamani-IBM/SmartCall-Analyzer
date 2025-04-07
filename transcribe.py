import azure.cognitiveservices.speech as speechsdk
import streamlit as st




speech_key = st.secrets["AZURE_SPEECH_KEY"]
service_region = st.secrets["AZURE_SPEECH_REGION"]

def transcribe_audio(file_path):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_input = speechsdk.AudioConfig(filename=file_path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    done = False
    transcript = []

    def stop_cb(evt):
        nonlocal done
        done = True

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcript.append(evt.result.text)

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        pass

    speech_recognizer.stop_continuous_recognition()

    return ' '.join(transcript)
