# Наталья Буданова, 4-я когорта — Финальный проект. 
# Инженер по тестированию плюс

import pytest
from wr_order import write_order, read_order
from configuration import *
from send_request import send_get_request, send_post_request

@pytest.fixture()
def create_order():
    """Устанавливаем стартовые условия, - сначал нужно создать заказ и 
    сохранить его номер для удобства в файле"""
    stat_create, num_track = send_post_request(JSON_ORDER)
    return num_track

def test_return_orders_by_number_good(create_order):
    """Отправляем запрос на просмотр заказа по номеру и сверяем статус-код и данные заказа\n
    Статус 200, данные совпадают с отправленным ранее запросом, все поля присутствуют
    """
    status, body = send_get_request(create_order)
    assert status == 200
    date = JSON_ORDER.pop("deliveryDate") # Дата хранится в формате 2020-06-06T00:00:00.000Z
    # поэтому сверим её отдельно
    for key in JSON_ORDER.keys():
        assert str(body["order"][key]) == str(JSON_ORDER[key]) # Числа хранятся где-то в виде строк а где-то в виде чисел
    assert date == body["order"]["deliveryDate"][:10]
    # Проверяем наличие полей в ответе
    assert "id" in body["order"]
    assert "status" in body["order"]
    assert "cancelled" in body["order"]
    assert "finished" in body["order"]
    assert "inDelivery" in body["order"]
    # assert "courierFirstName" in body["order"] # У нас нет курьеров и они еще не приняли наш заказ
    assert "createdAt" in body["order"]
    assert "updatedAt" in body["order"]
    
def test_return_orders_empty_number_wrong ():
    """Отправляем запрос на просмотр заказа по пустому номеру и сверяем статус-код и сообщение\n
    Статус 400, сообщение "Недостаточно данных для поиска"
    """
    status, body = send_get_request("")
    assert status == 400
    assert "message" in body
    assert body["message"] == "Недостаточно данных для поиска"

def test_return_orders_non_existent_number_wrong ():
    """Отправляем запрос на просмотр заказа по несуществующему номеру и сверяем статус-код и сообщение\n
    Статус 404, сообщение "Заказ не найден"
    """
    status, body = send_get_request(999999)
    assert status == 404
    assert "message" in body
    assert body["message"] == "Заказ не найден"

def test_return_orders_not_number_wrong ():
    """Отправляем запрос на просмотр заказа по некорректному номеру и сверяем статус-код\n
    Статус 500
    """
    status, body = send_get_request("str")
    assert status == 500

