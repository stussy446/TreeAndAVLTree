# Name: Steve Rector
# OSU Email: rectors@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/15/2022
# Description: Implements Binary Search Tree


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree
        :param value: value object to be added to the tree
        :type value: object
        """
        parent = None
        node = self.get_root()
        new_node = BSTNode(value)

        # if the bst is empty, sets new node to the root of the tree
        if self.is_empty():
            self._root = new_node
            return

        # traverse down the tree until getting to what will be the parent of new node
        while node is not None:
            parent = node
            if value >= node.value:
                node = node.right
            else:
                node = node.left

        # if the new nodes value is greater than or equal to the parent value, set it as right child of parent,
        # otherwise set it as the left child of the parent
        if value >= parent.value:
            parent.right = new_node
        else:
            parent.left = new_node

    def remove(self, value: object) -> bool:
        """
        Removes a value from the tree, returns True if value is removed and False otherwise

        :param value: value object to be removed from tree
        :type value: object
        :return: boolean indicating if value has been removed (True) or not (False)
        :rtype: bool
        """
        if self.is_empty():
            return False

        parent = None
        node = self.get_root()

        # traverses the tree looking for the requested value, assigns to node if found, returns False otherwise
        while node.value != value and node is not None:
            parent = node
            if value > node.value:
                node = node.right
            else:
                node = node.left

            if node is None:
                return False

        # handles the removal based on whether the node to be removed has no children, one child, or two children
        only_left_child = node.right is None and node.left is not None
        only_right_child = node.left is None and node.right is not None

        if node.left is None and node.right is None:
            self._remove_no_subtrees(parent, node)
        elif only_right_child or only_left_child:
            self._remove_one_subtree(parent, node)
        else:
            self._remove_two_subtrees(parent, node)

        return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes node that has no subtrees (no left or right nodes)

        :param remove_parent: parent of BSTNode to be removed
        :type remove_parent: BSTNode
        :param remove_node: BSTNode to be removed
        :type remove_node: BSTNode
        """

        # empties the tree if the node to be removed is the root and its been determined the root has no children
        if self.get_root() == remove_node:
            self.make_empty()
            return

        if remove_node.value >= remove_parent.value:
            remove_parent.right = None
        else:
            remove_parent.left = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes node that has a left or right subtree (only)

        :param remove_parent: parent of BSTNode to be removed
        :type remove_parent: BSTNode
        :param remove_node: BSTNode to be removed
        :type remove_node: BSTNode
        """
        
        if remove_node.right is not None:
            child_node = remove_node.right
        elif remove_node.left is not None:
            child_node = remove_node.left

        # if there is a parent, set the child node to the same side of the parent that the node being removed was in
        # otherwise, set the root to the child node
        if remove_parent is not None:
            if remove_node == remove_parent.right:
                remove_parent.right = child_node
            elif remove_node == remove_parent.left:
                remove_parent.left = child_node
        else:
            self._root = child_node

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes node that has two subtrees
        Need to find inorder successor and its parent (make a method!)

        :param remove_parent: Parent of node to be removed
        :type remove_parent: BSTNode
        :param remove_node: BSTNode to be removed
        :type remove_node: BSTNode
        """
        inorder_successor = remove_node.right
        inorder_parent = remove_node

        # traverses through remove_nodes right tree to the leftmost node, sets that node to inorder successor and
        # the inorder successors parent to its parent node
        while inorder_successor.left is not None:
            inorder_parent = inorder_successor
            inorder_successor = inorder_successor.left

        # rearranges nodes as needed and frees up (IE removes) the remove_node
        inorder_successor.left = remove_node.left

        if inorder_successor != remove_node.right:
            inorder_parent.left = inorder_successor.right
            inorder_successor.right = remove_node.right

        if remove_parent is not None:
            if inorder_successor.value >= remove_parent.value:
                remove_parent.right = inorder_successor
            else:
                remove_parent.left = inorder_successor
        else:
            self._root = inorder_successor

    def contains(self, value: object) -> bool:
        """
        Returns True if value is in the tree. Returns False if value is not in tree or the tree is empty.

        :param value: value to be searched for
        :type value: object
        :return: boolean value indicating if value was found (True) or if it was not/the tree was empty (False)
        :rtype: bool
        """
        if self.is_empty():
            return False

        node = self.get_root()

        # traverse down tree until value is either found or it is determined the value is not in the tree
        while node is not None:
            if value > node.value:
                node = node.right
            elif value < node.value:
                node = node.left
            else:
                return True

        return False

    def inorder_traversal(self) -> Queue:
        """
        Performs inorder traversal of the tree and returns a Queue object that contains values of visited nodes in the
        order they were visited. Returns empty Queue if the tree is empty

        :return: Queue object containing all the values of visited nodes
        :rtype: Queue
        """
        queue = Queue()

        if self.is_empty():
            return queue

        node = self.get_root()

        # makes recursive inorder traversal call to go through tree and add each value to queue in the order visited
        self._inorder_recursive_helper_queue(node, queue)

        return queue

    def _inorder_recursive_helper_queue(self, node:BSTNode, queue: Queue) -> None:
        """
        recursively traverses tree via inorder_traversal, where each value is added to the queue after the values node
        is visited for the second time.
        :param node: current Node
        :type node: BSTNode
        :param queue: queue to add values into
        :type node: Queue
        """
        if node is not None:
            self._inorder_recursive_helper_queue(node.left, queue)
            queue.enqueue(node.value)
            self._inorder_recursive_helper_queue(node.right, queue)

    def find_min(self) -> object:
        """
        Returns the lowest value of the tree. If the tree is empty, returns None

        :return: the lowest value object in the tree, or None if tree is empty
        :rtype: Object
        """
        if self.is_empty():
            return None

        # performs inorder traversal and returns the first item dequeued from the returned queue
        inorder_queue = self.inorder_traversal()
        return inorder_queue.dequeue()

    def find_max(self) -> object:
        """
        Returns the highest value of the tree. If the tree is empty, returns None

        :return: the highest value object in the tree, or None if tree is empty
        :rtype: Object
        """
        if self.is_empty():
            return None

        node = self.get_root()

        # traverses tree down to rightmost node and returns its value
        while node.right is not None:
            node = node.right

        return node.value


    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty. Returns false otherwise

        :return: Boolean if tree is empty (True) or not (False)
        :rtype: bool
        """
        return self.get_root() is None

    def make_empty(self) -> None:
        """
        Removes all the nodes from the tree
        """
        if not self.is_empty():
            self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    # print("\nPDF - method add() example 1")
    # print("----------------------------")
    # test_cases = (
    #     (1, 2, 3),
    #     (3, 2, 1),
    #     (1, 3, 2),
    #     (3, 1, 2),
    # )
    # for case in test_cases:
    #     tree = BST(case)
    #     print(tree)
    #
    # print("\nPDF - method add() example 2")
    # print("----------------------------")
    # test_cases = (
    #     (10, 20, 30, 40, 50),
    #     (10, 20, 30, 50, 40),
    #     (30, 20, 10, 5, 1),
    #     (30, 20, 10, 1, 5),
    #     (5, 4, 6, 3, 7, 2, 8),
    #     (range(0, 30, 3)),
    #     (range(0, 31, 3)),
    #     (range(0, 34, 3)),
    #     (range(10, -10, -2)),
    #     ('A', 'B', 'C', 'D', 'E'),
    #     (1, 1, 1, 1),
    # )
    # for case in test_cases:
    #     tree = BST(case)
    #     print('INPUT  :', case)
    #     print('RESULT :', tree)
    #
    # print("\nPDF - method add() example 3")
    # print("----------------------------")
    # for _ in range(100):
    #     case = list(set(random.randrange(1, 20000) for _ in range(900)))
    #     tree = BST()
    #     for value in case:
    #         tree.add(value)
    #     if not tree.is_valid_bst():
    #         raise Exception("PROBLEM WITH ADD OPERATION")
    # print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example steve")
    print("-------------------------------")
    tree = BST([-30, 8, 73, -55, 81, 51, -43, -37, -4, -97])
    tree.remove(-30)
    if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('RESULT :', tree)
    tree.remove(73)
    if not tree.is_valid_bst():
        raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('RESULT :', tree)
    tree.remove(81)
    if not tree.is_valid_bst():
        raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('RESULT :', tree)



    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
