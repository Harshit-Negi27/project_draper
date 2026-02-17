from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def post_tweet_visual_demo(text):
    print("🔌 Connecting to your Open Chrome Window...")
    
    # 1. Connect to the browser you already opened
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    
    # 2. Go to the Tweet Page
    driver.get("https://x.com/compose/tweet")
    time.sleep(4) # Wait for animation
    
    # 3. Type the Tweet (Character by Character looks cooler/more robotic)
    active_element = driver.switch_to.active_element
    for char in text:
        active_element.send_keys(char)
        time.sleep(0.05) # Typing speed
    
    time.sleep(1)
    
    # 4. Click Post (The "Nuclear" option - sending CTRL+ENTER)
    # This is safer than finding the button which changes IDs often
    active_element.send_keys(Keys.CONTROL, Keys.ENTER)
    # On Mac use: active_element.send_keys(Keys.COMMAND, Keys.ENTER)
    
    print("✅ Action Complete")