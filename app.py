import streamlit as st
import requests
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from prompts import (
    KNOWLEDGE_BASE_PROMPT,
    VERILOG_PROMPT,
    PROJECT_PROMPT
)

# page config
st.set_page_config(
    page_title="RTL Design Assistant",
    page_icon="🔌",
    layout="centered"
)

# sidebar
with st.sidebar:
    st.title("RTL Design Assistant")
    st.markdown("""
    An AI-powered assistant for VLSI and RTL design.
    
    **Mode 1 — Knowledge Base**  
    Ask anything about STA, timing, protocols, 
    flip-flops, CDC, FSMs
    
    **Mode 2 — Verilog Assistant**  
    Write Verilog modules, review RTL code, 
    catch latch inference and common bugs
    
    **Mode 3 — Project Assistant**  
    Generate boilerplate RTL, debug testbenches, 
    explain waveform behavior
    """)
    st.divider()
    st.markdown("[GitHub](https://github.com/yourusername/rtl-chatbot)")

# mode selector
mode = st.selectbox(
    "Select mode:",
    [
        "Mode 1 — Knowledge Base",
        "Mode 2 — Verilog Assistant",
        "Mode 3 — Project Assistant"
    ]
)

# map mode to prompt
def get_prompt_template(mode):
    if "Mode 1" in mode:
        return KNOWLEDGE_BASE_PROMPT
    elif "Mode 2" in mode:
        return VERILOG_PROMPT
    else:
        return PROJECT_PROMPT

# load ChromaDB — cached so it only loads once
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return vectorstore

vectorstore = load_vectorstore()

# function to query Ollama
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        return response.json()["response"]
    except Exception as e:
        return f"Error: Ollama is not running. Please start Ollama and try again. Details: {str(e)}"

# initialise chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

# clear chat history if mode changes
if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode

# display chat history
st.markdown(f"### {mode}")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# chat input
question = st.chat_input(
    "Ask your VLSI question here..."
)

if question:
    # show user message
    with st.chat_message("user"):
        st.write(question)

    # add to history
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # get answer
    with st.chat_message("assistant"):
        spinner_messages = {
    "Mode 1": "Searching knowledge base...",
    "Mode 2": "Reviewing RTL code...",
    "Mode 3": "Generating RTL assistance..."}
        spinner_text = "Thinking..."
        for key in spinner_messages:
            if key in mode:
                spinner_text = spinner_messages[key]
        with st.spinner(spinner_text):

            # retrieve top 3 chunks
            docs = vectorstore.similarity_search(
                question, k=3
            )
            context = "\n\n".join(
                [doc.page_content for doc in docs]
            )

            # build last 3 messages as conversation history
            history = ""
            recent = st.session_state.messages[-4:-1]
            if recent:
                history = "\n".join([
                    f"{m['role'].upper()}: {m['content']}"
                    for m in recent
                ])
                context = f"Previous conversation:\n{history}\n\n{context}"

            # get the right prompt for this mode
            prompt_template = get_prompt_template(mode)
            prompt = prompt_template.format(
                context=context,
                question=question
            )

            # get answer from LLM
            answer = ask_ollama(prompt)

        # display answer
        st.write(answer)

        # show retrieved source chunks
        with st.expander("View retrieved source chunks"):
            for i, doc in enumerate(docs):
                st.markdown(f"**Chunk {i+1}:**")
                st.write(doc.page_content)
                st.divider()

    # add assistant answer to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })