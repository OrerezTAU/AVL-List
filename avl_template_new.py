# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - noy's branch


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0
        self.size = 1

    def initVirtualValues(self):
        self.right = self
        self.left = self
        self.parent = self
        self.height = -1
        self.size = 0

    """
         creates virtual sons for node and attaches them appropriately

         :returns: A legal node with 2 virtual sons
         """

    def makeNodeLeaf(self):
        right_virtual_son = AVLNode("")
        left_virtual_son = AVLNode("")
        right_virtual_son.initVirtualValues()
        left_virtual_son.initVirtualValues()
        self.right = right_virtual_son
        right_virtual_son.parent = self
        self.left = left_virtual_son
        left_virtual_son.parent = self
        self.height = 0

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node
        node.parent = self

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node
        node.parent = self

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def __str__(self) -> str:
        return str(self.value)

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    def getSize(self):
        return self.size


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size = 0
        root = AVLNode("")
        root.initVirtualValues()
        self.root = root
        self.first_item = root
        self.last_item = root

    # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    def successor(self, node):
        """returns the successor of node or a virtual node if node is max, complexity O(logn)
         @pre: node belongs to this AVLTreeList
         :type node: AVLNode
         :rtype : AVLNode
         :param node: the node we want to find the successor for
         :returns the successor of given node in the tree
        """
        if node is self.last_item:
            return self.last_item.right
        if node.right.height == -1:
            father = node.parent
            while father.right.equals(node):
                father = father.parent
                node = node.parent
            return father
        else:
            node = node.right
            while node.left.height != -1:
                node = node.left
            return node

    def predecessor(self, node):
        """returns the predecessor of node or a virtual node if node is min, complexity O(logn)
        @pre: node belongs to this AVLTreeList
        :type node: AVLNode
        :rtype: AVLNode
        :param node: the node we want to find the predecessor for
        :returns the predecessor of given node in the tree
        """
        if node is self.first_item:
            return self.last_item.left
        if node.left.height == -1:
            father = node.parent
            while father.left.equals(node):
                father = father.parent
                node = node.parent
            return father
        else:
            node = node.left
            while node.right.height != -1:
                node = node.right
            return node

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        node = self.getRoot()
        if not node.isRealNode():  # list is empty
            return None
        if i == self.size - 1:
            return self.last_item
        elif i == 0:
            return self.first_item
        while i >= 0:
            if i == node.getLeft().getSize():
                return node
            elif i < node.getLeft().getSize():
                node = node.getLeft()
            elif i > node.getLeft().getSize():
                i = i - node.getLeft().getSize() - 1
                node = node.getRight()

    def rotateMinus2Minus1(self, node):
        """
        Handles the rotation where a node Balance Factor is -2, and it's right son's
        Balance Factor is -1

        (node)
              \
               \
                (r_son)
                   \
                    \
                     (tree)

        @pre: BF(node) == -2 and BF(node.getRight()) == -1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """

        direction = "r" if node.getParent().getRight() is node else "l"
        right_son = node.getRight()
        node.setRight(right_son.getLeft())
        node.getRight().setParent(node)
        right_son.setLeft(node)
        right_son.setParent(node.getParent())
        if direction == "r":
            right_son.getParent().setRight(right_son)
        else:
            right_son.getParent().setLeft(right_son)
        node.setParent(right_son)

    def rotateMinus2Plus1(self, node):
        """
        Handles the rotation where a node Balance Factor is -2, and it's right son's
        Balance Factor is +1

       (node)
             \
              \
               (r_son)
              /
            /
        (tree)

         @pre: BF(node)== -2 and BF(node.getRight())== 1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """

        return

    def rotatePlus2Minus1(self, node):
        """
        Handles the rotation where a node Balance Factor is +2, and it's left son's
        Balance Factor is -1

               (node)
              /
            /
        (l_son)
           \
            \
             (tree)


        @pre: BF(node) == 2 and BF(node.getLeft()) == -1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """
        return

    def rotatePlus2Plus1(self, node):
        """
        Handles the rotation where a node Balance Factor is +2, and it's left son's
        Balance Factor is +1

                       (node)
                      /
                    /
                (l_son)
              /
            /
        (tree)

        @pre: BF(node) == 2 and BF(node.getLeft()) == 1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """

        direction = "r" if node.getParent().getRight() is node else "l"
        left_son = node.getLeft()
        node.setLeft(left_son.getRight())
        node.getLeft().setParent(node)
        left_son.setRight(node)
        left_son.setParent(node.getParent())
        if direction == "r":
            left_son.getParent().setRight(left_son)
        else:
            left_son.getParent().setLeft(left_son)
        node.setParent(left_son)

    def balanceTree(self):
        return

    def insertFirstNode(self, node):
        """
        Handles the insert of the first node in the tree
        :param node: the to-be root node
        :type node: AVLNode
        """
        self.root = node
        self.last_item = node
        self.first_item = node
        self.size = 1

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        node = AVLNode(val)
        node.makeNodeLeaf()
        if self.size == 0:
            self.insertFirstNode(node)
            return 0
        current_i = self.retrieve(i)
        if current_i.getLeft().isRealNode() == False:
            current_i.setLeft(node)
        else:
            pred = self.predecessor(current_i)
            pred.setRight(node)
        if i == 0:
            self.first_item = node
        elif i == self.size:
            self.last_item = node
        self.size += 1
        return self.balanceTree()

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        return -1

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return self.first_item

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return self.last_item

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        array = []
        node = self.first_item
        for i in range(self.size):
            array.append(str(node))

        return array

    """returns the size of the list

    @rtype: int
    @returns: the size of the list"""

    def length(self):
        return self.size

    """sort the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        return None

    """permute the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        return None

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        node = self.first_item
        count = 0
        while node.isRealNode() and node.getValue != val:
            count += 1
            node = self.successor(node)
        return count if node.isRealNode() else -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        if not self.root.isRealNode():
            return None
        return self.root
