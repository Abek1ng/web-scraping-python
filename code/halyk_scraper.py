from flask import Flask, request, jsonify
from api.halyk_category import make_api_call
from bs4 import BeautifulSoup
import re

app = Flask(__name__)


def parse_string(string):
    soup = BeautifulSoup(string, 'html.parser')
    normal_string = soup.body.get_text(strip=True)
    return normal_string
   

def process_and_store_category_data(category_code, data):
    company_list = []
    for company in data.get('data'):
        name = company.get('name')
        category_name = company.get('category_name')
        description = None
        bonus = None
        
        text = company.get('tags')[0].get('text')
            
        match = re.search(r"([-+]?[0-9]*\.?[0-9]+)", text)
        if match:
            bonus = float(match.group(1))
        description = parse_string(company.get('tags')[0].get('description'))
    
        company_data = {
            'name': name,
            'category_name': category_name,
            'description': description + "при оплате QR и смартфоном",
            'bonus': bonus
        }

        company_list.append(company_data)
    return company_list

def get_company_list(bearer_token):
    company_list = []
    api_path = "/halykclub-api/v1/dictionary/categories"
    result = make_api_call(bearer_token, api_path)

    if result:
        code_and_id_list = [item['code'] for item in result]

        for category in code_and_id_list:
            data_path = f"/halykclub-api/v1/terminal/merchants?category_code={category}&filter="
            data = make_api_call(bearer_token, data_path)
            company_by_category = process_and_store_category_data(category, data)
            company_list.extend(company_by_category)
    return company_list

@app.route('/parse', methods=['GET'])
def start_parse():
    token = request.args.get('bearer_token') 
    if not token:
        return jsonify({"error": "Missing 'bearer_token' parameter"}), 400
    company_list = get_company_list(token)
    return jsonify(company_list)


if __name__ == "__main__":
    app.run(debug=True)
