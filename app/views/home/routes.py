from flask import render_template,request,jsonify
from app.models import ImageScraperModel
from app.views.home import home_bp
from app.utils.web_scrapping import *
import logging
from app.utils.logging import setup_logging
setup_logging()


@home_bp.route("/",methods=["GET"])
def homepage():
    return render_template('index.html')


@home_bp.route("/review", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            query = request.form["content"]
            img_data=scrape_google_images(query)
            model= ImageScraperModel()
            model.insert_image_data(img_data=img_data)
            logging.info("Images scraped and saved successfully.")
            return render_template("result.html")
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
            return "Something went wrong"
    else:
        return render_template("home/index.html")
