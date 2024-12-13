#import my_microservice.services
from my_microservice.services.data_service import DataService
from flask import Flask, jsonify, request

app = Flask(__name__)
data_service = DataService()

@app.route('/load-data', methods=['POST'])
def load_data():
    # try:
    #     file_path = request.json['file_path']
    #     print("file_path=",file_path, type(file_path))
    #     #file_path = "C:\\# pythonProject\\fileLoader\\my_microservice\\data.xlsx"
    #     data = data_service.process_data(file_path)
    #     print("data=", data)
    #     return jsonify(data.to_dict(orient='records')), 200
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 400
    try:
        file_path = request.json['file_path']
        data = data_service.process_data(file_path)
        return jsonify(data.to_dict(orient='records')), 200
    except FileNotFoundError as e:
        app.logger.error(f"File not found: {str(e)}")
        return jsonify({"error": "File not found"}), 404
    except ValueError as e:
        app.logger.error(f"Invalid file format: {str(e)}")
        return jsonify({"error": "Invalid file format"}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

#http://localhost:5000/load-data
if __name__ == "__main__":
    app.run(debug=True)
