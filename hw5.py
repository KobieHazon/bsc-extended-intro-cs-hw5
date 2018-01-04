#Skeleton file for HW5 - Winter 2017-2018 - extended intro to CS

#Add your implementation to this file

#You may add other utility functions to this file,
#but you may NOT change the signature of the existing ones.

from printree import * #for Binary_search_tree's __repr__

 


############
# QUESTION 1
############

# a

class Matrix:
    """
    Represents a rectangular matrix with n rows and m columns.
    """

    def __init__(self, n, m, val=0):
        """
        Create an n-by-m matrix of val's.
        Inner representation: list of lists (rows)
        """
        assert n > 0 and m > 0
        #self.rows = [[val]*m]*n #why this is bad? I explained in pdf
        self.rows = [[val]*m for i in range(n)]

    def dim(self):
        return len(self.rows), len(self.rows[0])

    def __repr__(self):
        if len(self.rows)>10 or len(self.rows[0])>10:
            return "Matrix too large, specify submatrix"
        s = ""
        for r in self.rows:
            s += str(r) + "\n"
            
        return s

    def __eq__(self, other):
        return isinstance(other, Matrix) and self.rows == other.rows

    def copy(self):
        ''' brand new copy of matrix '''
        n,m = self.dim()
        new = Matrix(n,m)
        for i in range (n):
           for j in range (m):
               new[i,j] = self[i,j]
        return new

    # cell/sub-matrix access/assignment
    ####################################
    def __getitem__(self, ij): #ij is a tuple (i,j). Allows m[i,j] instead m[i][j]
        i,j = ij
        if isinstance(i, int) and isinstance(j, int):
            return self.rows[i][j]
        elif isinstance(i, slice) and isinstance(j, slice):
            M = Matrix(1,1) # to be overwritten
            M.rows = [row[j] for row in self.rows[i]]
            return M
        else:
            return NotImplemented

    def __setitem__(self, ij, val): #ij is a tuple (i,j). Allows m[i,j] instead m[i][j]
        i,j = ij
        if isinstance(i,int) and isinstance(j,int):
            assert isinstance(val, (int, float, complex))
            self.rows[i][j] = val
        elif isinstance(i,slice) and isinstance(j,slice):
            assert isinstance(val, Matrix)
            n,m = val.dim()
            s_rows = self.rows[i]
            assert len(s_rows) == n and len(s_rows[0][j]) == m
            for s_row, v_row in zip(s_rows,val.rows):
                s_row[j] = v_row
        else:
            return NotImplemented

    # arithmetic operations
    ########################
    def entrywise_op(self, other, op):
        if not isinstance(other, Matrix):
            return NotImplemented
        assert self.dim() == other.dim()
        n,m = self.dim()
        M = Matrix(n,m)
        for i in range(n):
            for j in range(m):
                M[i,j] = op(self[i,j], other[i,j])
        return M

    def __add__(self, other):
        return self.entrywise_op(other,lambda x,y:x+y)

    def __sub__(self, other):
        return self.entrywise_op(other,lambda x,y:x-y)
    
    def __neg__(self):
        n,m = self.dim()
        return Matrix(n,m) - self

    def __mul__(self, other):
        assert isinstance(other, (int, float, complex))
        n,m = self.dim()
        return self.entrywise_op(Matrix(n,m,other), lambda x,y :x*y)
    
    __rmul__ = __mul__

    def minor(self, i, j): #Could simply copy to new matrix and delete accordingly but time complexity will be higher
        assert (i < self.dim()[0]) and (j < self.dim()[1]) and (isinstance(i, int)) and (isinstance(j, int))
        minor = Matrix(self.dim()[0] - 1, self.dim()[1] - 1)
        for row_num, row in enumerate(self.rows):
            if row_num < i:
                for elem_num, elem in enumerate(row):
                    if elem_num < j:
                        minor[row_num, elem_num] = self[row_num, elem_num]
                    elif elem_num != j:
                        minor[row_num, elem_num - 1] = self[row_num, elem_num]
            elif row_num != i:
                for elem_num, elem in enumerate(row):
                    if elem_num < j:
                        minor[row_num - 1, elem_num] = self[row_num, elem_num]
                    elif elem_num != j:
                        minor[row_num - 1, elem_num - 1] = self[row_num, elem_num]
        return minor
    
    def det(self, i=0): #Calculate det using the formula recuresively
        assert len(self.rows) == len(self.rows[0])
        if len(self.rows) == 1:
            return self.rows[0][0]
        return sum([((-1) ** (i + j)) * self.rows[i][j] * self.minor(i, j).det() for j in range(len(self.rows))])


