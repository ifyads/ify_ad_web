
from flask import Flask, render_template, request , send_from_directory 

import random

import mysql.connector

import socket

import requests

import datetime

import platform

from admin import admin 

from b3cd9LT import ClRa1

from yUTBrRaENu import r3KGwEgXI1
  
#import validators  

import re

import os


BASE_URL = "127.0.0.1:8000/"  
SECRET_KEY = "your_secret_key"  


REDIRECT_DELAY = 6000

DB_HOST = "localhost"
DB_USER = "itsmine"
DB_PASSWORD = "I8t9s2M5Y7d6A5t6A25@"
DB_NAME = "link"

app = Flask(__name__, template_folder='templates')  

app.config['STATIC_FOLDER'] = 'static'

app.secret_key = SECRET_KEY



def generate_short_code():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    used_codes = set() 

    while True:
        short_code = ''.join(random.choices(alphabet, k=6))  
        if short_code not in used_codes:
            used_codes.add(short_code)
            return short_code
        

def get_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  
    ip = s.getsockname()[0]
    s.close()
    return ip



def get_public_ip_address():

  try:

    api_url = "https://api.ipify.org?format=text"
    response = requests.get(api_url)
    response.raise_for_status()  
    return response.text.strip()  
  except requests.exceptions.RequestException as e:
    print(f"Error fetching IP address: {e}")
    return None


def get_long_url(short_code):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        sql = "SELECT long_url FROM shortener WHERE short_code = %s"
        cursor.execute(sql, (short_code,))
        long_url = cursor.fetchone()

        if long_url:
            return long_url[0]
        else:
            return None  
    except Exception as e:
        print(f"Error retrieving long URL: {e}")
        raise  
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
  
launch_date = datetime.datetime.now() + datetime.timedelta(days=30)

valid_url_regex = r"^(?:http|https)://\w+\.\w+(?:[/\w\-_\.]*)?|^\w+\.\w+(?:[/\w\-_\.]*)$"


def save_launch_date():
  with open("launch_date.txt", "w") as f:
    f.write(launch_date.isoformat())

def load_launch_date():
  try:
    with open("launch_date.txt", "r") as f:
      return datetime.datetime.fromisoformat(f.read().strip())
  except FileNotFoundError:
    return None

launch_date = load_launch_date() or launch_date
save_launch_date()

def get_random_image_and_link(folder_path, ad_links):

  try:
    files = os.listdir(folder_path)

    images = [file for file in files if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

    if not images:
      return "None"

    random_image = random.choice(images)

    image_url = os.path.join(folder_path, random_image)

    ad_link = ad_links.get(os.path.splitext(random_image)[0], None)  

    return image_url, ad_link

  except FileNotFoundError:
    print(f"Error: Folder '{folder_path}' not found.")
    return None
  
def get_device_type():

  os_family = platform.system().lower()
  if os_family in ("android", "ios"):
    return "Mobile"
  elif "windows" in os_family or "linux" in os_family or "darwin" in os_family:
    return "Desktop"
  else:
    return "Unknown"


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")



@app.route("/linkshortener", methods=["GET", "POST"])
def linkshortener():
    if request.method == "GET":
        return render_template("shorten.html")

    elif request.method == "POST":
        long_url = request.form.get("long_url")

        if not long_url:
            return "Please enter a valid URL.", 400
        
        if not re.match(valid_url_regex, long_url):
            return "Please enter a valid URL", 400
        
        #if not validators.url(long_url):
            #return "Please enter a valid URL.", 400
        

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        short_code = generate_short_code()

        ip=get_ip()

        ip_address = get_public_ip_address()


        IP= ip+" & "+ip_address


        sql = "INSERT INTO shortener (short_code, long_url, ip) VALUES (%s, %s, %s)"  
        cursor.execute(sql, (short_code, long_url, IP ))
        connection.commit()

        cursor.close()
        connection.close()

        short_url = BASE_URL + short_code
        return render_template("shorten.html", short_url=short_url)

    else:
        return "Method not allowed", 405


@app.route("/About_Us", methods=["GET"])
def about():
    if request.method == "GET":
        return render_template("about.html")


@app.route("/<short_code>", methods=["GET", "POST"])
def redirect_to_long_url(short_code):

    long_url = get_long_url(short_code)


    if not long_url:
        return "Short code not found.", 404
    
    remaining_seconds = int((launch_date - datetime.datetime.now()).total_seconds())

    folder_path = "static/ads"

    ad_links = {
    "ad": "https://ifypixels.pythonanywhere.com/",
    "ad1": "https://www.youtube.com/"
    }
    
    image_url, ad_link = get_random_image_and_link(folder_path, ad_links)
    
    return render_template("redirect.html", long =long_url, delay=REDIRECT_DELAY , remaining_seconds=remaining_seconds ,ad_image = image_url ,link = ad_link)



@app.route("/Ads_offer", methods=["GET", "POST"])
def Ads_offer():

        IP = get_public_ip_address()

        device=get_device_type()

        os=platform.system() + " " + platform.release()

        remaining_seconds = int((launch_date - datetime.datetime.now()).total_seconds())


        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        
        sql = "INSERT INTO advisement_log ( device , ip , operating) VALUES (%s, %s, %s)"  
        cursor.execute(sql, (device, IP , os))
        connection.commit()

        cursor.close()
        connection.close()


        return render_template("offer.html" , remaining_seconds=remaining_seconds)
  


@app.route("/terms-and-conditions", methods=["GET"])
def terms_and_conditions():
    if request.method == "GET":
        return render_template("terms.html") 


@app.route("/6379/admin/login")
def admin_login():
    return admin()
    
@app.route("/d51QV6P/ByOhFSeT9Q/admin/login", methods=["GET"])
def iFX1r0Aykd():
    return ClRa1()

@app.route("/7PjiyrS/evV0HiN1my/XhpYsHvdD5nMxke/log", methods=["POST"])
def zGkg62XtFY():
    name =request.form.get("piXDgcs")
    password = request.form.get("uRXfGLayOk")
    return r3KGwEgXI1(name , password)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
