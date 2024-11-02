'''Модуль со вспомогательными функциями'''


def wait_for_input():
    '''Создаёт задержку, чтобы пользователь успел прочитать текст выше
    '''
    input('Нажмите Enter чтобы продолжить...')


def required_input(input_text, var_type=str, **kwargs):
    '''Обязательный для ввода input с расширенными опциями

    Args:
        input_text (str): Текст, который видит пользователь
        var_type (type, optional): Тип, который будет иметь значение функции.
        По умолчанию str.

    Returns:
        any: значение, введенное пользователем
    '''
    result = None
    value_range = kwargs.get('value_range')
    should_run = True

    while should_run:
        try:
            result = var_type(input(input_text))
            if var_type == str and result.strip() == '':
                should_run = True
            elif var_type in (int, float) and value_range:
                start = value_range[0]
                end = value_range[1]
                should_run = not start <= result <= end
            else:
                should_run = False
        except ValueError:
            pass

    return result
