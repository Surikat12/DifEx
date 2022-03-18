from operations import Operations
from nodes import ArgNode, BinOpNode, FuncNode


class FuncNodeTests:

    def __init__(self):
        self._operations = Operations("operations.txt")

    def is_const_test_1(self):
        res = "is_const_test_1: "
        try:
            node = FuncNode("tg", [BinOpNode("-", ArgNode("10"), ArgNode("b"), self._operations)], self._operations)
            if node.is_const("x"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def is_const_test_2(self):
        res = "is_const_test_2: "
        try:
            node = FuncNode("tg", [BinOpNode("-", ArgNode("10"), ArgNode("b"), self._operations)], self._operations)
            if not node.is_const("b"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def copy_test_1(self):
        res = "copy_test_1: "
        try:
            node = FuncNode("tg", [BinOpNode("-", ArgNode("10"), ArgNode("b"), self._operations)], self._operations)
            node_copy = node.copy()
            if str(node) == str(node_copy) and node is not node_copy:
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def copy_test_2(self):
        res = "copy_test_2: "
        try:
            node = FuncNode("tg", [ArgNode("x")], self._operations)
            node_copy = node.copy()
            if str(node) == str(node_copy) and node is not node_copy:
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def substitution_test_1(self):
        res = "substitution_test_1: "
        try:
            node = FuncNode("cos", [BinOpNode("-", ArgNode("#v"), ArgNode("b"), self._operations)], self._operations)
            subs_res = node.substitution("y")
            if str(subs_res) == "cos(y-b)":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def substitution_test_2(self):
        res = "substitution_test_2: "
        try:
            node = FuncNode("ctg", [BinOpNode("+", ArgNode("10"), ArgNode("#0"), self._operations)], self._operations)
            subs_res = node.substitution("x", ArgNode("c"))
            if str(subs_res) == "ctg(10+c)":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_1(self):
        res = "diff_test_1: "
        try:
            node = FuncNode("sin", [BinOpNode("+", ArgNode("5"), ArgNode("x"), self._operations)], self._operations)
            diff_res = node.diff("x")
            if str(diff_res) == "cos(5+x)*(0+1)":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_2(self):
        res = "diff_test_2: "
        try:
            node = FuncNode("ctg", [BinOpNode("+", ArgNode("10"), ArgNode("5"), self._operations)], self._operations)
            diff_res = node.diff("y")
            if str(diff_res) == "0":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res


if __name__ == "__main__":
    arg_node_tests = FuncNodeTests()
    print(arg_node_tests.is_const_test_1())
    print(arg_node_tests.is_const_test_2())
    print(arg_node_tests.copy_test_1())
    print(arg_node_tests.copy_test_2())
    print(arg_node_tests.diff_test_1())
    print(arg_node_tests.diff_test_2())
    print(arg_node_tests.substitution_test_1())
    print(arg_node_tests.substitution_test_2())