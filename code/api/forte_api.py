import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape_forte', methods=['GET'])
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
    # "subCategory": {
    #                                         "id": "47",
    #                                         "title": "Клубы – загородные клубы, членство (отдых, спорт), частные поля для гольфа",
    #                                         "parentCategory": {
    #                                             "id": "134",
    #                                             "title": "Спорт"
    #                                         }
    #                                     },

    if partners_component:
        for partner in partners_component.get('partners', []):
            if partner.get("subCategory") and partner.get("subCategory").get("parentCategory"):
                parent_category_title = partner["subCategory"]["parentCategory"]["title"]
            else:
                parent_category_title = None
            companies.append({
                "name": partner['title'],
                "cashback": float(partner.get('cashbak', 0)),
                "category" :  parent_category_title

            })
            print(companies)

    return companies

if __name__ == "__main__":
    app.run(debug=True)
