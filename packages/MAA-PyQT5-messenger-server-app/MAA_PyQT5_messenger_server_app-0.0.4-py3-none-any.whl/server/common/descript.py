import logging




logger = logging.getLogger('server_dist')


class Port:
    '''
    Дескриптор проверяющий корректность значения порта
    '''
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска сервера с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        # Если порт прошёл проверку, добавляем его в список атрибутов экземпляра
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name

class Address:
    def __set__(self, instance, value):
        if value != '':
            logger.critical(
                f'Попытка запуска сервера с указанием неправильного формата адреса {value}.')
            exit(1)
        # Если адрес прошёл проверку, добавляем его в список атрибутов экземпляра
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name