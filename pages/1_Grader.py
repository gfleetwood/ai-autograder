import sys
sys.path.append("..")

import streamlit as st
import pandas as pd
import chromadb
from functions import *

st.set_page_config(layout = 'wide')
st.title('AI Grader')
st.header('Grading')

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name = "grader")

with st.form("marking-scheme-form", clear_on_submit = True):
  marking_scheme = st.file_uploader("Upload Marking Scheme", type = ["csv", "xlsx"])
  marked_responses = st.file_uploader("Upload Marked Responses", type = ["csv", "xlsx"])
  unmarked_responses = st.file_uploader("Upload Unmarked Responses", type = ["csv", "xlsx"])
  submitted = st.form_submit_button("UPLOAD")

if submitted:

  for question_info in marking_scheme.to_dict(orient = "records"): create_kb(collection, marked_responses, question_info)  
  ai_marked_responses = unmarked_responses.assign(ai_payload = lambda df: [mark_questions(collection, row) for row in df.to_dict(orient = "records")])
  
st.download_button(
  label = "Download Results",
  data = ai_marked_responses, 
  file_name = "marked_responses.csv", 
  mime = "text/csv"
)
