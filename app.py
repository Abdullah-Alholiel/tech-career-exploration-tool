import logging
from pydantic import ValidationError
import streamlit as st
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
from streamlit_tags import st_tags
import fitz  # PyMuPDF

# Set up the environment for AI model interaction
os.environ["OPENAI_API_KEY"] = "null"
os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] = "phi3:latest"

# Streamlit UI Configuration
st.set_page_config(page_title="Tech Career Exploration Tool", layout="centered", initial_sidebar_state="expanded")

# Initialize Ollama LLM
llm = ChatOpenAI(
    model=os.environ["OPENAI_MODEL_NAME"],
    base_url=os.environ["OPENAI_API_BASE"],
)

# Define career paths
career_paths = [
    "Software Development/Engineering",
    "DevOps/SRE",
    "Cloud Computing",
    ""
    "Machine Learning/AI",
    "Data Science/Analytics",
    "Cybersecurity",
    "Networking",
    "UX/UI Design",
    "Project Management",
    "Database Management",
]

# Custom CSS for styling
st.markdown(
    """
    <style>
    .nav-buttons {
        display: flex;
        justify-content: space-between;
    }
    .nav-button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state['step'] = 0
if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = {
        "degree": "",
        "experience": "",
        "skills": [],
        "interests": "",
        "work_preference": "",
        "long_term_goals": "",
        "cv_content": ""
    }

# Steps for the form
steps = ["Introduction", "Background Information", "Technical Skills", "Interests and Preferences", "Upload CV (Optional)", "Review and Submit"]

# Function to handle each step
def introduction():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>🎓 Welcome to the Tech Career Exploration Tool! 🚀</h1>
            <p style="font-size: 18px;">
                At our agency, we specialize in guiding students and graduates towards the perfect career path in the tech industry.
                Navigate through the steps using the sidebar to provide your information and embark on your journey to a successful tech career!
            </p>
            <img src="https://images.unsplash.com/photo-1556761175-4b46a572b786" alt="Tech Career" style="width: 100%; height: auto; margin-top: 20px;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("### Use the sidebar to navigate through the steps and provide your information.")
    st.sidebar.image("https://images.unsplash.com/photo-1581093458799-8175d07c027a", width=150)

def background_information():
    st.header("📚 Background Information")
    st.session_state['user_profile']["degree"] = st.text_input("1. What is your highest level of education and the field of study?", st.session_state['user_profile']["degree"])
    st.session_state['user_profile']["experience"] = st.text_area("2. Describe your relevant work experience, including internships and projects.", st.session_state['user_profile']["experience"])

def technical_skills():
    st.header("💻 Technical Skills")
    skills = st_tags(
        label="3. What technical skills and programming languages are you proficient in?",
        text="",
        suggestions=["Python", "Java", "C++", "JavaScript"],
        maxtags=10,
        key="skills_tags"
    )
    st.session_state['user_profile']["skills"] = st.session_state['user_profile']["skills"] + skills

def interests_and_preferences():
    st.header("🌟 Interests and Preferences")
    st.session_state['user_profile']["interests"] = st.text_area("4. What areas of technology are you most passionate about or interested in exploring further?", st.session_state['user_profile']["interests"])
    st.session_state['user_profile']["work_preference"] = st.text_area("5. Do you prefer working independently or as part of a team? Do you thrive in fast-paced environments?", st.session_state['user_profile']["work_preference"])
    st.session_state['user_profile']["long_term_goals"] = st.text_area("6. What are your long-term career goals in the tech industry?", st.session_state['user_profile']["long_term_goals"])

def upload_cv():
    st.header("📄 Upload CV (Optional)")
    uploaded_file = st.file_uploader("Upload your CV", type=["txt", "pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Read PDF file
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
            st.session_state['user_profile']["cv_content"] = text
        else:
            # Handle text files
            st.session_state['user_profile']["cv_content"] = uploaded_file.read().decode("utf-8")

def review_and_submit():
    st.header("🔍 Review and Submit")
    st.write("### Review your information:")
    for key, value in st.session_state['user_profile'].items():
        st.write(f"**{key.capitalize()}:** {value or 'NA'}")

    if st.button("Submit"):
        st.write("Analyzing your profile...")

        career_agent = Agent(
            role="Career Exploration Expert",
            goal="Provide personalized career recommendations based on user input",
            backstory="An experienced career counselor with deep knowledge of the tech industry",
            llm=llm,
            verbose=True,
            memory=True,
        )

        user_agent = Agent(
            role="User",
            goal="Explore potential tech career paths and receive personalized recommendations",
            backstory="A recent graduate or student seeking guidance on the best tech career path for their skills and interests",
            llm=llm,
            verbose=True,
        )

        # Construct user profile context as a list
        user_input_context = [
            {
                "key": "degree",
                "value": st.session_state['user_profile']["degree"],
                "description": "This is the user's degree",
                "expected_output": "Processed degree information"
            },
            {
                "key": "experience",
                "value": st.session_state['user_profile']["experience"],
                "description": "This is the user's experience",
                "expected_output": "Processed experience information"
            },
            {
                "key": "skills",
                "value": st.session_state['user_profile']["skills"],
                "description": "This is the user's skills",
                "expected_output": "Processed skills information"
            },
            {
                "key": "interests",
                "value": st.session_state['user_profile']["interests"],
                "description": "This is the user's interests",
                "expected_output": "Processed interests information"
            },
            {
                "key": "work_preference",
                "value": st.session_state['user_profile']["work_preference"],
                "description": "This is the user's work preference",
                "expected_output": "Processed work preference information"
            },
            {
                "key": "long_term_goals",
                "value": st.session_state['user_profile']["long_term_goals"],
                "description": "This is the user's long-term goals",
                "expected_output": "Processed long-term goals information"
            }
        ]

        if st.session_state['user_profile'].get("cv_content"):
            user_input_context.append({
                "key": "cv_content",
                "value": st.session_state['user_profile']["cv_content"],
                "description": "This is the user's CV content",
                "expected_output": "Processed CV content information"
            })

        try:
            user_input_task = Task(
                description="Gather user's background information, skills, and interests",
                agent=user_agent,
                context=user_input_context,
                expected_output="Detailed user profile, including experience, skills, and interests"
            )

            career_recommendation_task = Task(
                description="Analyze user profile and provide personalized career recommendations",
                agent=career_agent,
                context=user_input_context,
                expected_output="Tailored list of recommended career paths with strengths, weaknesses, and next steps"
            )

            crew = Crew(
                agents=[user_agent, career_agent],
                tasks=[user_input_task, career_recommendation_task],
                verbose=2,
            )

            result = crew.kickoff()
            st.write("### Career Recommendations")
            st.write(result)
            st.write("🚀 Ready to take the next step? Book a consultation with our expert career advisors today and unlock your potential in the tech industry! 🌟")
        except ValidationError as e:
            logging.error("Validation error occurred: %s", e)
            st.write("### Debug: ValidationError")
            st.write(e)
        except Exception as e:
            logging.error("An error occurred: %s", e)
            st.write("### Error")
            st.write("Oops, something went wrong. Please try again later.")

        
# Step handling
step = st.session_state['step']
if step == 0:
    introduction()
elif step == 1:
    background_information()
elif step == 2:
    technical_skills()
elif step == 3:
    interests_and_preferences()
elif step == 4:
    upload_cv()
elif step == 5:
    review_and_submit()

# Add navigation buttons
st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
if step != 0:
    if st.button("Previous", key="prev"):
        st.session_state['step'] = step - 1
        st.experimental_rerun()

if step != len(steps) - 1:
    if st.button("Next", key="next"):
        st.session_state['step'] = step + 1
        st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("♻️ Navigation")
st.sidebar.selectbox("Go to", steps, index=step, key='step_radio', on_change=lambda: st.session_state.update({'step': steps.index(st.session_state.step_radio)}))

# Function to reset the form
def reset_form():
    for key in st.session_state['user_profile'].keys():
        st.session_state['user_profile'][key] = ""
    st.session_state['step'] = 0
    st.experimental_rerun()

# Add a reset button
if st.sidebar.button("Reset Form"):
    reset_form()
