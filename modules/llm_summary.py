import openai

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key

def generate_summary(top_logs):
    """
    Generate LLM-based threat summary
    """
    logs_text = "\n".join(top_logs['log_text'] + " | Severity: " + top_logs['severity'])
    prompt = f"Analyze these system logs and summarize security threats, highlighting critical events:\n{logs_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        max_tokens=300
    )
    return response['choices'][0]['message']['content']
