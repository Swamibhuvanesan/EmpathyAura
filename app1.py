import streamlit as st
import replicate
import os

# Set the page configuration with a mental health theme
st.set_page_config(page_title="🍃EmpathyAura💖", page_icon="🌸", layout="centered")

# Sidebar with Persona Selection
with st.sidebar:
    st.title('🍃EmpathyAura💖')
    st.subheader("Your Mental Health Companion")

    # API Token Input
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    # Persona Selection with Mental Health Themes
    selected_persona = st.selectbox('Choose a Persona', ['Maya (Empathetic)', 'Patrick (Motivational)', 'Alex (Reflective)'], key='selected_persona')

# Assign LLM based on selected persona
if selected_persona == 'Maya (Empathetic)':
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    persona_prompt = "You are Maya, an empathetic and nurturing mental health chatbot. Your role is to provide emotional support and validation."
elif selected_persona == 'Patrick (Motivational)':
    llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    persona_prompt = "You are Patrick, a motivational mental health chatbot. Your role is to offer positive reinforcement and encourage positive actions."
else:
    llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    persona_prompt = "You are Alex, a reflective and insightful mental health chatbot. Your role is to help users engage in deep reflection and mindfulness."

# Developer Options
with st.sidebar.expander("Developer Options", expanded=False):
    temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.5, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=1, max_value=1000, value=100, step=1)

# Main Content Area
st.title(f"Welcome to EmpathyAura - {selected_persona.split()[0]}")
st.write("This persona is here to support your mental health journey. Please enter your message below:")

# Input prompt
user_input = st.text_area("Your message:")

# Send the request to the selected LLM
if st.button('Generate Response'):
    if not user_input:
        st.warning("Please enter a message to receive a response.")
    else:
        # Use the API to get the response from the LLM
        response = replicate.run(llm, input={"prompt": f"{persona_prompt}\nUser: {user_input}\nResponse:"})
        st.write(response)
