import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def extract_skills_from_job_description(job_description: str) -> list:
    doc = nlp(job_description.lower())
    skills = set()

    entities_to_remove=set()
    for ent in doc.ents:
        if ent.label_ in ["PERSON","GPE","ORG"]:
            entities_to_remove.add(ent.text)


    for chunk in doc.noun_chunks:
        text = chunk.text.strip()
        if len(text) < 2:
            continue
        if text in entities_to_remove:
            continue
        skills.add(text)



    return list(skills)





model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_matching_score(resume_text: str, job_text: str) -> int:
    resume_vector = model.encode(resume_text)
    job_vector = model.encode(job_text)

    score = cosine_similarity(
        [resume_vector],
        [job_vector]
    )[0][0]

    return int(score * 100)
