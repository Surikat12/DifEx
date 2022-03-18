from math_parser import Parser
from operations import Operations
from nodes import ArgNode, UnOpNode, BinOpNode, FuncNode


class ParserTests():

    def __init__(self):
        self._operations = Operations("operations.txt")

    def str_to_node_test_1(self):
        res = "str_to_node_test_1: "
        try:
            node = ArgNode("y")
            if str(node) == "y":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def str_to_node_test_2(self):
        res = "str_to_node_test_2: "
        try:
            node = FuncNode("tg", [BinOpNode("-", ArgNode("10"), ArgNode("b"), self._operations)], self._operations)
            if str(node) == "tg(10-b)":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def str_to_node_test_3(self):
        res = "str_to_node_test_3: "
        try:
            node = BinOpNode("/", UnOpNode("-", ArgNode("2"), self._operations), ArgNode("z"), self._operations)
            if str(node) == "-2/z":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def str_to_node_test_4(self):
        res = "str_to_node_test_4: "
        try:
            node = FuncNode("log", [ArgNode("k"), ArgNode("n")], self._operations)
            if str(node) == "log(k, n)":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res


if __name__ == "__main__":
    tests = ParserTests()
    print(tests.str_to_node_test_1())
    print(tests.str_to_node_test_2())
    print(tests.str_to_node_test_3())
    print(tests.str_to_node_test_4())