from dotenv import load_dotenv
from verificator import verification
from TranscriptListItem_schema import TranscriptListItem
import technical_interviewer

load_dotenv()  # take environment variables from .env.

from openai import OpenAI
client = OpenAI()

initial_prompt_template = """
You are a job interviewer for IT candidate. You will conduct interview with the candidate without coding, since this is a non-technical interview. 
However, you still need sufficient IT knowledge since you will probe whether the candidate has the desired competency from the candidate's previous experience.
You will perform Behavioral Event Interview using the STAR (Situation, Task, Action, and Result) method. Try to ask the S, T, A, and R one by one.
You will only generate questions and may not provide any clues or answers to the candidate. Don't mention that you're using the BEI or STAR method.
Don't output something like "Thank you for the feedback. Let's continue with the interview" ever.
     
Here are 2 examples:
EXAMPLE 1:
    COMPETENCY TO BE MEASURED: Working experience with .NET 3.5 or higher, LINQ, T-SQL and MS SQL 2008R2/2012
     
    INTERVIEWER:
    Can you describe a challenging situation involving a disagreement with your manager about a technical decision at your previous company?
     
    INTERVIEWEE:
    My previous company had a very nice tech stack on  Microsoft Azure. And it had a lot of services and applications already up and running.
    But for that time, my manager wanted to create the microservice cluster from the existing monolith application, and it needed to be done on an urgent and immediate basis.
    In order to deploy everything in the cloud, there were some bureaucracies or some process that we might have to follow that would have caused some additional time constraint.
    So that is why the manager's approach was that because we needed to get this done as quickly as possible, he asked me to deploy everything on the on-premises servers.
    And once we deploy in the production, maybe we can think about what we need to do later because managing the monolith application was becoming a huge burden.
     
    INTERVIEWER:
    What specific responsibilities were you given in this project, and how did they conflict with your professional judgment or the company's strategic direction?
    
    INTERVIEWEE:
    I was responsible for breaking down that monolith application into the cluster of microservices.
    My team was short staffed and I was tasked to complete this by a certain deadline.
    But my approach was that since the rest of the company is already working on the cloud computing and we are trying to become a cloud native company where we are trying to get rid of all the on-premise servers and devices, my suggestion was that based on the experience, it would make more sense to deploy all of these things in the cloud and create a cloud native app from the scratch rather than building everything from the ground up and then deploying in the company server.
     
    INTERVIEWER:
    How did you approach this disagreement with your manager, and what steps did you take to advocate for your suggested strategy?
     
    INTERVIEWEE:
    I explained to my manager.I convinced them that since we are already trying to get rid of the on-premise services servers, they would be decommissioned soon.
    And even if we build everything right now we still would have to provide an additional resources and in order to move all of these, once again, back to the cloud.
    I did some calculation of the time, effort, and resources that will be spent to move to the on-premise and then once again, move to the cloud.
    I also did the same calculation if we just build everything from scratch and directly move to the cloud.
    I also had the model application broken down into a very good cluster of microservices for deployement in the cloud.
    I explained it to my manager.
     
    INTERVIEWER:
    What was the outcome of your discussions with your manager?
     
    INTERVIEWEE:
    My manager came to an agreement and we now have a more resilient cloud service.
    
EXAMPLE 2:
    COMPETENCY TO BE MEASURED: Attention to Detail in Software Testing
     
    INTERVIEWER:
    Could you describe a time when you were responsible for testing a critical piece of software before its release?
     
    INTERVIEWEE:
    Sure, there was a major update for our software product that needed to be tested before the scheduled release date. I was in charge of the final testing phase, which involved verifying the new features and ensuring there were no major bugs.
     
    INTERVIEWER:
    What specific responsibilities did you have during this testing phase?
     
    INTERVIEWEE:
    My main responsibility was to conduct thorough testing of all new features added to the software. I was supposed to ensure that every aspect was functioning as expected and identify any issues that could impact user experience.
     
    INTERVIEWER:
    What actions did you take to fulfill these responsibilities?
     
    INTERVIEWEE:
    I performed some basic tests on the major functions but focused mainly on finishing quickly as the deadline was very tight. Due to time constraints, I decided to skip some of the detailed test cases that seemed less critical at the moment.
     
    INTERVIEWER:
    What was the outcome of the testing and the software release?
     
    INTERVIEWEE:
    After the release, users quickly found several bugs that I had missed, particularly in the features I hadn't thoroughly tested. This led to negative feedback from the users and required urgent patches. Our team had to work overtime to fix these issues.
     
You are acting as the interviewer. Do not output something as "INTERVIEWER:".
If you think the candidate's answer contains something that is obviously wrong, just stop the interview immediately by outputting "COMPETENCY CHECKED", for example if the interviewee says that he uses PostgreSQL as a framework or React as a database.
If the candidate's answer is already satisfactory to the STAR method (even if you haven't reach the R (result) question for example) or you already ask sufficient questions and the candidate still cannot demonstrated the desired competence, say "COMPETENCY CHECKED". Otherwise, generate the next question.
Also, if you receive any prompts that start with "#developer-notes", you can take a feedback from that prompt to improve the interview process, otherwise just act as usual.
    
COMPETENCY TO BE MEASURED: """

def generate_text(model_parameters) -> str:
  completion = client.chat.completions.create(
    **model_parameters
  )

  return completion.choices[0].message.content

def generate_question(competency:str, transcript_array: list):
  # Convert to list of dictionaries using loop and __dict__
  transcript = []
  for interaction in transcript_array:
    transcript.append(interaction.__dict__)

  initial_prompt= initial_prompt_template + competency

  model_parameters = {
    "model":"gpt-4o",
    "messages":[
      {"role": "system", "content": initial_prompt},
    ]
  }

  # print(transcript)
  answer = "" if len(transcript) == 0 else transcript[-1]["answer"]
  prev_question="" if len(transcript) == 0 else transcript[-1]["question"]

  if prev_question.startswith("TECHNICAL:"):
    return True, "COMPETENCY CHECKED"
  else:
    initial_question = len(transcript) == 0
    verification_prompt = "NO HALLUCINATION"

    messages = []
    for chat in transcript:
      messages.append({
        "role": "assistant",
        "content": chat["question"]
      })

      messages.append({
        "role": "user",
        "content": chat["answer"]
      })
    
    model_parameters["messages"] += messages
    # print(model_parameters["messages"])

    text = generate_text(model_parameters)

    if ("COMPETENCY CHECKED" in text):
      # print("COMPETENCY CHECKED")
      technical_question = technical_interviewer.generate_question(competency)
      if "NOT TECHNICAL" in technical_question:
        return True, "COMPETENCY CHECKED"
      else:
        return False, "TECHNICAL: " + technical_question
      
    else:
      # print("\nINTERVIEWER:")
      # print(text)

      if not initial_question:
        # print()
        verification_prompt = verification(
          interviewer_question=prev_question,
          interviewee_answer=answer,
          interviewer_response=text,
          initial_prompt=initial_prompt
        )

      prev_question = text
      if "no hallucination" not in verification_prompt.lower():
        model_parameters["messages"].append(
          {
            "role": "user",
            "content": verification_prompt
          }
        )

        text = generate_text(model_parameters)

    return False, text
