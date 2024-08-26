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

    def logout(self):
        self.driver.get('https://www.linkedin.com/m/logout?trk=hb_signout')

    def initiate(self, url, message):
        self.driver.get(url)
        username = url.rstrip('/').split('/')[-1]
        
        name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]'))).text
        print(f'Name: {name} - {username}')

        if self.check_pending_request(name, username):
            return

        isWithNote = True
        
        if not self.already_connected(name, username):
            self.try_connect(name, username, isWithNote, message)
        else:
            self.message(username, message)
            

    def check_pending_request(self, name, username):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Pending, click to withdraw invitation sent to {name}"]')))

            print(f"{username} - Already has a pending request.")
            
            return True
        except Exception as e:
            print(f"{username} - No Pending request found. Initiating Invitation Request.")
            return False
    
    def already_connected(self, name, username):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//div[@aria-label="Remove your connection to {name}"]')))
            
            print(f"{username} - User is already Connected.")
            
            return True
        except Exception as e:
            print(f"{username} - User Not Connected.")
            return False

    def try_connect(self, name, username, isWithNote, message):
        try:
            self.invite_method_1(name, username, isWithNote, message)
            return True
        except Exception as e:
            print(f"{username} - Connect button not found. Trying alternative method.")
            try:
                self.invite_method_2(name, username, isWithNote, message)
                return True
            except Exception as e:
                print(f"{username} - Failed to connect. User might be already connected.")
                return False

    def invite_modal_action(self, username, isWithNote, message):
        if isWithNote:
            send_invitation_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Add a note"]')))
            send_invitation_button.click()
            
            print(f'{username} - Adding a note')
            message_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[@id="custom-message"]')))
            message_box.clear()
            message_box.send_keys(message)
            time.sleep(1)
            
            send_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Send invitation"]')))
            send_button.click()
            
            print(f'{username} - Clicked on Send successfully!')
        else:
            send_invitation_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Send without a note"]')))
            send_invitation_button.click()
        
        

    def invite_method_1(self, name, username, isWithNote, message):
        # Try to find the "Connect" button
        connect_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Invite {name} to connect"]')))
        self.driver.execute_script("arguments[0].click();", connect_button)

        time.sleep(2)

        self.invite_modal_action(username, isWithNote, message)

        print(f"{username} - Invitation sent successfully!")

    def invite_method_2(self, name, username, isWithNote, message):
        # Click on the "More" button
        more_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="More actions"]')))
        self.driver.execute_script("arguments[0].click();", more_button)
        
        print(f'{username} - Clicked on More Button!')

        time.sleep(1)

        # Click on the "Connect" button in the dropdown
        connect_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//div[@aria-label="Invite {name} to connect"]')))
        connect_button.click()

        time.sleep(2)
        
        self.invite_modal_action(username, isWithNote, message)

        print(f"{username} - Invitation sent successfully using alternative method!")

    def message(self, username, message): 
        message_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action"]')))
        self.driver.execute_script("arguments[0].click();", message_button)
        print(f'{username} - Message Button Clicked.')
        
        time.sleep(1)
        
        hidden_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-hidden="true" and contains(@class, "msg-form__placeholder")]')))
        self.driver.execute_script("arguments[0].remove();", hidden_area)
        
        time.sleep(1)
        
        message_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[starts-with(@class, "msg-form__contenteditable")]/p')))
        message_box.send_keys(message)
        time.sleep(2)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
        print(f'{username} - Message sent Successfully!')
        message_box.send_keys(Keys.ESCAPE)