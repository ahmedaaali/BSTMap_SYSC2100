# Ahmed Ali (101181126)
# SYSC 2100 Lab 10
# SYSC 2100 Winter 2022 Lab 10

# An implementation of ADT Map that uses a binary search tree as the
# underlying data structure.

# History:
# Version 1.00 March 28, 2022 - Initial release.
# Version 1.01 March 29, 2022 - Modified __init__.
#                               self.put(key) changed to self.put(key, value)

from typing import Any

class BSTMap:

    class Node:
        def __init__(self, key: Any, value: Any) -> None:
            """Construct a node with no parent and no children,
            containing a key and the value associated with the key.
            """
            self._key = key
            self._value = value
            self._parent = None
            self._left = None
            self._right = None

    def __init__(self, iterable=[]) -> None:
        """Initialize this map with the contents of iterable
        (a sequence of (key, value) pairs).

        If iterable isn't provided, the new map is empty.

        >>> map = BSTMap()
        >>> map
        {}

        # In this example each key/value pair is a tuple containing a
        # 6-digit student number (an int) and that student's letter grade
        # (a str).

        >>> grades = BSTMap([(111537, 'A+'), (101156, 'A+'), (127118, 'B')])
        >>> grades
        {101156: 'A+', 111537: 'A+', 127118: 'B', }
        """
        self._root = None
        self._size = 0  # Number of key/value pairs in the table

        for key, value in iterable:
            self.put(key, value)  # put() updates self._size

    def __str__(self) -> str:
        """Return a string representation of this map, in the format:
        "{key_1: value_1, key_2: value_2, ...}"

        >>> grades = BSTMap([(111537, 'A+'), (101156, 'A+'), (127118, 'B')])
        >>> str(grades)
        "{101156: 'A+', 111537: 'A+', 127118: 'B'}"
        """
        if self._root is None:
            return '{}'

        # Perform an inorder traversal of the BST, collecting the
        # (key, value) pairs as a list of strings.

        items = self._inorder_traversal(self._root)
        return '{' + ', '.join(items) + '}'

    def _inorder_traversal(self, node: 'BSTMap.Node') -> list:
        """Return a list of strings, with each string containing the
        (key/value) pair from one node of the BST rooted at node.

        Each string in the list has the format: 'key: value'.
        The strings are arranged in ascending order according to the keys.

        Precondition: node is not None.
        """
        lst = []

        # Form a list of the key/value pairs in the tree rooted in the node's
        # left child.
        if node._left is not None:
            lst.extend(self._inorder_traversal(node._left))

        # Now store the node's key/value pair in the list.
        lst.append(repr(node._key) + ': ' + repr(node._value))

        # Extend the list to include the key/value pairs in the tree rooted
        # in the node's right child.
        if node._right is not None:
            lst.extend(self._inorder_traversal(node._right))
        return lst

    def __repr__(self) -> str:
        """Return a string representation of this map, in the format:
        "{key_1: value_1, key_2: value_2, ...}"

        >>> grades = BSTMap([(111537, 'A+'), (101156, 'A+'), (127118, 'B')])
        >>> str(grades)
        "{101156: 'A+', 111537: 'A+', 127118: 'B'}"
        """
        return str(self)

    def __len__(self) -> int:
        """Return the number of (key, value) pairs in this map.

        >>> grades = BSTMap()
        >>> len(grades)
        0

        >>> grades.put(111537, 'A+')
        >>> grades.put(101156, 'A+')
        >>> grades.put(127118, 'C')
        >>> len(grades)
        3
        """
        return self._size

    def put(self, key: Any, value: Any) -> None:
        """Insert key and the associated value in this map.

        If key is already in the map, replace the old value with value.

        >>> grades = BSTMap()
        >>> str(grades)
        '{}'

        >>> grades.put(111537, 'A+')
        >>> grades.put(101156, 'A+')
        >>> grades.put(127118, 'C')
        >>> str(grades)
        "{101156: 'A+', 111537: 'A+', 127118: 'C'}"

        # Replace an existing grade.
        >>> grades.put(127118, 'B')
        >>> str(grades)
        "{101156: 'A+', 111537: 'A+', 127118: 'B'}"
        """
        p = self._find_last(key)
        return self._add_child(p, BSTMap.Node(key, value))

    def _find_last(self, x: Any) -> Node:
        """If key x is in this BinarySearchTree, return the reference to the
        node that contains x.
        If key x is not in the BST, return the reference to the node that will
        become the parent of a new node containing x.
        If the BST is empty, return None.
        """
        w = self._root
        prev = None
        while w != None:
            prev = w
            if x < w._key:
                w = w._left
            elif x > w._key:
                w = w._right
            else:
                return w
        return prev

    def _add_child(self, p: Node, u: Node) -> bool:
        """If p is None, the BST is empty, so install u as the root node.

        If the BST is not empty, insert node u as the left or right child of
        node p, such that the BSM property is maintained,
        and return True.
        """
        if p == None:
            self._root = u
            self._size += 1
        else:
            if u._key < p._key:
                p._left = u
                self._size += 1
            elif u._key > p._key:
                p._right = u
                self._size += 1
            else:
                p._value = u._value  # insert u
            u._parent = p
        return True

    def get(self, key: Any) -> Any:
        """If key is in this map, return the value associated with key;
        otherwise return None.

        >>> grades = BSTMap()
        >>> grades.put(111537, 'A+')
        >>> grades.put(101156, 'A+')
        >>> grades.put(127118, 'C')

        >>> grades.get(127118)
        'C'
        >>> grade = grades.get(109771)  # get returns None
        >>> print(grade)
        None
        """
        w = self._root
        while w != None:
            if key < w._key:
                w = w._left
            elif key > w._key:
                w = w._right
            else:
                return w._value
        return None

    def __contains__(self, key: Any) -> bool:
        """Return True if key is in this map; otherwise False.

        >>> grades = BSTMap()
        >>> 101156 in grades
        False

        >>> grades.put(111537, 'A+')
        >>> grades.put(101156, 'A+')
        >>> grades.put(127118, 'C')
        >>> 101156 in grades
        True
        >>> 109771 in grades
        False
        """
        w = self._root
        while w != None:
            if key < w._key:
                w = w._left
            elif key > w._key:
                w = w._right
            else:
                return key == w._key

    def pop(self, key: Any) -> Any:
        """If key is in the map, remove it and return the value associated
        with the key.

        If key is not in the map, raise a KeyError with the message,
        "Key k not found" (where k is the value of parameter key).

        >>> grades = BSTMap()
        >>> grades.put(111537, 'A+')
        >>> grades.put(101156, 'A+')
        >>> grades.put(127118, 'C')

        >>> grades.pop(127118)
        'C'
        >>> str(grades)
       "{101156: 'A+', 111537: 'A+'}"

        >>> grades.pop(109771)
        builtins.KeyError: 'Key 109771 not found'
        >>> str(grades)
       "{101156: 'A+', 111537: 'A+'}"
        """
        u = self._find_last(key)
        x = BSTMap.Node(u._key, u._value)
        if u != None and key == u._key:
            self._remove_node(u)
            print(x._key)
            return x._value
        raise KeyError("Key " + str(x._key) + " not found")

    def _remove_node(self, u: Node) -> None:
        """Remove node u from this BinarySearchTree, such that the binary
        search tree property is maintained.
        """
        if u._left == None or u._right == None:
            # u is a leaf or has one child
            self._splice(u)  # Cases 2 & 3
        else:  # Case 4 (u has two children)
            # find the node containing the
            # smallest key greater than u.x
            w = u._right
            while w._left != None:
                w = w._left
            u._key = w._key  # Copy smallest key
            u._value = w._value  # Copy smallest key
            self._splice(w)

    def _splice(self, u: Node) -> None:
        """Remove node u from this BinarySearchTree.

        Precondition: u is a leaf or has one child.
        """
        if u._left != None:
            s = u._left  # s is u's child
        else:
            s = u._right  # s is u's child
        # if u is a leaf, s is nil
        if u == self._root:  # we're removing the root
            self._root = s
            p = None  # the root has no parent
        else:
            p = u._parent
            if p._left == u:
                p._left = s
            else:
                p._right = s
            if s != None:
                # p is now the parent of s
                s._parent = p
        self._size -= 1


if __name__ == '__main__':
    grades = BSTMap()
    print(grades)
    # '{}'

    grades.put(111537, 'A+')
    print(len(grades))
    grades.put(101156, 'A+')
    print(len(grades))
    grades.put(127118, 'C')
    print(len(grades))
    print(grades)
    #"{101156: 'A+', 111537: 'A+', 127118: 'C'}"

    # Replace an existing grade.
    grades.put(127118, 'B')
    print(len(grades))
    print(grades)
    # "{101156: 'A+', 111537: 'A+', 127118: 'B'}

    grades2 = BSTMap()
    assert(len(grades2) == 0)
    print(101156 in grades2)
    grades2 = BSTMap([(111537, 'D'), (101156, 'A+'), (127118, 'B')])
    print(101156 in grades2)
    print(109771 in grades2)
    print(len(grades2))
    print(grades2)
    assert(len(grades2) == 3)
    print(grades2.get(101156))
    assert grades2.get(101156) == 'A+'
    print(grades2.pop(111537))
    print(grades2)
    print(grades2.pop(101156))
    print(grades2)
    print(grades2.pop(127118))
    print(grades2)
    print(grades2.pop(2))
    print(grades2)
