# Ceneo Web Scraper

## Description

This application enables users to quickly obtain reviews of products from Ceneo.pl, one of the largest e-commerce
platforms in Poland. Users can download these reviews in JSON, CSV, and XLSX formats.

## Technologies Used

- Flask: A micro web framework for Python.
- Firebase: Backend platform used for building web and mobile applications.
- BeautifulSoup4: A library for pulling data out of HTML and XML files.

## Installation

To set up the project:

1. Clone the repository.
   ```
   git clone https://github.com/avanrish/ceneo-webscraper.git
   cd ceneo-webscraper
   ```
2. Create and activate a virtual environment.
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```
3. Install dependencies.
   ```
   pip install -r requirements.txt
   ```
4. Rename `.env.example` to `.env`.
5. Set up a Firebase project and enable Firestore.
6. Download the Firebase service account JSON file and add its content to the `.env` file as a one-line string.

## Usage

After completing the installation steps:

1. Run `run.py`.
   ```
   python run.py
   ```
2. Open a web browser and navigate to `localhost:8001`.
3. Visit Ceneo.pl, select a product, copy the product link, and paste it into the application to retrieve and download
   reviews.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
