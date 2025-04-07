import autogen
import streamlit as st

# Azure OpenAI configuration via Streamlit secrets
config_list = [
    {
        'model': st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"],
        'api_key': st.secrets["AZURE_OPENAI_API_KEY"],
        'base_url': st.secrets["AZURE_OPENAI_ENDPOINT"],
        'api_type': 'azure',
        'api_version': '2024-02-15-preview'
    }
]

# ✨ Concise, focused system messages for each agent
transcript_agent = autogen.AssistantAgent(
    name="TranscriptSummarizer",
    system_message="You are a conversation summarizer. Provide a short summary in 2-3 sentences focusing only on key actions and outcomes. Respond in plain text only. No explanations.",
    llm_config={"config_list": config_list}
)

employee_insights_agent = autogen.AssistantAgent(
    name="EmployeePerformanceAgent",
    system_message="You are an employee performance coach. Give 2-3 specific, constructive suggestions to help the employee improve. Use bullet points. Keep it concise. No extra commentary.",
    llm_config={"config_list": config_list}
)

sentiment_analysis_agent = autogen.AssistantAgent(
    name="SentimentEmotionAgent",
    system_message="You analyze customer service sentiment. Briefly describe the emotions of the customer and employee in 1–2 words per emotion. Use bullet points. Be objective. No explanations.",
    llm_config={"config_list": config_list}
)

customer_recommendation_agent = autogen.AssistantAgent(
    name="CustomerSatisfactionAgent",
    system_message="You suggest improvements to customer satisfaction. List 2 short, practical, and actionable tips. Use bullet points. No extra explanation.",
    llm_config={"config_list": config_list}
)

# 🧠 Generic message wrapper
def get_response_content(agent, message):
    formatted_message = [{"role": "user", "content": message}]
    reply = agent.generate_reply(messages=formatted_message)
    
    if isinstance(reply, dict):
        return reply.get('content', '')
    elif hasattr(reply, 'content'):
        return reply.content
    return str(reply)

# 🧩 Master function to extract insights
def get_insights(transcript):
    summary = get_response_content(transcript_agent, f"Transcript:\n\n{transcript}")
    employee_feedback = get_response_content(employee_insights_agent, f"Transcript:\n\n{transcript}")
    sentiment = get_response_content(sentiment_analysis_agent, f"Transcript:\n\n{transcript}")
    recommendations = get_response_content(customer_recommendation_agent, f"Transcript:\n\n{transcript}")

    return {
        "summary": summary,
        "employee_feedback": employee_feedback,
        "sentiment": sentiment,
        "recommendations": recommendations
    }
