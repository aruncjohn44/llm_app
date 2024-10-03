from openai import OpenAI
import os, openai
from dotenv import load_dotenv
import re
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from fuzzywuzzy import fuzz
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
# Set the OpenAI API key
openai.api_key = openai_api_key
client = OpenAI()


# Load the Sentence Transformer model
model = SentenceTransformer('thenlper/gte-small')


# Function to extract structured information from resume using OpenAI
def extract_resume_info(resume_text):
    data = {"candidate name": "extracted name",
    "phone number": +15879841956,
    "education details": ["bachelor of technology in engineering", "master of technology in engineering"],
    "relevant skills": ["data science", "machine learning", "leadership", "people management"],
    "required tools": ["python", "c++", "pytorch", "pandas"],
    "work experience": [{"position":"Principal Data scientist", "company":"Accenture", "duration":"3 years"}, 
                        {"position":"Sr Analyst", "company":"Google", "duration":"2 years"}],
    "certifications": ["certification 1", "certification 2"]}

    prompt_template = """ Extract the following information from the resume(Please look in the entire document): \n\
    1. Candidate name \n
    2. Education details \n
    3. Relevant skills \n
    4. Required tools \n
    5. Work experience (positions, companies, and durations) \n
    6. Certifications\n
    ##Resume:\n{resume_text}## \n
    Please make sure the output is STRICTLY the 'JSON' format below and only contain text that can be converted to a json object. \n
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
            "required tools": ["python", "SQL", "Tensorflow", "pandas"],
            "education details": ["Highest educational Qualification for the role"],
            "required experience": ["Experiences required which are mentioned in Job desc"],
            "certifications": ["certification 1", "certification 2"]}

    prompt_template = """Extract the following information from the job description: \n\
    1. Required skills \n\
    2. Required tools
    3. Required experience \n\
    4. Required education \n\
    5. Certifications \n\nJob Description:\n
    ###Job description: \n\n
    {job_description_text}
    ###
    Please make sure the output is STRICTLY the 'JSON' format below and only contain text that can be converted to a json object. \n
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

# Function to compare CV and Job Description using GPT-4 lite for chain-of-thought prompting
def llm_compare_cv_to_job_description(resume_text, job_description_text):

    data = {'skills match': 0.6,
            'education match': 0.4,
            'experience match': 0.7,
            'overall match': 0.6}

    # Chain-of-thought prompting template
    prompt_template = """
    You are a career matching assistant. I will provide a CV and a job description, and your task is to evaluate the similarity between them. 
    Follow these steps:
    
    1. **Skills Match**: Compare the skills listed in the CV with those required in the job description. Are the required skills covered in the CV? Provide a match score between 0 to 1.
    
    2. **Education Match**: Compare the education requirements in the job description with the candidate's qualifications in the CV. Is the required level of education met? Provide a match score between 0 to 1.
    
    3. **Experience Match**: Compare the candidate's experience with the job requirements, focusing on the number of years, relevant industries, leadership experience, and specific accomplishments. Provide a match score between 0 to 1.
    
    4. **Overall Match**: Based on the above analysis (skills, education, and experience matches), provide an overall similarity score between 0 and 1. This score should reflect how well the CV matches the job description in all these aspects.
    
    ## CV: 
    {resume_text}

    ## Job Description: 
    {job_description_text}

    Now, please perform the evaluation and provide a breakdown for each category along with the final match score.
    Provide the values in a STRICTLY JSON format as shown below

    ## Output

    {data}

    """

    # Fill the prompt with actual data
    prompt = prompt_template.format(resume_text=resume_text, job_description_text=job_description_text, data=data)

    # Call the GPT-4 API to evaluate the match
    print(client)
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Analyzing Job descriptions"},
            {"role": "user", "content": prompt}], max_tokens=200, temperature=0.1)

    # Extract the result from GPT's response
    return response.choices[0].message.content


# Function to calculate match score between resume and job description
def calculate_match_score(resume_info, job_info):
    # Extract skills from both resume and job info using regex or manual parsing

    resume_skills_set = resume_info['relevant skills'] + resume_info['required tools']
    resume_skills_set = set(map(lambda x: x.lower(), resume_skills_set))

    job_skills_set = job_info['resume tools'] +job_info['required tools']
    job_skills_set = set(map(lambda x: x.lower(), job_skills_set))
 
    # Match percentage calculation
    
    if job_skills_set:
        matched_skills = resume_skills_set.intersection(job_skills_set)
        match_score = len(matched_skills) / len(job_skills_set) * 100
    else:
        match_score = 0.0

    return match_score, matched_skills

# Function to compute exact matches
def exact_match(resume_skills, job_skills):
    return list(set(resume_skills).intersection(set(job_skills)))

# Function to compute fuzzy matches (partial and token-set ratio)
def fuzzy_match(resume_skills, job_skills, threshold=80):
    fuzzy_matches = defaultdict(list)
    for resume_skill in resume_skills:
        for job_skill in job_skills:
            score = fuzz.token_set_ratio(resume_skill.lower(), job_skill.lower())
            if score >= threshold:
                fuzzy_matches[resume_skill].append((job_skill, score))
    return list(fuzzy_matches)

# Function to compute semantic matches using SentenceTransformer embeddings
def semantic_match(resume_skills, job_skills, threshold=0.75):
    semantic_matches = defaultdict(list)
    
    # Encode both resume and job skills to get sentence embeddings
    resume_embeddings = model.encode(resume_skills)
    job_embeddings = model.encode(job_skills)
    
    for i, resume_skill in enumerate(resume_skills):
        for j, job_skill in enumerate(job_skills):
            # Compute cosine similarity
            similarity = cos_sim(resume_embeddings[i], job_embeddings[j]).item()
            if similarity >= threshold:
                semantic_matches[resume_skill].append((job_skill, similarity))
    
    return list(semantic_matches)

# Main function to find overlapping skills
def match_skills(resume_info, job_info):

    resume_skills = resume_info['relevant skills'] + resume_info['required tools']
    resume_skills = list(set(map(lambda x: x.lower(), resume_skills)))

    job_skills = job_info['required tools'] +job_info['required tools']
    job_skills = list(set(map(lambda x: x.lower(), job_skills)))

    exact_matches = exact_match(resume_skills, job_skills)
    fuzzy_matches = fuzzy_match(resume_skills, job_skills)
    semantic_matches = semantic_match(resume_skills, job_skills)

    matched_skills = list(set(exact_matches + fuzzy_matches + semantic_matches))
    missing_skills = list(set(job_skills) - set(matched_skills))
    return matched_skills, missing_skills
