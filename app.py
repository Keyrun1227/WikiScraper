from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from threading import Thread
from pymongo import MongoClient
from bson.json_util import dumps
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['wiki_scraping_db']
collection = db['wiki_pages']

scraped_pages_count = 0
total_pages_count = 0


def scrape_wikipedia_page(url):
    global scraped_pages_count

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the info box contents and other details
    info_box = soup.find('table', class_='infobox')
    page_title = soup.find('h1', class_='firstHeading').text
    timestamp = datetime.now()

    # Extract the page content
    content = soup.find('div', class_='mw-parser-output').text.strip()

    # Extract field-value pairs from the info box
    fields = {}
    if info_box:
        rows = info_box.find_all('tr')
        for row in rows:
            header = row.find('th')
            if header:
                field = header.text.strip()
                value_cells = row.find_all('td')
                values = []
                for value_cell in value_cells:
                    value = value_cell.text.strip()
                    values.append(value)
                fields[field] = values

    # Store the details in the database
    page_data = {
        'url': url,
        'title': page_title,
        'timestamp': timestamp,
        'info_box': fields,
        'content': content
    }
    collection.insert_one(page_data)

    scraped_pages_count += 1


def calculate_progress():
    global scraped_pages_count, total_pages_count

    if total_pages_count == 0:
        return 0

    progress = (scraped_pages_count / total_pages_count) * 100
    return round(progress)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/filter')
def fil():
    return render_template('filter.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    global scraped_pages_count, total_pages_count

    urls = request.get_json().get('urls')

    if not urls:
        return jsonify({'message': 'No URLs provided.'}), 400

    if scraped_pages_count > 0:
        return jsonify({'message': 'Scraping is already in progress.'}), 400

    scraped_pages_count = 0
    total_pages_count = len(set(urls))

    def start_scraping():
        global scraped_pages_count

        unique_urls = list(set(urls))  # Remove duplicate URLs

        with app.app_context():
            for i in range(0, len(unique_urls), 50):
                batch_urls = unique_urls[i:i + 50]  # Get the next batch of 50 unique URLs
                for url in batch_urls:
                    scrape_wikipedia_page(url)
                    scraped_pages_count += 1  # Increment the scraped pages count

        scraped_pages_count = 0  # Reset scraped pages count after scraping is finished

    thread = Thread(target=start_scraping)
    thread.start()
    return jsonify({'message': 'Scraping started.'})


@app.route('/fields', methods=['GET'])
def get_fields():
    # Retrieve all documents from the collection
    documents = collection.find({}, {'info_box': 1})

    # Extract the unique fields from the 'info_box' dictionaries
    fields = set()
    for doc in documents:
        info_box = doc.get('info_box', {})
        fields.update(info_box.keys())

    # Convert the set to a list for JSON serialization
    fields = list(fields)

    return jsonify({'fields': fields})


@app.route('/progress', methods=['GET'])
def get_progress():
    # Calculate and return the progress value
    progress = calculate_progress()
    return jsonify({'progress': progress})


@app.route('/values', methods=['GET'])
def get_values():
    field = request.args.get('field')

    # Retrieve all documents from the collection that have the specified field
    documents = collection.find({'info_box.' + field: {'$exists': True}}, {'info_box': 1})

    # Extract the unique values for the specified field from the 'info_box' dictionaries
    values = set()
    for doc in documents:
        info_box = doc.get('info_box', {})
        field_values = info_box.get(field, [])
        values.update(field_values)

    return jsonify({'values': list(values)})


@app.route('/pages', methods=['GET'])
def get_pages():
    # Retrieve all documents from the collection
    documents = collection.find()

    # Convert the documents to JSON format
    pages = dumps(documents)

    return pages


@app.route('/filter', methods=['POST'])
def filter_pages():
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    # Validate the field and value inputs
    if not field or not value:
        return jsonify({'message': 'Field and value must be provided.'}), 400

    # Filter the pages based on the field and value
    filtered_pages = collection.find({'info_box.' + field: {'$in': [value]}}, {'info_box': 0})

    # Convert the filtered pages to JSON format
    pages = dumps(filtered_pages)

    return pages


if __name__ == '__main__':
    app.run(debug=True)
