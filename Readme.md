AI Research Assistant
This project is a full-stack, real-time AI Research Assistant designed to help users quickly get summaries, references, and actionable suggestions on academic and scientific topics. The application features a dynamic, streaming user interface powered by Streamlit and a high-performance backend built with FastAPI, all while leveraging enterprise-grade AI from IBM Cloud.

Key Features
Live-Streaming Responses: Provides a real-time, ChatGPT-like experience by streaming the AI's response directly to the UI as it's generated.

Decoupled Architecture: Utilizes a professional, decoupled design with a dedicated frontend and backend, ensuring scalability and maintainability.

Enterprise AI Integration: Integrates with powerful AI models from IBM Cloud Services and the IBM Granite model to deliver high-quality, structured research summaries.

Query History: Saves and displays a history of user queries and responses for easy reference.

Structured Output: The AI's response is formatted into clear sections for Summary, References, and Suggestions, making the information easy to digest.

Technologies Used
Frontend: Streamlit

Backend: FastAPI & Uvicorn

AI Service: IBM Cloud Services & IBM Granite Model

Programming Language: Python

Libraries: requests, python-dotenv, pydantic

Key Concepts: Natural Language Processing (NLP)

How to Run Locally
To run this project on your local machine, you will need to set up both the backend and frontend in separate terminals.

Prerequisites:

Python 3.8+

A virtual environment (recommended)

Access to IBM Cloud Services with a deployed model and a generated API key.

Clone the Repository:

git clone <your-repository-url>
cd <your-project-directory>

Install Dependencies:

pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file in the root directory with your IBM API key and the URL of your deployed model.

IBM_API_KEY=your_ibm_api_key_here
DEPLOYMENT_URL=your_ibm_deployment_url_here

Run the Backend:
Open a terminal, navigate to the project directory, and start the FastAPI server.

uvicorn backend:app --reload

The server will run on http://127.0.0.1:8000.

Run the Frontend:
Open a second terminal, navigate to the project directory, and start the Streamlit application.

streamlit run ui.py

Your application will open automatically in your web browser.

Deployment

This project can be deployed using a variety of services, such as Streamlit Community Cloud for the frontend and Render or Railway for the FastAPI backend. You can also host the entire application from a single script on Streamlit by combining the backend logic into the main Streamlit file.

End Users
This tool is designed for:

Students and Researchers

Writers and Journalists

Lifelong Learners interested in academic and scientific topics