# RTL Design Assistant Chatbot

An AI-powered assistant for VLSI and RTL design questions, 
built with Retrieval-Augmented Generation (RAG). Retrieves 
context from a curated chip design knowledge base before 
answering — reducing hallucinations and improving accuracy 
over baseline LLMs.

## What it does
- Answers RTL and VLSI questions (timing, flip-flops, 
  Verilog, STA, power)
- Retrieves relevant context from a domain-specific 
  knowledge base using semantic search
- Shows which source documents were used for each answer

## Architecture
User question → Sentence embedding → ChromaDB vector search 
→ Top-3 chunk retrieval → LLM answer with context

## Tech stack
Python · LangChain · ChromaDB · Sentence-Transformers · 
Streamlit · Gemini API

## Results
RAG chatbot vs baseline LLM on 50-question VLSI benchmark:


## How to run
[fill this in once app.py is working]
