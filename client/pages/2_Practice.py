import streamlit as st
from app.questgen.quest_gen import QuestGen
# Initial setup
st.set_page_config(
    page_title="Practice",
    page_icon="👋",
)
inference_endpoint = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def select_mode():
    st.write("# Hi, select the quiz mode. 👋")
    paper = st.selectbox(
        "Select Paper...",
        ("GS 1", "GS 2", "GS 3")
    )    
    if paper:
        st.selectbox(
            "Select Subject...",
            ("All",) + get_subjects(paper)
        )
    
    if st.button("Next"):
        st.session_state.mode = option
        st.session_state.page = 'quiz'
        print(st.session_state.page)
        st.rerun()


def quiz():
    st.session_state.max_q = 30
    st.session_state.atm_q = 0
    col1, col2 = st.columns([3, 1])
    col2.subheader("Summary")
    col2.write(f"Attempted: {st.session_state.atm_q}")
    col2.write(f"Remaining: {st.session_state.max_q - st.session_state.atm_q}")
    # generate question
    QuestGen(inference_endpoint, mode=st.session_state.mode, name=st.session_state.name)
    # write question + options

    # next button -> new question 
    


def show_results():
    pass


if st.session_state.page == 'home':
    select_mode()
elif st.session_state.page == 'quiz':
    quiz()
else:
    show_results()