############
# QUESTION 2
############

class SparseMatrix:
    """
    Represents a rectangular matrix with n rows and m columns.
    """

    def __init__(self, n, m):
        """
        Create an n-by-m matrix of val's.
        Inner representation: list of lists (rows)
        """
        assert n > 0 and m > 0
        self.elements={}
        self.size = (n,m)
        
    def dim(self):
        return self.size

    def __repr__(self):
        if self.size[0] > 10 or self.size[1] > 10:
            return "Matrix too large, specify submatrix"
        s = ""
        for i in range(self.size[0]):
            s += '['
            for j in range(self.size[1]):
                if (i, j) in self.elements:
                    s += str(self.elements[(i, j)])
                else:
                    s += '0'
                if j != self.size[1] - 1:
                    s += ', '
            s += ']\n'
        return s
    
    def __eq__(self, other):
        return isinstance(other, SparseMatrix) and self.dim() == other.dim() and self.elements == other.elements

    def __getitem__(self, ij): #ij is a tuple (i,j). Allows m[i,j] instead m[i][j]
        if isinstance(ij[0], int) and isinstance(ij[1], int):
            if ij in self.elements:
                return self.elements[ij]
            return 0
        else:
            return NotImplemented
    
    def __setitem__(self, ij, val): #ij is a tuple (i,j). Allows m[i,j] instead m[i][j]
        i,j = ij
        if isinstance(i, int) and isinstance(j, int):
            assert isinstance(val, (int, float, complex))
            if val == 0:
                if ij in self.elements:
                    del self.elements[ij]
            else:
                self.elements[ij] = val
        else:
            return NotImplemented
    
    def __add__(self, other):
        if not isinstance(other, SparseMatrix):
            return NotImplemented
        assert self.dim() == other.dim()
        M = SparseMatrix(self.size[0], self.size[1])
        for ij in self.elements:
            if ij in other.elements:
                M[ij[0], ij[1]] = self.elements[ij] + other.elements[ij]
            else:
                M[ij[0], ij[1]] = self.elements[ij]
        for ij in other.elements:
            if ij not in self.elements:
                M[ij[0], ij[1]] = other.elements[ij]
        return M
    
    def __sub__(self, other):
        if not isinstance(other, SparseMatrix):
            return NotImplemented
        assert self.dim() == other.dim()
        M = SparseMatrix(self.size[0], self.size[1])
        for ij in self.elements:
            if ij in other.elements:
                M[ij[0], ij[1]] = self.elements[ij] - other.elements[ij]
            else:
                M[ij[0], ij[1]] = self.elements[ij]
        for ij in other.elements:
            if ij not in self.elements:
                M[ij[0], ij[1]] = -1 * other.elements[ij]
        return M

    def __neg__(self):
        M = SparseMatrix(self.size[0], self.size[1])
        for i, j in self.elements:
            M[i, j] = -1 * self.elements[(i, j)]
        return M
    
    def __mul__(self,other):
        assert isinstance(other, (int, float, complex))
        M = SparseMatrix(self.size[0], self.size[1])
        for i, j in self.elements:
            M[i, j] = other * self.elements[(i, j)]
        return M
    
    def __rmul__(self, other):
        return self * other

    def minor(self, i, j):
        assert (i < self.size[0]) and (j < self.size[1]) and (isinstance(i, int)) and (isinstance(j, int))
        minor = SparseMatrix(self.size[0] - 1, self.size[1] - 1)
        for ij in self.elements:
            if ij[0] < i:
                if ij[1] < j:
                    minor[ij[0], ij[1]] = self.elements[ij]
                elif ij[1] != j:
                    minor[ij[0], ij[1] - 1] = self.elements[ij]
            elif ij[0] != i:
                if ij[1] < j:
                    minor[ij[0] - 1, ij[1]] = self.elements[ij]
                elif ij[1] != j:
                    minor[ij[0] - 1, ij[1] - 1] = self.elements[ij]
        return minor
    
    def det(self, i=0):
        assert self.size[0] == self.size[1]
        if self.size[0] == 1:
            return self[0, 0]
        return sum([((-1) ** (i + j)) * self[i, j] * self.minor(i, j).det() for j in range(self.size[0])])

    def gen_row1(self, i): #iterating over m elements (lower than k)
        for j in range(self.size[1]):
            if (i, j) in self.elements:
                yield self.elements[i, j]
    
    def gen_row2(self, i): #iterating over k elements (lower than m)
        for ij in self.elements:
            if ij[0] == i:
                yield self.elements[ij]


