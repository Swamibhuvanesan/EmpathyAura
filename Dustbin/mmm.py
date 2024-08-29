import streamlit as st
import replicate
import os

# App title and configuration
st.set_page_config(page_title="🍃EmpathyAura💖")

# Replicate Credentials
with st.sidebar:
    st.title('🍃EmpathyAura💖')
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
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe07607'
elif selected_persona == 'Patrick':
    llm = 'some-model-for-mindfulness'  # Replace with the actual model
elif selected_persona == 'Alex':
    llm = 'some-model-for-listening'    # Replace with the actual model

# Adding Character Images
persona_images = {
    'Maya': 'maya_image.png',
    'Patrick': 'patrick_image.png',
    'Alex': 'alex_image.png'
}
st.image(persona_images[selected_persona], width=200)

# Example: Adding Different Dialogue Styles for Each Persona
persona_dialogues = {
    'Maya': {
        'greeting': "Hello, I'm Maya, your CBT therapist. How can I assist you today?",
        'prompt': lambda user_input: f"Let's explore that thought a bit more. Why do you think {user_input}?"
    },
    'Patrick': {
        'greeting': "Hi there! I'm Patrick, your mindfulness coach. Let's focus on some breathing exercises together.",
        'prompt': lambda user_input: "Try to focus on your breath and let the thought pass without judgment."
    },
    'Alex': {
        'greeting': "Hey, I'm Alex, here to listen. What's on your mind?",
        'prompt': lambda user_input: f"I hear you saying {user_input}. Can you tell me more about how that feels?"
    }
}

# Display Greeting Message Based on Persona
st.write(persona_dialogues[selected_persona]['greeting'])

# Input from the user
user_input = st.text_input("What's on your mind?", key='user_input')

# Integrate Different Therapeutic Techniques
def cbt_technique(user_input):
    return f"Let's think about why {user_input} is troubling you. What evidence do you have for or against this thought?"

def mindfulness_technique():
    return "Close your eyes and take a deep breath. Focus on the feeling of air filling your lungs."

def empathetic_listener_technique(user_input):
    return f"It sounds like you're feeling {user_input}. That's completely valid."

# Generate the response based on the selected persona and user input
if user_input:
    if selected_persona == 'Maya':
        response = cbt_technique(user_input)
    elif selected_persona == 'Patrick':
        response = mindfulness_technique()
    elif selected_persona == 'Alex':
        response = empathetic_listener_technique(user_input)

    st.write(response)

# To-Do: Add further interaction options and improvements (buttons, sliders, feedback loops, etc.)
