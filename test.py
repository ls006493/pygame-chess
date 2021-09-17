# from math import sqrt
# import gc

# WIDTH, HEIGHT = 800, 800
# PIECE_WIDTH, PIECE_HEIGHT = 100, 100
# BOARD_LENGTH = 8

# class fruit():
#     def __init__(self, name):
#         self.name = name

# apple1 = fruit("apple")
# banana1 = fruit("banana")
# lemon1 = fruit("lemon")

# num = 3
# def find_em(classType, attr, targ):
#     return [obj.name for obj in gc.get_objects() if isinstance(obj, classType) and getattr(obj, attr)==targ]
# aviableMove = [coord for i in range(BOARD_LENGTH) for j in range(BOARD_LENGTH) if i == ]
# print(find_em(fruit, name, lemon))
# coord = (4,5)
# BOARD_LENGTH = 8
# viableMove = [(i,j) for i in range(BOARD_LENGTH) for j in range(BOARD_LENGTH) if (i == coord[0] or j == coord[1]) and (i,j)!=coord]
# print(viableMove)

# a = set([1,2,3,4,5,6,7])
# b = set([3,5,9,9])
# print(list(a-b))
x = [(1,2),(3,4)]
y = [(5,6),(6,8),(1,2)]
if x not in y:
    print("no")