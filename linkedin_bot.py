import time
from selenium_utils import setup_driver
from security_check import check_security
from llm_utils import setup_llm
from linkedin_actions import LinkedInActions

class LinkedInBot:
    def __init__(self):
        self.driver = setup_driver()
        self.llm = setup_llm()
        self.actions = LinkedInActions(self.driver, self.llm)

    def run(self, email, password, urls, messages):
        try: 
            self.actions.login(email, password)
            print("Login Successful!")
            check_security(self.driver, self.llm)
            for url, message in zip(urls, messages):
                try:
                    print(f'Proceeding with {url}') 
                    time.sleep(3)
                    self.actions.initiate(url, message)
                except Exception as e:
                    print(f"Error Occurred with {url}: ", e)
                    
            time.sleep(2)
            
            print("Signing out")
            self.actions.logout()
            time.sleep(2)
        except Exception as e:
            print("Error occurred: ", e)
        finally:
            self.driver.quit()