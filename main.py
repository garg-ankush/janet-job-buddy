import json
import time
import os
import openai
from dotenv import load_dotenv
from read_text import speak
from record_audio import record_audio
from transcribe_audio import transcribe_audio
from utilities import generate_email_json, send_email_from_json_attachment, generate_job_search_link

load_dotenv()

# Constants
MAX_LENGTH_FOR_ARTICLE_SUMMARIES = 2000
MAX_LENGTH_FOR_ARTICLE_AUDIO = 3000
VOICE_ASSISTANT_NAME = "Joanna"

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
                        We are creating a script for a not for profit client intake specialist conducting an informational interview
                        on what are the client's job skills, job history, job interests, email, zip code, and, if applicable, education
                        background . Write this to be understood by someone with a 7th grade reading level.
                       
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
                        
                        Your job is to act as Janet and ask questions 1 by 1 to the client.
                        
                        Goal:
                            1. Be as helpful as you can.
                            2. Only ask questions 1 at a time.
                            3. Your name is Janet and you work at the Aspire Center.
                            4. Keep the responses short and simple.
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

    def help(self):
        history_file_name = f"history/history-{time.time()}.json"

        while True:
            response = self.openAI.ChatCompletion.create(
                model=self.model_name,
                messages=self.history
            )
            role = response['choices'][0]['message']['role']

            text_response = response['choices'][0]['message']['content']
            speak(text_response[6:], timestamp=round(time.time()))
            print(text_response)

            self.history.append({
                "role": role,
                "content": text_response
            })

            # Exit if the end of conversation is reached
            for word in ["goodbye", "Goodbye", "bye", "great day"]:
                if word in self.history[-1]['content']:
                    return

            # Record user's input
            record_audio(output_filename="output")

            # Transcribe user's input
            transcribed_audio = transcribe_audio("output")

            print(f"Transcribed audio: {transcribed_audio}")

            self.history.append({
                "role": "user",
                "content": transcribed_audio
            })

            # Open the file in write mode and write the data
            with open(history_file_name, "w") as file:
                json.dump(self.history, file)

    def find_keywords_for_jobs(self):
        prompt = [{
            "role": "user",
            "content": "Find top 5 keywords in the following message that can be used as job search keywords: "
        }]
        # history_file_name = "/Users/ankushgarg/Desktop/projects/ai-hackathon/history/history-1689446660.910517.json"
        #
        # with open(history_file_name) as f:
        #     history = json.load(f)
        self.openAI.api_key = os.getenv("OPENAI_API_KEY")

        response = self.openAI.ChatCompletion.create(
            model=self.model_name,
            messages=prompt + self.history[1:]
        )

        top_five_keywords = response['choices'][0]['message']['content']
        print(top_five_keywords)
        search_url = generate_job_search_link(top_five_keywords)
        generate_email_json(
            sender_email="janet.helperbot@gmail.com",
            recipient_email="janet.helperbot@gmail.com",
            subject="Your new job lead",
            body_file="email_txt.txt",
            search_url=search_url,
            json_file_path="email.json"
        )

        send_email_from_json_attachment(
            json_file_path="email.json"
        )

        return


def main():
    job_helper = JobHelper()
    job_helper.setup()
    # job_helper.help()
    job_helper.find_keywords_for_jobs()


main()
