# Финальный проект 7 спринта

Тестирование API сервисa [Яндекс Самокат](https://qa-scooter.praktikum-services.ru/docs/#api-Courier-DeleteCourier)

## Проект содержит:
- ### Папка "Tests"
  + test_courier.py
    - тесты возможности создать курьера с использованием разных наборов данных
    - тесты возможности войти в учётную запись созданного курьера с использованием разных наборов данных
    - тесты возможности принять заказ используя учётную запись курьера с разными наборами данных
    - тесты возможности удалить созданную учётную запись курьера с использованием разных наборов данных
  + test_orders.py
    - тесты возможности принять заказ с использованием разных наборов данных
    - тесты возможности создать заказ
    - тесты возможности получить список заказов

- ### Папка "data"
Содержит файл "data.py" со вспомогательными данными

### Файл "helpers.py"
Содержит вспомогательные функции.

### Для создания курьера и получения его учётных данных использовались метод класса и статический метод. После завершения тестирования учётная запись удаляется

- ### Папка "allure_results"
Отчёты о тестировании
