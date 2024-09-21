from openai import OpenAI
import os, openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
# Set the OpenAI API key
openai.api_key = openai_api_key
client = OpenAI()


# Function to extract structured information from resume using OpenAI
def extract_resume_info(resume_text):
    data = {"candidate name": "extracted name",
    "phone number": +15879841956,
    "education details": ["bachelor of technology in engineering", "master of technology in engineering"],
    "relevant skills": ["python", "data science", "machine learning", "leadership", "sql"],
    "work experience": [{"position":"Principal Data scientist", "company":"Accenture", "duration":"3 years"}, 
                        {"position":"Sr Analyst", "company":"Google", "duration":"2 years"}],
    "certifications": ["certification 1", "certification 2"]}

    prompt_template = """ Extract the following information from the resume: \n\
    1. Candidate name \n
    2. Education details \n
    3. Relevant skills \n
    4. Work experience (positions, companies, and durations) \n
    5. Certifications\n
    ##Resume:\n{resume_text}## \n
    Please make sure the output is STRICTLY the 'JSON' format below \n
    {data}

    """
    prompt = prompt_template.format(data=data, resume_text=resume_text)

    response = client.chat.completions.create(
        model ="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Analyzing Resume"},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# Function to extract job requirements from job description using OpenAI
def extract_jobdesc_info(job_description_text):

    data = {"required skills": ["list of skills required for the role"],
            "education details": ["Highest educational Qualification for the role"],
            "required experience": ["Experiences required which are mentioned in Job desc"],
            "certifications": ["certification 1", "certification 2"]}

    prompt_template = """Extract the following information from the job description: \n\
    1. Required skills \n\
    2. Required experience \n\
    3. Required education \n\
    4. Certifications \n\nJob Description:\n
    ###Job description: \n\n
    {job_description_text}
    ###
    Please make sure the output is STRICTLY the 'JSON' format below \n
    {data}
    """
    prompt = prompt_template.format(data=data, job_description_text=job_description_text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Analyzing Job descriptions"},
            {"role": "user", "content": prompt}
        ])
    return response.choices[0].message.content