#Q2, part C: These functions are not part of the class
    

def mat2a():
    return None


def mat2b():
    m = SparseMatrix(3, 3)
    m[2, 0] = 1
    m[2, 1] = 6
    return m


def mat2c():
    m = SparseMatrix(3, 3)
    m[2, 2] = 2
    m[2, 1] = 1
    return m


############
# QUESTION 4
############

class Func():
    def __init__(self, func, domain):
        self.func = func
        self.domain = domain

    def __call__(self, x):
        if self.domain(x):
            return self.func(x)
        return None

    def compose(self, other):
        if self.domain(lambda x: other(x)):
            return Func(lambda x: self(other(x)), other.domain)
        return None

    def exp(self, k):
        assert k >= 1
        F = Func(self.func, self.domain)
        for i in range(k-1):
            F = self.compose(F)
        return F

    def exp_rec(self, k):
        if k <= 1:
            return self
        k -= 1
        return self.compose(self.exp_rec(k))

############
# QUESTION 5
############


class Tree_node():
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.height = 0
       
    def __repr__(self):
        return "(" + str(self.key) + ":" + str(self.val) + ")"


class Binary_search_tree():

    def __init__(self):
        self.root = None

    def __repr__(self): #no need to understand the implementation of this one
        out = ""
        for row in printree(self.root): #need printree.py file
            out = out + row + "\n"
        return out

    def lookup(self, key):
        ''' return node with key, uses recursion '''

        def lookup_rec(node, key):
            if node == None:
                return None
            elif key == node.key:
                return node
            elif key < node.key:
                return lookup_rec(node.left, key)
            else:
                return lookup_rec(node.right, key)

        return lookup_rec(self.root, key)

    def insert(self, key, val):
        ''' insert node with key,val into tree, uses recursion '''

        def insert_rec(node, key, val):
            if key == node.key:
                node.val = val     # update the val for this key
            elif key < node.key:
                if node.left == None:
                    node.left = Tree_node(key, val)
                else:
                    insert_rec(node.left, key, val)
            else: #key > node.key:
                if node.right == None:
                    node.right = Tree_node(key, val)
                else:
                    insert_rec(node.right, key, val)
            return
        
        if self.root == None: #empty tree
            self.root = Tree_node(key, val)
        else:
            insert_rec(self.root, key, val)

    def minimum(self):
        ''' return node with minimal key '''
        if self.root == None:
            return None
        node = self.root
        left = node.left
        while left != None:
            node = left
            left = node.left
        return node

    def depth(self):
        ''' return depth of tree, uses recursion'''
        def depth_rec(node):
            if node == None:
                return -1
            else:
                return 1 + max(depth_rec(node.left), depth_rec(node.right))

        return depth_rec(self.root)

    def size(self):
        ''' return number of nodes in tree, uses recursion '''
        def size_rec(node):
            if node == None:
                return 0
            else:
                return 1 + size_rec(node.left) + size_rec(node.right)

        return size_rec(self.root)

    def store_heights(self):

        def store_heights_rec(node):
            if node.right is None and node.left is None:
                node.height = 0
            elif node.right is not None and node.left is None:
                node.height = 1 + store_heights_rec(node.right)
            elif node.right is None and node.left is not None:
                node.height = 1 + store_heights_rec(node.left)
            else:
                node.height = 1 + max(store_heights_rec(node.left) ,store_heights_rec(node.right))
            return node.height

        store_heights_rec(self.root)

    def height_diff(self):
        self.store_heights()

        def height_diff_rec(node):
            if node.left is None:
                if node.right is None:
                    return node.height
                return max(node.right.height, height_diff_rec(node.right))
            else:
                if node.right is None:
                    return max(node.left.height,height_diff_rec(node.left))
                return max((node.left.height - node.right.height) if (node.left.height - node.right.height) >=0 else -1 * (node.left.height - node.right.height) ,height_diff_rec(node.left), height_diff_rec(node.right))

        return height_diff_rec(self.root)


