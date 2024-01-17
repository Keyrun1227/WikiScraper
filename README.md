# Wikipedia Scraper 🌐📚

Wikipedia Scraper is a Flask-based web application for extracting information from Wikipedia pages. It provides functionalities such as web scraping, data storage in MongoDB, and filtering of scraped data.

## Features 🚀

- **Web Scraping:** Extracts information from Wikipedia pages, including URL, title, timestamp, info box contents, and page content.
- **MongoDB Integration:** Stores scraped data in a MongoDB database for efficient data retrieval and management.
- **Threading:** Utilizes threading to handle concurrent scraping of multiple URLs.
- **Filtering:** Allows users to filter scraped pages based on specified fields and values.

## Technologies Used 💻

- Flask: Python web framework for building the application.
- MongoDB: NoSQL database for storing scraped data.
- BeautifulSoup: Python library for web scraping.
- Flask-CORS: Enables Cross-Origin Resource Sharing for handling requests from different origins.

## Usage 📝

1. **Run the Application:**
   - Execute `python app.py` to start the Flask application.

2. **Access the Home Page:**
   - Visit `http://127.0.0.1:5000/` in your browser.
   - Enter Wikipedia URLs in the provided textarea and click the "Scrape" button.

3. **Monitor Scraping Progress:**
   - Observe the progress bar indicating the scraping progress.

4. **Filter Scraped Data:**
   - Once scraping is complete, you will be redirected to the filter page (`http://127.0.0.1:5000/filter`).
   - Select a field and value to filter the scraped pages and view the results in a table.

## Project Structure 📁

- `filename.py`: Main Flask application file.
- `home.html`: Home page HTML template.
- `filter.html`: Filter page HTML template.

## Recommendations 🛠️

- Ensure MongoDB is running and accessible.
- Implement user authentication and authorization.
- Enhance error handling and validation in front-end and back-end code.
- Consider adding logging for better debugging and monitoring.

## Contributions 🤝

Contributions, feedback, and bug reports are welcome! Feel free to open issues or submit pull requests.
