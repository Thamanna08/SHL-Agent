import os
from groq import Groq
from dotenv import load_dotenv

from agent.prompts import SYSTEM_PROMPT

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_reply(messages, recommendations):

    try:

        catalog_text = ""

        for item in recommendations:

            catalog_text += f"""
            Assessment Name: {item['name']}
            Test Type: {item['test_type']}
            URL: {item['url']}
            Description: {item['description']}
            """

        prompt = f"""
        Conversation History:
        {messages}

        Retrieved SHL Assessments:
        {catalog_text}

        Generate:
        1. Helpful conversational reply
        2. Mention why assessments fit
        3. Stay grounded in retrieved data only
        """

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        reply = completion.choices[0].message.content

        return reply

    except Exception as e:

        print("LLM Error:", e)

        return (
            "I found matching SHL assessments "
            "for your hiring requirements."
        )