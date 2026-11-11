from dotenv import load_dotenv
import groq
import os 

load_dotenv()

client = groq.Client(api_key=os.getenv("GROQ_API"))
response = client.chat.completions.create(
    model = "qwen/qwen3.8-27b",
    messages = [
        {"role":"user",
        "content" : [{
                    "type": "text",
                    "text": "Generate a caption for this image in about 50 words.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1"},
                }, ]
         
        }
    ]
)
print(response.choices[0].message.content)