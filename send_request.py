import requests
from config import *
from wr_order import write_order, read_order
import os

def send_post_request(data, url_req=URL_CREATE, url_serv = URL_SERVER):
    if not os.path.exists("order_num"):
        response = requests.post(url_serv + url_req, json=data)
        if response.status_code in (200, 201):
            write_order(response.json())
            return 201, response.json()["track"]
        else:
            # print(response.text)
            return response.status_code, response.text
    else:
        num = read_order()
        return 201, num

def send_get_request(num, url_serv = URL_SERVER, url_req=URL_TRACK):
    response = requests.get(url_serv + url_req + "?t=" + str(num))
    return response.status_code, response.json()
