
import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🍃EmpathyAura💖")

# Replicate Credentials
with st.sidebar:
    st.title('🍃EmpathyAura💖')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
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

# Function to display messages in a chat-like style
def display_message(message, is_user=False, user_image_base64=None):
    if is_user:
        st.markdown(f"<div style='text-align: right; margin-bottom: 10px;'>🧑‍💻: {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
            <img src='data:image/png;base64,{user_image_base64}' width='40' style='border-radius: 30%; margin-right: 30px;' />
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)
        
# Adding Character Images
persona_images = {
    'Maya': 'Dustbin/maya.png',
    'Patrick': 'Dustbin/patrick.png',
    'Alex': 'Dustbin/alex.png'
}
st.image(persona_images[selected_persona], width=200)
    
# Developer options hidden in a collapsible expander
with st.sidebar.expander("Developer Options", expanded=False):
    temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.5, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=1, max_value=1000, value=100, step=1)
    
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{f"role": "assistant", "content": "Hello! I'm EmpathyAura, your supportive companion. How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm EmpathyAura, your supportive companion. How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating EmpathyAura's response
def generate_empathyaura_response(prompt_input):
    string_dialogue = "You are a supportive and empathetic assistant focused on helping users with their mental health. Respond with understanding, compassion, and practical advice. Always remind the user to seek professional help if needed."
    
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
    # Adding a basic crisis management check
    crisis_keywords = ["suicide", "self-harm", "end my life", "give up"]
    if any(word in prompt_input.lower() for word in crisis_keywords):
        crisis_response = "I'm really sorry you're feeling this way, but I'm not equipped to help in this situation. Please reach out to a mental health professional or contact a crisis hotline immediately."
        return [crisis_response]
    
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_empathyaura_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

# Feedback Mechanism
st.sidebar.subheader('Feedback')
st.sidebar.text_area("Please provide your feedback on EmpathyAura", key='feedback')
st.sidebar.button('Submit Feedback', on_click=lambda: st.success('Thank you for your feedback!'))
