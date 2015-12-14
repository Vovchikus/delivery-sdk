Компонент (далее - SDK) для демонстрации интеграции с API сервисом Яндекс.Доставка (документация по API http://docs.yandexdelivery.apiary.io/) с использванием Python 2.7и Flask.

Настройка компонента:
1. sudo apt-get install python

2. sudo apt-get install python-pip (Python package manager)

3. sudo pip install virtualenv (виртуальное окружение для работы SDK)

4. install Flask (python lighweight web-framework, http://flask.pocoo.org/docs/0.10/installation/)

5. install Flask-WTForms http://flask-wtf.readthedocs.org/en/latest/install.html - sudo pip install flask-wtf (компонент для работы с формами)

6. sudo pip install flask-bootstrap (компонент для работы с Twitter Bootstrap)

Настройка подключения SDK к Яндекс Доставке.
1. На странице Интеграции в ЛК Я.Доставки необходимо скопировать API ключи и данные с личными идентификаторами

[
getPaymentMethods: ...
getSenderOrders: ...
getSenderOrderLabel: ...
...
]

["client_id":...,"sender_ids":["..."],"warehouse_ids":["..."],"requisite_ids":["..."]]

и преобразовать в формат json для корректной работы с SDK

{
  "getPaymentMethods": "...",
  "getSenderOrders": "...",
  "getSenderOrderLabel": "...",
  ...
}

{"client_id":...,"sender_ids":["..."],"warehouse_ids":["..."],"requisite_ids":["..."]}

2. Запускаем SDK в виртуальном окуржении выполнив python run.py в корне проекта (* Running on http://127.0.0.1:5000/ ); 
открываем в браузере страницу с адресом http://127.0.0.1:5000 и переходим на страницу http://127.0.0.1:5000/init ;
в поле Method Keys вставляем API ключи в формате json, а в поле Resource Settings - данные с личными идентификаторами в формате json;
SDK готово к работе.

3. На странице http://127.0.0.1:5000/createOrder доступно: 
- поиск доступных вариантов доставки (searchDeliveryList) 
- создание заказа (createOrder)
- автодополнение города, улицы, дома (autocomplete)
   На странице http://127.0.0.1:5000/confirmSenderOrders доступно:
- получение списка заказов клиента (getSenderOrders)
