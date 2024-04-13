import pytest
from flask_testing import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app import app

class TestWebScraper(TestCase):
    def create_app(self):
        # Configure the Flask app for testing
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Set up test variables and initialize the app."""
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        
    def tearDown(self):
        """Tear down any data added from a test."""
        self.driver.quit()

    def test_scrape_endpoint(self):
        """Test the /scrape endpoint of the web scraper."""
        # This uses the test client provided by Flask-Testing
        response = self.client.get('/scrape')
        
        # Check if the response is successful
        self.assert200(response, "The /scrape endpoint did not return HTTP 200")
        
        # Ensure data is returned
        self.assertTrue(len(response.json) > 0, "No data was returned from the /scrape endpoint")

        # Optional: Additional tests to validate the structure of returned data
        sample_data = response.json[0]
        self.assertIsInstance(sample_data, dict)
        self.assertIn('title', sample_data)
        self.assertIn('cashback', sample_data)
        # self.assertIn('description', sample_data)
        # self.assertIn('rating', sample_data)

# Run the tests if this file is called from the command line
if __name__ == '__main__':
    pytest.main()
