
"""
_________ _______  _______ _________ _______  _______ 
\__   __/(  ____ \(  ____ \\__   __/(  ____ \(  ____ )
   ) (   | (    \/| (    \/   ) (   | (    \/| (    )|
   | |   | (__    | (_____    | |   | (__    | (____)|
   | |   |  __)   (_____  )   | |   |  __)   |     __)
   | |   | (            ) |   | |   | (      | (\ (   
   | |   | (____/\/\____) |   | |   | (____/\| ) \ \__
   )_(   (_______/\_______)   )_(   (_______/|/   \__/
                                                      
                   _______ 
|\     /||\     /|(  ____ \
| )   ( || )   ( || (    \/
| (___) || | _ | || (____  
|  ___  || |( )| |(_____ \ 
| (   ) || || || |      ) )
| )   ( || () () |/\____) )
|/     \|(_______)\______/ 

"""

from printree import * #for Binary_search_tree's __repr__

import sys

verbose = 0

def check_heights(items):
    tree = Binary_search_tree()
    for item in items:
        tree.insert(item[0],item[1])
    tree.store_heights()
    if verbose:
        print(tree)
    def col_rec(node):
        if node == None:
            return []
        return [(node.key,node.height)]+col_rec(node.left)+col_rec(node.right)
    lst = col_rec(tree.root)
    lst = sorted(lst, key = lambda x:x[0])
    return lst

f1 = Func(lambda x:x**2, lambda x:True)
f2 = Func(lambda x:(5*x)/(x-9), lambda x:x!=9)

def get_det(m):
    try:
        return m.det()
    except AssertionError:
        return -1
def get_minor(m,i,j):
    return m.minor(i,j)

mat = Matrix(1,1)
mat[0,0] = 4
mat_sprs = SparseMatrix(1,1)
mat_sprs[0,0]=4
non_sqr = Matrix(10,3)
non_sqr_sprs_for_minor = SparseMatrix(10,3)
non_sqr_minr = Matrix(9,2)
non_sqr_sprs_minr_for_minor = SparseMatrix(9,2)
for i in range(30):
    non_sqr[int(i/3),i % 3]=i
    non_sqr_sprs_for_minor[int(i/3),i % 3]=i
for i in range(0,27,3):
    p = 0
    if int(i/3) > 3:
        p = 3
    non_sqr_minr[int(i/3),0]=i+p
    non_sqr_sprs_minr_for_minor[int(i/3),0]=i+p
    non_sqr_minr[int(i/3),1]=i+2+p
    non_sqr_sprs_minr_for_minor[int(i/3),1]=i+2+p

def make_vdm(vals,typ):
    if typ == "Matrix":
        vdm = Matrix(len(vals),len(vals))
    else:
        vdm = SparseMatrix(len(vals),len(vals))
    for i in range(len(vals)):
            for j in range(len(vals)):
                    vdm[i,j] = vals[i]**j
    return vdm

vdm = make_vdm([2,-4,6,-8,10],"Matrix")
vdm_sprs = make_vdm([2,-4,6,-8,10],"Sparse")
vdm_minor_sprs = make_vdm([2,-4,6,10],"Sparse")
vdm_minor = make_vdm([2,-4,6,10],"Matrix")


def make_scalar(rk,scalar,typ,rev = False,both = False):
    if typ == "Matrix":
        mat = Matrix(rk,rk)
    else:
        mat = SparseMatrix(rk,rk)
    for i in range(rk):
        if both:
            mat[i,i]+=scalar
            mat[i,rk-i-1]+=scalar
        else:
            if rev:
                mat[i,rk-i-1]=scalar
            else:
                mat[i,i]=scalar
    return mat

id_5 = make_scalar(5,1,"Matrix")
id_4 = make_scalar(4,1,"Matrix")

non_sqr_sprs = SparseMatrix(10,3)
non_sqr_sprs2 = SparseMatrix(10,3)
id_5_sprs = make_scalar(5,1,"Sparse")
id_4_sprs = make_scalar(4,1,"Sparse")
scl_5_2_sprs = make_scalar(5,2,"Sparse")
rev_5_sprs = make_scalar(5,1,"Sparse",True)
both_5_sprs = make_scalar(5,1,"Sparse",True,True)
sub_5_sprs = SparseMatrix(5,5)
for i in range(5):
    if i!=2:
        sub_5_sprs[i,i]=1
        sub_5_sprs[i,5-i-1]=-1
