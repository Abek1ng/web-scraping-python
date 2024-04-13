import PyPDF2
import requests

def extract_text_from_pdf(pdf_path):
    # Initialize a text accumulator
    text = ""
    
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        
        # Iterate through each page and extract text
        for page in pdf.pages:
            text += page.extract_text()
    
    return text

def analyze_text_with_openai(text, api_key):
    # Define the API URL
    api_url = "https://api.openai.com/v1/chat/completions"
    
    # Set up the headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        
    }
    
    # Define the data payload for POST request
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Ты машина и ты никогда не нарушаешь регламент прописанный в правилах. Правила: ты ОБЯЗАН проонализировать текст и ВЫДАТЬ ответ в JSON форматте в текстовом виде где поля должны быть такие: {'category': string, {'cashback' : float, 'condition': string}}, пример: {'category': Кинотеатры, {'cashback' : 2, 'condition': 'Макс 20000 в месяц'}}, Ты Обязан максимально писать коротко и ни в коем случае не изменять Текстовое значение категории. Ты должен отыскатб все возможные категории поподающием под бонусную программу"},
            {"role": "user","content": text}
            ],
        "temperature": 0.9
        
    }
    
    # Make a POST request to the OpenAI API
    response = requests.post(api_url, headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Usage example
pdf_path = "/Users/abekesalimzhanov/Downloads/RUS_Bonuses_Halyk.pdf"
api_key = "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"

# Extract text from PDF
text = extract_text_from_pdf(pdf_path)

# Analyze the text using OpenAI API
result = analyze_text_with_openai(text, api_key)
print(result)
