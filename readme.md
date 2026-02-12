## 🚀 Devcord

**Devcord** is an AI-based chatting platform for developers, built to enable intelligent and context-aware conversations.

It includes powerful features such as:

- 🤖 **RAG (Retrieval-Augmented Generation)** for context-aware AI responses  
- 🐙 **GitHub Tools Integration** for repository insights and developer workflows  
- 💬 Real-time chat architecture  
- ⚡ Scalable backend and modern frontend stack  

Devcord is designed to enhance developer collaboration by combining real-time communication with AI-driven intelligence.

Steps for Running the projects are given below:

Clone the GitHub repository to your local machine:
```bash
git clone https://github.com/Anonymous-Coder004/Discord.git
```
Set up the environment variables by creating the .env files in their respective directories using the specific formats provided below.

Backend Configuration
Create a file named .env inside the backend/ directory and paste the following:
```bash
# Database and Security
DATABASE_URL=postgresql+psycopg://<db_user>:<db_password>@<host>:<port>/<db_name>
SECRET_KEY=<your_generated_jwt_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=45

# AI and External Tools
GOOGLE_API_KEY=<your_google_gemini_api_key>
HUGGINGFACEHUB_API_TOKEN=<your_huggingface_token>
GITHUB_APP_ID=<your_github_app_id>
GITHUB_REPOSITORY=<username>/<repo_name>
GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n<your_private_key_content>\n-----END RSA PRIVATE KEY-----"
```

Frontend Configuration
Create a file named .env inside the frontend/ directory and paste the following:
```bash
VITE_BACKEND_BASEURL=http://127.0.0.1:8000
VITE_WS_BASEURL=ws://127.0.0.1:8000
```
### Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
### Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations to ensure your schema is up to date
alembic upgrade head

# Start the FastAPI server using Uvicorn
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
## 🌐 Live Demo

You can also visit the project using the deployed link:

🔗 https://devcord-two.vercel.app/

This project is deployed using **Render** for the backend and **Vercel** for the frontend.
