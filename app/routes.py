from app import app
from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time




# Переменная для хранения последовательности действий
actions = []


# Инициализация Selenium WebDriver
def init_driver():
    # Создаем объект с опциями для Chrome
    options = Options()
    #options.add_argument("--headless")  # Запуск браузера в фоновом режиме (опционально)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Указываем путь к драйверу с помощью ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Выполнение последовательности действий
def run_sequence(driver, actions):
    for action in actions:
        if action['type'] == 'open_url':
            driver.get(action['value'])
            print(f"Открыт URL: {action['value']}")

        elif action['type'] == 'click':
            element = driver.find_element(By.XPATH, action['value'])
            element.click()
            print(f"Клик по элементу с XPath: {action['value']}")

        elif action['type'] == 'input':
            element = driver.find_element(By.XPATH, action['xpath'])
            element.send_keys(action['value'])
            print(f"Ввод текста '{action['value']}' в поле с XPath: {action['xpath']}")

        elif action['type'] == 'wait':
            time.sleep(action['value'])
            print(f"Явное ожидание: {action['value']} секунд")
        time.sleep(1)  # Ожидание между действиями    


@app.route('/')
def index():
    return render_template('index.html', actions=actions)


@app.route('/add_action', methods=['POST'])
def add_action():
    action_type = request.form['action_type']
    if action_type == 'open_url':
        url = request.form['value']
        actions.append({'type': 'open_url', 'value': url})

    elif action_type == 'click':
        xpath = request.form['value']
        actions.append({'type': 'click', 'value': xpath})

    elif action_type == 'input':
        xpath = request.form['xpath']
        text = request.form['value']
        actions.append({'type': 'input', 'xpath': xpath, 'value': text})

    elif action_type == 'wait':
        seconds = int(request.form['value'])
        actions.append({'type': 'wait', 'value': seconds})

    return redirect(url_for('index'))




@app.route('/run')
def run():
    driver = init_driver()
    try:
        run_sequence(driver, actions)
    finally:
        
     driver.quit()
    return "Автоматизация выполнена успешно!"


@app.route('/clear')
def clear():
    global actions
    actions = []
    return redirect(url_for('index'))    














