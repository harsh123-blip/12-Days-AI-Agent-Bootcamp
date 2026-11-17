import json
import os
from groq import Groq

# ⚠️ 1. यहाँ अपनी असली Groq API Key लगाओ
ai_client = Groq(api_key="remove_for_security")
MEMORY_FILE = "jarvis_permanent_memory.json"

# 2. हार्ड डिस्क पर Jarvis की स्थायी तिजोरी बनाना और सेव करना
def save_memory(notes: list[str]):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)
    print("✅ Jarvis की स्थायी मेमोरी हार्ड डिस्क पर सेव हो गई है!")

# पुरानी यादें सेव करना
jarvis_notes = [
    "मेरे पिता जी की शुगर की दवा सुबह 8 बजे नाश्ते के बाद देनी है।",
    "मेरी अलमारी की चाबी लाल बैग के अंदर रखी है।"
]
save_memory(jarvis_notes)

# 3. असली AI + मेमोरी लूप (RAG System)
def ask_real_jarvis(user_question: str):
    print(f"\n❓ सवाल: {user_question}")
    
    # हार्ड डिस्क की तिजोरी से सारी पुरानी यादें पढ़ना
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        all_memories = json.load(f)
    
    # असली Groq AI को तिजोरी और सवाल भेजना
    secret_prompt = f"""
    तुम Jarvis हो। नीचे दी गई तिजोरी की यादों में से सही जानकारी ढूंढो और यूजर के सवाल का सटीक जवाब हिंदी में दो।
    तिजोरी की यादें: {all_memories}
    यूजर का सवाल: {user_question}
    """
    
    response = ai_client.chat.completions.create(
        messages=[{"role": "user", "content": secret_prompt}],
        model="openai/gpt-oss-20b"
    )
    
    return response.choices[0].message.content

# असली AI से टेस्ट करना
answer = ask_real_jarvis("पिता जी की दवा कब देनी है?")
print("🤖 असली Jarvis का जवाब:", answer)