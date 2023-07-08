import openai
import json

# Set up your OpenAI API credentials
openai.api_key = 'YOUR_API_KEY'

def collect_user_information():
    client_info = {}

    print("Client Intake Specialist: Good morning! Welcome to [Not-for-profit organization]. My name is [Specialist's Name], and I'm here to help you find a job that suits your skills and interests. How can I assist you today?")

    client_info['name'] = input("Client: Please enter your name: ")

    print("Client Intake Specialist: I understand your situation, and I'm here to support you. Let's start by getting to know you better.")

    client_info['job_skills'] = input("Client: Can you please tell me about your job skills? These are the abilities and things you're good at that could help you in a job: ")

    print("Client Intake Specialist: That's great to know. Now, let's talk about your job history.")

    client_info['job_history'] = input("Client: Have you worked before? If so, please tell me about your past jobs, including the names of the companies you worked for and the tasks you performed: ")

    print("Client Intake Specialist: Thank you for sharing that information. Now, let's talk about your job interests.")

    client_info['job_interests'] = input("Client: What kind of work are you interested in? Do you have any specific preferences or areas of interest? ")

    print("Client Intake Specialist: Another thing we need to know is your zip code.")

    client_info['zip_code'] = input("Client: Please provide me with your zip code: ")

    print("Client Intake Specialist: Lastly, could you tell me about your education background?")

    client_info['education_background'] = input("Client: Please enter your education background, including your highest level of education completed or any specific qualifications you have obtained: ")

    print("Client Intake Specialist: Thank you for your assistance. Based on the information you've provided, I will do my best to find job opportunities that match your skills, interests, and location. Please expect a follow-up call or visit from me soon with potential job leads.")

    return client_info


def save_to_json(data):
    with open('client_information.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def main():
    client_info = collect_user_information()
    save_to_json(client_info)


if __name__ == '__main__':
    main()

