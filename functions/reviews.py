import os
from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request, abort
import atexit

#Add your Cloudant service credentials here
CLOUDANT_USERNAME = os.environ.get('CLOUDANT_USERNAME', 'default')
CLOUDANT_API_KEY =  os.environ.get('CLOUDANT_API_KEY', 'default')
CLOUDANT_URL =  os.environ.get('CLOUDANT_URL', 'default')
client = Cloudant.iam(CLOUDANT_USERNAME, CLOUDANT_API_KEY, connect=True, url=CLOUDANT_URL)

session = client.session()
print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    print('this is get request')
    dealership_id = request.args.get('id')

    # Check if "id" parameter is missing
    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the URL"}), 400

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be an integer"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    return jsonify(data_list)


@app.route('/api/post_review', methods=['POST'])
def post_review():
    print('this is post request')
    if not request.json:
        print("invalid json data")
        abort(400, description='Invalid JSON data')
    
    # Extract review data from the request JSON
    review_data = request.json
    print("review_data,", review_data)
    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            print("lack of field,", field)
            abort(400, description=f'Missing required field: {field}')

    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)