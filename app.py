import streamlit as st
from gtts import gTTS
import os
import base64
import speech_recognition as sr

# Function to convert text to speech with options for language and speed
def text_to_speech_gtts(text, language='en', slow=False, file_name="output.mp3"):
    """
    Converts input text to speech using gTTS and saves it as a MP3 file.
    
    Args:
    - text (str): Text to be converted to speech.
    - language (str): Language for TTS (e.g., 'en' for English, 'fr' for French).
    - slow (bool): Slow speech option.
    - file_name (str): File name to save the output audio.
    """
    tts = gTTS(text=text, lang=language, slow=slow)
    tts.save(file_name)

# Function to generate download link for audio
def get_audio_download_link(file_path, file_label="Download audio"):
    with open(file_path, "rb") as file:
        audio_data = file.read()
    b64_audio = base64.b64encode(audio_data).decode()
    href = f'<a href="data:audio/mp3;base64,{b64_audio}" download="{file_path}">{file_label}</a>'
    return href

# Function for real-time speech-to-text (optional feature)
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
    return ""

# Streamlit app interface
def main():
    st.title("Advanced Text-to-Speech Application")
    st.write("Enter text to convert to speech or use the microphone to input text.")
    
    # Choose language
    language_option = st.selectbox("Select Language", ['English', 'French', 'Spanish', 'German'])
    language_map = {'English': 'en', 'French': 'fr', 'Spanish': 'es', 'German': 'de'}
    selected_language = language_map[language_option]
    
    # Choose speech speed
    slow_speed = st.checkbox("Slow Speech", value=False)
    
    # Text input from the user or speech-to-text
    input_method = st.radio("Input method", ("Type text", "Use microphone"))
    if input_method == "Type text":
        text_input = st.text_area("Enter text here", "Hello! This is an advanced text-to-speech demo.")
    else:
        text_input = speech_to_text()

    # Button to generate speech
    if st.button("Convert to Speech"):
        if text_input:
            file_name = "output.mp3"
            # Convert text to speech
            text_to_speech_gtts(text_input, language=selected_language, slow=slow_speed, file_name=file_name)
            
            # Display success message and audio
            st.success("Speech generated successfully!")
            audio_file = open(file_name, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            
            # Provide download link
            st.markdown(get_audio_download_link(file_name, "Download the audio"), unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
