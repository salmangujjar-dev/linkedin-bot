import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class LinkedInActions:
    def __init__(self, driver, llm):
        self.driver = driver
        self.llm = llm

    def login(self, email, password):
        self.driver.get('https://www.linkedin.com/uas/login')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(email)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(Keys.ENTER)

    def initiate(self, url):
        self.driver.get(url)
        name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]'))).text
        print(f'Name: {name}')

        if self.check_pending_request(name):
            return

        if not self.try_connect(name):
            print(f'Initiating Message {name}')
            self.message(self, "<p>Hi, how are you</p>")

    def check_pending_request(self, name):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Pending, click to withdraw invitation sent to {name}"]')))

            print(f"{name} - Already has a pending request.")
            
            return True
        except Exception as e:
            print(f"{name} - No Pending request found. Initiating Invitation Request.")
            return False

    def try_connect(self, name):
        try:
            self.invite_method_1(name)
            return True
        except Exception as e:
            print(f"{name} - Connect button not found. Trying alternative method.")
            try:
                self.invite_method_2(name)
                return True
            except Exception as e:
                print(f"{name} - Failed to connect. User might be already connected.")
                return False

    def invite_method_1(self, name):
        print(self.driver)
        # Try to find the "Connect" button
        connect_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Invite {name} to connect"]')))
        self.driver.execute_script("arguments[0].click();", connect_button)

        time.sleep(2)

        # If the button is clicked, a modal will appear. Click the "Send Invitation" button.
        send_invitation_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Send without a note"]')))
        send_invitation_button.click()

        print(f"{name} - Invitation sent successfully!")

    def invite_method_2(self, name):
        # Click on the "More" button
        more_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="More actions"]')))
        print(more_button)
        self.driver.execute_script("arguments[0].click();", more_button)
        
        print('Clicked on More Button')

        time.sleep(1)

        # Click on the "Connect" button in the dropdown
        connect_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//div[@aria-label="Invite {name} to connect"]')))
        connect_button.click()

        time.sleep(2)

        # If the button is clicked, a modal will appear. Click the "Send Invitation" button.
        send_invitation_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Send without a note"]')))
        send_invitation_button.click()

        print(f"{name} - Invitation sent successfully using alternative method!")

    def message(self, message): 
        message_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action"]')))
        self.driver.execute_script("arguments[0].click();", message_button)
        print('Message Button Clicked.')
        
        message_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[starts-with(@class, "msg-form__contenteditable") and @contenteditable="true"]')))
        message_box.clear()
        time.sleep(1)
        message_box.send_keys(message)
        time.sleep(2)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.RETURN).perform()
        print('Message sent Successfully!')