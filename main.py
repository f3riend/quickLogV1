import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template
from flask_socketio import SocketIO
from engineio.async_drivers import eventlet
from icecream import ic
from time import sleep
import threading
import pyautogui
import webview
import json
import os

width = 400
height = 225

locX = 0
locY = pyautogui.size().height - height

class LoginSystem:
    def __init__(self) -> None:
        self.gmailPath = "https://accounts.google.com/v3/signin/identifier?authuser=0&continue=https%3A%2F%2Fmyaccount.google.com%2F%3Fpli%3D1&ec=GAlAwAE&hl=tr&service=accountsettings&flowName=GlifWebSignIn&flowEntry=AddSession&dsh=S1292135306%3A1719765769885536&ddm=0"
        self.githubPath = "https://github.com/login"
        self.instagramPath = "https://www.instagram.com/"
        self.steamPath = "https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_600__global-header"
        self.discordPath = "https://discord.com/login"
        
        
        self.username = os.getlogin()
        self.profilePath = f"C:/Users/{self.username}/AppData/Local/Google/Chrome/User Data/Default/"

        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-save-password-bubble")
        self.options.add_argument(f"user-data-dir={self.profilePath}")

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        self.driver.maximize_window()

    def open_new_tab(self, url):
        self.driver.execute_script(f"window.open('{url}', '_blank');")

    def loginToGmail(self, email, password):
        try:
            self.open_new_tab(self.gmailPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
            emailBox.send_keys(email)
            self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
            passwordBox.send_keys(password)
            self.driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()

            sleep(2)

            WebDriverWait(self.driver, 10).until(EC.url_contains("myaccount.google.com"))
        except Exception as e:
            ic("Something went wrong", e)

    def loginToGithub(self, email, password):
        try:
            self.open_new_tab(self.githubPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_field"]')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="login"]/div[4]/form/div/input[13]').click()

        except Exception as e:
            ic("Something went wrong", e)

    def loginToInstagram(self, email, password):
        try:
            self.open_new_tab(self.instagramPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        except Exception as e:
            ic("Something went wrong", e)

    def loginToSteam(self, email, password):
        try:
            self.open_new_tab(self.steamPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[1]/input')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[2]/input')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[4]/button').click()
        except Exception as e:
            ic("Something went wrong", e)

    def loginToDiscord(self, email, password):
        try:
            self.open_new_tab(self.discordPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid_7"]')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid_9"]')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]').click()
        except Exception as e:
            ic("Something went wrong", e)

# Load passwords from JSON file
with open(os.path.join(os.path.abspath("."), "passwords.json"), "r") as file:
    data = json.load(file)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')


loginSystem = LoginSystem()

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html")

@socketio.on('login')
def login(i):
    try:
        if i == 0:
            emails = data.get('email')
            if emails:
                for key, value in emails.items():
                    loginSystem.loginToGmail(value.get('username'), value.get('pass'))
        elif i == 1:
            github = data.get('github')
            if github:
                loginSystem.loginToGithub(github.get('username'), github.get('pass'))
        elif i == 2:
            instagram = data.get('instagram')
            if instagram:
                loginSystem.loginToInstagram(instagram.get('username'), instagram.get('pass'))
        elif i == 3:
            steam = data.get('steam')
            if steam:
                loginSystem.loginToSteam(steam.get('username'), steam.get('pass'))
        elif i == 4:
            discord = data.get('discord')
            if discord:
                loginSystem.loginToDiscord(discord.get('username'), discord.get('pass'))
    except Exception as e:
        ic("Error during login:", e)

def run_flask():
    socketio.run(app, debug=True, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    window = webview.create_window("Password Manager", "http://localhost:5000", x=locX, y=locY, width=width, height=height, frameless=True, on_top=True, draggable=False)
    webview.start()
