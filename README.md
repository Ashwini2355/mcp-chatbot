# 🤖 MCP Tool with LangChain + Groq

This project provides a command-line interface that uses Groq’s LLaMA 3 models (via LangChain) to interact with custom tools exposed through the **Model Context Protocol (MCP)**.

---

## 📌 What is this?

This tool allows users to query and interact with academic research data using natural language. It connects a conversational AI model to tools via **MCP**, such as:

- `search_papers`: Searches arXiv for papers on a given topic
- `extract_info`: Retrieves information about a specific paper by ID

These tools are implemented in an **MCP server**, and automatically invoked by the AI based on your input.

---

## 🚀 How to Access

### Step 1: Clone the repo

-> In your gitbash

git clone https://github.com/<your-username>/mcp-chatbot.git

cd mcp-chatbot

### step 2: Install dependencies

pip install -r requirements.txt

### Step 3: Run the tool server

uv run mcp_project/server.py

### Step 4: Start the chatbot (in a new terminal)

python mcp_project/client.py

**You will be prompted to enter your GROQ API key securely when the chatbot starts.**

*Install Node.js and npx (if not installed):*


sudo apt update


sudo apt install nodejs npm