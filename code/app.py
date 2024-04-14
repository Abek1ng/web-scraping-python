from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import re
from api.halyk_category import make_api_call  

app = Flask(__name__)


@app.route('/parse_forte', methods=['GET'])
def scrape_forte_data():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')

    if script_tag:
        json_data = json.loads(script_tag.string)['props']['pageProps']
        companies = extract_company_data(json_data)
        return jsonify(companies)
    else:
        return jsonify({"error": "Company data not found on this page"}), 404

def extract_company_data(json_data):
    companies = []
    partners_component = next(
        (item for item in json_data.get('dynamicComponents', []) if item.get('__typename') == 'ComponentDynamicPagePartners'),
        None
    )

    if partners_component:
        for partner in partners_component.get('partners', []):
            if partner.get("subCategory") and partner.get("subCategory").get("parentCategory"):
                parent_category_title = partner["subCategory"]["parentCategory"]["title"]
            else:
                parent_category_title = None
            companies.append({
                "name": partner['title'],
                "cashback": float(partner.get('cashback', 0)),
                "category": parent_category_title
            })
    return companies

def parse_string(string):
    soup = BeautifulSoup(string, 'html.parser')
    return soup.get_text(strip=True)

def process_and_store_category_data(category_code, data):
    company_list = []
    for company in data.get('data', []):
        name = company.get('name')
        category_name = company.get('category_name')
        description = parse_string(company.get('tags')[0].get('description', ''))
        bonus_text = company.get('tags')[0].get('text', '')
        match = re.search(r"([-+]?[0-9]*\.?[0-9]+)", bonus_text)
        bonus = float(match.group(1)) if match else 0
        company_data = {
            'name': name,
            'category_name': category_name,
            'description': description + " при оплате QR и смартфоном",
            'bonus': bonus
        }
        company_list.append(company_data)
    return company_list

@app.route('/parse_halyk', methods=['GET'])
def start_parse():
    token = request.args.get('bearer_token')
    if not token:
        return jsonify({"error": "Missing 'bearer_token' parameter"}), 400
    company_list = get_company_list(token)
    return jsonify(company_list)

def get_company_list(bearer_token):
    company_list = []
    api_path = "/halykclub-api/v1/dictionary/categories"
    result = make_api_call(bearer_token, api_path)
    if result:
        code_and_id_list = [item['code'] for item in result]
        for category_code in code_and_id_list:
            data_path = f"/halykclub-api/v1/terminal/merchants?category_code={category_code}&filter="
            data = make_api_call(bearer_token, data_path)
            if data:
                company_by_category = process_and_store_category_data(category_code, data)
                company_list.extend(company_by_category)
    return company_list

if __name__ == '__main__':
    app.run(debug=True)
