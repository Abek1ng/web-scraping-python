from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_data():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    element_list = []

    

    try:
        page_url = "https://halykbank.kz/halykclub#!/1501/list?category_code=supermarketi&filter"  
        driver.get(page_url)

        block_elements = driver.find_elements(By.CSS_SELECTOR, 'div.block')
        element_list = []

        for block in block_elements:
            content = {}

            
            company_name = block.find_element(By.CSS_SELECTOR, 'span').text.strip()
            if company_name:
                content["company_name"] = company_name

            
            all_text = block.text
            
            cashback_matches = re.findall(r'(\d+)%', all_text)
            if cashback_matches:
                
                content["cashback"] = float(cashback_matches[0])

            
            if 'QR' in all_text:
                content["description"] = all_text.split('\n')[-1]  

            element_list.append(content)
        print(element_list)
    finally:
        driver.quit()

    return jsonify(element_list), 200, {'Content-Type': 'application/json'} 


if __name__ == '__main__':
    app.run(debug=True)



