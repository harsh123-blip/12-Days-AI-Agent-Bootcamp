import os
from crewai import Agent , Task,Crew,LLM
from crewai.tools import tool
os.environ["GROQ_API_KEY"] = ''
groq_llm = LLM(model="groq/openai/gpt-oss-20b",api_key = os.environ['GROQ_API_KEY'])


@tool("save report file")
def save_report_to_file(content:str)->str:
    """ yeh tool jarvis dwara tayar ki gayifinal tool ko computer me save karega """
    with open("jarvis_plan.txt","w",encoding="utf-8") as f:
        f.write(content)
    return"report successfully:jarvis_plan.txt computer par save kar diya hai "
writer_with_hands= Agent(role='jarvis executive assistant',
                   goal = '2026 me ai agents bechkar 5 lakh kamane ka sabse tej tarika dundhna ',
                   backstory = "tum jarvis ke sabse tej assistant ho jo har file ka record ek file me save rakhta hai",
                   llm = groq_llm,
                   tools = [save_report_to_file])


task1= Task(
    description = "december 2026 tak ai automation se 5 lakh earn karna ke  liye idea likho",
    expected_output = "final save hona ek confection message",
    agent = writer_with_hands
)


jarvis_crew = Crew(agents=[writer_with_hands],tasks = [task1]) 

print("ab jarvis ki agent kam shuru kar rahi hai")
result = jarvis_crew.kickoff()
print("\n -- jarvis ki final report ---")
print(result)