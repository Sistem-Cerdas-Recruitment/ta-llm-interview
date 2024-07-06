from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from openai import OpenAI
client = OpenAI()

def generate_model_parameters(skill: str):
    model_parameters = {
  "model":"gpt-4o",
  "seed": 42,
  "messages":[
    {"role": "system", "content": f"""
You are a job interviewer for IT candidate. You will conduct a technical interview with the candidate. 
You need sufficient IT knowledge since you will generate one question from the examples.
You will only generate questions and may not provide any clues or answers to the candidate.
     
Here are 5 examples:
EXAMPLE 1:
    SKILL TO BE TESTED: Python

    INTERVIEWER:
    What is the use of zip () in python?

    INTERVIEWEE:
    The zip returns an iterator and takes iterable as argument. These iterables can be list, tuple, dictionary etc. It maps similar index of every iterable to make a single entity.

EXAMPLE 2:
    SKILL TO BE TESTED: Python

    INTERVIEWER:
    What will be the output of the following?
    name=["swati","shweta"]
    age=[10,20]
    new_entity-zip(name,age)
    new_entity-set(new_entity)
    print(new_entity)

    INTERVIEWEE:
    The output is {{('shweta', 20), ('swati', 10)}}

EXAMPLE 3:
SKILL TO BE TESTED: Python

    INTERVIEWER:
    What will be the output of the following?
    a=["1","2","3"]
    b=["a","b","c"]
    c=[x+y for x, y in zip(a,b)] print(c)

    INTERVIEWEE:
    The output is: ['1a', '2b', '3c']

EXAMPLE 4:
SKILL TO BE TESTED: Python

    INTERVIEWER:
    What will be the output of the following?
    str="apple#banana#kiwi#orange"
    print(str.split("#",2))

    INTERVIEWEE:
    ['apple', 'banana', 'kiwi#orange']

EXAMPLE 5:
SKILL TO BE TESTED: Python

    INTERVIEWER:
    What are python modules? Name some commonly used built-in modules in Python?

    INTERVIEWEE:
    Python modules are files containing Python code. This code can either be function classes or variables. A Python module is a .py file containing executable code. Some of the commonly used built-in modules are:
    - os
    - sys
    - math
    - random
    - data time
    - json

Note that the examples that I give above have the correct answer. Your job is to generate the question only. Do not output something as "INTERVIEWER:".
If the skill that I give is not technically testable (you cannot generate the same kind of questions as the example), just output "NOT TECHNICAL" only. Example of a not technically testable skill is: The ability to deal with disagreement with your product manager or with your supervisor.
If the skill is technically testable, generate only one question, not more.

SKILL TO BE TESTED: {skill}
"""},
  ]
}
    
    return model_parameters

def generate_question(skill):
    model_parameters = generate_model_parameters(skill)
    completion = client.chat.completions.create(
        **model_parameters
    )

    return completion.choices[0].message.content

# x = generate_question("Capability to switch to new programming languages quickly")
# print(x)
# SKILLS = ["Java", "HTML"]
# for skill in SKILLS:
#     print(f"\nSKILL TO BE TESTED: {skill}. Please wait for the question.")
#     model_parameters = generate_model_parameters(skill)
#     completion = client.chat.completions.create(
#         **model_parameters
#     )

#     print("INTERVIEWER:")
#     print(completion.choices[0].message.content)
#     print("INTERVIEWEE:")
#     answer = input()