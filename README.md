# Business Information Chatbot

This project is a **Business Information Chatbot** built using **Streamlit**, **OpenAI GPT-4-Turbo**, and **PostgreSQL**. The chatbot allows users to query business information like business names, categories, locations, and opening hours directly from the database.

## Features
- Natural language chatbot interface
- Query business details like name, category, location, and hours
- GPT-4-Turbo integration for intelligent responses
- PostgreSQL database connectivity
- Interactive chat history
- Raw database data display (optional)

## Tech Stack
- Python
- Streamlit
- OpenAI API
- PostgreSQL (Neon.tech)
- SQLAlchemy

## Folder Structure
```
📁 Project Folder
├─ .streamlit/              # Streamlit configuration folder
│  └─ secrets.toml         # Secrets for API keys and DB URL
├─ app.py                  # Main Streamlit application
└─ requirements.txt        # Project dependencies
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/username/business-chatbot.git
cd business-chatbot
```

2. Create **`.streamlit/secrets.toml`** file:
```toml
[secrets]
OPENAI_API_KEY = "your_openai_api_key"
DB_URL = "your_database_url"
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud
1. Push the code to your **GitHub** repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your GitHub repository.
4. Add the **secrets** under the **Settings > Secrets** section.
5. Deploy the app!

## Example Queries
- What is the address of ABC Restaurant?
- Show me businesses in the "Hotel" category.
- What are the opening hours of XYZ Cafe?

## License
This project is licensed under the MIT License.

---
          **Kumar Mayank**
