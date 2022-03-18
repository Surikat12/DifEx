class EmptyStackError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def __str__(self):
        return str(self.value)


class Stack:
    def __init__(self):
        self.__top = None
        self.__size = 0

    def __str__(self):
        if self.__size == 0:
            return "[]"
        curr_node = self.__top
        res = [str(curr_node)]
        while curr_node.next is not None:
            curr_node = curr_node.next
            res.append(str(curr_node))
        return "[ " + ", ".join(reversed(res)) + " ]"

    def is_empty(self):
        return self.__size == 0

    def size(self):
        return self.__size

    def push(self, value):
        if self.__size == 0:
            self.__top = Node(value)
        else:
            self.__top = Node(value, self.__top)
        self.__size += 1

    def pop(self):
        if self.__size == 0:
            raise EmptyStackError("Попытка получить элемент из пустого стека")
        res = self.__top.value
        self.__top = self.__top.next
        self.__size -= 1
        return res

    def peek(self):
        if self.__size == 0:
            raise EmptyStackError("Попытка посмотреть элемент в пустом стеке")
        return self.__top.value

    def clear(self):
        self.__top = None
        self.__size = 0
