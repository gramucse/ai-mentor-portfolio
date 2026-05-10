"""Day 5 Lab 5A — Résumé-Scorer Streamlit (free tools)
Usage: streamlit run Day5_Resume_Scorer_app.py
"""
import streamlit as st
from google import genai
import os, json

st.set_page_config(page_title='Résumé Scorer', layout='wide')
st.title('Résumé vs JD Fit Scorer')
st.caption('Day 5 Lab 5A — Free tools end-to-end')

col1, col2 = st.columns(2)
with col1:
    resume = st.text_area('Paste résumé', height=400)
with col2:
    jd = st.text_area('Paste job description', height=400)

api_key = (
    st.secrets.get("GEMINI_API_KEY", None)
    or st.text_input("Gemini API key", type="password")
)

if st.button('Score') and resume and jd and api_key:
    with st.spinner('Scoring...'):
        client = genai.Client(api_key=api_key)
        prompt = f"""You are a placement coach. Given this résumé and JD,
return JSON: {{
  "score": int 0-100,
  "technical_skills_match": int 0-100,
  "soft_skills_match": int 0-100,
  "experience_relevance": int 0-100,
  "project_fit": int 0-100,
  "rationale": str,
  "missing_skills": [str],
  "learning_resources": [{"skill": str, "resource_type": str, "link": str}],
  "suggestions": [str]
}}. For "learning_resources", identify the top 3 missing skills and suggest one free YouTube channel or free course for each.

Résumé:
{resume}

JD:
{jd}"""
        resp = client.models.generate_content(
            model='gemini-2.5-flash', contents=prompt,
            config={'response_mime_type': 'application/json'})
        result = json.loads(resp.text)
        st.metric('Fit Score', f"{result['score']}/100")

        # Score Breakdown Chart
        breakdown_data = {
            "Technical Skills": result.get('technical_skills_match', 0),
            "Soft Skills": result.get('soft_skills_match', 0),
            "Experience": result.get('experience_relevance', 0),
            "Projects": result.get('project_fit', 0)
        }
        st.bar_chart(breakdown_data)

        st.subheader('Rationale')
        st.write(result['rationale'])
        st.subheader('Missing skills')
        for s in result['missing_skills']:
            st.write(f'- {s}')
        st.subheader('Suggestions')
        for s in result['suggestions']:
            st.write(f'- {s}')

        st.subheader('Top 3 Missing Skills & Learning Resources')
        for item in result.get('learning_resources', []):
            st.write(f"**{item['skill']}** ({item['resource_type']}): [Link]({item['link']})")


