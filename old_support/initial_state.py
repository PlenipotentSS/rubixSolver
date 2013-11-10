import copy
import random
import Tkinter, tkFileDialog

##  RubixCubeSolver.py
##  Steven Stevenson
##  CSE 415
##  Fall 2009
##
##  l_f: Red
##  r_f: Blue
##  r_b: Green
##  l_b: White
##  top: Orange
##  bottom: Yellow
##
##  beginning index [0][0] is always the top left if cube is rotated clockwise,
##  and top and bottom have beginning index at furthest left.
##

##
## Variables
################################################################################
l_f = [
        ["R","R","R"],
        ["R","R","R"],
        ["R","R","R"]]

r_f = [
        ["B","B","B"],
        ["B","B","B"],
        ["B","B","B"]]

r_b = [
        ["G","G","G"],
        ["G","G","G"],
        ["G","G","G"]]

l_b = [
        ["W","W","W"],
        ["W","W","W"],
        ["W","W","W"]]
top = [
        ["O","O","O"],
        ["O","O","O"],
        ["O","O","O"]]
bottom = [
        ["Y","Y","Y"],
        ["Y","Y","Y"],
        ["Y","Y","Y"]]

##  counter-clickwise around the cube, with top then bottom at end of sequence.
##
initial_state = [l_f, r_f, r_b, l_b, top, bottom]

##corresponding colors:
colors = ["R","B","G","W","O","Y"]

##  corners are always read from (in this order)
##                               left(front)->right(front)->up/down
##                               right(front)->right(back)->up/down
##                               right(back)->left(back)->up/down
##                               left(back)->left(front)->up/down
top_middle_corner = [ l_f[0][2], r_f[0][0], top[2][0] ]
bottom_f_middle_corner = [ l_f[0][2], r_f[0][0], bottom[2][0] ]

top_right_corner = [ r_f[0][2], r_b[0][0], top[2][2] ]
bottom_right_corner = [ l_f[0][2], r_f[0][0], bottom[2][2] ]

top_b_middle_corner = [ r_b[0][2], l_b[0][0], top[0][2] ]
bottom_b_middle_corner = [ r_b[0][2], l_b[0][0], bottom[0][2] ]

top_left_corner = [ l_b[0][2], l_f[0][0], top[0][0] ]
bottom_left_corner = [ l_b[0][2], l_f[0][0], bottom[0][0] ]



##
## FUNCTIONS
################################################################################

## Prepares the rubix cube
##          Choose: to  1) randomize a cube
##                      2) load a given cube from file
##
def prepare():
    output = ""
    output += ""
    print output
    print ""
    state = initial_state
    rdy = False
    global utter
    utter = True
    for i in range(5):
        if rdy:
            break
        fromFile = raw_input("Would you like to load a configuration? (Y/N) ")
        if fromFile == "Y" or fromFile == "y":
            theFile = None
            root = Tkinter.Tk()
            theFile = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
            if theFile != None:
                state = readFromFile(state, theFile)
                if state == -1:
                    break
                else:
                    rdy = True
                    break
            else:
                print "No output Selected."
                break
        elif fromFile == "N" or fromFile =="n":
            for j in range(5):
                toRandom = raw_input("Would you like me to randomize a cube" + \
                           " for you? (Y/N) ")
                if toRandom == "Y" or toRandom == "y":
                    state = randomize(state)
                    rdy = True
                    break
                elif toRandom == "N" or toRandom == "n":
                    print "You chose to start of with a rubix cube with its " \
                            +  "initial state."
                    rdy = True
                    break
                else:
                    print "We don't recognize that input."
        else:
            print "We don't recognize that input."
    if not rdy:
        "Sorry you're having trouble, try inputing better values next time"
        return
    else:
        for i in range(5):
            printUtter = raw_input("Print Utterances? (Y/N) ")
            if printUtter == "Y" or printUtter == "y":
                utter = True
                break
            if printUtter == "N" or printUtter == "n":
                utter = False
                break
            else:
                "We don't recognize that input."
        print_rubix(state)
        print "OK"
        global state_stored
        state_stored = state
        return state

def readFromFile(state, theFile):
    newState = copy.deepcopy(state)
    line = theFile.read()
    line = str(line)
    err = False
    if line.count("R") == 9 and line.count("B") == 9 and line.count("G") == 9 and \
                    line.count("W") == 9 and line.count("O") == 9 and \
                    line.count("Y") == 9 and len(line) == 54:
        print "Processing..."
        row = -1
        for i in range(9):
            col = i%3
            if col == 0: row += 1
            newState[4][row][col] = line[i]
        thisSide = -1
        row = 0
        for i in range(9,45):
            col = i%3
            if col == 0: thisSide += 1
            if thisSide > 3:
                thisSide = 0
                row += 1
            newState[thisSide][row][col] = line[i]
        row = -1
        for i in range(45,54):
            col = i%3
            if col == 0: row += 1
            newState[5][row][col] = line[i]        
    else:
        print "Your file is not configured properly"
        
        return -1
    return newState

