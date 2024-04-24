import os
import boto3
import botocore
from flask import Flask, jsonify, Response
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Initialize Flask app
app = Flask(__name__)


# Initialize S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                  region_name='eu-north-1')

BUCKET_NAME = "lovabledog"

@app.route('/upload', methods=["GET"])
def upload() -> Response:
    print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
    print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)
    
    # Print current directory
    print("Current Directory:", os.getcwd())

    # Check if test.txt exists
    file_path = 'routes/:p.txt'  # Adjusted file path
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                s3.upload_fileobj(f, BUCKET_NAME, ':p.txt')
            return jsonify({"message": "File uploaded successfully"}), 200
        except botocore.exceptions.ClientError as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "test.txt not found"}), 404

    

# @app.route("/download/<str:filename>", methods= ["GET"])
# def download(filename : str) -> Response:
#     try:
#         response = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
#         file_data = response['Body'].read()
#         return jsonify({'data': file_data.decode('utf-8')}), 200
#     except botocore.exceptions.ClientError as e:
#         return jsonify({'error': str(e)}), 404
