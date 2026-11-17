import os
from crewai import Agent , Task,Crew,Process,LLM
os.environ["GROQ_API_KEY"] = ''
groq_llm = LLM(model="groq/openai/gpt-oss-20b",api_key =os.environ['GROQ_API_KEY'])

researcher = Agent(role = 'jarvis tech researcher',
                   goal = '2026 me ai agents bechkar 5 lakh kamane ka sabse tej tarika dundhna in english',
                   backstory = "tum jarvis ke sabse tej market researcher ho",
                   llm = groq_llm)

planner = Agent(
    role = "jarvis action planner",
    goal = 'research se mile tarike ko ek sakht daily action plan me change karna in english',
    backstory = "tum hard target ko easy steps me break karne me mahir ho ",
    llm=groq_llm
)


task=Task(
    description = "december 2026 tak ai automation se 5 lakh earn karna ka idea dena",
    expected_output = "ideas lo clear point me dena in english"
)

jarvis_crew = Crew(agents=[researcher,planner],tasks = [task],process=Process.hierarchical,manager_llm = groq_llm) 

print("ab jarvis ki multi agent team kam shuru kar rahi hai")
result = jarvis_crew.kickoff()
print("\n -- jarvis team ki final report ---")
print(result)