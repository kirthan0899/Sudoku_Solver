from __future__ import print_function
import os, sys
import webbrowser
import cv2
import numpy as np
from PIL import Image

filename=raw_input("Enter the name of the image you want to solve : ")

# function to print the board on to a file.
def printFileBoard(board):
    string = ""
    string = string + "*********************\n"
    for x in range(0, 9):
        if x == 3 or x == 6:
            string = string + "*********************\n"
        for y in range(0, 9):
            if y == 3 or y == 6:
                string = string + " * "
            string = string + str(board[x][y]) + " "
        string = string + "\n"
    string = string + "*********************\n"
    return string

# function to print the board on to the console
def printBoard(board):
    print()
    print("*********************")
    for x in range(0, 9):
        if x == 3 or x == 6:
            print("*********************")
        for y in range(0, 9):
            if y == 3 or y == 6:
                print("*", end=" ")
            print(board[x][y], end=" ")
        print()
    print("*********************")
    
# function to check if the board is full or not
# returns true if it is full and false if it isn't
# it works on the fact that if it finds at least one 
# zero in the board it returns false
def isFull(board):
    for x in range(0, 9):
        for y in range (0, 9):
            if board[x][y] == 0:
                return False
    return True
    
# function to find all of the possible numbers which 
# can be put at the specified location by
# checking the horizontal and vertical and the 
# three by three square in which the numbers are present
def possibleEntries(board, i, j):
    
    possibilityArray = {}
    
    for x in range (1, 10):
        possibilityArray[x] = 0
    
    #For horizontal entries
    for y in range (0, 9):
        if not board[i][y] == 0: 
            possibilityArray[board[i][y]] = 1
     
    #For vertical entries
    for x in range (0, 9):
        if not board[x][j] == 0: 
            possibilityArray[board[x][j]] = 1
            
    #For squares of three x three
    k = 0
    l = 0
    if i >= 0 and i <= 2:
        k = 0
    elif i >= 3 and i <= 5:
        k = 3
    else:
        k = 6
    if j >= 0 and j <= 2:
        l = 0
    elif j >= 3 and j <= 5:
        l = 3
    else:
        l = 6
    for x in range (k, k + 3):
        for y in range (l, l + 3):
            if not board[x][y] == 0:
                possibilityArray[board[x][y]] = 1          
    
    for x in range (1, 10):
        if possibilityArray[x] == 0:
            possibilityArray[x] = x
        else:
            possibilityArray[x] = 0
    
    return possibilityArray

# recursive function which solves the board and 
# prints it. 
def sudokuSolver(board):
    
    i = 0
    j = 0
    
    possiblities = {}
    
    # if board is full, there is no need to solve it any further
    if isFull(board):
        print()
        print("Board Solved Successfully!")
        print()
        printBoard(board)
        html = open('index.html','w')
        html.write('''
            <html>
                <head><title>Sudoku Solver</title>
                <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
                <link type="text/css" rel="stylesheet" href="style.css"  media="screen"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                </head>
                <body>
                ''')
        html.write('<center><h1>SUDOKU SOLVED!</h1><br>')
        html.write('<center><h2>Original Image :</h2><img src=%s><br>'%(filename))
        html.write('<center><h2>Solved Puzzle :</h2>')
        html.write('<table>')
        for x in range(9):
            html.write('<tr>')
            for y in range(9):
                html.write('<td><p>'+str(board[x][y])+'</p></td>')
            html.write('</tr>')
        html.write('</table></center></body></html>')
        html.close()
        webbrowser.open('index.html', new=2)
        os.remove('output.png')
        os.remove('test.png')
        os.remove('data.txt')
        for i in range(1,10):
            for j in range(1,10):
                os.remove('slice_img_'+str(i)+'_'+str(j)+'.png')
        sys.exit()
    else:
        # find the first vacant spot
        for x in range (0, 9):
            for y in range (0, 9):
                if board[x][y] == 0:
                    i = x
                    j = y
                    break
            else:
                continue
            break
        
        # get all the possibilities for i,j
        possiblities = possibleEntries(board, i, j)
        
        # go through all the possibilities and call the the function
        # again and again
        for x in range (1, 10):
            if not possiblities[x] == 0:
                board[i][j] = possiblities[x]
                #file.write(printFileBoard(board))
                sudokuSolver(board)
        # backtrack
        board[i][j] = 0

