from math_parser import Parser
from operations import Operations


class DiffTree:

    def __init__(self, file, head = None):
        self.__file = file
        self.__operations = Operations(self.__file)
        self.__parser = Parser(self.__operations)
        self.__head = head

    def __str__(self):
        return str(self.__head)

    # Сформировать дерево из строки
    def from_str(self, string):
        self.__head = self.__parser.str_to_node(string)

    # Взять производную
    def diff(self, var):
        try:
            return DiffTree(self.__file, self.__head.diff(var))
        except RecursionError:
            raise RecursionError("Бесконечная рекурсия. Скорее всего производная какой-то операции"
                                 "определена через производную этой же операции.")
