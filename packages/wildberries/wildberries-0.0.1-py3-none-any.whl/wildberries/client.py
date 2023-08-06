import json
from typing import List

import requests


class Wildberries(object):
  URL = 'https://suppliers-api.wildberries.ru/'

  def __init__(self, token):
    self.token = token

  def _send_request(self, endpoint, params):
    headers = {
      'content-type': 'application/json',
      "Authorization": self.token
      }
    data = {'id': 1, 'jsonrpc': '2.0', 'params': params}

    response = requests.post(self.URL + endpoint, headers=headers, data=json.dumps(data))
    return response.json()

  def get_cards(self, limit: int, offset: int, total: int):
    """Получить список карточек поставщика с фильтром и сортировкой"""
    params = {'query': {'limit': limit, 'offset': offset, 'total': total}}
    response = self._send_request('card/list', params=params)

    return response['result']

  def get_card_imtId(self, imtId: int):
    """Получение карточки поставщика по imt id"""
    params = {"imtID": imtId}
    response = self._send_request('card/cardByImtID', params=params)

    return response['result']

  def generate_barcode(self, quantity: int) -> List:
    """Позволяет сгенерировать штрих-код для размера"""
    params = {"quantity": quantity}
    response = self._send_request('card/getBarcodes', params=params)

    return response['result']['barcodes']

  def delete_nomenclature(self, nomenclatureID: int):
    """Удаляет одну номенклатуру из карточки товара."""
    params = {"nomenclatureID": nomenclatureID}
    response = self._send_request('card/deleteNomenclature', params=params)

    return response


    
