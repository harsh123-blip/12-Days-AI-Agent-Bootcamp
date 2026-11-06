import asyncio 
import json
 
 
async def fetch_ai_response(prompt):
     print(f"prompt bhej diya hai: {prompt}")
     
     await asyncio.sleep(3)
     
     ai_raw_response = '{"status":"success" , "reply": "Hello developer i am active."}'
     parsed_response = json.loads(ai_raw_response)
     return parsed_response
 
 
async def main():
     print("system is starting.....")
     result = await fetch_ai_response("create an ai agent")
     
     print("\n  ai ka jawab aa gaya...")
     print(f"Status:{result['status']}")
     print(f"Reply : {result['reply']}")
     
     
     
#  ab last me ham code ko run karenge
asyncio.run(main())