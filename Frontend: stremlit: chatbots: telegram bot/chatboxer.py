import os
import openai

client = openai.OpenAI(
    api_key='14cd78f5-2970-4c31-aa6a-23427d00f898',
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model='Meta-Llama-3.1-8B-Instruct',
    messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Hello"}],
    temperature =  0.1,
    top_p = 0.1
)

print(response.choices[0].message.content)
      