def saveToFile(state):
    output = ""
    row = -1
    for i in range(9):
        col = i%3
        if col == 0: row += 1
        output += state[4][row][col]
    thisSide = -1
    row = 0
    for i in range(9,45):
        col = i%3
        if col == 0: thisSide += 1
        if thisSide > 3:
            thisSide = 0
            row += 1
        output += state[thisSide][row][col]
    row = -1
    for i in range(45,54):
        col = i%3
        if col == 0: row += 1
        output += state[5][row][col]
    theFile = open("layout.txt", "w")
    theFile.write(output)
    theFile.close()

## row is   1: panel
##          2: middle
##          3: bottom
def horizontal_rotate(state, row, LorR):
    global utter
    if utter:
        print "Rotating Horizontally \"" + LorR + "\" with row " + \
              str(row) + "."
    row = row-1
    newState = copy.deepcopy(state)
    if LorR == "L":
        tmp = newState[0][row]
        for i in range(3):
            newState[i][row] = newState[i+1][row]
        newState[3][row] = tmp
        #move top/bottom clockwise
        if row == 0 or 2:
            if row == 0:
                panel = newState[4]
            else:
                panel = newState[5]
            #move corners 
            tmp = panel[0][0]
            panel[0][0] = panel[2][0]
            panel[2][0] = panel[2][2]
            panel[2][2] = panel[0][2]
            panel[0][2] = tmp
            #move edges 
            tmp = panel[0][1]
            panel[0][1] = panel[1][0]
            panel[1][0] = panel[2][1]
            panel[2][1] = panel[1][2]
            panel[1][2] = tmp
    if LorR == "R":
        tmp = newState[3][row]
        for i in range(3):
            j = 3-i
            newState[j][row] = newState[j-1][row]
        newState[0][row] = tmp
        #move top/bottom counter-clockwise
        if row == 0 or 2:
            if row == 0:
                panel = newState[4]
            else:
                panel = newState[5]
            #move corners 
            tmp = panel[0][0]
            panel[0][0] = panel[0][2]
            panel[0][2] = panel[2][2]
            panel[2][2] = panel[2][0]
            panel[2][0] = tmp
            #move edges 
            tmp = panel[0][1]
            panel[0][1] = panel[1][2]
            panel[1][2] = panel[2][1]
            panel[2][1] = panel[1][0]
            panel[1][0] = tmp
    global state_stored
    state_stored = newState
    return newState


