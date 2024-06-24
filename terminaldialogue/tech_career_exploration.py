# Python script to simulate terminal dialogue for career exploration 
import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Set up the environment for AI model interaction
os.environ["OPENAI_API_KEY"] = "null"
os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] = "mistral:latest"

# Initialize Ollama LLM
llm = ChatOpenAI(
    model_name=os.environ["OPENAI_MODEL_NAME"],
    base_url=os.environ["OPENAI_API_BASE"],
)

# Define career paths
career_paths = [
    "Software Development/Engineering",
    "DevOps/SRE",
    "Cloud Computing",
    "Machine Learning/AI",
    "Data Science/Analytics",
    "Cybersecurity",
    "Networking",
    "UX/UI Design",
    "Project Management",
    "Database Management",
]

# Function to gather user input
def gather_user_input():
    user_profile = {}

    # Gather user details through a series of professional questions
    print("Welcome to the Tech Career Exploration tool! Please answer the following questions to help us provide you with personalized career recommendations.\n")

    user_profile["degree"] = input("1. What is your highest level of education and the field of study? (e.g., Bachelor's in Computer Science) ")
    user_profile["experience"] = input("2. Could you please describe your relevant work experience, including internships and projects? ")
    user_profile["skills"] = input("3. What technical skills and programming languages are you proficient in? ")
    user_profile["interests"] = input("4. What areas of technology are you most passionate about or interested in exploring further? ")
    user_profile["work_preference"] = input("5. Do you prefer working independently or as part of a team? Do you thrive in fast-paced environments? ")
    user_profile["long_term_goals"] = input("6. What are your long-term career goals in the tech industry? ")

    return user_profile

# Function to simulate the dialogue and interaction
def simulate_dialogue():
    # Gather user input first
    user_profile = gather_user_input()

    print("\nThank you for providing your details. We will now analyze your profile to recommend suitable career paths.\n")

    # Initialize agents
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
        backstory="A recent graduate seeking guidance on the best tech career path for their skills and interests",
        llm=llm,
        verbose=True,
    )

    # Define tasks
    user_input_task = Task(
        description="Gather user's background information, skills, and interests",
        agent=user_agent,
        expected_output="Detailed user profile, including experience, skills, and interests",
    )

    career_recommendation_task = Task(
        description="Analyze user profile and provide personalized career recommendations",
        agent=career_agent,
        expected_output="Tailored list of recommended career paths with strengths, weaknesses, and next steps",
    )

    # Create the crew
    crew = Crew(
        agents=[user_agent, career_agent],
        tasks=[user_input_task, career_recommendation_task],
        verbose=2,
    )

    # Provide the detailed context for the user input task
    user_input_context = {
        "degree": user_profile["degree"],
        "experience": user_profile["experience"],
        "skills": user_profile["skills"],
        "interests": user_profile["interests"],
        "work_preference": user_profile["work_preference"],
        "long_term_goals": user_profile["long_term_goals"]
    }

    # Execute the user input task with the collected context
    user_agent_output = user_agent.execute_task(user_input_task, context=user_input_context)
    print("User Profile: ", user_agent_output)

    # Provide the detailed context for the career recommendation task
    career_recommendation_context = {
        "context": user_agent_output
    }

    # Execute the career recommendation task
    career_agent_output = career_agent.execute_task(career_recommendation_task, context=career_recommendation_context)
    print("Career Recommendations: ", career_agent_output)

    # Generate a call-to-action for consultation
    call_to_action = (
        "To further discuss your career options and receive personalized guidance, "
        "please book a video consultation with us. We can also assist you with courses "
        "and certifications to enhance your profile in the tech market."
    )
    print(call_to_action)

# Run the dialogue simulation
simulate_dialogue()

# Logic Explanation:
# 1. We set up the environment and initialize the Ollama LLM.
# 2. We define potential career paths in technology.
# 3. We gather user inputs through a structured dialogue.
# 4. We create two agents: one for gathering user information (User) and another for providing career recommendations (Career Exploration Expert).
# 5. We define tasks for gathering user information and providing career recommendations.
# 6. We create a Crew with the defined agents and tasks.
# 7. We execute tasks using the collected user inputs to generate personalized career recommendations.
# 8. We generate a call-to-action encouraging the user to book a consultation for further assistance.