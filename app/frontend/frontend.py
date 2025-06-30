import streamlit as st
import requests

st.set_page_config(
    page_title="Role Based Chat Bot",
    page_icon=":robot:",
    layout="wide")
st.markdown(
    """
    ## Welcome to the Role Based Chat Bot
    This application allows you to ask questions based on your role.
    Please enter your name and password, select your role, and start chatting!
    """)

name = st.text_input(
    "Enter your name",
    placeholder="Type your name here...",
    key="name_input")
password = st.text_input(
    "Enter your password",
    type="password",
    placeholder="Type your password here...",
    key="password_input")

role = st.selectbox(
    "Select a role",
    ["engineering", "marketing", "finance", "hr"], index=0)


##  call /login api here based on the name, password and role selected

if "login_success" not in st.session_state:
    st.session_state["login_success"] = False
if st.button("Login", key="login_button"):
    if name and password and role:
        try:
            # Use HTTP Basic Auth instead of JSON
            response = requests.post(
                "http://127.0.0.1:8000/login",
                auth=(name, password),  # Use HTTP Basic Auth
                timeout=5
            )
            if response.status_code == 200:
                st.session_state["login_success"] = True
                st.session_state["user_role"] = response.json().get("role")
                st.session_state["username"] = name
                st.success(f"Login successful! Welcome {name}")
            else:
                st.session_state["login_success"] = False
                st.error(f"Login failed: {response.json().get('detail', 'Invalid credentials')}")
        except Exception as e:
            st.session_state["login_success"] = False
            st.error(f"Error connecting to API: {e}")

if st.session_state.get("login_success"):
    st.write(f"Logged in as: **{st.session_state.get('username')}** (Role: **{st.session_state.get('user_role')}**)")
    
    question = st.text_area("Ask a question based on your role", height=100, placeholder="Type your question here...", key="question_input")
    if st.button("Submit", key="submit_button"):
        if question:
            try:
                # Use HTTP Basic Auth for chat endpoint too
                resp = requests.post(
                    "http://127.0.0.1:8000/chat/",  # Note the trailing slash
                    json={"message": question, "role" : st.session_state.get('user_role')},  # Use correct field name
                    auth=(st.session_state.get('username'), password),  # Use stored auth
                    timeout=10
                )
                if resp.status_code == 200:
                    response_data = resp.json()
                    answer = response_data.get("answer", "No answer returned.")
                    source = response_data.get("source", "No source provided.")
                    st.text_area("Response:", value=f"{answer}\n\nSource: {source}", height=200, key="response_area")
                else:
                    error_detail = resp.json().get("detail", "Failed to get response from server.")
                    st.text_area("Response:", value=f"Error: {error_detail}", height=200, key="response_area")
            except Exception as e:
                st.text_area("Response:", value=f"Error: {e}", height=200, key="response_area")
else:
    st.info("Please login to ask questions.")


st.markdown(
    """
    ## How to use this app
    1. Select a role from the sidebar.
    2. Type your question in the text area.
    3. Click the Submit button to get a response.
    
    This app is designed to provide role-specific responses based on your input.
    """
)


