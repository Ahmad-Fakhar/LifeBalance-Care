import streamlit as st
import anthropic
# import os
# from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd

# Load environment variables from .env file
# load_dotenv()
# api_key = os.getenv("ANTHROPIC_API_KEY")
api_key = st.secrets("ANTHROPIC_API_KEY")

# Set the title of the app
st.title("LifeBalance Coach")

# Add a section for description and disclaimer
st.write("""
*Personalized Health and Wellness Coach* is a comprehensive tool designed to help you manage your health and wellness effectively.
By entering your details, we generate personalized exercise, meal, and disease management plans tailored to your needs.
""")

st.write("""
**Disclaimer**: This app provides general information and is not a substitute for medical advice. 
Always consult with a healthcare professional for medical concerns. Do not delay seeking medical advice 
because of something you read here.
""")

# Sidebar inputs for user details
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Age", min_value=18, max_value=100, step=1)
weight = st.sidebar.number_input("Weight (kg)", min_value=40, max_value=150, step=1)
height = st.sidebar.number_input("Height (m)", min_value=1.5, max_value=2.0, step=0.01)
exercise_frequency = st.sidebar.selectbox("Exercise Frequency", ["2-3 times a week", "3-4 times a week", "4-5 times a week"])
dietary_preferences = st.sidebar.text_input("Dietary Preferences (e.g., vegetarian, low-carb)")
disease_information = st.sidebar.text_input("Disease Information (e.g., diabetes, hypertension)")
goal = st.sidebar.selectbox("Goal", ["Weight Loss", "Weight Gain", "Maintain Weight", "Improve Overall Health"])

# Calculate BMI
bmi = weight / (height ** 2)
st.sidebar.write(f"Your BMI is: {bmi:.2f}")

# Generate personalized plans button
if st.sidebar.button("Generate Plans"):
    client = anthropic.Anthropic(api_key=api_key)
    
    # Define prompts for exercise, meal, and disease management plans
    exercise_prompt = (
        f"My age is {age}, "
        f"my weight is {weight} kg, "
        f"my height is {height} m, "
        f"my BMI is {bmi:.2f}, "
        f"I exercise {exercise_frequency}. "
        f"My dietary preferences are {dietary_preferences}. "
        f"I suffer from {disease_information}. "
        f"My goal is to {goal}. "
        "Please provide a personalized exercise plan that can help me achieve my goal."
    )
    
    meal_prompt = (
        f"My age is {age}, "
        f"my weight is {weight} kg, "
        f"my height is {height} m, "
        f"my BMI is {bmi:.2f}. "
        f"My dietary preferences are {dietary_preferences}. "
        f"I suffer from {disease_information}. "
        f"My goal is to {goal}. "
        "Please provide a personalized meal plan that can help me achieve my goal."
    )
    
    disease_prompt = (
        f"I suffer from {disease_information}. "
        f"My age is {age}, "
        f"my weight is {weight} kg, "
        f"my height is {height} m, "
        f"my BMI is {bmi:.2f}. "
        f"My goal is to {goal}. "
        "Please provide a personalized disease management plan that can help me achieve my goal."
    )
    
    # Call Claude AI API for exercise, meal, and disease management plans
    exercise_message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.7,
        system="You are a world-class fitness coach who specializes in personalized exercise planning.",
        messages=[
            {
                "role": "user",
                "content": exercise_prompt
            }
        ]
    )
    
    meal_message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.7,
        system="You are a world-class nutritionist who specializes in personalized meal planning.",
        messages=[
            {
                "role": "user",
                "content": meal_prompt
            }
        ]
    )
    
    disease_message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.7,
        system="You are a world-class healthcare professional who specializes in personalized disease management.",
        messages=[
            {
                "role": "user",
                "content": disease_prompt
            }
        ]
    )
    
    # Display personalized plans
    st.write("### Personalized Exercise Plan")
    st.markdown(f"<div style='color:#ffffff;'>{exercise_message.content[0].text}</div>", unsafe_allow_html=True)
    
    st.write("### Personalized Meal Plan")
    st.markdown(f"<div style='color:#ffffff;'>{meal_message.content[0].text}</div>", unsafe_allow_html=True)
    
    st.write("### Personalized Disease Management Plan")
    st.markdown(f"<div style='color:#ffffff;'>{disease_message.content[0].text}</div>", unsafe_allow_html=True)

    # Sample data for visualization
    data = pd.DataFrame({
        "Days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Calories": [1800, 1700, 1750, 1600, 1800, 1900, 2000]
    })

    # Displaying a line chart of calories over the week
    st.write("### Weekly Calorie Intake")
    plt.figure(figsize=(10, 4))
    plt.plot(data["Days"], data["Calories"], marker='o', color='#004d40')  # Dark teal color for the line
    plt.title('Calorie Intake Over the Week', fontsize=16, color='#ffffff')  # White for title
    plt.xlabel('Day', fontsize=14, color='#ffffff')
    plt.ylabel('Calories', fontsize=14, color='#ffffff')
    plt.grid(True)
    st.pyplot(plt)

# Footer
st.markdown("Developed by Ahmad Fakhar")
