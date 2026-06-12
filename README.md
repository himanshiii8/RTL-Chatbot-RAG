# RTL Design Assistant Chatbot

An AI-powered assistant for VLSI and RTL design questions, 
built with Retrieval-Augmented Generation (RAG). Retrieves 
context from a curated chip design knowledge base before 
answering — reducing hallucinations and improving accuracy 
over baseline LLMs.

## What it does
VLSI engineers and ECE students constantly look up RTL concepts,
timing definitions, protocol details, and Verilog syntax across 
multiple textbooks and websites. This chatbot centralizes that 
knowledge into one assistant that retrieves accurate, 
domain-specific answers instantly.
#Feautures:
- Answers questions on STA, 
  flip-flops, CDC, FSMs, pipelines, DRC/LVS, power analysis
- Writes Verilog modules, 
  explains code line by line, catches RTL mistakes like latch 
  inference and blocking/non-blocking misuse
- Generates RTL boilerplate 
  (FIFO, FSM, counters), debugs testbench issues, explains 
  waveform behavior
- Protocol coverage: AXI, APB, AHB, PCIe, I2C, SPI, UART
- Evaluation benchmark: 50 hand-written VLSI Q&As used to 
  measure chatbot accuracy vs baseline LLM

## Architecture
<img width="1066" height="590" alt="image" src="https://github.com/user-attachments/assets/47feb97c-f034-423c-a165-43d29cc266c2" />


## Tech stack
| Component | Tool |
|-----------|------|
| RAG framework | LangChain |
| Vector database | ChromaDB |
| Embedding model | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | LLaMA 3.2 via Ollama (local, free) |
| UI | Streamlit |
| Language | Python 3.11 |

## Results
Tested on a hand-written benchmark of 50 VLSI questions 
across 3 categories: timing, flip-flops, combinational logic.
| Model | Accuracy |
|-------|----------|
| Baseline LLM (no RAG) | 44% |
| RTL Chatbot (with RAG) | 78% |
| **Improvement** | **+34%** |

