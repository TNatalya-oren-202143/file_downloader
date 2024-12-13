import unittest
from my_microservice.controllers.data_controller import app
from flask import jsonify
import json

class TestDataController(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_load_data(self):
        #data = json.dumps({'file_path': 'C:/data.xlsx'})
        response = self.client.post('/load-data',
                                    #data,#400 Bad Request:
                                    data=json.dumps({'file_path': 'data.xlsx'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn({'q': 1, 'w': 2}, response.json)

if __name__ == '__main__':
    unittest.main()
