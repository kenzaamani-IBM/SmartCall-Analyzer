import streamlit as st
from transcribe import transcribe_audio
from agents import get_insights
import pandas as pd
from datetime import datetime
import ffmpeg

st.title("🎧 Customer Service Call Analyzer")

uploaded_file = st.file_uploader("Upload Call Audio (.mp3/.wav)", type=['mp3', 'wav'])

def convert_mp3_to_wav(input_mp3, output_wav):
    try:
        (
            ffmpeg
            .input(input_mp3)
            .output(output_wav, format='wav')
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        st.error(f"Audio conversion error: {e}")

if uploaded_file:
    file_extension = uploaded_file.name.split('.')[-1]

    input_audio = f"temp_audio.{file_extension}"
    output_audio = "temp_audio.wav"

    # Save uploaded audio file temporarily
    with open(input_audio, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # If mp3, convert to wav
    if file_extension == "mp3":
        convert_mp3_to_wav(input_audio, output_audio)
    else:
        output_audio = input_audio  # already wav, no conversion needed

    st.audio(output_audio, format='audio/wav')

    transcript = transcribe_audio(output_audio)
    st.subheader("📄 Transcript")
    st.write(transcript)

    if st.button("🔍 Analyze Call"):
        insights = get_insights(transcript)

        st.subheader("📝 Summary")
        st.write(insights['summary'])

        st.subheader("👤 Employee Insights")
        st.write(insights['employee_feedback'])

        st.subheader("😊 Sentiment & Emotions")
        st.write(insights['sentiment'])

        st.subheader("💡 Customer Recommendations")
        st.write(insights['recommendations'])

        call_data = {
            'DateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Summary': insights['summary'],
            'EmployeeFeedback': insights['employee_feedback'],
            'Sentiment': insights['sentiment'],
            'Recommendations': insights['recommendations']
        }

        try:
            df = pd.read_csv('daily_insights.csv')
        except FileNotFoundError:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([call_data])], ignore_index=True)
        df.to_csv('daily_insights.csv', index=False)

        st.success("Insights saved!")
