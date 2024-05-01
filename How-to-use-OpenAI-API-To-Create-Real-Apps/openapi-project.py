from openai import OpenAI
import datetime

client = OpenAI(api_key="your-openapi-key")


today = datetime.datetime.now().strftime("%B %d")

response = client.chat.completions.create(
        messages = [{"role":"user", "content":f"What is the most famous thing that happened on {today} in history?"}],
        model = "gpt-3.5-turbo",
        )

if response.choices:
    print(response.choices[0].message.content)
else:
    print("No response found.")
