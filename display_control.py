#!/usr/bin/env python

import unicornhathd
import colorsys
import time
from sys import exit
import requests
import json
import datetime
from dateutil.parser import parse
import dateutil
from PIL import Image, ImageDraw, ImageFont #sudo pip install pillow


def update_pixels(w, h, img):
    for x in range(w):
            for y in range(h):
                pixel = img.getpixel((x, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(w - x-1, y, r, g, b)


def draw_text(text, placement, color, font_size):
    width, height = unicornhathd.get_shape()

    if len(text) == 1 or len(text) == 2:
        FONT = ('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)
        font_file, size = FONT
        font = ImageFont.truetype(font_file, font_size)

        image = Image.new('RGB', (width,height), (0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text(placement, text[0], color, font=font)

        if len(text)==2:
            draw.text((placement[0], placement[1] + int(height/len(text))), text[1], color, font=font)

        update_pixels(width, height, image)
        unicornhathd.show()


tag_id = '3456'
cities = {"Helsinki":"HKI", "Turku":"TKU", "Kotka":"KOT", "Oulu":"OUL", "Pori":"POR", "Haima":"HAM"}
light_blue = (0, 255, 255)
time_text_color = (0, 255, 255)
unicornhathd.rotation(90)
unicornhathd.brightness(0.7)
url = 'http://?.?.?.?:?'
failed_request_count = 0

try:
    tag_response = requests.get(url + "/api/tag/" + tag_id)
    tag_data = json.loads(tag_response.text)[0]

    tag_routes = []
    for route_id in tag_data["routes"]:
        tag_routes.append(route_id['$oid'])
    
    for route in tag_routes:
        route_response = requests.get(url + "/api/route/" + route)
        route_data = json.loads(route_response.text)
        if route_data['tour_status'] == 'ONGOING':
            ongoing_route = route_data
            ongoing_route_url = url + "/api/route/" + route
            
    origin = ongoing_route["origin"]
    destination = ongoing_route["destination"]
    arrival_time = ongoing_route["arrival_time"]

    while route_response:
        # TAG ID TEXT
        draw_text([tag_id], (0,0), light_blue, 14)
        time.sleep(3)

        # ORIGIN AND DESTINATION TEXT
        origin_destination_text = [cities[origin], cities[destination]]
        draw_text(origin_destination_text, (0,0), light_blue, 8)
        time.sleep(3)

        # REMAINING TIME TEXT
        arrival = parse(arrival_time)
        tz_info = arrival.tzinfo
        timediff = arrival - datetime.datetime.now(tz_info)
        hours, minutes = timediff.seconds // 3600, timediff.seconds // 60 % 60

        hours_text = str(hours) + " h" 
        minutes_text = str(minutes) + " m" 
        draw_text([hours_text, minutes_text], (0,0), time_text_color, 8)
        time.sleep(3)

        if failed_request_count >= 1:
            time_text_color = (255,0,0)
       
        route_response = requests.get(ongoing_route_url)

        if route_response.status_code == 200:
            failed_request_count = 0
            ongoing_route = json.loads(route_response.text)
            origin = ongoing_route["origin"]
            destination = ongoing_route["destination"]
            
        elif route_response.status_code != 304:
            failed_request_count+=1


except Exception as e:
    unicornhathd.off()

finally:
    unicornhathd.off()
