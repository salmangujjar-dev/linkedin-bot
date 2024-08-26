import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain_openai import AzureChatOpenAI

def check_security(driver, llm):
    try:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Let’s do a quick security check"]')))
            print('Security Check header found.')
        except Exception as e:
            print('No Security Check Found.')
            return True
        
        print('Switching driver to captcha-internal iframe.')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha-internal")))
        driver.switch_to.frame("captcha-internal")

        print('Switching driver to arkoseframe iframe.')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "arkoseframe")))
        driver.switch_to.frame("arkoseframe")

        print('Switching driver to Verification challenge iframe.')
        enforcement_frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Verification challenge']")))
        driver.switch_to.frame(enforcement_frame)

        print('Switching driver to fc-iframe-wrap iframe.')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fc-iframe-wrap")))
        driver.switch_to.frame("fc-iframe-wrap")

        print('Switching driver to CaptchaFrame iframe.')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CaptchaFrame")))
        driver.switch_to.frame("CaptchaFrame")

        verify_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-describedby, "descriptionVerify")]')))
        verify_button.click()
        print('Clicked on Verify Button.')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "game")]')))
        print('Game Loaded in iframe.')

        time.sleep(3)

        screenshot = driver.get_screenshot_as_base64()

        llm = AzureChatOpenAI(
            azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
            api_version="2023-09-15-preview",
            temperature=0.3
        )

        messages=[
            {"role": "system", "content": "You are a intelligent assistant that solves puzzles with clarity and max success rate."},
            {"role": "user", "content": [
                {"type": "text", "text": "Solve the puzzle. image indexes starts from 1 and moves from left to right and increment on each index change. I want the only response you should give is that integer and nothing else should be in response."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{screenshot}"}
                }
            ]}
        ]
        ai_message = llm.invoke(messages)
        print(f"Correct index is {ai_message.content}")
        correct_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//li[contains(@id, "image{ai_message.content}")]/a')))
        correct_box.click()

        print("Puzzle Solved Successfully!")
        driver.switch_to.default_content()
        return True
    except Exception as e:
        print('Security Check Error.')
        raise e