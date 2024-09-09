from django.test import TestCase
from unittest.mock import  patch, MagicMock
from rest_framework.test import APIClient
from django.urls import reverse

# Create your tests here.
"""
Mock the elastic search  client
You'll typically want to mock the Elasticsearch client and its responses. 
"""

class DiseaseSearchTestCase(TestCase):

    def setUp(self):
        # Initialize the test client
        self.client = APIClient()

    @patch('mic_api.views.Search')
    def test_disease_search(self, mock_search):
        # Setup the mock
        mock_response = MagicMock()
        mock_response.hits.total.value = 1
        mock_hit = MagicMock()
        mock_hit.to_dict.return_value = {
            'code': '1A00',
            'title_en': 'Cholera',
            'title_ar': 'الكوليرا'
        }
        mock_response.__iter__.return_value = [mock_hit]
        mock_search_instance = mock_search.return_value
        mock_search_instance.execute.return_value = mock_response

        # Call the API endpoint
        response = self.client.get(reverse('disease_search'), {'search': 'Cholera', 'page': 1})

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = response.json()
        self.assertEqual(response_data['total_count'], 1)
        self.assertEqual(response_data['page'], 1)
        self.assertEqual(response_data['total_pages'], 1)
        self.assertEqual(len(response_data['results']), 1)
        self.assertEqual(response_data['results'][0]['code'], 'A00')
        self.assertEqual(response_data['results'][0]['title_en'], 'Cholera')
        self.assertEqual(response_data['results'][0]['title_ar'], 'الكوليرا')

    @patch('mic_api.views.Search')
    def test_disease_search_no_results(self, mock_search):
        # Setup the mock for no results
        mock_response = MagicMock()
        mock_response.hits.total.value = 0
        mock_response.__iter__.return_value = []
        mock_search_instance = mock_search.return_value
        mock_search_instance.execute.return_value = mock_response

        # Call the API endpoint with a search term that doesn't exist
        response = self.client.get(reverse('disease_search'), {'search': 'NonExistentDisease', 'page': 1})

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = response.json()
        self.assertEqual(response_data['total_count'], 0)
        self.assertEqual(response_data['page'], 1)
        self.assertEqual(response_data['total_pages'], 1)
        self.assertEqual(len(response_data['results']), 0)
    
    @patch('mic_api.views.Search')
    def test_disease_search_error(self, mock_search):
        # Setup the mock to raise an exception
        mock_search_instance = mock_search.return_value
        mock_search_instance.execute.side_effect = Exception('Something went wrong')

        # Call the API endpoint expecting an error
        response = self.client.get(reverse('disease_search'), {'search': 'Cholera', 'page': 1})

        # Check the response status code
        self.assertEqual(response.status_code, 500)

        # Check the response data
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Something went wrong')
