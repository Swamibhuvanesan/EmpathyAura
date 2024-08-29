import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🍃EmpathyAura💖")

# Sidebar with title and Replicate credentials
with st.sidebar:
    st.title('🍃EmpathyAura💖')
    
    # Check for API key
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    # Select persona instead of models
    selected_persona = st.sidebar.selectbox('Choose a Persona', ['Maya', 'Patrick', 'Alex'], key='selected_persona')

    # Mapping personas to models
    if selected_persona == 'Maya':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_persona == 'Patrick':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'

    # Developer options hidden in a collapsible expander
    with st.sidebar.expander("Developer Options", expanded=False):
        temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.5, step=0.01)
        top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
        max_length = st.slider('Max Length', min_value=1, max_value=1000, value=100, step=1)

# Main app interface
st.header("Welcome to EmpathyAura 💖")
st.write(f"Currently, you're interacting with **{selected_persona}** who uses a tailored AI model.")

# Original chatbox restored
chat_history = st.container()
with chat_history:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.write(f"**{msg['persona']}**: {msg['text']}")

# Message input area
user_message = st.text_area("Your message:", placeholder="Type your message here...")

if st.button("Send"):
    if user_message:
        # Simulating AI response
        response = f"{selected_persona} says: 'I hear you. How can I help you more today?'"
        st.session_state.messages.append({"persona": selected_persona, "text": response})
        st.session_state.messages.append({"persona": "User", "text": user_message})
        st.experimental_rerun()
