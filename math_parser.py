from time import sleep
from nodes import *
from stack import Stack


class ParsingError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Parser:

    def __init__(self, operations):
        self.__operations = operations

    def __token_is_digit(self, token):
        points_count = 0
        if not token[0].isdigit():
            return False
        for symbol in token:
            if symbol == ".":
                points_count += 1
            if not symbol.isdigit() and symbol != "." or points_count > 1:
                return False
        return True

    def __token_is_var(self, token):
        return token == "pi" or len(token) == 1 and token.isalpha()

    def __token_is_bin_op(self, token):
        return self.__operations.token_is_bin_op(token)

    def __token_maybe_is_un_op(self, token):
        return self.__operations.token_is_un_op(token)

    def __token_is_un_op(self, token):
        return token.startswith("#u")

    def __token_is_op(self, token):
        return self.__operations.token_is_op(token) or self.__token_is_un_op(token)

    def __token_is_func(self, token):
        return self.__operations.token_is_func(token)

    def __token_is_delimiter(self, token):
        return token == "(" or token == ")" or token == ","

    def __func_args_count(self, func):
        return self.__operations.func_args_count(func)

    def __delete_spaces(self, string):
        string = string.replace(" ", "")
        string = string.replace("\n", "")
        string = string.replace("\f", "")
        string = string.replace("\t", "")
        string = string.replace("\v", "")
        string = string.replace("\r", "")
        return string

    # Разбивка строки на токены
    def __str_to_tokens(self, string):
        if string == "":
            raise ParsingError("Пустая строка")

        string = self.__delete_spaces(string)
        tokens = []
        temp = ""
        for symbol in string:
            if self.__token_is_op(symbol) or self.__token_is_delimiter(symbol):
                if temp != "":
                    tokens.append(temp)

                # Пометка унарного оператора
                if self.__token_maybe_is_un_op(symbol):
                    if len(tokens) == 0:
                        tokens.append("#u{}".format(symbol))
                    else:
                        prev = tokens[len(tokens) - 1]
                        if prev == "(" or self.__token_is_op(prev) or prev == ",":
                            tokens.append("#u{}".format(symbol))
                        else:
                            tokens.append(symbol)

                else:
                    tokens.append(symbol)
                temp = ""
            else:
                temp += symbol
        if temp != "":
            tokens.append(temp)
        return tokens

    # Проверка функции на корректность
    def __check_func(self, tokens, i):
        curr = tokens[i]

        if i + 1 > len(tokens) or tokens[i + 1] != "(":
            raise ParsingError("Отсутствует открывающая скобка после функции")
        else:
            brackets_count = 0
            commas_count = 0
            required_commas_count = self.__func_args_count(curr) - 1

            for j in range(i + 1, len(tokens)):
                if tokens[j] == "(":
                    brackets_count += 1
                elif tokens[j] == ")":
                    brackets_count -= 1
                elif tokens[j] == ",":
                    commas_count += 1
                elif self.__token_is_func(tokens[j]):
                    required_commas_count += self.__func_args_count(tokens[j]) - 1

                if commas_count > required_commas_count:
                    raise ParsingError("Слишком много аргументов в функции")
                if brackets_count == 0:
                    break

            if brackets_count > 0:
                raise ParsingError("Отсутствует закрывающая скобка после аргументов функции")
            if commas_count != required_commas_count:
                raise ParsingError("Слишком мало аргументов в функции")

    # Проверка, что запятая используется корректно и внутри функции
    def __check_comma(self, tokens, i):
        prev = tokens[i - 1]
        if prev != ")" and not self.__token_is_var(prev) and not self.__token_is_digit(prev):
            raise ParsingError("Некорректное использование запятой")
        j = i

        # Количество = -1, так как где-то после запятой должна быть закрывающая скобка, относящаяся к функции
        brackets_count = -1

        while brackets_count != 0:
            if j == 0:
                raise ParsingError("Использование запятой за пределами функции")
            elif tokens[j] == "(":
                brackets_count += 1
            elif tokens[j] == ")":
                brackets_count -= 1
            j -= 1
        if not self.__token_is_func(tokens[j]):
            raise ParsingError("Некорректное использование запятой")

    # Проверка, корректно ли выражение
    def __check_tokens(self, tokens):
        brackets_count = 0
        for i in range(len(tokens)):
            curr = tokens[i]

            if self.__token_is_func(curr):
                self.__check_func(tokens, i)

            if i == 0:
                if self.__token_is_bin_op(curr):
                    raise ParsingError("Пропущен первый аргумент у бинарного оператора")

                elif curr == "(":
                    brackets_count += 1

                elif curr == ")":
                    raise ParsingError("Закрывающая скобка в начале выражения")
            else:
                if i == len(tokens) - 1:
                    if self.__token_is_bin_op(curr):
                        raise ParsingError("Пропущен второй аргумент у бинарного оператора")
                    elif self.__token_is_un_op(curr):
                        raise ParsingError("Пропущен аргумент у унарного оператора")
                    elif curr == ",":
                        raise ParsingError("Отсутствует аргумент после запятой")
                    elif curr == "(":
                        raise ParsingError("Открывающая скобка в конце выражения")

                prev = tokens[i - 1]

                if self.__token_is_var(curr):
                    if prev == ")":
                        raise ParsingError("Переменная сразу после закрывающей скобки")

                elif self.__token_is_digit(curr):
                    if prev == ")":
                        raise ParsingError("Число сразу после закрывающей скобки")

                elif self.__token_is_bin_op(curr):
                    if self.__token_is_bin_op(prev):
                        raise ParsingError("Пропущен второй аргумент у бинарного оператора")
                    elif prev == "(" or prev == ",":
                        raise ParsingError("Пропущен первый аргумент у бинарного оператора")

                elif self.__token_is_func(curr):
                    if prev == ")":
                        raise ParsingError("Функция сразу после закрывающей скобки")
                    elif self.__token_is_var(prev):
                        raise ParsingError("Функция сразу после переменной")
                    elif self.__token_is_digit(prev):
                        raise ParsingError("Функция сразу после числа")

                elif curr == "(":
                    if self.__token_is_var(prev):
                        raise ParsingError("Открывающая скобка сразу после переменной")
                    elif self.__token_is_digit(prev):
                        raise ParsingError("Открывающая скобка сразу после числа")
                    elif prev == ")":
                        raise ParsingError("Открывающая скобка сразу после закрывающей")
                    return brackets_count + 1

                elif curr == ")":
                    if self.__token_is_bin_op(prev):
                        raise ParsingError("Пропущен второй аргумент у бинарного оператора")
                    elif self.__token_is_un_op(prev):
                        raise ParsingError("Пропущен аргумент у унарного оператора")
                    elif prev == "(":
                        raise ParsingError("Пустые скобки")
                    return brackets_count - 1

                elif curr == ",":
                    self.__check_comma(tokens, i)

                elif self.__token_maybe_is_un_op(curr):
                    raise ParsingError("Некорректное применение унарного оператора")

                elif not self.__token_is_un_op(curr):
                    raise ParsingError("Некорректная последовательность символов")

        if brackets_count != 0:
            raise ParsingError("В выражении не согласованы скобки")

    # Переписать выражение справа налево
    def __reverse_tokens(self, tokens):
        res = []
        for i in range(len(tokens) - 1, -1, -1):
            if tokens[i] == "(":
                res.append(")")
            elif tokens[i] == ")":
                res.append("(")
            else:
                res.append(tokens[i])
        return res

    def __prior(self, token):
        if self.__token_is_bin_op(token):
            return self.__operations.bin_op_prior(token)
        elif self.__token_is_un_op(token):
            return 2
        else:
            return 1

    # Преобразование из инфиксной формы в постфиксную при помощи алгоритма сортировочной станции
    def __infix_to_postfix(self, tokens):
        res = []
        stack = Stack()
        for token in tokens:
            if self.__token_is_digit(token) or self.__token_is_var(token):
                res.append(token)

            elif token == "(":
                stack.push(token)

            elif token == ")":
                while stack.peek() != "(":
                    res.append(stack.pop())
                stack.pop()
                if not stack.is_empty() and self.__token_is_func(stack.peek()):
                    res.append(stack.pop())

            elif token == ",":
                while stack.peek() != "(":
                    res.append(stack.pop())

            else:
                while not stack.is_empty() and \
                        (self.__token_is_op(stack.peek()) or self.__token_is_func(stack.peek())) and \
                        self.__prior(stack.peek()) < self.__prior(token):
                    res.append(stack.pop())

                stack.push(token)

        while not stack.is_empty():
            res.append(stack.pop())

        return res

    # Преобразование из инфиксной формы записи в префиксную
    def __infix_to_prefix(self, tokens):
        tokens = self.__reverse_tokens(tokens)
        tokens = self.__infix_to_postfix(tokens)
        return self.__reverse_tokens(tokens)

    # Создание узла из выражения в префиксной форме записи
    def __prefix_to_node(self, tokens, index):
        token = tokens[index]
        if self.__token_is_digit(token) or self.__token_is_var(token):
            return ArgNode(token), index + 1

        elif self.__token_is_un_op(token):
            index += 1
            arg, index = self.__prefix_to_node(tokens, index)
            token = token[2:]
            return UnOpNode(token, arg, self.__operations), index

        elif self.__token_is_bin_op(token):
            index += 1
            f_arg, index = self.__prefix_to_node(tokens, index)
            s_arg, index = self.__prefix_to_node(tokens, index)
            return BinOpNode(token, f_arg, s_arg, self.__operations), index

        else:
            args = []
            index += 1
            for i in range(self.__func_args_count(token)):
                node, index = self.__prefix_to_node(tokens, index)
                args.append(node)
            return FuncNode(token, args, self.__operations), index

    # Создание узла из строки с выражением
    def str_to_node(self, string):
        tokens = self.__str_to_tokens(string)
        self.__check_tokens(tokens)
        tokens = self.__infix_to_prefix(tokens)
        return self.__prefix_to_node(tokens, 0)[0]
