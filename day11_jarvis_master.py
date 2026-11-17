import time
import json
import webbrowser
import pyautogui
from groq import Groq
api_keys = ""
ai_client = Groq(api_key=api_keys)
pyautogui.FAILSAFE=True

def open_app(app_name:str):
    pyautogui.press("win")
    time.sleep(0.003)
    pyautogui.write(app_name)
    pyautogui.press("enter")
    return f"{app_name} open ho raha hai"
    
def open_website(url:str):
    webbrowser.open(url)
    return f' {url}open ho raha hai boss!'


tools_schema = [{
    "type":"function","function":{"name":"open_app","description":"computer ka koi bhi app kholna jaise ki calculator msedge, notepad,paint",
                                  'parameters':{"type":"object","properties":{"app_name":{"type":"string"}},
                                                "required":["app_name"]}}
},
                {"type":"function","function":{"name":"open_website","description":"browser me koi bhi url search karne ke liye",
                                               "parameters":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}}}]


print("jarvis online hai! band karne ke liye'exit' type kare....")
while True:
    user_cmd = input("\nyour order:")
    if user_cmd.lower()=="exit":
        break
    messages = [{"role":"system","content":"tum jarvis ho . short me jawab do in english aur jarurat parne par tool chalao"},
                {"role":"user","content":user_cmd}]    
    res = ai_client.chat.completions.create(messages=messages,tools=tools_schema,model="openai/gpt-oss-20b")
    ai_msg = res.choices[0].message
    
    if ai_msg and ai_msg.tool_calls:
        messages.append(ai_msg)
        for tool in ai_msg.tool_calls:
            raw_args = tool.function.arguments or "{}"
            
            args = json.loads(raw_args)
            if tool.function.name =="open_app":
                output = open_app(args.get("app_name","notepad"))
            else:
                open_website(args.get("url","https://youtube.com"))
            messages.append({"role":"tool","tool_call_id":tool.id,"content":output})
        
        
        final = ai_client.chat.completions.create(messages=messages,model="openai/gpt-oss-20b")
        
        
        print("jarvis:",final.choices[0].message.content)
    else:
        print('jarvis:',ai_msg.content)    