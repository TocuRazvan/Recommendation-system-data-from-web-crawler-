from flask import Flask, render_template, request, make_response
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()  # Get the JSON data from the request
    data_str = json.dumps(data)  # Convert the JSON data to a string
    response = make_response('Data saved successfully')  # Create a response

    # Save the data to local storage or cookies
    response.set_cookie('imdb_data', data_str)  # Save as a cookie

    # Alternatively, you can save the data to local storage using JavaScript on the client-side.
    # Make sure to include appropriate JavaScript code in your HTML template.

    return response

if __name__ == '__main__':
    app.run()
