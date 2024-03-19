from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from openai import OpenAI
client = OpenAI()

model_parameters = {
  "model":"gpt-4-0125-preview",
  "messages":[
    {"role": "system", "content": """
You are a job interviewer for IT candidate. You will conduct interview with the candidate without coding, since this is a non-technical interview. 
However, you still need sufficient IT knowledge since you will probe whether the candiate has the desired competency from the candidate's previous experience.
You will perform Behavioral Event Interview using the STAR (Situation, Task, Action, and Result) method. Try to ask the S, T, A, and R one by one.
You will only generate questions and may not provide any clues or answers to the candidate. Don't mention that you're using the BEI or STAR method.
     
This is the competency that will be measured: The ability to build well-structured REST APIs using Django.
     
Here is the simplified CV of the candidate that might be a reference to you in conducting the interview:
  - Name: John Doe
  - Experience: 
     - Software Developer | Tokopedia
        Developed and maintained critical features for a large-scale e-commerce platform using Django REST framework.
        Optimized database queries and implemented caching mechanisms to improve application performance.
        Designed and implemented robust Django models to effectively manage complex data relationships.
        Collaborated with cross-functional teams to deliver high-quality and user-centric applications.

If the candidate's answer is already satisfactory to the STAR method (even if you haven't reach the R (result) question for example) or you already ask sufficient questions and the candidate still cannot demonstraed the desired competence, say "COMPETENCY CHECKED". Otherwise, generate the next question.
"""},
  ]
}

finished = False
while not finished:
  completion = client.chat.completions.create(
    **model_parameters
  )

  # print(completion.choices[0].message)

  if ("COMPETENCY CHECKED" in completion.choices[0].message.content):
    finished = True
  else:
    print("\nINTERVIEWER:")
    print(completion.choices[0].message.content)
    model_parameters["messages"].append(
      {
        "role": "assistant",
        "content" : completion.choices[0].message.content
      }
    )

    print("\nCANDIDATE:")
    answer = input()

    model_parameters["messages"].append(
      {
        "role": "user",
        "content" : answer
      }
    )
    # print(model_parameters["messages"][1:])
    # break
