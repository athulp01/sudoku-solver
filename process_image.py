#%%
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pprint
import copy

#%%
def show(image):
    cv2.imshow('da', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#%%
def digit(image):
    os.system('tesseract %s tmp  --oem 0 --psm 10'%image)
    digit = open('tmp.txt', 'r')
    return digit.readlines()[0].strip('\n')

#%%
sudoko_img = cv2.imread('./images/leetcode.png')
gray = cv2.cvtColor(sudoko_img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
new = np.zeros([len(dst), len(dst[0])])
new[dst>0.01*dst.max()] = 255
print(len(new[0]))



# show(sudoko_img)
#%%
boundaries = list()
count = 0

cell_len = len(sudoko_img[0])/12
for h, i in enumerate(new):
    before = -100
    if count > 9:
        count -= 1
        continue
    count = 0
    l = list()
    for pos, j in enumerate(i):
        if j > 100 and pos - before > cell_len:
            l.append([h,pos])
            before = pos
            count += 1
    if count > 9:
        count = cell_len
        print(l)
        boundaries.append(l)

#%%
cells = list()
offset = 20

sudoku = list()
for i in range(len(boundaries) - 1):
    row = list()
    for j in range(len(boundaries[0]) - 1):
        top_y = boundaries[i][j][0] + offset
        bottom_y = boundaries[i+1][j][0]
        left_x = boundaries[i][j][1] + offset
        right_x = boundaries[i][j+1][1]
        cv2.imwrite("cell_%d.jpg"%(i+j), sudoko_img[top_y:bottom_y, left_x:right_x])
        cv2.imwrite("tmp.jpg", sudoko_img[top_y:bottom_y, left_x:right_x])
        d = digit('./tmp.jpg')
        if d.isdigit():
            row.append(int(d))
        else:
            row.append('_')
    sudoku.append(row)
pprint.pprint(sudoku)





#%%
def validate(sudoko, i, j, val):
    print("checking %d at %d %d"%(val,i,j))
    for y in range(len(sudoko)):
        if y == i:
            continue
        if sudoko[y][j] == val:
            return False
    for x in range(len(sudoko[0])):
        if x == j:
            continue
        if sudoko[i][x] == val:
            return False
    for y in range(int(i/3)*3,(int(i/3)+1)*3):
        for x in range(int(j/3)*3,(int(j/3)+1)*3):
            if y == i and x == j:
                continue
            if sudoko[y][x] == val:
                return False
    print("%d is valid at %d %d"%(val, i, j))
    return True



#%%
def solve(sudoku, i, j):
    if(i > 8):
        return True
    if(j > 8):
        return solve(sudoku, i + 1, 0)

    if sudoku[i][j] != '_':
        return solve(sudoku, i, j+1)

    for val in range(1,10):
        if validate(sudoku, i, j, val):
            sudoku[i][j] = val
            if solve(sudoku, i, j+1):
                return True
            sudoku[i][j] = '_'

    sudoku[i][j] = '_'
    return False


#%%
s = copy.deepcopy(sudoku)
solve(s, 0, 0)
pprint.pprint(s)#%%


#%%
