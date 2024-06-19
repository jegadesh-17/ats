class ChatBot:
    def __init__(self):
        self.details = {}

    def start_application(self):
        print("Chatbot (Talkie): 'Thank you for showing interest in the Management Consultant position at [Company Name]. Let's get started with your application. Can you please provide your first name?'")
        self.details['first_name'] = input()
        self.collect_last_name()

    def collect_last_name(self):
        print("Chatbot (Talkie): 'Great! Now, can you provide your last name?'")
        self.details['last_name'] = input()
        self.collect_email()

    def collect_email(self):
        print(f"Chatbot (Talkie): 'Thank you, {self.details['first_name']}. What's your email address?'")
        self.details['email'] = input()
        self.collect_phone_number()

    def collect_phone_number(self):
        print("Chatbot (Talkie): 'Got it. Can you also provide your phone number?'")
        self.details['phone'] = input()
        self.collect_address()

    def collect_address(self):
        print("Chatbot (Talkie): 'Perfect. Can you please provide your current address? Start with your house number and street name.'")
        self.details['address_street'] = input()
        print("Chatbot (Talkie): 'Thank you. Now, can you provide your city or town?'")
        self.details['address_city'] = input()
        print("Chatbot (Talkie): 'Thanks. Can you provide your postal code?'")
        self.details['address_postal_code'] = input()
        print("Chatbot (Talkie): 'Great. And finally, can you provide your country?'")
        self.details['address_country'] = input()
        self.collect_employment_details()

    def collect_employment_details(self):
        print("Chatbot (Talkie): 'Excellent. Now, let's move on to your employment history. Please provide the name of your most recent employer.'")
        self.details['employer'] = input()
        print(f"Chatbot (Talkie): 'Thank you. What was your job title at {self.details['employer']}?'")
        self.details['job_title'] = input()
        print("Chatbot (Talkie): 'Great. How long did you work there? (Please specify in months or years)'")
        self.details['job_duration'] = input()
        print("Chatbot (Talkie): 'Got it. Can you briefly describe your responsibilities in this role?'")
        self.details['job_responsibilities'] = input()
        self.collect_educational_details()

    def collect_educational_details(self):
        print("Chatbot (Talkie): 'Thank you. Let's move on to your educational background. Please provide the name of the institution where you obtained your highest degree.'")
        self.details['education_institution'] = input()
        print("Chatbot (Talkie): 'Great. What was your degree?'")
        self.details['education_degree'] = input()
        print("Chatbot (Talkie): 'When did you graduate? (Please specify the month and year)'")
        self.details['education_graduation_date'] = input()
        print("Chatbot (Talkie): 'Thank you. Can you also provide any additional qualifications or certifications relevant to the Management Consultant position?'")
        self.details['additional_qualifications'] = input()
        self.collect_skills()

    def collect_skills(self):
        print("Chatbot (Talkie): 'Excellent. Can you list your top three skills relevant to this position?'")
        self.details['skills'] = input()
        print("Chatbot (Talkie): 'Thank you. Do you have any specific competencies or experiences that make you a strong fit for this role? (e.g., project management, data analysis, etc.)'")
        self.details['competencies'] = input()
        self.collect_additional_info()

    def collect_additional_info(self):
        print("Chatbot (Talkie): 'Great. Is there anything else you would like us to know about your application or experience?'")
        self.details['additional_info'] = input()
        # self.upload_documents()

    # def upload_documents(self):
    #     print("Chatbot (Talkie): 'Thank you for all the information. Can you please upload your CV/resume? You can simply drag and drop the file here.'")
    #     self.details['cv'] = "Uploaded"  # Simulate the upload.
    #     print("Chatbot (Talkie): 'Thank you. Do you have a cover letter to upload as well?'")
    #     self.details['cover_letter'] = "Uploaded"  # Simulate the upload.
    #     self.final_confirmation()

    def final_confirmation(self):
        print("Chatbot (Talkie): 'Please review the information you've provided. Type 'yes' to confirm and submit your application or 'no' to make any changes.'")
        confirmation = input()
        if confirmation.lower() == 'yes':
            print(f"Chatbot (Talkie): 'Thank you, {self.details['first_name']}. Your application for the Management Consultant position has been submitted successfully. You will receive a confirmation email shortly. Have a great day!'")
        else:
            print("Chatbot (Talkie): 'Please specify which information you'd like to change.'")

# Create an instance of ChatBot and start the application process
if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.start_application()
