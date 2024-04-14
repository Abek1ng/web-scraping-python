Web scraper microservice
Currently implemented banks: Halyk Bank, Forte bank

HOW TO DEPLOY:
1. Clone the git
2. Activate virtual environment 
3. Run app.py locally or on host

ENDPOINTS:
host/parse_halyk{
parameters: bearer_token
}

host/parse_forte{
paraemters: url #in our case "https://club.forte.kz/partneroffers"
}