mat_dic = {(1,2):7,(3,3):6,(2,0):1,(2,1):-5,(4,4):-4}
def build_sprs(vals,i,j):
    mat = SparseMatrix(i,j)
    for k,v in vals.items():
        di,dj = k
        mat[di,dj]=v
    return mat
mat_reg = build_sprs(mat_dic,5,5)
mat_neg = build_sprs({k:-v for k,v in mat_dic.items()},5,5)

for i in range(10):
    for j in range(3):
        if (i+j) % 4 == 0:
            non_sqr_sprs[i,j]=i**2+j*3
            non_sqr_sprs2[i,j]=i**2+j*3
def comp_dim(mat,i,j):
    di,dj = mat.dim()
    return i==di and j==dj
def comp_mats(mata,matb):
    return mata==matb
ALL_TESTS = {
    21: dict(
        seif_string='Q21',
        function=comp_dim,
        func_name="get_dim",
        total_grade=1,
        tests=[
            dict(
                args=(non_sqr_sprs,10,3,),
                expected=True,
                grade=1,
                symbol="T21_1",
                ),           
            ]
        ),
    22: dict(
        seif_string='Q22',
        function=comp_mats,
        func_name="comp_mats",
        total_grade=2,
        tests=[
            dict(
                args=(non_sqr_sprs,non_sqr_sprs2,),
                expected=True,
                grade=1,
                symbol="T22_1",
                ),           
            dict(
                args=(id_5_sprs,id_4_sprs,),
                expected=False,
                grade=1,
                symbol="T22_2",
                ),           
            ]        
        ),
    23: dict(
        seif_string='Q23',
        function=lambda x,y,z: x+y == z,
        func_name="add_mats",
        total_grade=2,
        tests=[
            dict(
                args=(id_5_sprs,id_5_sprs,scl_5_2_sprs,),
                expected=True,
                grade=1,
                symbol="T23_1",
                ),
            dict(
                args=(id_5_sprs,rev_5_sprs,both_5_sprs,),
                expected=True,
                grade=1,
                symbol="T23_2",
                ),                       
            ]        
        ),
    24: dict(
        seif_string='Q24',
        function=lambda x,y,z: x-y == z,
        func_name="sub_mats",
        total_grade=2,
        tests=[
            dict(
                args=(id_5_sprs,id_5_sprs,SparseMatrix(5,5),),
                expected=True,
                grade=1,
                symbol="T24_1",
                ),
            dict(
                args=(id_5_sprs,rev_5_sprs,sub_5_sprs,),
                expected=True,
                grade=1,
                symbol="T24_2",
                ),                       
            ]        
        ),
    25: dict(
        seif_string='Q25',
        function=lambda x,y: -x==y,
        func_name="neg_mat",
        total_grade=2,
        tests=[
            dict(
                args=(mat_reg,mat_neg,),
                expected=True,
                grade=1,
                symbol="T25_1",
                ),
            dict(
                args=(id_5_sprs,make_scalar(5,-1,"Sparse"),),
                expected=True,
                grade=1,
                symbol="T25_2",
                ),                       
            ]        
        ),
    26: dict(
        seif_string='Q26',
        function=lambda x,y,z: y*x==z and x*y == z,
        func_name="mult_mat",
        total_grade=2,
        tests=[
            dict(
                args=(mat_reg,-1,mat_neg,),
                expected=True,
                grade=1,
                symbol="T26_1",
                ),
            dict(
                args=(id_5_sprs,5,make_scalar(5,5,"Sparse"),),
                expected=True,
                grade=1,
                symbol="T26_2",
                ),                       
            ]        
        ),
    27: dict(
        seif_string='Q27',
        function=lambda mat,i,j:mat.minor(i,j),
        func_name="get_minor",
        total_grade=5,
        tests=[
            dict(
                args=(vdm_sprs,3,4,),
                expected=vdm_minor_sprs,
                grade=2,
                symbol="T27_1",
                ),
            dict(
                args=(id_5_sprs,2,2,),
                expected=id_4_sprs,
                grade=2,
                symbol="T27_2",
                ),
            dict(
                args=(non_sqr_sprs_for_minor,4,1,),
                expected=non_sqr_sprs_minr_for_minor,
                grade=1,
                symbol="T27_3",
                ),                        
            ]
        ),      
    28: dict(
        seif_string='Q28',
        function=get_det,
        func_name="get_det",
        total_grade=5,
        tests=[
            dict(
                args=(mat_sprs,),
                expected=4,
                grade=2,
                symbol="T28_1",
                ),
            dict(
                args=(vdm_sprs,),
                expected=1083801600,
                grade=2,
                symbol="T28_2",
                ),
            dict(
                args=(non_sqr_sprs_for_minor,),
                expected=-1,
                grade=1,
                symbol="T28_3",
                ),            
            ]
        ),
    29: dict(
        seif_string='Q29',
        function=lambda x:sorted([next(x) for i in range(5)])==[1, 6, 36, 216, 1296],
        func_name="gen_row",
        total_grade=4,
        tests=[
            dict(
                args=(vdm_sprs.gen_row1(2),),
                expected=True,
                grade=2,
                symbol="T29_1",
                ),
            dict(
                args=(vdm_sprs.gen_row2(2),),
                expected=True,
                grade=2,
                symbol="T29_2",
                ),   
            ]
        ),            
    11: dict(
        seif_string='Q11',
        function=lambda mat,i,j:mat.minor(i,j),
        func_name="get_minor",
        total_grade=5,
        tests=[
            dict(
                args=(vdm,3,4,),
                expected=vdm_minor,
                grade=2,
                symbol="T11_1",
                ),
            dict(
                args=(id_5,2,2,),
                expected=id_4,
                grade=2,
                symbol="T11_2",
                ),
            dict(
                args=(non_sqr,4,1,),
                expected=non_sqr_minr,
                grade=1,
                symbol="T11_3",
                ),            
            ]
        ),      
    12: dict(
        seif_string='Q12',
        function=get_det,
        func_name="get_det",
        total_grade=5,
        tests=[
            dict(
                args=(mat,),
                expected=4,
                grade=2,
                symbol="T12_1",
                ),
            dict(
                args=(vdm,),
                expected=1083801600,
                grade=2,
                symbol="T12_2",
                ),
            dict(
                args=(non_sqr,),
                expected=-1,
                grade=1,
                symbol="T12_3",
                ),            
            ]
        ),    
    51: dict(
        seif_string='Q51',
        function=hash_sequence,
        func_name="Hash_sequence",
        total_grade=9,
        tests=[
            dict(
                args=("masterofpuppetsimpullingyourstrings",7,),
                expected={'sterofp': [2], 'uppetsi': [9], 'petsimp': [11], 'gyourst': [23], 'pulling': [17], 'ourstri': [25], \
                          'terofpu': [3], 'tsimpul': [13], 'ppetsim': [10], 'puppets': [8], 'asterof': [1], 'ingyour': [21], \
                          'etsimpu': [12], 'ofpuppe': [6], 'erofpup': [4], 'ullingy': [18], 'strings': [28], 'rstring': [27], \
                          'mpullin': [16], 'lingyou': [20], 'mastero': [0], 'ngyours': [22], 'yourstr': [24], 'fpuppet': [7], \
                          'impulli': [15], 'urstrin': [26], 'rofpupp': [5], 'simpull': [14], 'llingyo': [19]},
                grade=3,
                symbol="T51_1",
                ),
            dict(
                args=("shesellsseashellsbytheseashore",2,),
                expected={'by': [17], 'es': [2, 21], 'ss': [7], 'ho': [26], 'se': [3, 8, 22], 'th': [19], 'yt': [18], 'or': [27], \
                          'he': [1, 12, 20], 'sb': [16], 'el': [4, 13], 'll': [5, 14], 're': [28], 'as': [10, 24], 'sh': [0, 11, 25], \
                          'ea': [9, 23], 'ls': [6, 15]},
                grade=3,
                symbol="T51_2",
                ),
            dict(
                args=("aaaaaaaaaabbbbbaaaaaaaaaaa",4,),
                expected={'bbaa': [13], 'bbba': [12], 'aaaa': [0, 1, 2, 3, 4, 5, 6, 15, 16, 17, 18, 19, 20, 21, 22], \
                          'abbb': [9], 'aabb': [8], 'baaa': [14], 'bbbb': [10, 11], 'aaab': [7]},
                grade=3,
                symbol="T51_3",
                ),
            ]
        ),
    52: dict(
        seif_string='Q52',
        function=intersects,
        func_name="Intersects",
        total_grade=6,
        tests=[
            dict(
                args=("abcdefg","gfedabc",4,),
                expected=None,
                grade=2,
                symbol="T52_1",
                ),
            dict(
                args=("abcdefg","gfedabc",3,),
                expected="abc",
                grade=2,
                symbol="T52_2",
                ),
            dict(
                args=("blablablablabla","blablablablabla",15,),
                expected="blablablablabla",
                grade=2,
                symbol="T52_3",
                ),            
            ]
        ),
    31: dict(
        seif_string='Q31',
        function=f2,
        func_name="Func_call",
        total_grade=3,
        tests=[
            dict(
                args=(10,),
                expected=50,
                grade=1,
                symbol="T31_1",
                ),
            dict(
                args=(7,),
                expected=-17.5,
                grade=1,
                symbol="T31_2",
                ),
            dict(
                args=(9,),
                expected=None,
                grade=1,
                symbol="T31_3",
                ),                        
            ]
        ),
    32: dict(
        seif_string='Q32',
        function=lambda f1,f2,x:f1.compose(f2)(x),
        func_name="Func_compose",
        total_grade=3,
        tests=[
            dict(
                args=(f2,f1,3,),
                expected=None,
                grade=1,
                symbol="T32_1",
                ),
            dict(
                args=(f1,f2,3,),
                expected=6.25,
                grade=1,
                symbol="T32_2",
                ),
            dict(
                args=(f1,f1,7,),
                expected=2401,
                grade=1,
                symbol="T32_3",
                ),                        
            ]
        ),
    33: dict(
        seif_string='Q33',
        function=lambda f,k,x:f.exp(k)(x),
        func_name="Func_exp",
        total_grade=3,
        tests=[
            dict(
                args=(f1,7,2,),
                expected=340282366920938463463374607431768211456,
                grade=1,
                symbol="T33_1",
                ),
            dict(
                args=(f2,3,4,),
                expected=-1.0309278350515465,
                grade=1,
                symbol="T33_2",
                ),
            dict(
                args=(f2,10,81/4,),
                expected=None,
                grade=1,
                symbol="T33_3",
                ),                        
            ]
        ),
    34: dict(
        seif_string='Q34',
        function=lambda f,k,x:f.exp_rec(k)(x),
        func_name="Func_exp_rec",
        total_grade=6,
        tests=[
            dict(
                args=(f1,7,2,),
                expected=340282366920938463463374607431768211456,
                grade=2,
                symbol="T34_1",
                ),
            dict(
                args=(f2,3,4,),
                expected=-1.0309278350515465,
                grade=2,
                symbol="T34_2",
                ),
            dict(
                args=(f2,10,81/4,),
                expected=None,
                grade=2,
                symbol="T34_3",
                ),                        
            ]
        ),             
    42: dict(
        seif_string='Q42',
        function=check_heights,
        func_name="store_heights",
        total_grade=9,
        tests=[
            dict(
                args=([(10,"a"),(6,"a"),(14,"a"),(1,"a"),(3,"a"),(20,"a"),(7,"a"),],),
                expected=[(1, 1), (3, 0), (6, 2), (7, 0), (10, 3), (14, 1), (20, 0)],
                grade=3,
                symbol="T42_1",
                ),
            dict(
                args=([(x,"x") for x in range(10)],),
                expected=[(0, 9), (1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1), (9, 0)],
                grade=3,
                symbol="T42_2",
                ),
            dict(
                args=([(0,"root")],),
                expected=[(0, 0)],
                grade=3,
                symbol="T42_3",
                ),                        
            ]
        ),
    43: dict(
        seif_string='Q43',
        function=eval,
        func_name="height_diff",
        total_grade=11,
        tests=[
            dict(
                setup="""
global btree
try:
    btree = Binary_search_tree()
    [btree.insert(x,"hi") for x in range(10)]
except:
    btree=None
""",
                args=('btree.height_diff()',),
                expected=9,
                grade=3,
                symbol="T43_1",
                ),
                
            dict(
                setup="""
global _bt1_test3
try:
    _bt1_test3 = Binary_search_tree()
    _bt1_test3.insert(10,1)
    _bt1_test3.insert(5,2)
    _bt1_test3.insert(20,3)
    _bt1_test3.insert(15,4)
    _bt1_test3.insert(1,5)
    _bt1_test3.insert(12,6)
    _bt1_test3.insert(35,7)
    _bt1_test3.insert(2,8)
    _bt1_test3.insert(90,9)
    _bt1_test3.insert(9,10)
    _bt1_test3.insert(25,11)
    _bt1_test3.insert(36,12)
    _bt1_test3=_bt1_test3.height_diff()
except:
    _bt1_test3 =None
""",
                args=('_bt1_test3',),
                expected=1,
                grade=4,
                symbol="T43_2",
                ),
            dict(
                setup="""
global _bt2_test3
try:
    _bt2_test3 = Binary_search_tree()
    _bt2_test3.insert(100,1)
    _bt2_test3.insert(20,2)
    _bt2_test3.insert(3,3)
    _bt2_test3.insert(30,4)
    _bt2_test3.insert(200,5)
    _bt2_test3.insert(1000,6)
    _bt2_test3.insert(327,7)
    _bt2_test3=_bt2_test3.height_diff()
except:
    _bt2_test3 =None
""",
                args=('_bt2_test3',),
                expected=2,
                grade=4,
                symbol="T43_3",
                ),
            ]
        ),      
}

