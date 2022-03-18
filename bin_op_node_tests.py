from operations import Operations
from nodes import ArgNode, BinOpNode


class BinOpNodeTests:

    def __init__(self):
        self._operations = Operations("operations.txt")

    def is_const_test_1(self):
        res = "is_const_test_1: "
        try:
            node = BinOpNode("+", ArgNode("x"), ArgNode("5"), self._operations)
            if not node.is_const("x"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def is_const_test_2(self):
        res = "is_const_test_2: "
        try:
            node = BinOpNode("+", ArgNode("x"), ArgNode("5"), self._operations)
            if node.is_const("y"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def copy_test_1(self):
        res = "copy_test_1: "
        try:
            node = BinOpNode("+", ArgNode("x"), ArgNode("5"), self._operations)
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
            node = BinOpNode("+", ArgNode("10"), ArgNode("5"), self._operations)
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
            node = BinOpNode("/", ArgNode("z"), ArgNode("#0"), self._operations)
            subs_res = node.substitution("x", ArgNode("5"))
            if str(subs_res) == "z/5":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def substitution_test_2(self):
        res = "substitution_test_2: "
        try:
            node = BinOpNode("-", ArgNode("y"), ArgNode("5"), self._operations)
            subs_res = node.substitution("y")
            if str(subs_res) == "y-5":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_1(self):
        res = "diff_test_1: "
        try:
            node = BinOpNode("/", ArgNode("z"), ArgNode("2"), self._operations)
            diff_res = node.diff("x")
            if str(diff_res) == "0":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_2(self):
        res = "diff_test_2: "
        try:
            node = BinOpNode("+", ArgNode("x"), ArgNode("3"), self._operations)
            diff_res = node.diff("x")
            if str(diff_res) == "1+0":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res


if __name__ == "__main__":
    tests = BinOpNodeTests()
    print(tests.is_const_test_1())
    print(tests.is_const_test_2())
    print(tests.copy_test_1())
    print(tests.copy_test_2())
    print(tests.diff_test_1())
    print(tests.diff_test_2())
    print(tests.substitution_test_1())
    print(tests.substitution_test_2())