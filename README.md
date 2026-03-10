# AI_Resume_Analyzer_JobMatcher
# AI Resume Analyzer & Job Matcher

## Project Overview
AI Resume Analyzer & Job Matcher is a backend system that analyzes a candidate’s resume and compares it with a job description to determine how well the resume matches the job requirements.

The system uses Natural Language Processing (NLP) techniques to extract skills from the resume and job description, then calculates a similarity score to determine the match percentage.

This project helps job seekers understand how well their resume fits a particular job role.



## Features
- Upload and analyze resumes
- Extract skills from resume and job description
- Match resume with job description
- Calculate match percentage
- Identify missing skills
- Provide suggestions for improving the resume



## Tech Stack
- Python
- FastAPI
- NLP (Natural Language Processing)
-  Similarity matching
- PostgreSQL
- UUID based document handling



## How It Works
1. The user uploads a resume.
2. The system extracts text from the resume.
3. NLP techniques are used to identify skills and keywords.
4. The job description is also processed using NLP.
5. The system compares resume skills with job requirements.
6. A match score is generated along with missing skills.