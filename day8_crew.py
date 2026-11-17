import os
from crewai import Agent , Task,Crew,LLM
os.environ["GROQ_API_KEY"] = '' # os .environ
groq_llm = LLM(model="groq/openai/gpt-oss-20b",api_key = os.environ['GROQ_API_KEY'])
researcher = Agent(role = 'jarvis tech researcher',
                   goal = '2026 me ai agents bechkar 5 lakh kamane ka sabse tej tarika dundhna ',
                   backstory = "tum jarvis ke sabse tej market researcher ho",
                   llm = groq_llm)

planner = Agent(
    role = "jarvis action planner",
    goal = 'research se mile tarike ko ek sakht daily action plan me change karna',
    backstory = "tum hard target ko easy steps me break karne me mahir ho ",
    llm=groq_llm
)


task1= Task(
    description = "december 2026 tak ai automation se 5 lakh earn karna ",
    expected_output = "3 thos tarike ki list in english",
    agent = researcher
)

task2 = Task(
    description = "upar mile 3 tariko ko lagu karna  ke kiye 5step action plan hindi me likho",
    expected_output = '5 easy and strict action plan in english plan',
    agent = planner
)

jarvis_crew = Crew(agents=[researcher,planner],tasks = [task1,task2])

print("ab jarvis ki multi agent team kam shuru kar rahi hai")
result = jarvis_crew.kickoff()
print("\n -- jarvis team ki final report ---")
print(result)