############
# QUESTION 5
############
       
def remove(string,char):
    return ''.join(letter for letter in string if letter!=char)

def hash_sequence(genome,k):
    n_dict = {}
    for i in range(len(genome) - k + 1):
        if genome[i:i+k] in n_dict:
            n_dict[genome[i:i+k]].append(i)
        else:
            n_dict[genome[i:i+k]] = [i]
    return n_dict


def intersects(genome1,genome2,k):
    if len(genome1) < len(genome2):
        chk_dict = hash_sequence(genome1, k)
        for i in range(len(genome2) - k + 1):
            if genome2[i:i+k] in chk_dict:
                return genome2[i:i+k]
        return None
    else:
        chk_dict = hash_sequence(genome2, k)
        for i in range(len(genome1) - k + 1):
            if genome1[i:i+k] in chk_dict:
                return genome1[i:i+k]
        return None
        
from Legionella import legionella
from Brucella import brucella
from Shigella_sonnei import shigella
from Helicobacter_pylori import helicobacter



   
    
########
# Tester
########

def test():
    #Testing Q1 & 2
    mat = Matrix(3,3)
    mat[0,0] = 1
    mat[0,1] = 2
    mat[0,2] = 3
    mat[1,0] = 4
    mat[1,1] = 5
    mat[1,2] = 6
    mat[2,0] = 7
    mat[2,1] = 8
    mat[2,2] = 9
    
    minor = mat.minor(1,2)
    if minor == None:
        print("error in Matrix.minor")
    elif minor[0,0] != 1 or  minor[0,1] != 2 or minor[1,0] != 7 or minor[1,1] != 8:
        print("error in Matrix.minor")
        
    minor = mat.minor(0,0)
    if minor == None:
        print("error in Matrix.minor")
    elif minor[0,0] != 5 or  minor[0,1] != 6 or minor[1,0] != 8 or minor[1,1] != 9:
        print("error in Matrix.minor")

    if mat.det() != 0:
        print("error in Matrix.det")

    mat[2,1] = 600
    if mat.det() != 3552:
        print("error in Matrix.det")

    
    m = SparseMatrix(3,2)
    m[1,0] = 30
    m[2,1] = -2
    x = m[1,1]
    y = m[2,1]
    if (x != 0 or y != -2):
        print("error in SparseMatrix.__getitem__ or SparseMatrix.__setitem__")
    if m.__repr__() != "[0, 0]\n[30, 0]\n[0, -2]\n":
        print("error in SparseMatrix.__repr__")
    if m.dim() != (3, 2):
        print("error in SparseMatrix.dim")
    m2 = SparseMatrix(3,2)
    m2[0,0] = 100
    m3 = m + m2
    if m3 == None:
        print("error in SparseMatrix.__add__")
    elif m3[0,0] != 100 or m3[2,1]!= -2:
        print("error in SparseMatrix.__add__")
    if m.__repr__() != "[0, 0]\n[30, 0]\n[0, -2]\n":
        print("error in SparseMatrix.__repr__ or SparseMatrix.__add__")
    m4 = m- m2
    if m4 == None:
        print("error in SparseMatrix.__sub__")
    elif m4[0,0] != -100 or m4[2,1]!= -2:
        print("error in SparseMatrix.__sub__")
    m4 = m-m
    if m4 == None:
        print("error in SparseMatrix.__sub__")
    elif m4[0,0] != 0 or m4[2,1]!= 0:
        print("error in SparseMatrix.__sub__")
    m5 = -m
    if m5 == None:
        print("error in SparseMatrix.__neg__")
    elif m5[1,0] != -30 or m4[0,1]!= 0:
        print("error in SparseMatrix.__neg__")
    m6 = m*3
    if m6 == None:
        print("error in SparseMatrix.__mul__")
    elif m6[2,1] != -6 or m6[0,1]!= 0:
        print("error in SparseMatrix.__mul__")
    m7 = 3*m
    if m7 == None:
        print("error in SparseMatrix.__rmul__")
    elif m7[2,1] != -6 or m7[0,1]!= 0:
        print("error in SparseMatrix.__rmul__")
    

    smat = SparseMatrix(3,3)
    smat[0,0] = 1
    smat[0,1] = 2
    smat[0,2] = 3
    smat[1,0] = 4
    smat[1,1] = 5
    smat[1,2] = 6
    smat[2,0] = 7
    smat[2,1] = 8
    smat[2,2] = 9

    
    minor = smat.minor(1,2)
    if minor == None:
        print("error in SparseMatrix.minor")
    elif minor[0,0] != 1 or  minor[0,1] != 2 or minor[1,0] != 7 or minor[1,1] != 8:
        print("error in SparseMatrix.minor")
    
    minor = smat.minor(0,0)
    if minor == None:
        print("error in SparseMatrix.minor")
    elif minor[0,0] != 5 or  minor[0,1] != 6 or minor[1,0] != 8 or minor[1,1] != 9:
        print("error in SparseMatrix.minor")

    if smat.det() != 0:
        print("error in SparseMatrix.det")

    smat[2,1] = 600
    if smat.det() != 3552:
        print("error in SparseMatrix.det")

    if smat.__repr__() != mat.__repr__():
        print("error in SparseMatrix.__repr__")
    

    m8 = SparseMatrix(3,4)
    m8[1,0] = 3
    m8[2,3] = 90
    m8[1,1] = -10
    g = m8.gen_row1(1)
    if g == None:
        print("error in SparseMatrix.gen_row1")
    else:
        next(g)
        non_zero_elements = list(m8.gen_row1(1))
        if (sorted(non_zero_elements) != [-10, 3]):
            print("error in SparseMatrix.gen_row1")
        if (sorted(list(m8.gen_row2(1))) != [-10, 3]):
            print("error in SparseMatrix.gen_row2")
        if (sorted(list(m8.gen_row2(0))) != []):
            print("error in SparseMatrix.gen_row2")



    #Testing Q3
    f1 = Func(lambda x:1/x, lambda x:x!=0)
    if f1(4) != 0.25:
        print("error in Func.__call__")
    if f1(0) != None:
        print("error in Func.__call__")
    f2 = Func(lambda x:x+3, lambda x:True)
    f3 = f1.compose(f2)
    f4 = f2.compose(f1)
    if (f3 == None) or ((f3 != None) and f3(1)!= 0.25):
        print("error in Func.compose")
    if (f3 == None) or ((f3 != None) and f3(-3) != None):
        print("error in Func.compose")
    if (f4 == None) or ((f4 != None) and f4(2) != 3.5):
        print("error in Func.compose")
    f5 = f2.exp(4)
    if (f5 == None) or ((f5 != None) and f5(0) != 12):
        print("error in Func.exp")
    f5 = f2.exp_rec(4)
    if (f5 == None) or ((f5 != None) and f5(0) != 12):
        print("error in Func.exp_rec")

    #Testing Q4
    bin_tree = Binary_search_tree()
    bin_tree.insert(2,"a")
    bin_tree.insert(4,"b")
    bin_tree.insert(2,"c")
    bin_tree.insert(3,"d")
    bin_tree.insert(1,"e")
    bin_tree.store_heights()
    if bin_tree.root.height != 2 or\
       bin_tree.root.left.height != 0 or\
       bin_tree.root.right.height != 1 or\
       bin_tree.root.right.left.height != 0 :
        print("error in Binary_search_tree.store_heights")
    bin_tree = Binary_search_tree()
    bin_tree.insert(2,"a")
    bin_tree.insert(4,"b")
    bin_tree.insert(2,"c")
    bin_tree.insert(3,"d")
    bin_tree.insert(1,"e")
    bin_tree.insert(0,"f")
    bin_tree.insert(5,"g")
    bin_tree.insert(7,"h")
    bin_tree.insert(6,"i")
    if (bin_tree.height_diff() != 2):
        print("error in Binary_search_tree.height_diff")
    bin_tree.insert(4.5, "j")
    bin_tree.insert(3.5, "k")
    bin_tree.insert(-1, "l")
    bin_tree.insert(1.5, "m")
    if bin_tree.height_diff() != 1:
        print("error in Binary_search_tree.height_diff")


        
    #Testing Question 5A
    if hash_sequence("byebyeboy",3) != {'yeb':[1,4], 'boy':[6],'bye':[0,3], 'ebo':[5], 'eby':[2]}:
        print("Error in hash_sequence()")

    #Testing Question 5B
    if intersects("byebyebaboonboy","babyboy",4) != None or\
        intersects("byebyebaboonboy","babyboy",3) == None:
        print("Error in intersects()")


