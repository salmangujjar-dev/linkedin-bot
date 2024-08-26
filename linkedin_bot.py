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

    def run(self, email, password, urls):
        try: 
            self.actions.login(email, password)
            print("Login Successful!")
            check_security(self.driver, self.llm)
            for url in urls:
                try:
                    print(f'Proceeding with {url}') 
                    time.sleep(3)
                    self.actions.initiate(url)
                except Exception as e:
                    print(f"Error Occurred with {url}: ", e)
        except Exception as e:
            print("Error occurred: ", e)
        finally:
            self.driver.quit()