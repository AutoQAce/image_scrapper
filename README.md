# ImageScrapper with MongoDB & Docker

This Flask application allows you to search for images using Google Images and store them in a MongoDB database. It leverages web scraping techniques with error handling and logging for robust operation.

## Table of Contents

- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [Running the App in Docker Container](#Running-the-App-in-Docker-Container)
- [Contributing](#contributing)

## Functionality

1. **Homepage:** When you access the app's root URL (`/`), you'll see a simple search form where you can enter keywords or phrases related to the images you want to find.

2. **Image Search and Scraping:**  
   - After submitting the search form, the app sends a request to Google Images with your query.
   - It extracts image URLs from the search results using web scraping.
   - It downloads the images and stores them in the `images/` directory.
   - It also extracts relevant image data (e.g., URLs, potentially metadata) and stores it in a MongoDB collection named `image_scrap_data`.

3. **Error Handling and Logging:** 
   - The app includes robust error handling to catch and log any exceptions during the scraping process.
   - Logs are saved to `app.log` for debugging and monitoring.

4. **Data Retrieval (Future Enhancement):**
   - Currently, the app primarily focuses on scraping and storing images.
   - In a future enhancement, you could add functionality to retrieve and display the stored image data from MongoDB on a results page (`results.html`).



## Project Structure

Imagescrapper/
├── app/
│   ├── init.py        # Application factory function
│   ├── config.py         # Configuration settings
│   ├── models.py          # MongoDB models
│   ├── static/            # Static files (CSS)
│   │   └── style.css
│   ├── templates/        # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── results.html

│   ├── utils/
│   │   ├── init.py
│   │   ├── logging.py     # Logging configuration
│   │   └── web_scraping.py # Web scraping functions
│   └── views/             # Blueprints
│       ├── init.py
│       └── home/
│           ├── init.py
│           ├── routes.py
│           └── templates/
│               ├── index.html
│               └── results.html
├── run.py                # Main entry point
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
├── README.md             # This file


## Configuration

The application uses different configurations for testing and production environments. These are defined in the `app/config.py` file:

- **`ProductionConfig`:** Configuration for production deployment (default).
- **`TestingConfig`:** Configuration for testing and local development.

You can customize these configurations in `config.py` to suit your needs.


## Environment Variables

To run the app, you'll need to set the following environment variables in a `.env` file at the project root:


* **DB_USERNAME:** Database username for the application.
* **DB_PASSWORD:** Database password for the application.


## Running the App in Docker Container

The application can be run in either testing or production configuration modes. To run the app in the default production configuration 

For testing configuration, you can specify it in Dockerfile where you have to modify the **Dockerfile**(line no 19) in root directory of the project.
RUN export FLASK_CONFIG=<env>. Default is set to production.

```bash
docker-compose build
docker-compose up
```

## Contributing
Feel free to fork this repository and submit pull requests if you'd like to contribute.

Let me know if you'd like me to add or modify any sections of the `README.md`!
