from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
import operator

# ==========================================
# 1. Jarvis की तिजोरी + सुरक्षा काउंटर (State)
# ==========================================
class JarvisState(TypedDict):
    messages: Annotated[list[str], operator.add]
    email_draft: str
    is_valid: str
    retry_count: int  # अनंत लूप रोकने वाला पहरेदार

# ==========================================
# 2. ईमेल लिखने वाला मॉड्यूल (Writer Node)
# ==========================================
def draft_writer(state: JarvisState):
    attempt = state.get("retry_count", 0) + 1
    print(f"\n✍️ [कोशिश #{attempt}]: Jarvis ईमेल ड्राफ्ट लिख रहा है...")
    
    # पहली कोशिश में जानबूझकर गलती करेगा, दूसरी में सुधार लेगा
    if attempt == 1:
        draft = "Hello Sir, let us talk tomorrow at 10 AM."  # 'Meeting' शब्द गायब है!
    else:
        draft = "Hello Sir, let us have a Meeting tomorrow at 10 AM."  # गलती सुधार ली!
        
    return {"email_draft": draft, "retry_count": attempt}

# ==========================================
# 3. गलती पकड़ने वाला इंस्पेक्टर (Checker Node)
# ==========================================
def quality_checker(state: JarvisState):
    print("🔍 [इंस्पेक्टर]: Jarvis ईमेल की जाँच कर रहा है...")
    if "Meeting" in state["email_draft"]:
        print("✅ जाँच पास! ईमेल बिल्कुल सही है।")
        return {"is_valid": "YES", "messages": ["ईमेल ड्राफ्ट 100% सही तैयार हो गया।"]}
    else:
        print("❌ गलती पकड़ी गई! 'Meeting' शब्द गायब है। वापस सुधारने के लिए भेजा जा रहा है...")
        return {"is_valid": "NO", "messages": ["गलती: ईमेल में Meeting शब्द नहीं मिला।"]}

# ==========================================
# 4. फैसले का चौराहा (Self-Healing Router)
# ==========================================
def healing_router(state: JarvisState):
    if state["is_valid"] == "YES":
        return "finish"
    elif state["retry_count"] >= 3:
        print("⚠️ चेतावनी: 3 कोशिशें पूरी हो गईं! अनंत लूप से बचने के लिए रोका जा रहा है।")
        return "finish"
    else:
        return "fix_again"

# ==========================================
# 5. ग्राफ और पीछे मुड़ने वाली वायरिंग (Edges)
# ==========================================
workflow = StateGraph(JarvisState)
workflow.add_node("writer", draft_writer)
workflow.add_node("checker", quality_checker)

workflow.add_edge(START, "writer")
workflow.add_edge("writer", "checker")

# यहाँ लगा है Self-Healing चौराहा
workflow.add_conditional_edges(
    "checker",
    healing_router,
    {
        "finish": END,
        "fix_again": "writer"  # डेटा वापस पीछे 'writer' नोड में मुड़ गया!
    }
)

jarvis_healer = workflow.compile()

# Jarvis को जगाना
initial_state = {
    "messages": ["Jarvis, क्लाइंट को मीटिंग का ईमेल लिखो।"],
    "email_draft": "",
    "is_valid": "NO",
    "retry_count": 0
}

final_result = jarvis_healer.invoke(initial_state)

print("\n🏆 --- फाइनल सुरक्षित आउटपुट ---")
print("अंतिम ईमेल:", final_result["email_draft"])
print("कुल कोशिशें:", final_result["retry_count"])