import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Constants
MAX_LENGTH_FOR_ARTICLE_SUMMARIES = 2000
MAX_LENGTH_FOR_ARTICLE_AUDIO = 3000
VOICE_ASSISTANT_NAME = "Joanna"

import os
import openai

# Constants
MODEL_NAME = "gpt-3.5-turbo"


class JobHelper:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.openAI = openai
        self.history = [{
                        "role": "user", "content": '''
                            Here is a complete conversation that you can have as an agent helping someone with a job.
    
                        ===
                        Pretend I'm a single mom living below the federal poverty link going to my local not for profit to find a
                        job. Create a script for a not for profit client intake specialist conducting an informational interview
                        on what are the client's job skills, job history, job interests, zip code, and, if applicable, education
                        background . Write this to be understood by someone with a 7th grade reading level.
                        ChatGPT
                        Client Intake Specialist: Good morning! Welcome to [Not-for-profit organization]. My name is
                        [Specialist's Name], and I'm here to help you find a job that suits your skills and interests. How can I
                        assist you today?
                        Client Intake Specialist: I understand your situation, and I'm here to support you. Let's start by getting
                        to know you better. First, can you please tell me about your job skills? These are the abilities and
                        things you're good at that could help you in a job.
                        Client Intake Specialist: That's great to know. Customer service and cash handling skills can be
                        valuable in many different jobs. Now, let's talk about your job history. Have you worked before? If so,
                        please tell me about your past jobs, including the names of the companies you worked for and the
                        tasks you performed.
                        
                        Client Intake Specialist: Thank you for sharing that information. It's helpful to understand your
                        experience. Now, let's talk about your job interests. What kind of work are you interested in? Do you
                        have any specific preferences or areas of interest?
                        
                        Client Intake Specialist: Thank you for sharing that information. Can you share your email with me?
                        
                        Client Intake Specialist: I understand. Flexibility and a passion for helping others are important
                        factors we'll consider when looking for suitable job options for you. Another thing we need to know
                        is your zip code. Could you please provide me with your zip code? This will help us find job
                        opportunities near your location.
                        Client Intake Specialist: Thank you for sharing that. Lastly, if applicable, could you tell me about your
                        education background? This includes your highest level of education completed or any specific
                        qualifications you have obtained.
  
                        Client Intake Specialist: Wonderful! Having completed high school and gaining some computer
                        application skills will definitely help us in finding suitable job options for you.
                        Client Intake Specialist: You're welcome! It's my pleasure to assist you. Based on the information
                        you've provided, I will do my best to find job opportunities that match your skills, interests, and
                        location. We'll work together to improve your current situation. Please expect a follow-up call or visit
                        from me soon with potential job leads. Are you interested in learning about job training programs?
                       
                        
                        Client Intake Specialist: Ok. I’ll ask you some questions to find out which job training programs might
                        be a good fit for you to explore?
                        
                        Is there anything else you'd like to add or any questions you have for me?
                        Client Intake Specialist: You're welcome! Stay positive, and we'll work together towards a better
                        future. Have a great day, and I'll be in touch soon.
                        
                        
                        ===
                        
                        Your job is to act as the Client Intake Specialist and ask questions one by one to the client. 
                        
                        Goal:
                            1. Be as helpful as you can.
                            2. Only ask questions 1 at a time.
                            4. You can only act as the client intake specialist and not as the client.
                            5. Your name is Janet and you work at the Aspire Center.
                '''}]

    def setup(self):
        self.openAI.api_key = os.getenv("OPENAI_API_KEY")

    def get_user_input(self):
        user_input = input("Response here: ")
        self.history.append({
            "role": "user",
            "content": user_input
        })
        return

    def check_if_chat_should_continue(self):
        for word in ["goodbye", "Goodbye", "bye", "Goodbye!"]:
            if word in self.history[-1]['content']:
                return False
        return True

    def help(self):
        chat_should_continue = self.check_if_chat_should_continue()

        while chat_should_continue:
            response = self.openAI.ChatCompletion.create(
                model=self.model_name,
                messages=self.history
            )
            role = response['choices'][0]['message']['role']
            if role == "assistant":
                text_response = response['choices'][0]['message']['content']
                print(text_response)
                self.history.append({
                    "role": role,
                    "content": text_response
                })

            for word in ["goodbye", "Goodbye", "bye"]:
                if word in self.history[-1]['content']:
                    return

            user_input = input("Response here: ")
            self.history.append({
                "role": "user",
                "content": user_input
            })

            # Open the file in write mode and write the data
            with open("history.json", "w") as file:
                json.dump(self.history, file)

        return


def main():
    job_helper = JobHelper()
    job_helper.help()

main()
