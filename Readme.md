
# 🧠 AI Research Assistant

A **full-stack, real-time AI Research Assistant** designed to supercharge academic and scientific exploration.
Get **summaries, references, and actionable insights** instantly — all through a sleek UI powered by **Streamlit** and a high-performance **FastAPI** backend.

---

## ✨ Key Features

* ⚡ **Live-Streaming Responses** – Real-time, ChatGPT-like interaction with continuous streaming output.
* 🏗️ **Decoupled Architecture** – Professional separation of frontend (Streamlit) and backend (FastAPI) for scalability.
* 🤖 **Enterprise AI Integration** – Leverages **IBM Cloud Services** and the **IBM Granite model** for structured, high-quality results.
* 📝 **Query History** – Automatically saves and displays past queries & responses.
* 📑 **Structured Output** – Responses are neatly organized into:

  * **Summary**
  * **References**
  * **Suggestions**

---

## 🛠️ Tech Stack

**Frontend:** Streamlit

**Backend:** FastAPI + Uvicorn

**AI Services:** IBM Cloud Services (Granite Model)

**Language:** Python 🐍

**Libraries:** `requests`, `python-dotenv`, `pydantic`

**Concepts:** Natural Language Processing (NLP)

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python **3.8+**
* Virtual environment (recommended)
* IBM Cloud account with a deployed model + API key

---

### 📥 Installation

1. **Clone the Repository**

   ```bash
   git clone <your-repository-url>
   cd <your-project-directory>
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory:

   ```env
   IBM_API_KEY=your_ibm_api_key_here
   DEPLOYMENT_URL=your_ibm_deployment_url_here
   ```

---

### ▶️ Run Locally

#### 1️⃣ Start Backend (FastAPI)

```bash
uvicorn backend:app --reload
```

Server will be live at 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

#### 2️⃣ Start Frontend (Streamlit)

```bash
streamlit run ui.py
```

The app will open in your browser automatically 🌐

---

## 🌍 Deployment

* **Frontend** → Streamlit Community Cloud
* **Backend** → Render / Railway
* **Single Deployment Option** → Merge backend into Streamlit app

---

## 👥 End Users

This AI Assistant is perfect for:

* 🎓 **Students & Researchers** – Quick summaries & references
* ✍️ **Writers & Journalists** – Research and fact-checking aid
* 📚 **Lifelong Learners** – Explore academic & scientific knowledge with ease

---

