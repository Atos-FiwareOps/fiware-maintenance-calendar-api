from flask import Flask

app = Flask(__name__)

#This import allows the gunicorn to see the views
#uncomment next row, if you want to use gunicorn application such as production environments
#import maintenance_calendar.views
