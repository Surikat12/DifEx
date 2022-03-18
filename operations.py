from derivative_parser import Parser


# Класс для хранения информации об операциях
class Operations:

    def __init__(self, file):
        self.__file = file
        self.__un_ops = {}
        self.__bin_ops = {}
        self.__funcs = {}
        self.__from_file()

    # Заполнить поля информацией из файла
    def __from_file(self):
        self.__read_from_file()
        self.__convert_derivatives()

    # Считать информацию из файла
    def __read_from_file(self):
        try:
            f = open(self.__file, "r")
        except IOError:
            raise IOError("Не удалось открыть файл {}".format(self.__file))
        lines = f.read().split("\n")
        f.close()

        for i in range(len(lines)):
            line = self.__delete_spaces(lines[i])

            if line.startswith("unary_operator("):
                self.__un_op_from_line(line, i + 1)

            elif line.startswith("binary_operator("):
                self.__bin_op_from_line(line, i + 1)

            elif line.startswith("function("):
                self.__func_from_line(line, i + 1)

            elif line != "":
                raise IOError("Строка {} некорректна".format(i + 1))

    # Считать строку с унарным оператором
    def __un_op_from_line(self, line, line_number):
        error_message = "Некорректное определение унарного оператора (строка {})".format(line_number)
        name, index = self.__next_arg(line, 15, error_message)

        if len(name) != 1:
            raise IOError("Имя унарного оператора должно состоять из одного символа (строка {})".format(line_number))
        if name.isdigit() or name.isdigit():
            raise IOError("Имя унарного оператора не должно содержать букв и цифр (строка {})".format(line_number))
        if line[index] != ",":
            raise IOError(error_message)

        derivative, index = self.__next_arg(line, index + 1, error_message)

        if line[index] != ")":
            raise IOError(error_message)

        self.__un_ops[name] = {"derivative": derivative, "line": line_number}

    # Считать строку с бинарным оператором
    def __bin_op_from_line(self, line, line_number):
        error_message = "Некорректное определение бинарного оператора (строка {})".format(line_number)
        name, index = self.__next_arg(line, 16, error_message)

        if len(name) != 1:
            raise IOError("Имя бинарного оператора должно состоять из одного символа (строка {})".format(line_number))
        if name.isdigit() or name.isdigit():
            raise IOError("Имя бинарного оператора не должно содержать букв и цифр (строка {})".format(line_number))
        if line[index] != ",":
            raise IOError(error_message)

        prior, index = self.__next_arg(line, index + 1, error_message)

        if not prior.isdigit():
            raise IOError("Приоритет бинарного оператора должен быть числом (строка {})".format(line_number))

        prior = int(prior)

        if line[index] != ",":
            raise IOError(error_message)

        derivative, index = self.__next_arg(line, index + 1, error_message)

        if line[index] != ")":
            raise IOError(error_message)

        self.__bin_ops[name] = {"prior": prior, "derivative": derivative, "line": line_number}

    # Считать строку с функцией
    def __func_from_line(self, line, line_number):
        error_message = "Некорректное определение функции (строка {})".format(line_number)
        name, index = self.__next_arg(line, 9, error_message)

        if len(name) < 2:
            raise IOError("Имя функции должно содержать хотя бы два символа (строка {})".format(line_number))
        if name.startswith("#u"):
            raise IOError("Имя функции не должно начинаться с #u (строка {})".format(line_number))
        if line[index] != ",":
            raise IOError(error_message)

        args_count, index = self.__next_arg(line, index + 1, error_message)

        if not args_count.isdigit():
            raise IOError("Количество аргументов функции должно быть числом (строка {})".format(line_number))

        args_count = int(args_count)

        if args_count <= 0:
            raise IOError("Функция должна иметь хотя бы один аргумент (строка {})".format(line_number))
        if line[index] != ",":
            raise IOError(error_message)

        derivative, index = self.__next_arg(line, index + 1, error_message)

        if line[index] != ")":
            raise IOError(error_message)

        self.__funcs[name] = {"args_count": args_count, "derivative": derivative, "line": line_number}

    def __delete_spaces(self, line):
        line = line.replace(" ", "")
        line = line.replace("\f", "")
        line = line.replace("\t", "")
        line = line.replace("\v", "")
        line = line.replace("\r", "")
        return line

    def __next_arg(self, line, index, error_message):
        if line[index] != '"':
            raise IOError(error_message)
        index += 1
        start_index = index
        if '"' not in line[index:]:
            raise IOError(error_message)
        end_index = line.index('"', index)
        arg = line[start_index: end_index]
        return arg, end_index + 1

    # Преобразовать производные из строкового формата в узлы
    def __convert_derivatives(self):
        parser = Parser(self)

        for un_op in self.__un_ops:
            parser.line = self.__un_ops[un_op]["line"]
            derivative = parser.derivative_to_node(self.__un_ops[un_op]["derivative"], 1)
            self.__un_ops[un_op]["derivative"] = derivative

        for bin_op in self.__bin_ops:
            parser.line = self.__bin_ops[bin_op]["line"]
            derivative = parser.derivative_to_node(self.__bin_ops[bin_op]["derivative"], 2)
            self.__bin_ops[bin_op]["derivative"] = derivative

        for func in self.__funcs:
            parser.line = self.__funcs[func]["line"]
            derivative = parser.derivative_to_node(self.__funcs[func]["derivative"], self.__funcs[func]["args_count"])
            self.__funcs[func]["derivative"] = derivative

    def change_file(self, new_file):
        self.__file = new_file
        self.__un_ops.clear()
        self.__bin_ops.clear()
        self.__funcs.clear()
        self.__from_file()

    def token_is_func(self, token):
        return token in self.__funcs

    def token_is_un_op(self, token):
        return token in self.__un_ops

    def token_is_bin_op(self, token):
        return token in self.__bin_ops

    def token_is_op(self, token):
        return token in self.__un_ops or token in self.__bin_ops

    def func_args_count(self, func):
        return self.__funcs[func]["args_count"]

    def bin_op_prior(self, bin_op):
        return self.__bin_ops[bin_op]["prior"]

    def func_derivative(self, func):
        return self.__funcs[func]["derivative"]

    def un_op_derivative(self, un_op):
        return self.__un_ops[un_op]["derivative"]

    def bin_op_derivative(self, bin_op):
        return self.__bin_ops[bin_op]["derivative"]
