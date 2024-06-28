from flask import Flask, render_template ,request


app = Flask(__name__)

def admin():
   if request.method == "GET":
       return render_template("/admin/login.html")

