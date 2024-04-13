from flask import Flask, request, jsonify
from api.halyk_category import make_api_call

app = Flask(__name__)

def process_and_store_category_data(category_code, data):
    company_list = []
    for company in data:
        name = company.get('name')
        category_name = company.get('category_name')
        description = None
        bonus = None
        for tag in company.get('tags', []):
            bonus = tag.get('text')
            description = tag.get('description')
            
        company_data = {
            'name': name,
            'category_name': category_name,
            'description': description,
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
            data_path = f"/halykclub-api/v1/terminal/devices?category_code={category}&filter="
            data = make_api_call(bearer_token, data_path)
            company_by_category = process_and_store_category_data(category, data)
            company_list.extend(company_by_category)
    return company_list

@app.route('/parse', methods=['GET'])
def start_parse():
    if not request.json or 'bearer_token' not in request.json:
        return jsonify({'error': 'Bearer token is required in the JSON body'}), 400
    bearer_token = request.json['bearer_token']
    company_list = get_company_list(bearer_token)
    return jsonify(company_list)

if __name__ == "__main__":
    app.run(debug=True)
