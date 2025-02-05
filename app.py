import os
import yt_dlp
import whisper
import streamlit as st
import google.generativeai as genai

# Set page config
st.set_page_config(
    page_title="🎥 AI Video Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for light theme
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    div.stButton > button {
        background-color: #000000;
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        height: 4em;
        width: 100%;
        margin: 20px 0;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1a1a1a;
        color: white !important;
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .success-message {
        padding: 20px;
        border-radius: 10px;
        background-color: #D1E7DD;
        color: #0F5132;
    }
    .error-message {
        padding: 20px;
        border-radius: 10px;
        background-color: #F8D7DA;
        color: #842029;
    }
    </style>
    """, unsafe_allow_html=True)

# Configure Gemini API with your key
genai.configure(api_key="ADD-Your-API-Key-Here") #Gemini API Key


def download_audio(youtube_url, output_folder=r"C:\Users\umars\Video Audios\xyz"):
    # In folder path you can change the path to save the audio file
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)


        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, 'xyz.%(ext)s'),
            'ffmpeg_location': r'C:\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin\ffmpeg.exe',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            return os.path.join(output_folder, 'xyz.webm'), info.get('title', 'Unknown Title')

    except Exception as e:
        st.error(f"Error while downloading audio: {e}")
        return None, None

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
        
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

def summarize_text_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Summarize the following text in few line:\n\n{text}")
        summary = response.text.strip()
        return summary

    except Exception as e:
        st.error(f"Error during summarization with Gemini: {e}")
        return None

def main():
    st.markdown("# 🎥 YouTube Video Summarizer 🤖")
    st.markdown("### 🌟 Turn any YouTube video into a quick summary with AI magic! ✨")
    
    youtube_url = st.text_input("🔗 Paste YouTube URL here:", placeholder="https://youtube.com/...")
    
    if st.button("🚀 Generate Summary", help="Click to start the magic!"):
        if youtube_url:
            progress_bar = st.progress(0)
            
            # Fun loading messages for downloading
            with st.spinner("🎵 Downloading audio... 🎧 *beep boop*"):
                audio_file_path, video_title = download_audio(youtube_url)
                progress_bar.progress(33)

            if audio_file_path:
                st.markdown(f"📽️ **Now Processing**: _{video_title}_")
                
                # Fun loading messages for transcription
                with st.spinner("🎯 Converting speech to text... 🔊 ➡️ 📝"):
                    transcribed_text = transcribe_audio(audio_file_path)
                    progress_bar.progress(66)

                if transcribed_text:
                    # Fun loading messages for AI processing
                    with st.spinner("🤖 AI is working its magic... ✨💫 *processing intensifies*"):
                        summary = summarize_text_gemini(transcribed_text)
                        progress_bar.progress(100)
                        
                        if summary:
                            st.balloons()  # Add celebratory balloons!
                            st.markdown("---")
                            st.markdown("### 📝 Summary Ready! 🎉")
                            st.info(summary)
                            
                            with st.expander("📚 View Full Transcription"):
                                st.markdown(transcribed_text)

                    os.remove(audio_file_path)
                    st.markdown("""
                        <div class="success-message">
                            ✨ Magic Complete! ✨<br>
                            🎉 Your summary is ready to read! 🎈
                        </div>
                        """, 
                        unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="error-message">
                    ⚠️ Oops! We need a YouTube URL to work our magic! 🎥
                </div>
                """, 
                unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        Made with ❤️ using Streamlit, Whisper AI, and Gemini
        <br>
        🎵 → 📝 → 🤖 → 📚
        <br>
        ✨ Where AI meets creativity! ✨
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()




