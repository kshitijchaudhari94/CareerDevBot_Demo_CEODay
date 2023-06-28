from dataclasses import dataclass
from typing import Literal
import streamlit as st
import streamlit.components.v1 as components
from fuzzywuzzy import fuzz

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0


def on_click_callback(qna_list):
    human_prompt = st.session_state.human_prompt

    # Search for the closest matching question in the Q&A list
    highest_similarity = 0
    closest_question = None
    for question, _ in qna_list:
        similarity = fuzz.ratio(question.lower(), human_prompt.lower())
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_question = question

    if closest_question is not None:
        # Retrieve the corresponding answer
        answer = next(response for q, response in qna_list if q == closest_question)
        st.session_state.history.append(Message("human", human_prompt))
        st.session_state.history.append(Message("ai", answer))
    else:
        st.session_state.history.append(Message("human", human_prompt))
        st.session_state.history.append(Message("ai", "I'm sorry, I don't have an answer to that question."))


def load_qna_list():
    # Load your Q&A list here
    qna_list = [
        ("what is the career development framework?", "The Career Development Framework is a tool that enables BC members to develop in their careers by giving a clear understanding of progression opportunities, and guiding L&D choices. In the annual assessment process, you and your manager will review your skills and development criteria set out in the Career Development Framework, which will give you tangible guidance to assist you in moving through your career with BC."),
        ("I am a level 2 venture builder and I am thinking about a career in sales. What training should I focus on to get started?", "The sales track in the career development framework contains an additional set of technical sales skills which are not included in the venture builder track. As a level 2 venture builder, I therefore recommend you attend the Red Team session 'An Introduction to Sales as a Science'. This course will give you an introduction to the fundamental principles of sales and guide you through different techniques used in the sales process."),
        ("CareerDevBotPOC, could you remind me what training I should focus on following my last performance review?", "Sure. Based on the outcomes of your performance review on hibob and your Red Team data, your main development goals for this year are to evolve your understanding of product-market fit and to improve your management skills. I see you have already completed the Red Team course on ‘Management essentials’. Well done! I recommend you now enroll in the Red Team Product Development Sprint which is designed to accelerate your journey toward creating successful and impactful products."),
        ("CareerDevBotPOC, will my salary increase as a result of my performance review?", "Bonus allocation remains discretionary as per employee contracts and is subject to company performance, so while your review may contribute to your bonus allocation, it does not directly determine your salary increase. I suggest discussing any salary increase-related questions with your line manager."),
        ("Hello Bot", "Hi, How can I help you today?")
    ]
    return qna_list

load_css()
initialize_session_state()
qna_list = load_qna_list()

st.image("/Users/kshitijchaudhari/Documents/CareerDevBot/BC-Logo.png", width=200)
st.markdown("<h1 style='text-align: center; color: red; font-family: Arial, sans-serif; font-weight: bold; font-size: 32px;'>CareerDevBot</h1>", unsafe_allow_html=True)

# # Set the title
# st.markdown("<h1 style='text-align: center; color: red;style='font-family: Arial, sans-serif; font-weight: bold; font-size: 24px;'>CareerDevBotPOC</h1>", unsafe_allow_html=True)

# logo_image = "/Users/kshitijchaudhari/Documents/Streamlit_Chatbot/BC-Logo.png"



chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

with chat_placeholder:
    for chat in st.session_state.history:
        if chat.origin == 'ai':
            div = f"""
    <div class="chat-row 
        {'' if chat.origin == 'ai' else 'row-reverse'}">
        <img class="chat-icon" src="app/static/{
            'ai_icon.png' if chat.origin == 'ai' 
                        else 'user_icon.png'}"
            width=32 height=32>
        <div class="chat-bubble
        {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
            &#8203;{chat.message}
        </div>
    </div>
            """
            st.markdown(div, unsafe_allow_html=True)
        
    for _ in range(3):
        st.markdown("")

with prompt_placeholder:
    st.markdown("**Chat**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        value=" ",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit", 
        type="primary", 
        on_click=lambda: on_click_callback(qna_list),
    )
if st.button("Reset"):
    # Clear the session state and refresh the page
    st.session_state.history = []
    st.session_state.token_count = 0
    components.html("<script>window.location.reload();</script>")
components.html("""
<script>
const streamlitDoc = window.parent.document;
const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Submit'
);
streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""", 
    height=0,
    width=0,
)

