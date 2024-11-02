'''База данных'''
from helpers import required_input, wait_for_input


def get_product_type():
    '''Выводит типы товаров и считывает пользовательский тип с клавиатуры

    Returns:
        int: Тип товара
    '''
    print('Типы товаров:')
    for idx, item in enumerate(PRODUCT_TYPES, start=1):
        print(f'{idx}) {item}')
    return required_input('Выберите тип товара: ', int,
                          value_range=(1, len(PRODUCT_TYPES))) - 1


def print_products(data):
    '''Выводит товары на экран

    Args:
        data (list): Список товаров
    '''
    if data:
        for item in data:
            print(
                '--------------------',
                f'Продукт №{item['id']}',
                f'Название: {item['title']}',
                f'Тип: {PRODUCT_TYPES[item['type']]}',
                f'Цена: {item['price']} рублей',
                f'В наличии: {item['quantity']}',
                '--------------------', sep='\n'
            )
    else:
        print('Не найдено ни одного товара!')

    wait_for_input()


def sort_products(data):
    '''Сортирует товары и выводит их на экран

    Args:
        data (list): Список товаров
    '''
    sort_keys = ['quantity', 'price']

    print('Типы сортировок:',
          '1) По количеству',
          '2) По цене', sep='\n')
    choice = required_input('Выберите действие: ', int, value_range=(1, 2))
    print('Типы сортировок: ',
          '1) по возрастанию',
          '2) по убыванию', sep='\n')
    asc = bool(required_input(
            'Выберите тип сортировки: ', int,
            value_range=(1, 2)) - 1)

    sort_key = sort_keys[choice - 1]
    sorted_products = sorted(data, key=lambda product: product[sort_key],
                             reverse=asc)
    print_products(sorted_products)


def calculate_summary(data):
    '''Вычисляет количество и суммарную стоимость товаров определенного типа
    и выводит их на экран

    Args:
        data (list): Список товаров
    '''
    choice = get_product_type()
    matching_products = [item for item in data if item['type'] == choice]
    product_quantities = [item['quantity'] for item in matching_products]
    product_prices = [item['price'] for item in matching_products]
    prices_sum = sum(product_quantities[i] * product_prices[i]
                     for i in range(len(matching_products)))
    quantities_sum = sum(product_quantities)
    print(
        f'Найдено товаров заданного типа: {quantities_sum}',
        f'Суммарная стоимость товаров: {round(prices_sum, 3)} рублей',
        sep='\n'
    )

    wait_for_input()


def search(data):
    '''Считывает поисковый запрос товара от пользователя, находит товары
    и выводит их на экран

    Args:
        data (list): Список товаров
    '''
    query = required_input('Введите название: ').lower().split()
    result = []

    for item in data:
        item_title = item['title'].lower().split()
        # Проверка на наличие хотя бы одного общего слова
        if bool(set(query) & set(item_title)):
            result.append(item)
    print(f'Найдено товаров: {len(result)}')
    print_products(result)


def add_new_product(data):
    '''Запрашивает инфорацию о создаваемом товаре от пользователя
    и создает его

    Args:
        data (list): Список товаров
    '''
    product_id = data[-1]['id'] + 1 if data else 1
    product_title = required_input('Введите название товара: ')
    product_type = get_product_type()
    product_price = required_input('Введите цену товара: ', float,
                                   value_range=(1, 100000))
    product_quantity = required_input('Введите количество товара: ', int,
                                      value_range=(0, 10**10))

    new_product = {
        'id': product_id,
        'title': product_title,
        'type': product_type,
        'price': product_price,
        'quantity': product_quantity
    }
    data.append(new_product)
    print(f'Товар "{product_title}" успешно добавлен!')

    wait_for_input()


def delete_product(data):
    '''Запрашивает от пользователя id удаляемого товара и удаляет
    его, если товар существует

    Args:
        data (list): Список товаров
    '''
    delete_id = required_input('Введите номер удаляемого товара: ', int)
    delete_item = [item for item in data if item['id'] == delete_id]

    if delete_item:
        for idx, item in enumerate(data):
            if item['id'] == delete_id:
                del data[idx]
                print(f'Товар "{item['title']}" успешно удален!')
    else:
        print(f'Товар с номером {delete_id} не найден!')

    wait_for_input()


def main(data):
    '''Главная функция программа, которая зацикливает ее выполнение

    Args:
        data (list): Список товаров

    Returns:
        bool: Возвращает булево выражение, определяющее будет ли
        программа запущена еще раз
    '''

    print('База данных')
    print('1) Вывести данные',
          '2) Сортировать',
          '3) Вычислить суммарное количество и стоимость',
          '4) Найти',
          '5) Добавить',
          '6) Удалить',
          '7) Выйти', sep='\n')
    choice = required_input('Выберите действие: ', int, value_range=(1, 7))

    if choice == 7:
        return False
    command = db_commands[choice - 1]
    command(data)
    return True


PRODUCT_TYPES = ('напитки', 'полуфабрикаты', 'консервы')

is_running = True  # pylint: disable=invalid-name
db_commands = (
    print_products, sort_products,
    calculate_summary, search, add_new_product, delete_product
)
products = []

while is_running:
    is_running = main(products)  # pylint: disable=invalid-name
