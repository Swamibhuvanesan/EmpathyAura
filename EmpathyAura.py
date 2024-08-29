import streamlit as st
import replicate
import os

st.set_page_config(page_title="🍃EmpathyAura💖")

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

selected_persona = st.sidebar.selectbox('Choose a Persona', ['Maya', 'Patrick', 'Alex'], key='selected_persona')

if selected_persona == 'Maya':
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
elif selected_persona == 'Patrick':
    llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
else:
    llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'

with st.sidebar.expander("Developer Options", expanded=False):
    temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.5, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=1, max_value=1000, value=100, step=1)

os.environ['REPLICATE_API_TOKEN'] = replicate_api

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm EmpathyAura, your supportive companion. How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in replicate.run(
            llm,
            input={"prompt": prompt, "temperature": temperature, "top_p": top_p, "max_length": max_length},
        ):
            full_response += response
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
