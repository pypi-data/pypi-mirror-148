"""Цены

POST /public​/api​/v1​/prices
Загрузка цен. За раз можно загрузить не более 1000 номенклатур.


GET /public​/api​/v1​/info
Получение информации по номенклатурам, их ценам, скидкам и промокодам. Если не указывать фильтры, вернётся весь товар."""
"""
Промокоды и скидки

POST /public​/api​/v1​/updateDiscounts
Установка скидок для номенклатур. Максимальное количество номенклатур на запрос - 1000

POST /public​/api​/v1​/revokeDiscounts
Сброс скидок для номенклатур

POST /public​/api​/v1​/updatePromocodes
Установка промокодов для номенклатур. Максимальное количество номенклатур на запрос - 1000

POST /public​/api​/v1​/revokePromocodes
Сброс промокодов для номенклатур
"""

"""
Marketplace

GET /api​/v2​/supplies
Возвращает список поставок

POST /api​/v2​/supplies
Создаёт новую поставку

PUT /api​/v2​/supplies​/{id}
Добавляет к поставке заказы

POST /api​/v2​/supplies​/{id}​/close
Закрывает поставку

GET /api​/v2​/supplies​/{id}​/barcode
Возвращает штрихкод поставки в заданном формате

GET /api​/v2​/supplies​/{id}​/orders
Возвращает список заказов, закреплённых за поставкой

GET ​/api​/v2​/stocks
Возвращает список товаров поставщика с их остатками

POST /api​/v2​/stocks
Обновляет остатки товаров

DELETE /api​/v2​/stocks
Удаляет остатки товаров

GET /api​/v2​/warehouses
Возвращает список складов поставщика

GET /api​/v2​/orders
Возвращает список сборочных заданий поставщика.

PUT ​/api​/v2​/orders
Обновляет статус переданных сборочных заданий.

POST /api​/v2​/orders​/stickers
Возвращает список стикеров по переданному массиву сборочных заданий.

POST /api​/v2​/orders​/stickers​/pdf
Возвращает список стикеров в формате pdf по переданному массиву сборочных заданий.
"""

"""
Card

POST /card​/batchCreate
Создание группы карточек

POST /card​/cardByImtID
Получение карточки поставщика по imt id

POST /card​/create
Создание одной карточки

POST /card​/deleteNomenclature
Удалить номенклатуру из карточки

GET ​/card​/file​/{supplierID}​/{fileID}
Выгрузить файл из хранилища

POST /card​/getBarcodes
Сгенерировать шк

POST /card​/list
Получить список карточек поставщика с фильтром и сортировкой

POST /card​/update
Обновить карточку

POST /card​/upload​/file​/multipart
Загрузить файл в хранилище
"""

"""
Конфигуратор полей карточки

GET /api​/v1​/config​/get​/object​/translated
Получение конфигурации предмета

GET /api​/v1​/config​/get​/object​/list
Поиск предмета по паттерну

GET /api​/v1​/directory​/colors
Справочник основных и дополнительных цветов

GET /api​/v1​/directory​/kinds
Справочник пол

GET /api​/v1​/directory​/countries
Справочник стран

GET /api​/v1​/directory​/collections
Справочник коллекций

GET /api​/v1​/directory​/seasons
Справочник сезонов

GET /api​/v1​/directory​/contents
Справочник комплектации

GET /api​/v1​/directory​/consists
Справочник составов

GET /api​/v1​/directory​/tnved
Справочник тнвэд

GET /api​/v1​/directory​/options
Справочник дополнительных свойств

GET /api​/v1​/directory​/brands
Справочник брендов

GET /api​/v1​/directory​/si
Справочник систем измерений

GET /api​/v1​/directory​/ext
Справочник значений для дополнительных свойств

GET /api​/v1​/directory​/wbsizes
Справочник российских размеров

GET /api​/v1​/directory​/get​/list
Все доступные справочники

GET /api​/v1​/config​/get​/object​/all
Все доступные предметы

GET /api​/v1​/config​/get​/object​/parent​/list
Все паренты

GET /api​/v1​/config​/object​/byparent
Получение списка объектов по паренту

"""

