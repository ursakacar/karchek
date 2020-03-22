import os
import time
import urllib
import sendgrid
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sendgrid.helpers.mail import *

if os.environ.get('SENDGRID_API_KEY') == None:
    raise Exception('SENDGRID_API_KEY not set')

if os.environ.get('CARS_URLS') == None:
    raise Exception('CARS_URLS not set')

if os.environ.get('TO_EMAIL') == None:
    raise Exception('TO_EMAIL not set')

while True:
    cars_urls = os.environ.get('CARS_URLS').split(",")
    new_cars = dict()

    for cars_url in cars_urls:
        all_cars = urllib.urlopen(cars_url).read()
        cars_html = BeautifulSoup(all_cars, 'html.parser')
        car_model = urllib.unquote(cars_url.split("model=")[1].split("&")[0])
        car_make = urllib.unquote(cars_url.split("znamka=")[1].split("&")[0])
        car_name = car_make + " " + car_model

        for link in cars_html.find_all('a', class_="Adlink"):
            is_car_new = False
            car_url = 'https://www.avto.net' + link.get('href')[2:]
            car_url = car_url.split("&")[0]
            car = urllib.urlopen(car_url).read()
            car_html = BeautifulSoup(car, 'html.parser')

            el_date_added = car_html.find('div', class_="OglasContactStatLeftRecap")
            if el_date_added != None:
                date_added = el_date_added.get_text()
                added = datetime.strptime(date_added.split()[2], '%d.%m.%Y')
                yesterday = datetime.now() - timedelta(days=1)

                if added > yesterday:
                    is_car_new = True
            else:
                for image in link.parent.parent.find_all('img'):
                    if image['src'] == "../_graphics/Novo_H_rob.png":
                        is_car_new = True
                        break

            if is_car_new == True:
                if car_name in new_cars:
                    new_cars[car_name].append(car_url)
                    print "added new car to existing model: " + car_name + " , " + car_url
                else:
                    new_cars[car_name] = [car_url]
                    print "added new model: " + car_name + ", " + car_url

    if len(new_cars) > 0:
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        message = "<b>Here is a list of new cars:</b><br>"
        for car_name, new_car_urls in new_cars.items():
            message = message + " " + car_name + ": " + ", ".join(new_car_urls) + "<br>"

        from_email = Email("karchek@karchek.com")
        to_email = Email(os.environ.get('TO_EMAIL'))
        subject = "NEW CAR ALERT"
        content = Content("text/html", message)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    time.sleep(86400)
