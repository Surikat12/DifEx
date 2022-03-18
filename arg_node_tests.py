from nodes import ArgNode


class ArgNodeTests:

    def is_const_test_1(self):
        res = "is_const_test_1: "
        try:
            node = ArgNode("x")
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
            node = ArgNode("x")
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
            node = ArgNode("5")
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
            node = ArgNode("x")
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
            node = ArgNode("#0")
            subs_res = node.substitution("x", ArgNode("5"))
            if str(subs_res) == "5":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def substitution_test_2(self):
        res = "substitution_test_2: "
        try:
            node = ArgNode("#v")
            subs_res = node.substitution("y")
            if str(subs_res) == "y":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_1(self):
        res = "diff_test_1: "
        try:
            node = ArgNode("x")
            diff_res = node.diff("x")
            if str(diff_res) == "1":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res

    def diff_test_2(self):
        res = "diff_test_2: "
        try:
            node = ArgNode("x")
            diff_res = node.diff("y")
            if str(diff_res) == "0":
                res += "PASS"
            else:
                res += "FAILED"
        except Exception as e:
            res += "FAILED BECAUSE EXCEPTION: '" + str(e) + "'"
        return res


if __name__ == "__main__":
    tests = ArgNodeTests()
    print(tests.is_const_test_1())
    print(tests.is_const_test_2())
    print(tests.copy_test_1())
    print(tests.copy_test_2())
    print(tests.diff_test_1())
    print(tests.diff_test_2())
    print(tests.substitution_test_1())
    print(tests.substitution_test_2())