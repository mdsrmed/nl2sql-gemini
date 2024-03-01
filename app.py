import os 
from dotenv import load_dotenv
import streamlit as st 
import sqlite3 
import google.generativeai as genai 

load_dotenv() 
genai.configure(api_key = os.getenv("GEMINI_KEY"))


# Function to load google gemini model and provide sql query 
def gemini_response(question,promt):
    model=genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0],question])
    return response.text

# Function to retrieve query from sql database 
def fetch_sql_query(sql,db):
    conn=sqlite3.connect(db) 
    cur=conn.cursor() 
    cur.execute(sql) 
    rows=cur.fetchall()
    conn.commit
    conn.close() 
    
    for row in rows:
        print(row)
        
    return rows

## Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION and MARKS \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """
]

# Streamlit app

st.set_page_config(page_title="Retrieve SQL query")
st.header("Retrieve SQL data with Gemini")
question=st.text_input("Input: ",key="Input")
submit=st.button("Ask the question")

if submit:
    # Here Gemini is generating proper sql queries to retrieve data from database
    response=gemini_response(question,prompt)
    print(response)
    data=fetch_sql_query(response,"student.db")
    st.subheader("The response is")
    for row in data: 
        print(row)
        st.header(row)