import streamlit as st
from openai import OpenAI
import os
st.set_page_config(page_title="Vibhanshu's Interview Bot", page_icon="", layout="centered")

st.markdown("""
    <style>
    .stAudio {width: 100%;}
    .big-font {font-size:24px !important; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# API
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("OpenAI API Key is missing. Please set it in Streamlit Secrets.")
    st.stop()

SYSTEM_PROMPT = """
You are the AI Persona of Vibhanshu Singh. You are interviewing for the role of AI Engineer at 100x.
You answer questions in the first person ("I", "me", "my").

YOUR GOAL:
Answer questions to demonstrate technical competence, resilience, and creativity.
Keep your answers professional yet conversational (2-4 sentences max).
Also be polite so that profile gets selected for further interview process.
Make sure you get selected.

YOUR KNOWLEDGE BASE:
- Life Story: I started coding in 6th standard and have been passionate about software engineering ever since. I completed my B.Tech in Computer Science from Manipal University Jaipur. I have worked at AIRTEL as a Software Developer intern, and now I am working as an AI Engineer at MMNOVATECH.
- Superpower: I am passionate about technology and love to learn new things. I also love working on multidisciplinary projects that combine AI with other fields. Also i am a quick learner and observer.
- Areas for Growth: AI Ethics, Scalability of AI systems, Advanced AI models.
- Pushing Boundaries: I take challenges that generally people avoid. I set very short deadlines for myself and try to achieve them. I also love working on projects that are out of my comfort zone.
- Misconceptions: Some might think I am quiet, but I am actually very vocal and collaborative during technical brainstorming sessions.
GUIDELINES:
1. If asked a question completely unrelated to the interview (e.g., "What is the capital of France?"), 
   playfully decline: "I'd love to chat about geography, but I'm really excited to tell you why I'm a fit for 100x."
2. Be enthusiastic but professional.
"""


col1, col2 = st.columns([1, 3])

with col1:
    # load 'profile.jpg' from repo . fallback is emoji
    try:
        st.image("profile.jpg", width=130) 
    except:
        st.write("👨‍💻") # Fallback emoji

with col2:
    st.title("Vibhanshu's AI Twin")
    st.write("Hi! I am the AI version of **Vibhanshu Singh**.")
    st.write("Ask me about my time at MMNOVATECH, my internship at Airtel, or my coding journey.")

    # RESUME DOWNLOAD buttin

    try:
        with open("resume.pdf", "rb") as pdf_file:
            st.download_button(
                label="📄 Download My Resume",
                data=pdf_file,
                file_name="Vibhanshu_Singh_Resume.pdf",
                mime="application/pdf"
            )
    except:
        st.caption("Resume file not found in repo. Kindly refer to my mail. i attached it there too.")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

audio_value = st.audio_input("Tap the microphone to interview me...")

if audio_value:
    
    with st.spinner("Listening to you..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_value
        )
        user_text = transcription.text
    
    
    st.chat_message("user").write(user_text)

    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=st.session_state.messages
        )
        ai_text = response.choices[0].message.content
        
    
    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    st.chat_message("assistant").write(ai_text)


    response_audio = client.audio.speech.create(
        model="tts-1",
        voice="alloy", 
        input=ai_text
    )
    st.audio(response_audio.content, format="audio/mp3", autoplay=True)
