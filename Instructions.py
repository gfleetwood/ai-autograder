import streamlit as st
import pandas as pd

st.set_page_config(layout = 'wide')
 
st.title('AI Grader')

st.header('Instructions')

st.text("""The first step is to upload your marking scheme in this format.""")

st.dataframe(pd.read_csv("1_marking_scheme - Sheet2.csv"),  use_container_width = True)

st.text("""The second is to upload examples of how you mark student responses in this format.""")

st.dataframe(pd.read_csv("2_student_responses_marked - Sheet2.csv"),  use_container_width = True)

st.text("""Lastly, upload the student responses you want marked.""")

st.dataframe(pd.read_csv("3_student_responses_unmarked - Sheet2.csv"),  use_container_width = True)

st.text("""And you receive a file with the questions graded.""")

st.dataframe(pd.read_csv("4_student_responses_marked_by_ai.csv"),  use_container_width = True)
