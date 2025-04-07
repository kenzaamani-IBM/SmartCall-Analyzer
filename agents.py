import autogen
import streamlit as st

config_list = [
    {
        'model': st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"],
        'api_key': st.secrets["AZURE_OPENAI_API_KEY"],
        'base_url': st.secrets["AZURE_OPENAI_ENDPOINT"],
        'api_type': 'azure',
        'api_version': '2024-02-15-preview'
    }
]

transcript_agent = autogen.AssistantAgent(
    name="TranscriptSummarizer",
    system_message="Summarize customer service calls concisely.",
    llm_config={"config_list": config_list}
)

employee_insights_agent = autogen.AssistantAgent(
    name="EmployeePerformanceAgent",
    system_message="Identify clear, actionable insights to improve employee performance.",
    llm_config={"config_list": config_list}
)

sentiment_analysis_agent = autogen.AssistantAgent(
    name="SentimentEmotionAgent",
    system_message="Perform detailed sentiment and emotion analysis.",
    llm_config={"config_list": config_list}
)

customer_recommendation_agent = autogen.AssistantAgent(
    name="CustomerSatisfactionAgent",
    system_message="Provide actionable recommendations to improve customer satisfaction.",
    llm_config={"config_list": config_list}
)

# Properly formatted messages for AutoGen
def get_response_content(agent, message):
    formatted_message = [{"role": "user", "content": message}]
    reply = agent.generate_reply(messages=formatted_message)
    
    if isinstance(reply, dict):
        return reply.get('content', '')
    elif hasattr(reply, 'content'):
        return reply.content
    return str(reply)

def get_insights(transcript):
    summary = get_response_content(transcript_agent, f"Summarize call:\n\n{transcript}")

    employee_feedback = get_response_content(
        employee_insights_agent, f"Employee improvement areas:\n\n{transcript}"
    )

    sentiment = get_response_content(
        sentiment_analysis_agent, f"Analyze sentiment/emotions:\n\n{transcript}"
    )

    recommendations = get_response_content(
        customer_recommendation_agent, f"Actionable customer satisfaction recommendations:\n\n{transcript}"
    )

    return {
        "summary": summary,
        "employee_feedback": employee_feedback,
        "sentiment": sentiment,
        "recommendations": recommendations
    }