def main():
	# Read the image and convert it to grayscale
    img = cv2.imread(filename, 0)
    if img is None:
		print("Invalid image entered")
		exit(0)

	# Perform thresholding by setting a threshold value
    ret, thresh = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
    print("Threshold selected : ", ret)
    cv2.imwrite("./output.png", thresh)
    
    # call hough program to detect the borders of the puzzle
    os.system('python hough.py')
    # to slice the image into 9x9=81 blocks
    os.system('python slice_img.py')
    # to recognize the digits in each slice
    os.system('python recog.py')
    SudokuBoard = [[0 for x in range(9)] for x in range(9)] 

	# read the sudoku board values from the data.txt file
    f = open('data.txt','rU')
    values = f.read()
    f.close()
    SudokuBoard[0][0] = int(values[0])
    SudokuBoard[0][1] = int(values[1])
    SudokuBoard[0][2] = int(values[2])
    SudokuBoard[0][3] = int(values[3])
    SudokuBoard[0][4] = int(values[4])
    SudokuBoard[0][5] = int(values[5])
    SudokuBoard[0][6] = int(values[6])
    SudokuBoard[0][7] = int(values[7])
    SudokuBoard[0][8] = int(values[8])
    SudokuBoard[1][0] = int(values[9])
    SudokuBoard[1][1] = int(values[10])
    SudokuBoard[1][2] = int(values[11])
    SudokuBoard[1][3] = int(values[12])
    SudokuBoard[1][4] = int(values[13])
    SudokuBoard[1][5] = int(values[14])
    SudokuBoard[1][6] = int(values[15])
    SudokuBoard[1][7] = int(values[16])
    SudokuBoard[1][8] = int(values[17])
    SudokuBoard[2][0] = int(values[18])
    SudokuBoard[2][1] = int(values[19])
    SudokuBoard[2][2] = int(values[20])
    SudokuBoard[2][3] = int(values[21])
    SudokuBoard[2][4] = int(values[22])
    SudokuBoard[2][5] = int(values[23])
    SudokuBoard[2][6] = int(values[24])
    SudokuBoard[2][7] = int(values[25])
    SudokuBoard[2][8] = int(values[26])
    SudokuBoard[3][0] = int(values[27])
    SudokuBoard[3][1] = int(values[28])
    SudokuBoard[3][2] = int(values[29])
    SudokuBoard[3][3] = int(values[30])
    SudokuBoard[3][4] = int(values[31])
    SudokuBoard[3][5] = int(values[32])
    SudokuBoard[3][6] = int(values[33])
    SudokuBoard[3][7] = int(values[34])
    SudokuBoard[3][8] = int(values[35])
    SudokuBoard[4][0] = int(values[36])
    SudokuBoard[4][1] = int(values[37])
    SudokuBoard[4][2] = int(values[38])
    SudokuBoard[4][3] = int(values[39])
    SudokuBoard[4][4] = int(values[40])
    SudokuBoard[4][5] = int(values[41])
    SudokuBoard[4][6] = int(values[42])
    SudokuBoard[4][7] = int(values[43])
    SudokuBoard[4][8] = int(values[44])
    SudokuBoard[5][0] = int(values[45])
    SudokuBoard[5][1] = int(values[46])
    SudokuBoard[5][2] = int(values[47])
    SudokuBoard[5][3] = int(values[48])
    SudokuBoard[5][4] = int(values[49])
    SudokuBoard[5][5] = int(values[50])
    SudokuBoard[5][6] = int(values[51])
    SudokuBoard[5][7] = int(values[52])
    SudokuBoard[5][8] = int(values[53])
    SudokuBoard[6][0] = int(values[54])
    SudokuBoard[6][1] = int(values[55])
    SudokuBoard[6][2] = int(values[56])
    SudokuBoard[6][3] = int(values[57])
    SudokuBoard[6][4] = int(values[58])
    SudokuBoard[6][5] = int(values[59])
    SudokuBoard[6][6] = int(values[60])
    SudokuBoard[6][7] = int(values[61])
    SudokuBoard[6][8] = int(values[62])
    SudokuBoard[7][0] = int(values[63])
    SudokuBoard[7][1] = int(values[64])
    SudokuBoard[7][2] = int(values[65])
    SudokuBoard[7][3] = int(values[66])
    SudokuBoard[7][4] = int(values[67])
    SudokuBoard[7][5] = int(values[68])
    SudokuBoard[7][6] = int(values[69])
    SudokuBoard[7][7] = int(values[70])
    SudokuBoard[7][8] = int(values[71])
    SudokuBoard[8][0] = int(values[72])
    SudokuBoard[8][1] = int(values[73])
    SudokuBoard[8][2] = int(values[74])
    SudokuBoard[8][3] = int(values[75])
    SudokuBoard[8][4] = int(values[76])
    SudokuBoard[8][5] = int(values[77])
    SudokuBoard[8][6] = int(values[78])
    SudokuBoard[8][7] = int(values[79])
    SudokuBoard[8][8] = int(values[80])
    printBoard(SudokuBoard)
    sudokuSolver(SudokuBoard)
    
if __name__ == "__main__":
    main()
