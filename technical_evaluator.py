from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from openai import OpenAI
client = OpenAI()

def generate_model_parameters(skill: str, transcript: str):
    model_parameters = {
  "model":"gpt-4-0125-preview",
  "messages":[
    {"role": "system", "content": f"""
You are tasked with evaluating a transcript of an IT job interview. The interview that is conducted in the transcript is technical. 
You need sufficient IT knowledge since you will evaluate the answer of the interviewee to determine whether the interviewee answer correctly or not.
You will output "SUCCESS" if the interviewee's answer is deemd correct and "FAIL" if it's deemed false.
Below are 5 examples of correct answers.
     
Here are 5 examples:
EXAMPLE 1:
SKILL TO BE EVALUATED: Python

INTERVIEWER:
What is the use of zip () in python?

INTERVIEWEE:
The zip returns an iterator and takes iterable as argument. These iterables can be list, tuple, dictionary etc. It maps similar index of every iterable to make a single entity.
    
OUTPUT: SUCCESS

EXAMPLE 2:
SKILL TO BE EVALUATED: Python

INTERVIEWER:
What will be the output of the following?
name=["swati","shweta"]
age=[10,20]
new_entity-zip(name,age)
new_entity-set(new_entity)
print(new_entity)

INTERVIEWEE:
The output is {{('shweta', 20), ('swati', 10)}}

OUTPUT: SUCCESS

EXAMPLE 3:
SKILL TO BE EVALUATED: Python

INTERVIEWER:
What will be the output of the following?
a=["1","2","3"]
b=["a","b","c"]
c=[x+y for x, y in zip(a,b)] print(c)

INTERVIEWEE:
The output is: ['1a', '2b', '3c']

OUTPUT: SUCCESS

EXAMPLE 4:
SKILL TO BE EVALUATED: Python

INTERVIEWER:
What will be the output of the following?
str="apple#banana#kiwi#orange"
print(str.split("#",2))

INTERVIEWEE:
['apple', 'banana', 'kiwi#orange']

OUTPUT: SUCCESS

EXAMPLE 5:
SKILL TO BE EVALUATED: Python

INTERVIEWER:
What are python modules? Name some commonly used built-in modules in Python?

INTERVIEWEE:
Python modules are files containing Python code. This code can either be function classes or variables. A Python module is a .py file containing executable code. Some of thecommonly used built-in modules are:
- Os
- sys
- math
- random
- data time
- json

OUTPUT: SUCCESS

Note that the examples that I give above have the correct answer. Your job is to generate the output only (SUCCESS OR FAIL). You don't need to explain your justification.
SKILL TO BE EVALUATED: {skill}
{transcript}

"""},
  ]
}
    
    return model_parameters

def generate_evaluation(skill: str, transcript: str):
    model_parameters = generate_model_parameters(skill, transcript)
    completion = client.chat.completions.create(
        **model_parameters
    )

    generated = completion.choices[0].message.content
    return "SUCCESS" in generated

# SKILLS = ["Java"]
# TRANSCRIPTS = [
# # """INTERVIEWER:
# What is the difference between abstract classes and interfaces in Java?
# INTERVIEWEE:
# Abstract Classes:
# - Abstract classes can have both abstract (methods without a body) and concrete methods.
# - An abstract class can have instance variables.
# - A class can extend only one abstract class.
# Interfaces:
# - Interfaces can only declare abstract methods.
# - Interfaces cannot have instance variables.
# - Interfaces allow multiple inheritance. A class can implement multiple interfaces.
# """
# ]

# TRANSCRIPTS = [
# """INTERVIEWER:
# What is the difference between abstract classes and interfaces in Java?
# INTERVIEWEE:
# Abstract Classes:
# - Abstract classes can only have abstract methods.
# - An abstract class can have instance variables.
# Interfaces:
# - Interfaces can only declare abstract methods.
# - Interfaces cannot have instance variables.
# - Interfaces allow multiple inheritance. A class can implement multiple interfaces.
# """
# ]

# for idx, skill in enumerate(SKILLS):
#     print(f"\nSKILL TO BE EVALUATED: {skill}")
#     model_parameters = generate_model_parameters(skill, TRANSCRIPTS[idx])
#     completion = client.chat.completions.create(
#         **model_parameters
#     )

#     print("OUTPUT:")
#     print(completion.choices[0].message.content)