## col is   1: left
##          2: middle
##          3: right
## U : Up
## D : Down
## LR : Left Front / Right Back
## RL : Right Front / Left Back
def vertical_rotate(state, col, UorD, LRorRL):
    global utter
    if utter:
        print "Rotating Verticaly    \"" + UorD + "\" with face:" + \
              LRorRL + " with column " + str(col) + "."
    col = col-1
    newState = copy.deepcopy(state)
    if UorD == "U":
        faceInd = 0
        if LRorRL == "LR":
            ##Left and Right AWAY (UP)
            if col == 0 or col == 2:
                if col == 0:
                    panel = newState[3]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[0][2]
                    panel[0][2] = panel[2][2]
                    panel[2][2] = panel[2][0]
                    panel[2][0] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][2]
                    panel[1][2] = panel[2][1]
                    panel[2][1] = panel[1][0]
                    panel[1][0] = tmp    
                else:
                    panel = newState[1]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[2][0]
                    panel[2][0] = panel[2][2]
                    panel[2][2] = panel[0][2]
                    panel[0][2] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][0]
                    panel[1][0] = panel[2][1]
                    panel[2][1] = panel[1][2]
                    panel[1][2] = tmp
            ##rotate moves up
            ##
            tmp1 = newState[faceInd][0][col]
            tmp2 = newState[faceInd][1][col]
            tmp3 = newState[faceInd][2][col]
            ##replace front with bottom
            newState[faceInd][0][col] = newState[5][2-col][0]
            newState[faceInd][1][col] = newState[5][2-col][1]
            newState[faceInd][2][col] = newState[5][2-col][2]
            ##replace bottom with back
            newState[5][2-col][0] = newState[faceInd+2][2][2-col]
            newState[5][2-col][1] = newState[faceInd+2][1][2-col]
            newState[5][2-col][2] = newState[faceInd+2][0][2-col]
            ##replace back with top
            newState[faceInd+2][0][2-col] = newState[4][col][0]
            newState[faceInd+2][1][2-col] = newState[4][col][1]
            newState[faceInd+2][2][2-col] = newState[4][col][2]
            ##replace top with front
            newState[4][col][2] = tmp1
            newState[4][col][1] = tmp2
            newState[4][col][0] = tmp3
        if LRorRL == "RL":
            faceInd = 1
            ##Left and Right AWAY (UP)
            if col == 0 or col == 2:
                if col == 0:
                    panel = newState[0]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[0][2]
                    panel[0][2] = panel[2][2]
                    panel[2][2] = panel[2][0]
                    panel[2][0] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][2]
                    panel[1][2] = panel[2][1]
                    panel[2][1] = panel[1][0]
                    panel[1][0] = tmp
                else:
                    panel = newState[2]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[2][0]
                    panel[2][0] = panel[2][2]
                    panel[2][2] = panel[0][2]
                    panel[0][2] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][0]
                    panel[1][0] = panel[2][1]
                    panel[2][1] = panel[1][2]
                    panel[1][2] = tmp
            ##rotate moves up
            ##
            tmp1 = newState[faceInd][0][col]
            tmp2 = newState[faceInd][1][col]
            tmp3 = newState[faceInd][2][col]
            ##replace front with bottom
            newState[faceInd][0][col] = newState[5][0][col]
            newState[faceInd][1][col] = newState[5][1][col]
            newState[faceInd][2][col] = newState[5][2][col]
            ##replace bottom with back
            newState[5][0][col] = newState[faceInd+2][2][2-col]
            newState[5][1][col] = newState[faceInd+2][1][2-col]
            newState[5][2][col] = newState[faceInd+2][0][2-col]
            ##replace back with top
            newState[faceInd+2][2][2-col] = newState[4][0][col]
            newState[faceInd+2][1][2-col] = newState[4][1][col]
            newState[faceInd+2][0][2-col] = newState[4][2][col]
            ##replace top with front
            newState[4][0][col] = tmp1
            newState[4][1][col] = tmp2
            newState[4][2][col] = tmp3
    if UorD == "D":
        faceInd = 0
        if LRorRL == "LR":
            if col == 0 or col == 2:
                if col == 0:
                    panel = newState[3]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[2][0]
                    panel[2][0] = panel[2][2]
                    panel[2][2] = panel[0][2]
                    panel[0][2] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][0]
                    panel[1][0] = panel[2][1]
                    panel[2][1] = panel[1][2]
                    panel[1][2] = tmp
                else:
                    panel = newState[1]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[0][2]
                    panel[0][2] = panel[2][2]
                    panel[2][2] = panel[2][0]
                    panel[2][0] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][2]
                    panel[1][2] = panel[2][1]
                    panel[2][1] = panel[1][0]
                    panel[1][0] = tmp          
            ##rotate moves down
            ##
            tmp1 = newState[faceInd][0][col]
            tmp2 = newState[faceInd][1][col]
            tmp3 = newState[faceInd][2][col]
            ##replace front with top
            newState[faceInd][2][col] = newState[4][col][0]
            newState[faceInd][1][col] = newState[4][col][1]
            newState[faceInd][0][col] = newState[4][col][2]
            ##replace top with back
            newState[4][col][0] = newState[faceInd+2][0][2-col]
            newState[4][col][1] = newState[faceInd+2][1][2-col]
            newState[4][col][2] = newState[faceInd+2][2][2-col]
            ##replace back with bottom
            newState[faceInd+2][0][2-col] = newState[5][2-col][2]
            newState[faceInd+2][1][2-col] = newState[5][2-col][1]
            newState[faceInd+2][2][2-col] = newState[5][2-col][0]
            ##replace bottom with front
            newState[5][2-col][0] = tmp1
            newState[5][2-col][1] = tmp2
            newState[5][2-col][2] = tmp3
        if LRorRL == "RL":
            faceInd = 1
            if col == 0 or col == 2:
                if col == 0:
                    panel = newState[0]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[2][0]
                    panel[2][0] = panel[2][2]
                    panel[2][2] = panel[0][2]
                    panel[0][2] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][0]
                    panel[1][0] = panel[2][1]
                    panel[2][1] = panel[1][2]
                    panel[1][2] = tmp
                else:
                    panel = newState[2]
                    #move corners 
                    tmp = panel[0][0]
                    panel[0][0] = panel[0][2]
                    panel[0][2] = panel[2][2]
                    panel[2][2] = panel[2][0]
                    panel[2][0] = tmp
                    #move edges 
                    tmp = panel[0][1]
                    panel[0][1] = panel[1][2]
                    panel[1][2] = panel[2][1]
                    panel[2][1] = panel[1][0]
                    panel[1][0] = tmp
            ##rotate moves down
            ##
            tmp1 = newState[faceInd][0][col]
            tmp2 = newState[faceInd][1][col]
            tmp3 = newState[faceInd][2][col]
            ##replace front with top
            newState[faceInd][0][col] = newState[4][0][col]
            newState[faceInd][1][col] = newState[4][1][col]
            newState[faceInd][2][col] = newState[4][2][col]
            ##replace top with back
            newState[4][0][col] = newState[faceInd+2][2][2-col]
            newState[4][1][col] = newState[faceInd+2][1][2-col]
            newState[4][2][col] = newState[faceInd+2][0][2-col]
            ##replace back with bottom
            newState[faceInd+2][2][2-col] = newState[5][0][col]
            newState[faceInd+2][1][2-col] = newState[5][1][col]
            newState[faceInd+2][0][2-col] = newState[5][2][col]
            ##replace bottom with front
            newState[5][0][col] = tmp1
            newState[5][1][col] = tmp2
            newState[5][2][col] = tmp3
    global state_stored
    state_stored = newState
    return newState

