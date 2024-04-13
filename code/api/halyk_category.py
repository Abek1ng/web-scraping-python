import requests

def make_api_call(bearer_token, path):
    
    url = "https://pelican-api.homebank.kz" + path
    base_headers = {
        "authority": "pelican-api.homebank.kz",
        "method": "GET",
        "scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru",
        "Authorization": f"Bearer {bearer_token}",  
        "City_id": "1501",
        "Origin": "https://halykbank.kz",
        "Referer": "https://halykbank.kz/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=base_headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API request failed with status code: {response.status_code}")
        return None



