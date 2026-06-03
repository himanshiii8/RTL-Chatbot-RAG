import requests
import json

questions = [
    "What is setup time in VLSI?",
    "What is hold time in VLSI?",
    "What is slack in static timing analysis?"
]

results = []

for question in questions:
    print(f"Asking: {question}")
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": question,
            "stream": False
        }
    )
    
    answer = response.json()["response"]
    print(f"Answer: {answer}")
    print("-" * 50)
    
    results.append({
        "question": question,
        "answer": answer
    })

with open("vlsi_answers.json", "w") as f:
    json.dump(results, f, indent=2)

print("All answers saved to vlsi_answers.json")