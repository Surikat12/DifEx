# Узел для аргумента
class ArgNode:

    def __init__(self, value):
        # Значение узла
        self.name = value

    def __str__(self):
        return self.name

    def prior(self):
        return 0

    # Является ли значение узла переменной, по которой берётся производная
    def is_const(self, var):
        return self.name != var

    def copy(self):
        return ArgNode(self.name)

    # Подстановка реальных значений вместо условных из определения производной
    def substitution(self, var, *args):
        if self.name == "#v":
            return ArgNode(var)
        elif self.name.startswith("#"):
            index = int(self.name[1:])
            return args[index].copy()
        else:
            return self

    # Взятие производной
    def diff(self, var):
        if self.is_const(var):
            return ArgNode("0")
        else:
            return ArgNode("1")


# Узел для унарного оператора
class UnOpNode:

    def __init__(self, name, arg, operations):
        # Название оператора
        self.name = name

        # Аргумент унарного оператора
        self.arg = arg

        # Список операций
        self.__operations = operations

    def __str__(self):
        if self.prior() <= self.arg.prior():
            return "{}({})".format(self.name, str(self.arg))
        else:
            return "{}{}".format(self.name, str(self.arg))

    def prior(self):
        return 2

    def __derivative(self):
        return self.__operations.un_op_derivative(self.name)

    # Есть ли в поддереве переменная, по которой берётся производная
    def is_const(self, var):
        return self.arg.is_const(var)

    def copy(self):
        return UnOpNode(self.name, self.arg.copy(), self.__operations)

    # Подстановка реальных значений вместо условных из определения производной
    def substitution(self, var, *args):
        self.arg = self.arg.substitution(var, *args)
        return self

    # Взятие производной
    def diff(self, var):
        if self.is_const(var):
            return ArgNode("0")
        else:
            return self.__derivative().copy().substitution(var, self.arg)


# Узел для бинарного оператора
class BinOpNode:

    def __init__(self, name, f_arg, s_arg, operations):
        # Название оператора
        self.name = name

        # Первый аргумент оператора
        self.f_arg = f_arg

        # Второй аргумент оператора
        self.s_arg = s_arg

        # Список операций
        self.__operations = operations

    def __str__(self):
        if self.prior() <= self.f_arg.prior():
            f_arg = "({})".format(str(self.f_arg))
        else:
            f_arg = str(self.f_arg)

        if self.prior() <= self.s_arg.prior():
            s_arg = "({})".format(str(self.s_arg))
        else:
            s_arg = str(self.s_arg)

        return "{}{}{}".format(f_arg, self.name, s_arg)

    def prior(self):
        return self.__operations.bin_op_prior(self.name)

    def __derivative(self):
        return self.__operations.bin_op_derivative(self.name)

    # Есть ли в поддереве переменная, по которой берётся производная
    def is_const(self, var):
        return self.f_arg.is_const(var) and self.s_arg.is_const(var)

    def copy(self):
        return BinOpNode(self.name, self.f_arg.copy(), self.s_arg.copy(), self.__operations)

    # Подстановка реальных значений вместо условных из определения производной
    def substitution(self, var, *args):
        self.f_arg = self.f_arg.substitution(var, *args)
        self.s_arg = self.s_arg.substitution(var, *args)
        return self

    # Взятие производной
    def diff(self, var):
        if self.is_const(var):
            return ArgNode("0")
        else:
            return self.__derivative().copy().substitution(var, self.f_arg, self.s_arg)


# Узел для функции
class FuncNode:

    def __init__(self, name, args, operations):
        # Название функции
        self.name = name

        # Аргументы функции
        self.args = args

        # Список операций
        self.__operations = operations

    def __str__(self):
        args = ""
        for arg in self.args:
            args += str(arg) + ", "
        args = args[:-2]
        return "{}({})".format(self.name, args)

    def prior(self):
        return 1

    def __derivative(self):
        return self.__operations.func_derivative(self.name)

    # Есть ли в поддереве переменная, по которой берётся производная
    def is_const(self, var):
        for arg in self.args:
            if not arg.is_const(var):
                return False
        return True

    def copy(self):
        args_copy = []
        for arg in self.args:
            args_copy.append(arg.copy())
        return FuncNode(self.name, args_copy, self.__operations)

    # Подстановка реальных значений вместо условных из определения производной
    def substitution(self, var, *args):
        for i in range(len(self.args)):
            self.args[i] = self.args[i].substitution(var, *args)

        if self.name == "#d":
            return self.args[0].diff(self.args[1].name)
        else:
            return self

    # Взятие производной
    def diff(self, var):
        if self.is_const(var):
            return ArgNode("0")
        else:
            return self.__derivative().copy().substitution(var, *self.args)
