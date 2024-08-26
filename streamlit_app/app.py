import streamlit as st
import ollama
import requests
import numpy as np
from numpy.linalg import norm
import json
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama.llms import OllamaLLM

backend_url = "http://127.0.0.1:5000/search"

def get_embeddings(chunks, modelname="mxbai-embed-large"):
    embeddings = []
    for chunk in chunks:
        if chunk.strip(): 
            embedding = ollama.embeddings(model=modelname, prompt=chunk)["embedding"]
            if len(embedding) > 0:  
                embeddings.append(embedding)
    return embeddings

def find_most_similar(needle, haystack):
    if len(needle) == 0 or len(haystack) == 0:
        return []
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

if "conversation_chain" not in st.session_state:
    conversation_memory = ConversationBufferMemory()
    st.session_state["conversation_chain"] = ConversationChain(
        llm=OllamaLLM(model="llama3.1"),  
        memory=conversation_memory,
        verbose=True
    )

# Initialize chat history and context
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "context" not in st.session_state:
    st.session_state["context"] = []

if "content_texts" not in st.session_state:
    st.session_state["content_texts"] = []
    st.session_state["content_embeddings"] = []

def generate_response(user_question, retrieved_content):
    system_prompt = (
        "You are a helpful assistant who answers questions based on the following content. "
        "Answer using the provided content as your primary source, and if the answer is not "
        "in the content or you are unsure, say 'I don't know.'\n\n"
        f"Content:\n{retrieved_content}\n\n"
        "Now, respond to the following question:\n"
    )

    conversation_chain = st.session_state["conversation_chain"]
    assistant_reply = conversation_chain.predict(input=system_prompt + user_question)
    
    st.session_state["context"].append({"role": "user", "content": user_question})
    st.session_state["context"].append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

st.title("QA Chatbot with Enhanced UI")

for message in st.session_state["messages"]:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        try:
            with st.spinner("Retrieving content..."):
                response = requests.get(backend_url, params={"query": query})
                response.raise_for_status()
                data = response.json()
                preprocessed_content = data.get('preprocessed_content', [])
                
                if preprocessed_content:
                    content_texts = preprocessed_content
                    content_embeddings = get_embeddings(content_texts, "mxbai-embed-large")
                    st.session_state["content_texts"] = content_texts
                    st.session_state["content_embeddings"] = content_embeddings
                    st.success("Content retrieved and processed successfully!")
                else:
                    st.error("No content retrieved. Please try a different query.")
                    st.stop()

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to retrieve data: {e}")
            st.stop()

user_question = st.text_input("Ask a question about the content:")

if st.button("Get Answer"):
    if user_question:
        st.session_state["messages"].append({"role": "user", "content": user_question})
        
        with st.chat_message("user"):
            st.markdown(user_question)

        try:
            with st.spinner("Processing your question..."):
                prompt_embedding = ollama.embeddings(
                    model="mxbai-embed-large", 
                    prompt=user_question
                )["embedding"]

                if len(prompt_embedding) == 0:
                    st.error("Failed to generate an embedding for your question.")
                    st.stop()

                most_similar_chunks = find_most_similar(prompt_embedding, st.session_state["content_embeddings"])[:5]

                if not most_similar_chunks:
                    st.error("No similar content found.")
                    st.stop()

                # Use the most relevant chunks as retrieved content
                retrieved_content = "\n".join(
                    [st.session_state["content_texts"][idx] for _, idx in most_similar_chunks]
                )

                assistant_reply = generate_response(user_question, retrieved_content)
                
                st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})
                
                with st.chat_message("assistant"):
                    st.markdown(assistant_reply)

        except Exception as e:
            st.error(f"Error in retrieving answer: {e}")
