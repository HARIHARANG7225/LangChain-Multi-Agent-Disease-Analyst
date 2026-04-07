import streamlit as st 
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

st.title("Langchain Multi Agent disease Analyst ")

questions=st.text_area(label="What is the Disease ")
button= st.button('Ask')

if button:
    if questions:
        llm=OllamaLLM(model='gemma:2b')

        #Research Agent(A1)
        Research_prompt_template="""Persona: You are a senior researcher in the health industry.
                           Task: Gather information for the following question: {input}
                           Instructions: Only refer to factual, scientifically proven information.
                           Avoid speculation or personal opinions.
                           Output Format:Present findings in clear bullet points."""

        research_prompt=PromptTemplate(template=Research_prompt_template,input_variables=['input'])
        research_chain=research_prompt|llm
        st.subheader("Agent one on the Mark")
        research_agent_output=research_chain.invoke({'input':questions})

        #Analyst Agent(A2)
        analyst_template="""persona : you are an Analyst Agent
        task: anyise the researchagent output {research_output}
        instrcution: extract the key points ,trends and  Healthy outcomes
        ouput formate : provide structure explaination """
        anayst_promtp=PromptTemplate(template=analyst_template,input_variables=['research_output'])
        analyst_chain=anayst_promtp|llm
        st.subheader("Agent 2 On the mark")
        anayst_out=analyst_chain.invoke({'research_output':research_agent_output})

        #Criticise agent
        critic_agent_prompt_template="""Persona: You are a senior medical information reviewer.
        Task: Improve the Analyst Agent’s content: {Analyst_output}
        Instructions:Remove redundancy and improve clarity.
        Maintain a professional, neutral tone.
        Provide general health insights or lifestyle recommendations.
        Remind the user to consult a licensed healthcare professional for medical advice.
        Output Format:Four concise paragraphs covering clarity, tone, key recommendations, and next steps."""

        critic_prompt=PromptTemplate(template=critic_agent_prompt_template,input_variables=['Analyst_output'])
        critc_agent_chain=critic_prompt|llm
        st.subheader("Agent 3 On the Mark")
        response=critc_agent_chain.invoke({'Analyst_output':anayst_out})

        st.markdown(str(response))
  
