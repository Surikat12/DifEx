from diff_tree import DiffTree
from operations import Operations
from nodes import ArgNode, UnOpNode, BinOpNode, FuncNode


class DiffTreeTests:

    def __init__(self):
        self._file = "operations.txt"
        self._diff_tree = DiffTree("operations.txt")
        self._operations = Operations("operations.txt")

    def _compare_trees(self, tree1, tree2):
        return str(tree1) == str(tree2)

    def _from_str_test(self, str, res_tree):
        self._diff_tree.from_str(str)
        return self._compare_trees(self._diff_tree, res_tree)

    def _diff_test(self, tree, var, diff_res):
        deprevative = tree.diff(var)
        return str(deprevative) == diff_res

    def to_str_test_1(self):
        res = "to_str_test_1: "
        try:
            tree = DiffTree(self._file, ArgNode("y"))
            if str(tree) == "y":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def to_str_test_2(self):
        res = "to_str_test_2: "
        try:
            res_tree = DiffTree(self._file, FuncNode("tg", [BinOpNode("-", ArgNode("10"), ArgNode("b"), self._operations)], self._operations))
            if self._from_str_test("tg(10-b)", res_tree):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def to_str_test_3(self):
        res = "to_str_test_3: "
        try:
            res_tree = DiffTree(self._file, BinOpNode("/", UnOpNode("-", ArgNode("2"), self._operations), ArgNode("z"), self._operations))
            if self._from_str_test("-2/z", res_tree):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def to_str_test_4(self):
        res = "to_str_test_4: "
        try:
            res_tree = DiffTree(self._file, FuncNode("log", [ArgNode("k"), ArgNode("n")], self._operations))
            if self._from_str_test("log(k, n)", res_tree):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def from_str_test_1(self):
        res = "from_str_test_1: "
        try:
            res_tree = DiffTree(self._file, FuncNode("sin", [BinOpNode("+", ArgNode("5"), ArgNode("a"), self._operations)], self._operations))
            if self._from_str_test("((sin(5+a)))", res_tree):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def from_str_test_2(self):
        res = "from_str_test_2: "
        try:
            res_tree = DiffTree(self._file, BinOpNode("*", UnOpNode("-", ArgNode("5"), self._operations), ArgNode("y"), self._operations))
            if self._from_str_test("-5*y", res_tree):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def from_str_test_3(self):
        res = "from_str_test_3: "
        try:
            res_tree = DiffTree(self._file, FuncNode("log", [ArgNode("10"), ArgNode("120")], self._operations))
            if self._from_str_test("log(10, 120)", res_tree):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_1(self):
        res = "diff_test_1: "
        try:
            tree =  DiffTree(self._file, BinOpNode("*", UnOpNode("-", ArgNode("5"), self._operations), ArgNode("y"), self._operations))
            if self._diff_test(tree, "y", "0*y+1*-5"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_2(self):
        res = "diff_test_2: "
        try:
            tree = DiffTree(self._file, ArgNode("x"))
            if self._diff_test(tree, "y", "0"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_3(self):
        res = "diff_test_3: "
        try:
            tree = DiffTree(self._file, FuncNode("sin", [BinOpNode("+", ArgNode("5"), ArgNode("x"), self._operations)], self._operations))
            if self._diff_test(tree, "x", "cos(5+x)*(0+1)"):
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res


if __name__ == "__main__":
    tests = DiffTreeTests()
    print(tests.to_str_test_1())
    print(tests.to_str_test_2())
    print(tests.to_str_test_3())
    print(tests.to_str_test_4())
    print(tests.from_str_test_1())
    print(tests.from_str_test_2())
    print(tests.from_str_test_3())
    print(tests.diff_test_1())
    print(tests.diff_test_2())
    print(tests.diff_test_3())
