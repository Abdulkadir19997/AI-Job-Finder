import streamlit as st
import read_pdfs
import pandas as pd
import requests
import json

api = 'http://localhost:8000/predict'

def shorten_url(url):
    return f'<a href="{url}" target="_blank">apply</a>'

def main():
    # Center the title using HTML and CSS
    st.markdown(
        "<h1 style='text-align: center;'>AI Job Finder</h1>", 
        unsafe_allow_html=True
    )
    
    job_title = st.text_input('Please provide the Job Title to be searched')
    job_location = st.text_input('Please provide the location of post')
    job_search_number = st.number_input('Please provide number of job posts',step=1)
    
    resume_upload = st.file_uploader('Please Upload Resume/CV', type='pdf')

    if job_title and job_location and job_search_number:
        with st.spinner(''):
            if resume_upload is not None:
                read_resume = read_pdfs.extract_text_from_pdf(resume_upload)
                # st.write(read_resume)
                st.write('Resume Uploaded Successfully!')
            else:
                st.warning('Please Add Resume', icon="⚠️")
    
    if st.button('Start'):
        if job_title == '' or len(job_title) <= 4 or job_location == '':
            st.warning('Please Write Job Title or Job Location', icon="⚠️")
        
        feature_data = {
            'job_title': job_title,
            'job_location': job_location,
            'job_search_number': job_search_number,
            'resume': read_resume
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=api, data=json.dumps(feature_data), headers=headers)
        
        response_dataset = pd.DataFrame(response.json()['score'])
        response_dataset = response_dataset[['title', 'link', 'company', 'location', 'date', 'Similarity Scores']]
        response_dataset['link'] = response_dataset['link'].apply(shorten_url)
        response_dataset = response_dataset.sort_values(by=['Similarity Scores'], ascending=False)

        # Center the Prediction Results title
        st.markdown(
            "<h2 style='text-align: center;'>Prediction Results</h2>", 
            unsafe_allow_html=True
        )
        st.write(response_dataset.to_html(escape=False), unsafe_allow_html=True)
        st.write('Here are the results!')

if __name__ == "__main__":
    main()
