
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pprint
import copy


def show(image):
    cv2.imshow('da', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def digit(image):
    os.system('tesseract %s tmp  --oem 0 --psm 10'%image)
    digit = open('tmp.txt', 'r')
    return digit.readlines()[0].strip('\n')

def load_sudoku(image):
    sudoku_img = cv2.imread(image)
    gray = cv2.cvtColor(sudoku_img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    new = np.zeros([len(dst), len(dst[0])])
    new[dst>0.01*dst.max()] = 255
    return new

def get_data(corners, sudoku_img):
    boundaries = list()
    count = 0
    cell_len = len(corners[0])/12
    for h, i in enumerate(corners):
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

    offset = 20
    sudoku = list()
    for i in range(len(boundaries) - 1):
        row = list()
        for j in range(len(boundaries[0]) - 1):
            top_y = boundaries[i][j][0] + offset
            bottom_y = boundaries[i+1][j][0]
            left_x = boundaries[i][j][1] + offset
            right_x = boundaries[i][j+1][1]
            cv2.imwrite("tmp.jpg", sudoku_img[top_y:bottom_y, left_x:right_x])
            d = digit('./tmp.jpg')
            if d.isdigit():
                row.append(int(d))
            else:
                row.append('_')
        sudoku.append(row)
    return sudoku

def validate_move(sudoku, i, j, val):
    for y in range(len(sudoku)):
        if y == i:
            continue
        if sudoku[y][j] == val:
            return False
    for x in range(len(sudoku[0])):
        if x == j:
            continue
        if sudoku[i][x] == val:
            return False
    for y in range(int(i/3)*3,(int(i/3)+1)*3):
        for x in range(int(j/3)*3,(int(j/3)+1)*3):
            if y == i and x == j:
                continue
            if sudoku[y][x] == val:
                return False
    return True




def solve(sudoku, i, j):
    if(i > 8):
        return True
    if(j > 8):
        return solve(sudoku, i + 1, 0)

    if sudoku[i][j] != '_':
        return solve(sudoku, i, j+1)

    for val in range(1,10):
        if validate_move(sudoku, i, j, val):
            sudoku[i][j] = val
            if solve(sudoku, i, j+1):
                return True
            sudoku[i][j] = '_'

    sudoku[i][j] = '_'
    return False



# solve(sudoku, 0, 0)


def create_image(sudoku):
    solved = np.ndarray((70,70*10))
    x = 0
    for col in sudoku:
        ans = np.ndarray((70,70))
        for row in col:
            print(row)
            dig = cv2.imread('./images/%d.png'%row,0)
            print(dig)
            ans = np.concatenate((ans, dig), axis=1)
        solved = np.concatenate((solved, ans))
    cv2.imwrite("./images/solved.png",solved[70:,70:])


# create_image(sudoku)

        



