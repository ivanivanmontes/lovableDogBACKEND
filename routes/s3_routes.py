import io
import os
import boto3
import botocore
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from init import app

# Load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# app = Flask(__name__)


# Initialize S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                  region_name='eu-north-1')

BUCKET_NAME = "lovabledog"

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#     try:
#         s3.upload_fileobj(file, BUCKET_NAME, file.filename)
#         return jsonify({"message": "File uploaded successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@app.route("/getPhoto", methods = ["POST"])
def get_photo():
    try:
        file = request.files['file']  # Access uploaded file
        if file:
            filename = file.filename
            s3.upload_fileobj(file, BUCKET_NAME, filename)  # Upload file to S3 bucket
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/download/<string:filename>", methods=["GET"])
def download(filename):
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
        file_data = response['Body'].read()
        return send_file(
            io.BytesIO(file_data),
            mimetype='image/jpeg',  # Adjust mimetype based on your file type
            as_attachment=True,
            attachment_filename=filename
        )
    except botocore.exceptions.ClientError as e:
        return jsonify({'error': str(e)}), 404
    

