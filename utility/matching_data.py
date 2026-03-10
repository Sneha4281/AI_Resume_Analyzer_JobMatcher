def find_matching_and_missing_skills(job_skills, resume_text):
    resume_text = resume_text.lower()

    matching = []
    missing = []

    for skill in job_skills:
        if skill in resume_text:
            matching.append(skill)
        else:
            missing.append(skill)

    return matching, missing
