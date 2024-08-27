import asyncio
from selenium_utils import setup_driver
from security_check import check_security
from llm_utils import setup_llm
from linkedin_actions import LinkedInActions

class LinkedInBot:
    def __init__(self):
        self.driver = setup_driver()
        self.llm = setup_llm()
        self.actions = LinkedInActions(self.driver, self.llm)

    async def run(self, email, password, urls, messages):
        try: 
            await asyncio.to_thread(self.actions.login, email, password)
            print("Login Successful!")
            await asyncio.to_thread(check_security, self.driver, self.llm)
            for url, message in zip(urls, messages):
                try:
                    print(f'Proceeding with {url}') 
                    await asyncio.sleep(3)
                    await asyncio.to_thread(self.actions.initiate, url, message)
                except Exception as e:
                    print(f"Error Occurred with {url}: ", e)
                    
            await asyncio.sleep(2)
            
            print("Signing out")
            await asyncio.to_thread(self.actions.logout)
            await asyncio.sleep(2)
        except Exception as e:
            print("Error occurred: ", e)
            raise e
        finally:
            self.driver.quit()