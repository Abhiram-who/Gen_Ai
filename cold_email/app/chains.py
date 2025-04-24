import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm=ChatGroq(
    model="llama3-70b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    )
    
    def extract_jobs(self, cleaned_text):
        prompt_extract= PromptTemplate.from_template(
    """ 
    ###SCRAPED TEXT: 
    {page_data}
    The text is from the career page of a data science company.
    Extract the job postings and return them in JSON format containing the following fields:
    - job title
    - job description
    - skills required
    - location
    - salary
    - decription
    Only return valid JSON
    ### VALID JSON(NO PREAMBLE TEXT):
    """
     )
        chain_extract= prompt_extract | self.llm
        res= chain_extract.invoke(input={'page_data':cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res= json_parser.parse(res.content)
            if not isinstance(res, list):
                res = [res]
            # Validate structure (optional but recommended)
            for job in res:
             if not isinstance(job, dict):
                 raise OutputParserException("Job is not a dictionary")
             if 'jobDescription' not in job:
                 job['jobDescription'] = "No description available"
            return res
            

        except OutputParserException:
            raise OutputParserException("Content too big, unable to parse")
        return res if isinstance(res, list) else [res]
    

    
    def generate_email(self, job, portfolio_link):
        prompt_email= PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### PORTFOLIO LINK:
        {portfolio_link}

        ### INSTRUCTIONS:
        Create a medium sized cold email based on my portfolio ({portfolio_link}) and resume in ({portfolio_link})
        attach the resume link and portfolio link in the email.
        I am an aspiring data scientist with a strong background in statistics, machine learning, deep learning and genai.
        make use of my skills and experience from my projects.
        Highlight relevant projects from my portfolio that match these job requirements:
          {job_description}
        """
        )

 
        chain_email= prompt_email | self.llm
        email= chain_email.invoke({
             'job_description': job['jobDescription'],
             'portfolio_link': portfolio_link
        })
            
        return email.content
    
    


        

        


