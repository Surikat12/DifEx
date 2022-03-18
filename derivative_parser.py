from nodes import *
from stack import Stack


class DerivativeConvertingError(Exception):
    def __init__(self, message, line):
        super().__init__("{} (строка {})".format(message, line))


class Parser:

    def __init__(self, operations, line=0):
        self.__operations = operations
        self.line = line

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
        return token == "pi" or (len(token) == 1 and token.isalpha()) or token == "#v" or \
               (len(token) >= 2 and token.startswith("#") and token[1:].isdigit())

    def __token_is_bin_op(self, token):
        return self.__operations.token_is_bin_op(token)

    def __token_maybe_is_un_op(self, token):
        return self.__operations.token_is_un_op(token)

    def __token_is_un_op(self, token):
        return token.startswith("#u")

    def __token_is_op(self, token):
        return self.__operations.token_is_op(token)

    def __token_is_func(self, token):
        return token == "#d" or self.__operations.token_is_func(token)

    def __token_is_delimiter(self, token):
        return token == "(" or token == ")" or token == ","

    def __func_args_count(self, func):
        if func == "#d":
            return 2
        return self.__operations.func_args_count(func)

    # Разбивка строки на токены
    def __str_to_tokens(self, string):
        if string == "":
            raise DerivativeConvertingError("Пустая строка", self.line)

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
            raise DerivativeConvertingError("Отсутствует открывающая скобка после функции", self.line)
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
                    raise DerivativeConvertingError("Слишком много аргументов в функции", self.line)
                if brackets_count == 0:
                    break

            if brackets_count > 0:
                raise DerivativeConvertingError("Отсутствует закрывающая скобка после аргументов функции", self.line)
            if commas_count != required_commas_count:
                raise DerivativeConvertingError("Слишком мало аргументов в функции", self.line)

    # Проверка, что запятая используется корректно и внутри функции
    def __check_comma(self, tokens, i):
        prev = tokens[i - 1]
        if prev != ")" and not self.__token_is_var(prev) and not self.__token_is_digit(prev):
            raise DerivativeConvertingError("Некорректное использование запятой", self.line)
        j = i

        # Количество = -1, так как где-то после запятой должна быть закрывающая скобка, относящаяся к функции
        brackets_count = -1

        while brackets_count != 0:
            if j == 0:
                raise DerivativeConvertingError("Использование запятой за пределами функции", self.line)
            elif tokens[j] == "(":
                brackets_count += 1
            elif tokens[j] == ")":
                brackets_count -= 1
            j -= 1
        if not self.__token_is_func(tokens[j]):
            raise DerivativeConvertingError("Некорректное использование запятой", self.line)

    # Проверка, корректно ли выражение
    def __check_tokens(self, tokens, args_count):
        brackets_count = 0
        for i in range(len(tokens)):
            curr = tokens[i]

            if self.__token_is_func(curr):
                self.__check_func(tokens, i)

            if i == 0:
                if self.__token_is_bin_op(curr):
                    raise DerivativeConvertingError("Пропущен первый аргумент у бинарного оператора", self.line)

                elif curr == "(":
                    brackets_count += 1

                elif curr == ")":
                    raise DerivativeConvertingError("Закрывающая скобка в начале выражения", self.line)
            else:
                if i == len(tokens) - 1:
                    if self.__token_is_bin_op(curr):
                        raise DerivativeConvertingError("Пропущен второй аргумент у бинарного оператора", self.line)
                    elif self.__token_is_un_op(curr):
                        raise DerivativeConvertingError("Пропущен аргумент у унарного оператора", self.line)
                    elif curr == ",":
                        raise DerivativeConvertingError("Отсутствует аргумент после запятой", self.line)
                    elif curr == "(":
                        raise DerivativeConvertingError("Открывающая скобка в конце выражения", self.line)

                prev = tokens[i - 1]

                if self.__token_is_var(curr):
                    if prev == ")":
                        raise DerivativeConvertingError("Переменная сразу после закрывающей скобки", self.line)
                    if curr != "#v" and curr.startswith("#") and int(curr[1:]) >= args_count:
                        raise DerivativeConvertingError("В операции отсутствует аргумент с заданным номером", self.line)

                elif self.__token_is_digit(curr):
                    if prev == ")":
                        raise DerivativeConvertingError("Число сразу после закрывающей скобки", self.line)

                elif self.__token_is_bin_op(curr):
                    if self.__token_is_bin_op(prev):
                        raise DerivativeConvertingError("Пропущен второй аргумент у бинарного оператора", self.line)
                    elif prev == "(" or prev == ",":
                        raise DerivativeConvertingError("Пропущен первый аргумент у бинарного оператора", self.line)

                elif self.__token_is_func(curr):
                    if prev == ")":
                        raise DerivativeConvertingError("Функция сразу после закрывающей скобки", self.line)
                    elif self.__token_is_var(prev):
                        raise DerivativeConvertingError("Функция сразу после переменной", self.line)
                    elif self.__token_is_digit(prev):
                        raise DerivativeConvertingError("Функция сразу после числа", self.line)

                elif curr == "(":
                    if self.__token_is_var(prev):
                        raise DerivativeConvertingError("Открывающая скобка сразу после переменной", self.line)
                    elif self.__token_is_digit(prev):
                        raise DerivativeConvertingError("Открывающая скобка сразу после числа", self.line)
                    elif prev == ")":
                        raise DerivativeConvertingError("Открывающая скобка сразу после закрывающей", self.line)
                    brackets_count += 1

                elif curr == ")":
                    if self.__token_is_bin_op(prev):
                        raise DerivativeConvertingError("Пропущен второй аргумент у бинарного оператора", self.line)
                    elif self.__token_is_un_op(prev):
                        raise DerivativeConvertingError("Пропущен аргумент у унарного оператора", self.line)
                    elif prev == "(":
                        raise DerivativeConvertingError("Пустые скобки", self.line)
                    brackets_count -= 1

                elif curr == ",":
                    self.__check_comma(tokens, i)

                elif self.__token_maybe_is_un_op(curr):
                    raise DerivativeConvertingError("Некорректное применение унарного оператора", self.line)

                elif not self.__token_is_un_op(curr):
                    raise DerivativeConvertingError("Некорректная последовательность символов", self.line)

        if brackets_count != 0:
            raise DerivativeConvertingError("В выражении не согласованы скобки", self.line)

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
            if token == "#d" and (type(args[1]) != ArgNode or
                                  args[1].name == "pi" or args[1].name == "e" or args[1].name.isdigit()):
                raise DerivativeConvertingError("Попытка взять производную не по переменной", self.line)
            return FuncNode(token, args, self.__operations), index

    # Создание узла из строки с производной
    def derivative_to_node(self, derivative, args_count):
        tokens = self.__str_to_tokens(derivative)
        self.__check_tokens(tokens, args_count)
        tokens = self.__infix_to_prefix(tokens)
        return self.__prefix_to_node(tokens, 0)[0]
