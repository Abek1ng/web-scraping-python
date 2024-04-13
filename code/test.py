from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_data():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    element_list = []

    try:
        for page in range(1, 3):  # You can parameterize the page range if needed
            page_url = f"https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={page}"
            driver.get(page_url)
            titles = driver.find_elements(By.CLASS_NAME, "title")
            prices = driver.find_elements(By.CLASS_NAME, "price")
            descriptions = driver.find_elements(By.CLASS_NAME, "description")
            ratings = driver.find_elements(By.CLASS_NAME, "ratings")

            for i in range(len(titles)):
                element_list.append({
                    "title": titles[i].text, 
                    "price": prices[i].text, 
                    "description": descriptions[i].text, 
                    "rating": ratings[i].text
                })
    finally:
        driver.quit()

    return jsonify(element_list)

if __name__ == '__main__':
    app.run(debug=True)
