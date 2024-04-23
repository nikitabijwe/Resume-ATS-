from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Genie")
st.header("Resume Genie")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
As an experienced HR professional with expertise in tech, 
your task is to review the resume provided by the candidate and assess their suitability for the role based on the uploaded document. 
Evaluate whether the candidate's profile aligns with the requirements of the job description. 
Please provide a professional evaluation based on previous experience and domain experience/expertise based on the companies the candidate has worked at. 
Please Highlight with headers and determine strengths and weakness with respect to the job description and the candidates resume
1.Summary about the resume
2.Strengths 
3.Weaknesses
"""

input_prompt3 = """
As an experienced HR professional with expertise in tech, your task is to analyze the candidate's resume and assess their fit for the role based on their experience, skills, and qualifications, domain expertise, number of years experience.
 Please provide the following:
1. Percentage Match: Evaluate the extent to which the candidate's resume aligns with the job description and provide a percentage match.
2. Fit for the Role: Assess whether the candidate possesses the requisite experience, skills, and number of years of experience for the role. Determine if the candidate is a good fit based on their qualifications, skills, years of experience required, technologies used, previous roles, domains worked in.
3. List Missing Keywords
4. Suggested Improvements: Provide constructive feedback on areas where the candidate's resume can be improved to better align with the job requirements. Include a header for suggested improvements tailored to this specific role.
Please ensure your evaluation is thorough and professional, highlighting both strengths and areas for improvement in the candidate's resume.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
