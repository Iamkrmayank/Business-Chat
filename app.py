import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import openai

# Retrieve API key and DB URL from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]
DB_URL = st.secrets["database"]["db_url"]

if not openai.api_key:
    st.error("OpenAI API key is not set.")
    st.stop()

# PostgreSQL Connection
engine = create_engine(DB_URL)

# Load data from the database into a DataFrame (cache for performance)
@st.cache_data
def load_business_data():
    query = """
    SELECT business_name, rating, reviews, category, address, opening_hours, status, website, directions_link, validation
    FROM validated_business_data
    """
    df = pd.read_sql(query, engine)
    return df

# Function to query the database based on user input
def query_database(user_query, df):
    user_query = user_query.lower()
    results = pd.DataFrame()

    if "name" in user_query or "business" in user_query:
        business_name = user_query.split("name")[-1].strip() or user_query.split("business")[-1].strip()
        results = df[df['business_name'].str.lower().str.contains(business_name, na=False)]
    elif "category" in user_query:
        category = user_query.split("category")[-1].strip()
        results = df[df['category'].str.lower().str.contains(category, na=False)]
    elif "location" in user_query or "address" in user_query:
        location = user_query.split("location")[-1].strip() or user_query.split("address")[-1].strip()
        results = df[df['address'].str.lower().str.contains(location, na=False)]
    elif "hours" in user_query or "opening" in user_query:
        hours = user_query.split("hours")[-1].strip() or user_query.split("opening")[-1].strip()
        results = df[df['opening_hours'].str.lower().str.contains(hours, na=False)]
    else:
        results = df

    return results

# Function to generate a response using OpenAI
def generate_response(user_query, db_results):
    if db_results.empty:
        return "Sorry, I couldn't find any matching business information in the database."

    context = db_results.to_string(index=False)
    prompt = f"""You are a helpful chatbot assisting with business information. Use the following data to answer the user's query:
    {context}

    User query: {user_query}
    Provide a concise and accurate response based on the data, or say 'I don’t have enough information' if the data doesn’t address the query."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot providing business information from a database."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Streamlit UI
st.title("Business Information Chatbot")

# Load the data
business_data = load_business_data()
st.write("Database loaded with", len(business_data), "business records.")

st.subheader("Ask about businesses, categories, locations, or opening hours!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    results = query_database(prompt, business_data)
    response = generate_response(prompt, results)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

if st.checkbox("Show Raw Database Data"):
    st.write(business_data)