def printUtterances(default):
    global utter
    if default:
        utter = True
    else:
        utter = False

def randomize(state):
    newState = copy.deepcopy(state)
    numRotations = random.choice(range(5,10))
    for i in range(numRotations):
        operators = ["vertical","horizontal"]
        choice = random.choice(operators)
        if choice == "vertical":
            UorD = random.choice(["U","D"])
            RLorLR = random.choice(["LR","RL"])
            col = random.choice([1,2,3])
            newState = vertical_rotate(newState, col, UorD, RLorLR)
        if choice == "horizontal":
            LorR = random.choice(["L","R"])
            row = random.choice([1,2,3])
            newState = horizontal_rotate(newState, row, LorR)
    return newState

def finished_side(side,col):
    for i in range(len(side)):
        if side[i].count(col) != 3:
            return False
    return True

def has_won(state):
    for i in range(len(state)):
        if not finished_side(state[i],colors[i]):
            return False
    return True

def print_disp_help():
    print "                   [   top  ]"
    print "          [ l_f ]  [   r_f  ]  [ r_b ] [ l_b ]"
    print "                   [ bottom ]"

def print_rubix(state):
    print " "
    for i in range(3):
        print "                " + str(state[4][i])
    print "                " + "..............."
    for i in range(3):
        print str(state[0][i]) + " " + str(state[1][i]) + " " + \
              str(state[2][i])+ " " + str(state[3][i])
    print "                " + "..............."
    for i in range(3):
        print "                " + str(state[5][i])
    print " "


##
## MAIN
################################################################################

newState = prepare()
while True:
    userInput = raw_input("What would you like to do? (Q for Quit) ")
    if userInput == "Q" or userInput == "q":
        print "Thanks for playing"
        break
    if userInput == "help" or userInput == "?":
        print "++++++ COMMANDS ++++++"
        print "layout_form:        Prints the layout of the rubix cube"
        print "save:               Saves the current cube configuration"
        print "rotate:"
        print "     vert : Vertically"
        print "         Face [LR or RL]: Rotates vertically from either left "
        print "                      front (LR) or right front (RL)."
        print "         Column [1,2,3]: rotates column number (1-3)"
        print "         Up or Down [U or D]: Rotates the column, up or down."
        print "     hori : Horizontally"
        print "         Row [1,2,3]: rotates row number (1-3)"
        print "         Left or Right [L or R]: Rotates the row, left or right."
    if userInput == "layout_form":
        print_disp_help()
    if userInput == "save":
        global state_stored
        saveToFile(state_stored)
    if userInput == "rotate":
        rotateInput = raw_input("vert or hori? ")
        if rotateInput == "vert":
            faceInput = raw_input("Face [LR or RL]? ")
            colInput = raw_input("Column [1,2,3]? ")
            UorDInput = raw_input("Up or Down [U or D]? ")
            if not 4 > int(colInput) > 0 or faceInput != "LR" and faceInput != "RL" or \
                       UorDInput != "U" and UorDInput != "D":
                print "Your input is not recognized"
            else:
                print ""
                print " "
                newState = vertical_rotate(newState, int(colInput), UorDInput, faceInput)
                print_rubix(newState)
        elif rotateInput == "hori":
            rowInput = raw_input("Row [1,2,3]? ")
            LorRInput = raw_input("Left or Right [L or R]? ")
            if not 4 > int(rowInput) > 0 or LorRInput != "L" and LorRInput != "R":
                print "Your input is not recognized"
            else:
                print " "
                print " "
                newState = horizontal_rotate(newState, int(rowInput), LorRInput)
                print_rubix(newState)
        else:    
            print "Your input is not recognized"
