# -*- coding: utf-8 -*-
import os
import csv


# import json


class PriceMachine:

    def __init__(self):
        self.data = []
        # self.result = ''
        # self.name_length = 0

    def load_prices(self, file_path=''):
        """
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        """
        #  Загружает данные из CSV-файлов, обрабатывает их и сохраняет в self.data.
        if not file_path:
            file_path = os.getcwd()
        files = [file for file in os.listdir(file_path) if 'price' in file]
        for file in files:
            with open(os.path.join(file_path, file), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=',')
                headers = reader.fieldnames
                product_col, price_col, weight_col = self._search_product_price_weight(headers)
                for row in reader:
                    product = row[product_col]
                    price = float(row[price_col])
                    weight = float(row[weight_col])
                    price_per_kg = price / weight if weight > 0 else 0
                    self.data.append({
                        'product': product,
                        'price': price,
                        'weight': weight,
                        'file': file,
                        'price_per_kg': price_per_kg
                    })

    def _search_product_price_weight(self, headers):
        """
            Возвращает номера столбцов
        """
        #  Возвращает названия столбцов для товара, цены и веса.
        product_col = next(col for col in headers if col in ['товар', 'название', 'наименование', 'продукт'])
        price_col = next(col for col in headers if col in ['цена', 'розница'])
        weight_col = next(col for col in headers if col in ['фасовка', 'масса', 'вес'])
        return product_col, price_col, weight_col

    def export_to_html(self, fname='output.html'):
        #  Генерирует HTML-таблицу с данными о товарах.
        result = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table border="1">
                        <tr>
                            <th>Номер</th>
                            <th>Название</th>
                            <th>Цена</th>
                            <th>Фасовка</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                '''
        for idx, item in enumerate(sorted(self.data, key=lambda x: x['price_per_kg'])):
            result += f'''
                        <tr>
                            <td>{idx + 1}</td>
                            <td>{item['product']}</td>
                            <td>{item['price']}</td>
                            <td>{item['weight']}</td>
                            <td>{item['file']}</td>
                            <td>{item['price_per_kg']:.2f}</td>
                        </tr>
                    '''
        result += '''
                    </table>
                </body>
                </html>
                '''
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def find_text(self, text):
        # Позволяет искать товары по фрагменту названия и возвращает отсортированный список.
        results = [item for item in self.data if text.lower() in item['product'].lower()]
        return sorted(results, key=lambda x: x['price_per_kg'])


# Работа программы
pm = PriceMachine()
# print(pm.load_prices())
pm.load_prices(file_path='pricelists')  # Укажите путь к папке с прайсами

'''
    Логика работы программы
'''

# Интерфейс для поиска
# Реализован цикл для ввода текста поиска и вывода результатов.
while True:
    search_text = input("Введите текст для поиска (или 'exit' для выхода): ")
    if search_text.lower() == 'exit':
        print("Работа завершена.")
        break
    results = pm.find_text(search_text)
    if results:
        print(f"№ - Наименование - Цена - Вес - Имя файла - Цена за кг")
        for idx, item in enumerate(results):
            print(f"{idx + 1}. {item['product']} - {item['price']} - {item['weight']} - {item['file']} - "
                  f"{item['price_per_kg']:.2f}")
    else:
        print("Товары не найдены.")

# print('the end')
# Экспорт данных в HTML
print('Загрузка завершена.')
# print(pm.export_to_html())
pm.export_to_html()
print('Данные экспортированы в HTML.')
