import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
# Replace with your actual API key
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Say hello!"}
    ]
)

print(message.content[0].text)