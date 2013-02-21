#CS 2450
#Binary Search Tree Class

class Node:
    def __init__(self, item):
        self.item = item
        self.R = None
        self.L = None

class BSTree():
    def __init__(self):
        self.root = None
        self.size = 0

    def Exists(self, item):
        c = self.root
        while c:
            if c.item == item:
                return True
            if item < c.item:
                c = c.L
            else:
                c = c.R
        return False

    def Insert(self, item):
        if self.Exists(item):
            return False
        n = Node(item)
        self.root = self.InsertR(self.root, n)
        return True

    def InsertR(self, c, n):
        if c is None:
            c = n
            self.size += 1
        elif n.item < c.item:
            c.L = self.InsertR(c.L, n)
        else:
            c.R = self.InsertR(c.R, n)
        return c

    def Traverse(self, callback):
        self.TraverseR(self.root, callback)

    def TraverseR(self, c, callback):
        if c is None:
            return
        callback(c.item)
        self.TraverseR(c.L, callback)
        self.TraverseR(c.R, callback)

    def Delete(self, item):
        if not self.Exists(item):
            return False
        self.root = self.DeleteR(self.root, item)
        self.size -= 1
        return True

    def DeleteR(self, c, item):
        if c.item == item:
            # no childern case
            if not c.L and not c.R:
                c=None
            # one child case
            elif not c.R:
                c = c.L
            elif not c.L:
                c = c.R
            # two childern case
            else:
                # get the in-order successor
                # first, cut right
                s = c.R
                # then, cut left until None
                while s.L:
                    s = s.L

                # c's item becomes in-order successor
                c.item = s.item

                # delete the successor
                c.R = self.DeleteR(c.R, s.item)
        else:
            if item < c.item:
                c.L = self.DeleteR(c.L, item)
            else:
                c.R = self.DeleteR(c.R, item)
        return c

    def Retrieve(self, item):
        if not self.Exists(item):
            return None
        return self.RetrieveR(self.root, item)

    def RetrieveR(self, c, item):
        if item == c.item:
            return c.item
        elif item < c.item:
            return self.RetrieveR(c.L, item)
        else:
            return self.RetrieveR(c.R, item)

    def GetSize(self):
        return self.size




