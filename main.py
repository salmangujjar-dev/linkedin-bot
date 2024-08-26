import os
from dotenv import load_dotenv
from linkedin_bot import LinkedInBot

load_dotenv()

if __name__ == "__main__":
    bot = LinkedInBot()
    
    session_key = os.getenv('LINKEDIN_EMAIL')
    session_password = os.getenv('LINKEDIN_PASSWORD')
    
    if not session_key or not session_password:
        raise ValueError("LinkedIn credentials not found in environment variables.")
    
    urls = [
        'https://www.linkedin.com/in/danishafzalkhan/'
    ]
    
    bot.run(session_key, session_password, urls)