# Name: Steve Rector
# OSU Email: rectors@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/15/2022
# Description: Implements AVL Tree

import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds new AVLNode with value to the AVL tree and rebalances the tree as necessary
        :param value: value to be added to tree
        :type  value: object
        """
        # if its an empty tree, add node as root and end operation
        if self.is_empty():
            self._root = AVLNode(value)
            return

        node = self.get_root()
        parent = None

        # traverses down tree, if value equals a node on the tree just return since we cant have duplicates
        while node is not None:
            parent = node
            if value > node.value:
                node = node.right
            elif value < node.value:
                node = node.left
            else:
                return

        if value > parent.value:
            parent.right = AVLNode(value)
            parent.right.parent = parent
        else:
            parent.left = AVLNode(value)
            parent.left.parent = parent
        # rebalancing part
        while parent is not None:
            self._rebalance(parent)
            parent = parent.parent

    def remove(self, value: object) -> bool:
        """
        Removes the value from the AVL tree. Returns True if value is removed, otherwise returns False
        :param value: Value object to be removed from tree
        :type  value: Object
        :return: boolean (True if value is found, False otherwise)
        """
        if self.is_empty():
            return False

        parent = None
        node = self.get_root()

        # traverses the tree looking for value to remove
        while node.value != value and node is not None:
            parent = node
            if value > node.value:
                node = node.right
            else:
                node = node.left

            # if value was not found after traversal, return False
            if node is None:
                return False

        # handles the removal based on whether the node to be removed has no children, one child, or two children
        only_left_child = node.right is None and node.left is not None
        only_right_child = node.left is None and node.right is not None

        # no subtrees
        if node.left is None and node.right is None:
            self._remove_no_subtrees(parent, node)
            node.parent = None

            if self.is_empty():
                return True

            while parent is not None:
                self._rebalance(parent)
                parent = parent.parent

        # one subtree
        elif only_right_child or only_left_child:
            # stores nodes child before removing the node
            if node.right is not None:
                child = node.right
            else:
                child = node.left
            self._remove_one_subtree(parent, node)

            if node.right is not None:
                node.right = None
            else:
                node.left = None

            node.parent = None
            child.parent = parent

            if self.is_empty():
                return True

            while parent is not None:
                self._rebalance(parent)
                parent = parent.parent

        # two subtrees
        else:
            remove_parent = self._remove_two_subtrees(parent, node)

            if self.is_empty():
                return True

            while remove_parent is not None:
                self._rebalance(remove_parent)
                remove_parent = remove_parent.parent

        return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Handles removal of a node that has two subtrees
        :param remove_parent: Parent of the node to be removed
        :type  remove_parent AVLNode
        :param remove_node: Node to be removed
        :type  remove_node: AVLNode
        :return: AVLNode
        """
        inorder_successor = remove_node.right
        inorder_parent = remove_node

        # sets the inorder successor of the node to be removed as well as the inorder successor's parent
        while inorder_successor.left is not None:
            inorder_parent = inorder_successor
            inorder_successor = inorder_successor.left

        inorder_successor.left = remove_node.left
        inorder_successor.left.parent = inorder_successor

        # handle case if the inorder successor of the node to be removed is not the nodes right node
        if inorder_successor != remove_node.right:
            inorder_parent.left = inorder_successor.right
            inorder_successor.right = None
            if inorder_parent.left is not None:
                inorder_parent.left.parent = inorder_parent

            if inorder_successor.right is not None:
                inorder_successor.right.parent = inorder_successor
            inorder_successor.right = remove_node.right
            remove_node.right.parent = inorder_successor

        # handle case where the node to be removed parent is none
        if remove_parent is not None:
            if inorder_successor.value >= remove_parent.value:
                remove_parent.right = inorder_successor
                inorder_successor.parent = remove_parent
            else:
                remove_parent.left = inorder_successor
                inorder_successor.parent = remove_parent

            self._rebalance(inorder_successor)
        else:
            self._root = inorder_successor
            inorder_successor.parent = None

        # rebalances before passing the inorder successor back to remove for final processing 
        while inorder_parent is not None:
            self._rebalance(inorder_parent)
            inorder_parent = inorder_parent.parent

        return inorder_successor


    def _balance_factor(self, node: AVLNode) -> int:
        """
        calculates the given Nodes balance factor (right subtree - left subtree)

        :param node: AVLNode which balance factor will be calculated
        :return: int
        """
        if node is None:
            return 0

        balance_factor = self._get_height(node.right) - self._get_height(node.left)

        return balance_factor


    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of the given node

        :param node: AVLNode which the height will come from
        :return: int
        """
        if node is None:
            return -1

        return node.height


    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Rotates AVL tree left centered around node

        :param node: AVLNode to be rotated around
        :return: AVLNode (new root of the subtree)
        """
        child = node.right
        node.right = child.left
        if node.right is not None:
            # inserts new parent into node
            node.right.parent = node

        child.left = node
        node.parent = child

        self._update_height(node)
        self._update_height(child)

        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Rotates AVL tree right centered around node

        :param node: AVLNode to be rotated around
        :return: AVLNode (new root of the subtree)
        """
        child = node.left
        node.left = child.right
        if node.left is not None:
            # inserts new parent into node
            node.left.parent = node

        child.right = node
        node.parent = child

        self._update_height(node)
        self._update_height(child)

        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of the provided AVLNode

        :param node: AVLNode which height will be updated
        """
        if node is None:
            return

        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Receives an AVLNode and rebalances AVL tree as needed based on balance factor
        :param node: current node
        :type  node: AVLNode
        """
        # grandparent holds the nodes parent before any rotations take place, since the rotations change nodes parents
        if node.parent is not None:
            grandparent = node.parent
        else:
            grandparent = None

        node_balance_factor = self._balance_factor(node)

        # handles LL and LR re-balancing
        if self._balance_factor(node) < -1:
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node

            # right rotation on original node occurs here
            new_root = self._rotate_right(node)
            new_root.parent = grandparent

            # conditional to set the root of the tree and end rebalancing if the new subroot has no parent
            if new_root.parent is None:
                self._root = new_root
                return

            # if the new roots parent is smaller than the new root, set it to the right child, otherwise set to left
            if new_root.parent.value < new_root.value:
                new_root.parent.right = new_root
            else:
                new_root.parent.left = new_root

        # handles RR and RL re-balancing
        elif self._balance_factor(node) > 1:
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node

            # left rotation occurs here
            new_root = self._rotate_left(node)
            new_root.parent = grandparent

            if new_root.parent is None:
                self._root = new_root
                return

            if new_root.parent.value < new_root.value:
                new_root.parent.right = new_root
            else:
                new_root.parent.left = new_root

        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':
    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\n steve test cases")
    print("-------------------------------")

    test = (97, -94, -93, -38, 70, 6, -72, 56, 92, -2)
    tree = AVL(test)
    print('INPUT :', tree)
    tree.remove(97)
    tree.remove(-93)

    print('RESULT :', tree)

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
