
import streamlit as st
from dotenv import load_dotenv # type: ignore
from utils import *
import uuid
import clipboard # type: ignore


st.set_page_config(page_title="Resume Screening Assistance")

#Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] =''

def main():
    load_dotenv()

    st.title("HR - Resume Screening Assistance.🔎")
    st.subheader("I can help you in resume screening process")
#--------------------------------------------------------------------------------------------------------------------
    expander_text = """
            ### Sample Job Description: Junior ML Engineer at ExampleTech

            **About ExampleTech:**
            ExampleTech is a leading provider of innovative technology solutions for modern businesses. Our cutting-edge products and services empower companies to thrive in today's digital world.

            **About the Role:**
            As a Junior ML Engineer at ExampleTech, you will be responsible for integrating Language Models into our codebase. The ideal candidate will have a strong background in Python and a deep understanding of large language models and related libraries.

            **Responsibilities:**
            - Collaborate with the Product teams to integrate Language Models into our Product
            - Develop and maintain unit and integration tests
            - Write clear and concise documentation
            - Work closely with other engineers on cross-functional projects

            **Qualifications:**
            - Bachelor's degree in Computer Science or a related field
            - 1-3 years of relevant experience
            - Proficiency in Python
            - Familiarity with LangChain, Llama Index, and Pinecone is a plus
            - Strong problem-solving and analytical abilities
            - Excellent communication and teamwork skills

            **Why ExampleTech:**
            - Join a dynamic team dedicated to building a globally recognized technology company.
            - Opportunity to make a meaningful impact, establish processes, and explore new challenges.
            - Exposure to an international audience, enriching your professional experience.
            - Engage with supportive colleagues, enjoy a positive work culture, and experience a flat hierarchy.

            **Perks:**
            - Health and wellness benefits for employees and their families
            - Professional development budget
            - Flexible work hours and generous leave policy

            **ExampleTech is an equal opportunity employer.** We celebrate diversity and are committed to creating an inclusive environment for all employees.

            """
#--------------------------------------------------------------------------------------------------------------------

    with st.expander('**Example job description for Junior ML Engineer**'): 
        if st.button("Copy Expander Text"):
            clipboard.copy(expander_text)
            st.success("Expander text copied to clipboard!")   
        st.info(expander_text)

    
    job_description = st.text_area("Please paste the 'JOB DESCRIPTION' here...",key="1")
    document_count = st.text_input("No.of 'RESUMES' to return",key="2")
    # Upload the Resumes (pdf files)
    pdf = st.file_uploader("Upload resumes here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)

    submit=st.button("Help me with the analysis")

    if submit and job_description:
        with st.spinner('Wait for it...'):

            #Creating a unique ID, so that we can use to query and get only the user uploaded documents from PINECONE vector store
            st.session_state['unique_id']=uuid.uuid4().hex

            #Create a documents list out of all the user uploaded pdf files
            final_docs_list=create_docs(pdf,st.session_state['unique_id'])
            # st.write(final_docs_list)#-------------------------------------

            # Displaying the count of resumes that have been uploaded
            st.write("*Resumes uploaded* :"+str(len(final_docs_list)))

#             #Create embeddings instance
            embeddings=create_embeddings_load_data()
            # st.write(embeddings.embed_query("This is a test document."))#-------------------------------------
            
            #Push data to PINECONE
            ##push_to_pinecone(pinecone_apikey,pinecone_index_name,embeddings,docs):
            vectordb=push_to_pinecone(embeddings=embeddings,docs=final_docs_list)

            # Fecth relavant documents from PINECONE
            relavant_docs=similar_docs(vectordb,job_description,document_count,st.session_state['unique_id'])
            # st.write(relavant_docs)#--------------------------------------------------------------------------

            #Introducing a line separator
            st.write(":heavy_minus_sign:" * 30)

            #For each item in relavant docs - we are displaying some info of it on the UI
            for item in range(len(relavant_docs)):
                
                st.subheader("👉 "+str(item+1))

                #Displaying Filepath
                st.write("**File** : "+relavant_docs[item][0].metadata["name"])

                #Introducing Expander feature
                with st.expander('Show me Match Score and Content👀'): 
                    st.info("**Match Score** : "+str(relavant_docs[item][1]))
                    # st.write("***"+relavant_docs[item][0].page_content)

                    #Gets the summary of the current item using 'get_summary' function that we have created which uses LLM & Langchain chain
                    # st.write(relavant_docs[item][0])#--------------------
                    # st.write(relavant_docs[item][0].page_content)#--------------------
                    summary = get_summary(relavant_docs[item][0])['output_text']
                    st.write("**Summary** : "+str(summary))

        st.success("Hope I was able to save your time⏰")


#Invoking main function
if __name__ == '__main__':
    main()