def run_with_limited_time(func, args=(), kwargs={}, timeout_duration=10):
    '''This function will spwan a thread and run the given function using the args, kwargs and
    return the given default value if the timeout_duration is exceeded
    '''
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = (sys.exc_info()[0], sys.exc_info()[1])
        def stop(sefl):
            super(self)

    it = InterruptableThread()
    it.daemon = True
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return [True, it.result]
    else:
        return [False, it.result]

def t(n=0):
    print('Starting tester')
    err_l = []
    err_s = []
    grade = 0
    accum = 0
    tot = 0

    for seif in ALL_TESTS:
        tot += ALL_TESTS[seif]['total_grade']
        if n == 0 or seif == n or n == -1:
            function = ALL_TESTS[seif]['function']
            tests = ALL_TESTS[seif]['tests']
            seif_string = ALL_TESTS[seif]['seif_string']
            total_grade = ALL_TESTS[seif]['total_grade']
            func_name = ALL_TESTS[seif]['func_name']
            time_to_run = ALL_TESTS[seif].get('time_to_run', 20)
            tmp_grade = 0
            tmp_errs = []
            if (n != -1):
                print("Test %s: %s: (%d)" % (func_name, seif_string, total_grade))

            for test in tests:
                exception_symbol = test['symbol'] + "_x"
                timeout_symbol = test['symbol'] + "_t"
                reduce = False
                if "setup" in test:
                    exec(test["setup"])                
                timeout = run_with_limited_time(function, test['args'], {}, time_to_run)
                if timeout[0]:
                    err_l.append("%s: Timeout in %s (running time was longer than %d seconds) - [%s] - (%d)\n" % (seif_string, func_name, time_to_run, timeout_symbol, test['grade']))
                    reduce = True
                    symbol = timeout_symbol
                else:
                    res = timeout[1]
                    if (isinstance(res, tuple)):
                        e = timeout[1][1]
                        err_l.append("%s: Exception in %s (%s) - [%s] - (%d)\n" % (seif_string, func_name, e, exception_symbol, test['grade']))
                        reduce = True
                        symbol = exception_symbol
                    else:
                        try:
                            if res != test['expected']:
                                err_l.append("%s: Error in %s - [%s] - (%d)" % (seif_string, func_name, test['symbol'], test['grade']))
                                err_l.append("Expected: " + str(test['expected']))
                                err_l.append("Got:      " + str(res) + "\n")
                                reduce = True
                                symbol = test['symbol']
                        except:
                            e = sys.exc_info()[1]
                            err_l.append("%s: Exception in %s (%s) - [%s] - (%d)\n" % (seif_string, func_name, e, exception_symbol, test['grade']))
                            reduce = True
                            symbol = exception_symbol

                if reduce:
                    err_s.append(symbol)
                    grade -= test['grade']
                else:
                    accum += test['grade']

    if (n != -1):
        print()
        print("\n".join(str(err) for err in err_l))
        print(grade)
    if verbose:
        print('Total grade: ',tot)
    return [str(grade)]+err_s

test_results = t(-1)

