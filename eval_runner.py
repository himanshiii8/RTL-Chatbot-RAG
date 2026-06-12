import pandas as pd
import requests
import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db",
    embedding_function=embeddings
)
def ask_rag(question):
    # retrieve top 3 chunks
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""You are a VLSI expert. Answer the question using 
only the context below. Be concise — 2-3 sentences maximum.

Context:
{context}

Question: {question}
Answer:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

def ask_baseline(question):
    # ask LLM directly with no RAG context
    prompt = f"""Answer this VLSI question in 2-3 sentences:
{question}"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

df = pd.read_csv("eval_ques.csv", skiprows=1, names=["questions", "answers", "category"])
results = []

print(f"Running evaluation on {len(df)} questions...")

for i, row in df.iterrows():
    question = row["questions"]
    correct = row["answers"]
    categories = row["category"]
    
    print(f"Q{i+1}: {question}")
    
    rag_answer = ask_rag(question)
    baseline_answer = ask_baseline(question)
    
    results.append({
        "question": question,
        "correct_answer": correct,
        "rag_answer": rag_answer,
        "baseline_answer": baseline_answer,
        "category": categories
    })
    
    print(f"Done Q{i+1}")

# save results
results_df = pd.DataFrame(results)
results_df.to_csv("eval_results.csv", index=False)
print("Saved to eval_results.csv")

