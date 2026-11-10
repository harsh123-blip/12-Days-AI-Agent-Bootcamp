from fastapi import FastAPI
from groq import AsyncGroq
from pydantic import BaseModel,Field , ValidationError
import json


app = FastAPI()

GROQ_API_KEY = "remove_for_security"
ai_client = AsyncGroq(api_key = GROQ_API_KEY)

class UserAddress(BaseModel):
    city:str
    pincode:int=Field(gt=100000, lt=999999)
class UserProfile(BaseModel):
    name:str
    age:int = Field(gt = 18)
    address:UserAddress
    skills:list[str]
def calculate_salary(base: int, months: int,) ->int:
    
    """
    multiples the base salary by the number of month to calculate the total annual earnings."""
    return base *months


tools_schema = [ { "type":"function", "function":{ "name":"calculate_salary","description":"calculate total salary by multplying base amount with months .",
                                                    "parameters":{"type":"object","properties":{'base':{"type":"integer","description":" monthly base salary"},
                                                                                                'months':{"type":"integer","description":"number of months"}
                                                                                                },"required":["base","months",]}}}]

@app.post("/run-finance-agent")
async def tool_agent_endpoint(user_prompt:str, base_salary: int):
    try:
        profile_prompt =f"generate a valid json object for character {user_prompt}. age 22 , city lucknow, pincode 226001. skills:python, fastapi.strictly follow fields : name , age , address(with  city and pincode), and skills."
        chat_completion = await ai_client.chat.completions.create(messages = [{"role": "user", 'content':(profile_prompt)}],model="openai/gpt-oss-20b",
                                                                  response_format={"type":"json_object"})
        
    
          
        ai_messages = chat_completion.choices[0].message.content
        json_message = json.loads(ai_messages)
        validated_message = UserProfile(**json_message)
        
        
        tool_prompt = f"calculate the annual salary using the available tool . the base salary is a{base_salary} and month 12"
        tool_completion = await ai_client.chat.completions.create( messages = [{"role":"user" , "content":tool_prompt}] , 
                                                                  model="openai/gpt-oss-20b",tools = tools_schema,
                                                                  tool_choice="auto" )
        ai_message = tool_completion.choices[0].message
        final_salary = 0
        message_history = [{"role":"user","content": user_prompt}]
    
        if ai_message.tool_calls:
            message_history.append(ai_message)
            
            

        
            tool_call = ai_message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
    
    
        if function_name =="calculate_salary":
            tool_output = calculate_salary(
            base = function_args["base"],
            months = function_args["months"]
           
           
        )   
            print(f"tool ka result aaya hai {tool_output}")
            message_history.append({"role":"tool","tool_call_id":tool_call.id,'name':function_name,"content":str(tool_output)})
            final_response = await ai_client.chat.completions.create(messages=message_history,model="openai/gpt-oss-20b")  
                
          
            return {"status":"success","agent_decision":" multi turn loop tool executed successfully","final_human_touch": final_response.choices[0].message.content}         


    except Exception as e:
        return {"status": 'error',"message":str(e)}
    except ValidationError as a:
        return {"status":"error","type":"general exception","details":e.errors()} 
          
          
          
     

     