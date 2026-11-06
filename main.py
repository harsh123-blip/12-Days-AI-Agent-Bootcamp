from fastapi import FastAPI
from groq import AsyncGroq
import json
app = FastAPI()
GROQ_API_KEY = "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"
ai_client = AsyncGroq(api_key = GROQ_API_KEY)
@app.get("/")
def home():
     return {"status":"active","message":"ai server is live"}
@app.post("/ai-ask")
async def ask_ai_endpoint(user_prompt: str):
     
     chat_completion = await ai_client.chat.completions.create(
          messages=[{ "role": "user"
                     , "content": user_prompt}]
          , model = "openai/gpt-oss-120b",
          
     )
     ai_reply = chat_completion.choices[0].message.content


     return {"status":"success",
        "prompt_sent":user_prompt,
        "ai_response" :ai_reply}

     