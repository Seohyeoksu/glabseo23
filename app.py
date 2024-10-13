import openai
import streamlit as st
from difflib import SequenceMatcher
import streamlit.components.v1 as components

# OpenAI API 키 설정
openai.api_key = st.secrets['API_KEY']

# 초기 대본 정의
initial_script = [
    "Narrator: It's a beautiful fall morning on the farm.",
    "Narrator: The leaves are turning yellow and red.",
    "Narrator: Fern comes to visit Wilbur, her favorite pig.",
    "Fern: Good morning, Wilbur! How are you today?",
    "Wilbur: Oh, Fern! I'm so happy to see you. I was feeling a little lonely.",
    "Fern: Don't be lonely, Wilbur. You have so many friends here on the farm!",
    "Charlotte: Good morning, Fern. You're right, Wilbur has many friends, including me.",
    "Wilbur: Charlotte! I'm so glad you're here. Fern, isn't Charlotte amazing? She can make the most beautiful webs."
]

if 'current_line' not in st.session_state:
    st.session_state.current_line = 0
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTextInput>div>div>input {
        background-color: #e6f3ff;
        border-radius: 5px;
    }
    h1 {
        color: #2E8B57;
        text-align: center;
    }
    h2 {
        color: #4682B4;
    }
    .script-line {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🕷️ Charlotte's Web Interactive Learning 🐷")

def text_to_speech(text):
    # 브라우저 기반 TTS를 위한 JavaScript 사용
    escaped_text = text.replace("'", "\\'").replace("\n", " ")
    tts_html = f"""
    <script>
        var utterance = new SpeechSynthesisUtterance('{escaped_text}');
        window.speechSynthesis.speak(utterance);
    </script>
    """
    components.html(tts_html, height=0, width=0)

def generate_response(prompt):
    st.session_state.conversation_history.append({"role": "user", "content": prompt})

    try:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4o",  # 또는 "gpt-4"로 변경 가능
            messages=[
                {"role": "system", "content": "You are an AI tutor helping a student learn English through the story of Charlotte's Web. Provide explanations, answer questions, and engage in dialogue about the story, characters, and language used. Keep your responses appropriate for young learners."},
                *st.session_state.conversation_history
            ]
        )

        ai_response = chat_completion.choices[0].message.content.strip()
        st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "I'm sorry, I encountered an error. Please try again."

def evaluate_speech_accuracy(original_text, recognized_text):
    similarity = SequenceMatcher(None, original_text.lower(), recognized_text.lower()).ratio()
    return similarity * 100

st.sidebar.header("Full Script")
for i, line in enumerate(initial_script):
    st.sidebar.markdown(f'<div class="script-line">{line}</div>', unsafe_allow_html=True)
    if st.sidebar.button(f"🔊 Listen", key=f"listen_{i}"):
        text_to_speech(line)

# 순차적 듣기 기능 복원
st.header("🎧 Sequential Listening")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⏮️ Previous line") and st.session_state.current_line > 0:
        st.session_state.current_line -= 1

with col2:
    if st.button("▶️ Listen to current line"):
        text_to_speech(initial_script[st.session_state.current_line])

with col3:
    if st.button("⏭️ Next line") and st.session_state.current_line < len(initial_script) - 1:
        st.session_state.current_line += 1

st.info(f"Current line: {initial_script[st.session_state.current_line]}")

# 대화형 학습 섹션
st.header("💬 Interactive Learning")
user_input = st.text_input("Ask a question about the story, characters, or language:")

if st.button("🚀 Submit") and user_input:
    with st.spinner("AI Tutor is thinking..."):
        ai_response = generate_response(user_input)
    st.success("AI Tutor: " + ai_response)
    if st.button("🔊 Listen to AI response"):
        text_to_speech(ai_response)

st.header("📜 Conversation History")
for message in st.session_state.conversation_history:
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**AI Tutor:** {message['content']}")
