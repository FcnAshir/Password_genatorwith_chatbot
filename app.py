import re
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configure Page
st.set_page_config(
    page_title="SmartBit Pro - Password Strength Checker",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Error: Missing API key. Please check your .env file.")

# Configure API
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.0-flash"

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be **at least 8 characters long**.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Password should include **both uppercase and lowercase letters**.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Password should include **at least one number (0-9)**.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include **at least one special character (!@#$%^&*)**.")

    if score == 4:
        st.success("✅ **Strong Password** - Your password is secure.")
    elif score == 3:
        st.info("⚠️ **Moderate Password** - Consider improving security.")
    else:
        st.error("❌ **Weak Password** - Follow suggestions below to strengthen it.")
    
    if feedback:
        with st.expander("🔵 **Improve Your Password**"):
            for item in feedback:
                st.write(item)
    
    return score, feedback

# Function to generate strong password suggestions
def suggest_password():
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction="You are a security expert. Provide strong password suggestions that include uppercase, lowercase, numbers, and special characters. Avoid generic answers."
        )
        response = model.generate_content("Suggest a strong password with explanations.")
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# UI Components
st.title("Password Strength Checker")
st.write("Enter a password to check its strength or get strong password suggestions.")

password = st.text_input("Enter your password:", type="password", help="Ensure your password is strong 🔒")

if st.button("Check Strength"):
    if password:
        check_password_strength(password)
    else:
        st.warning("⚠️ Please enter a password first!")

st.divider()
st.subheader("💡 Need Help? Get a Strong Password Suggestion!")
if st.button("Generate Strong Password"):
    with st.spinner("🔐 Generating..."):
        suggestion = suggest_password()
        st.success(suggestion)
