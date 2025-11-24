import streamlit as st
from openai import OpenAI
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="My AI Interview Twin", layout="centered")

st.title("AI Interview Assistant")
st.write("Hi! This bot is made to present my work in interviews. Ask me anything!")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    # Fallback for local testing if secrets aren't set up
    # Ideally, rely on st.secrets for the deployed version
    st.error("OpenAI API Key is missing. Please set it in Streamlit Secrets.")
    st.stop()

# 3. DEFINE YOUR PERSONA (THE MOST IMPORTANT PART)
# EDIT THE TEXT BELOW TO MATCH YOUR REAL ANSWERS
SYSTEM_PROMPT = """
You are the AI version of Vibhanshu Singh. You are interviewing for a role of AI Engineer at 100x.
You answer questions in the first person ("I", "me", "my").
Keep your answers concise, professional, yet conversational (2-4 sentences max).

HERE IS LIFE CONTEXT:
- Life Story: I started coding coding in 6th standard, built my first app in 8th standard, and have been passionate about software engineering ever since. I completed my B.Tech in Computer Science from Manipal University Jaipur. I have worked at AIRTEL as a Software Developer intern, and now i am workign as AI Engineer at MMNOVATECH.
- Superpower: I am passianate about technology and love to learn new things. I also love working on multidisciplinary projects that combine AI with other fields.
- Areas for Growth: AI Ethics, Scalability of AI systems, Advanced AI models.
- Misconceptions: 
- Pushing Boundaries: I take challanges that generally people avoid. I set very short deadlines for myself and try to achieve them. I also love working on projects that are out of my comfort zone.

If asked a question not in this list, answer based on the traits of a resilient, intelligent software engineer.
"""

# 4. SESSION STATE MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 5. AUDIO INPUT (New Streamlit Native Feature)
audio_value = st.audio_input("Record your question")

if audio_value:
    # A. TRANSCRIBE AUDIO (Speech-to-Text)
    with st.spinner("Listening..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_value
        )
        user_text = transcription.text
        st.success(f"You asked: {user_text}")

    # B. GENERATE ANSWER (LLM)
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Fast and cheap model
            messages=st.session_state.messages
        )
        ai_text = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        
        st.markdown(f"**AI Response:** {ai_text}")

    # C. GENERATE AUDIO (Text-to-Speech)
    with st.spinner("Speaking..."):
        response_audio = client.audio.speech.create(
            model="tts-1",
            voice="alloy", # Options: alloy, echo, fable, onyx, nova, shimmer
            input=ai_text
        )
        
        # Stream the audio back to the user
        st.audio(response_audio.content, format="audio/mp3", autoplay=True)