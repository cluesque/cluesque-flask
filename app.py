"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import pywapi
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/walk/')
def hello_world():
    points = 0
    end = 0

    days = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    weather_com_result = pywapi.get_weather_from_weather_com('USMA0011')

    temp = weather_com_result['forecasts'][1]['high']
    forecast = weather_com_result['forecasts'][1]['day']
    weather = forecast['text']
    precip = int(forecast['chance_precip'])
    wind = forecast['wind']
    wind_speed = wind['speed']

    temp = int(temp) * 1.8 + 32
    wind = round(int(wind_speed) * 0.6214, 0)
    if temp > 31:
        if temp < 86:
            points = points + round(float(temp)/16, 1)
    if "Sunny" in weather:
        if "Mostly Sunny" == weather:
            points = points + 1
        else:
            points = points + 0.5
    if "Cloudy" in weather:
        if "Mostly Cloudy" == weather:
            points = points + 1
        else:
            points = points + 0.5
    else:
        points = points + 0

    if precip <= 20:
        points = points + 5
    elif precip >= 80:
        end = end + 1
    else:
        predec = 1./(float(precip) / 100)
        points = points + float(Decimal(predec))
    if wind <= 20:
        points = points + 3
    else:
        points = points + 3 - ((wind - 15)/15) * 3
    if end >= 1:
        return "you should not walk!"
    else:
        if points > 6:
            return "you should walk!"
        elif points < 8:
            return "you should not walk!"
        else:
           return "you could walk, but you dont really have to. your choice!"


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
