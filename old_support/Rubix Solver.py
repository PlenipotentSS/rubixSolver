'''
mySolver.py
Steven Stevenson


'''
import rubixTStar as TStar
import copy
import random
import Tkinter, tkFileDialog
from Tkinter import *

##
## FUNCTIONS
################################################################################

## Prepares the rubix cube
##
def prepare():
    global initial_state, state_stored
    output = ""
    output += ""
    print output
    print ""
    state = initial_state
    utter = True
    if utter: print_rubix(state)
    print "OK"
    state_stored = state
    return state

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
    return newState

##
## HELPERS
################################################################################

def successors(s):
    original = copy.deepcopy(s)
    sList = []
    sList += [horizontal_rotate(original,1,"L")]
    sList += [horizontal_rotate(original,2,"L")]
    sList += [horizontal_rotate(original,3,"L")]
    sList += [horizontal_rotate(original,1,"R")]
    sList += [horizontal_rotate(original,2,"R")]
    sList += [horizontal_rotate(original,3,"R")]

    sList += [vertical_rotate(original, 1, "U", "LR")]
    sList += [vertical_rotate(original, 2, "U", "LR")]
    sList += [vertical_rotate(original, 3, "U", "LR")]
    sList += [vertical_rotate(original, 1, "D", "LR")]
    sList += [vertical_rotate(original, 2, "D", "LR")]
    sList += [vertical_rotate(original, 3, "D", "LR")]
    
    sList += [vertical_rotate(original, 1, "U", "RL")]
    sList += [vertical_rotate(original, 2, "U", "RL")]
    sList += [vertical_rotate(original, 3, "U", "RL")]
    sList += [vertical_rotate(original, 1, "D", "RL")]
    sList += [vertical_rotate(original, 2, "D", "RL")]
    sList += [vertical_rotate(original, 3, "D", "RL")]
    titles = ["hor_l_on_1","hor_l_on_2","hor_l_on_3",
                "hor_r_on_1","hor_r_on_2","hor_r_on_3",
                "ver_lr_u_on_1","ver_lr_u_on_2","ver_lr_u_on_3",
                "ver_lr_d_on_1","ver_lr_d_on_2","ver_lr_d_on_3",
                "ver_rl_u_on_1","ver_rl_u_on_2","ver_rl_u_on_3",
                "ver_rl_d_on_1","ver_rl_d_on_2","ver_rl_d_on_3"]
    return [titles, sList]

def print_successors():
    global state_stored
    titles, sList = successors(state_stored)
    print titles
    for i in range(len(sList)):
        TStar.TREE_DISP.selected_node = TStar.NODE_CLASS(TStar.INITIAL_STATE)
        node = TStar.TREE_DISP.selected_node
        for o in TStar.OPERATORS:
            if o.id == titles[i]:
                print o.id
                break
            #print titles[i]
            #print_rubix(sList[i])

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

def saveToFile():
    global state_stored
    state = state_stored
    output = convert_toLine(state)
    theFile = open("layout.txt", "w")
    theFile.write(output)
    theFile.close()

def convert_toLine(state):
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
    return output

def printUtterances(default):
    global utter
    if default:
        utter = True
    else:
        utter = False

def finished_side(side):
    col = side[0][0]
    for i in range(len(side)):
        if side[i].count(col) != 3:
            return False
    return True

def has_won(state):
    for i in range(len(state)):
        if not finished_side(state[i]):
            return False
    return True

def has_layer1(state):
    if not finished_side(state[4]):
        return False
    side = -1
    row = -1
    for i in range(12):
        j = i % 3
        if j == 0:
            side += 1
            thisColor = state[side][0][j]
        if state[side][0][j] != thisColor:
            return False    
    return True

def has_layer2(state):
    side = -1
    row = -1
    for i in range(12):
        j = i % 3
        if j == 0:
            side += 1
            thisColor = state[side][0][j]
        if state[side][1][j] != thisColor:
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
## FUNCTIONS TO LOAD CUBES
################################################################################

def randomize_global():
    global initial_State, utter
    newState2 = copy.deepcopy(initial_state)
    numRotations = random.choice(range(3,15))
    for i in range(numRotations):
        operators = ["vertical","horizontal"]
        choice = random.choice(operators)
        if choice == "vertical":
            UorD = random.choice(["U","D"])
            RLorLR = random.choice(["LR","RL"])
            col = random.choice([1,2,3])
            newState2 = vertical_rotate(newState2, col, UorD, RLorLR)
        if choice == "horizontal":
            LorR = random.choice(["L","R"])
            row = random.choice([1,2,3])
            newState2 = horizontal_rotate(newState2, row, LorR)
    if utter: print_rubix(newState2)
    TStar.INITIAL_DATA = newState2
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    global state_stored
    state_stored = newState2
    return 

def cube_ina_cube():
    global utter
    l_f = [
            ["B","R","R"],
            ["B","R","R"],
            ["B","B","B"]]

    r_f = [
            ["B","B","O"],
            ["B","B","O"],
            ["O","O","O"]]

    r_b = [
            ["W","W","W"],
            ["W","G","G"],
            ["W","G","G"]]

    l_b = [
            ["Y","Y","Y"],
            ["W","W","Y"],
            ["W","W","Y"]]
    top = [
            ["R","R","R"],
            ["O","O","R"],
            ["O","O","R"]]
    bottom = [
            ["G","G","G"],
            ["G","Y","Y"],
            ["G","Y","Y"]]
    newState = [l_f, r_f, r_b, l_b, top, bottom]
    if utter: print_rubix(newState)
    TStar.INITIAL_DATA = newState
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    global state_stored
    state_stored = newState
    return     

def twisted_rings():
    global utter
    l_f = [
            ["R","B","R"],
            ["R","B","B"],
            ["R","R","R"]]

    r_f = [
            ["B","O","B"],
            ["O","O","B"],
            ["B","B","B"]]

    r_b = [
            ["G","G","G"],
            ["G","W","W"],
            ["G","W","G"]]

    l_b = [
            ["W","W","W"],
            ["Y","Y","W"],
            ["W","Y","W"]]
    top = [
            ["O","O","O"],
            ["R","R","O"],
            ["O","R","O"]]
    bottom = [
            ["Y","Y","Y"],
            ["Y","G","G"],
            ["Y","G","Y"]]
    newState = [l_f, r_f, r_b, l_b, top, bottom]
    if utter: print_rubix(newState)
    TStar.INITIAL_DATA = newState
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    global state_stored
    state_stored = newState
    return

def completed_cube():
    global initial_state, utter
    if utter: print_rubix(initial_state)
    TStar.INITIAL_DATA = initial_state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    global state_stored
    state_stored = newState
    return

def load_from_file():
    global initial_state
    theFile = None
    theFile = tkFileDialog.askopenfile(mode='rb',title='Choose a file')
    if theFile != None:
        newState = readFromFile(initial_state, theFile)
        TStar.INITIAL_DATA = newState
        TStar.create_initial_state()
        TStar.initialize_states_and_display()
        global state_stored
        state_stored = newState
        return
    else:
        print "Failed Load."
        return

##
## FUNCTIONS TO SOLVE CUBES
################################################################################

def solve_layer1():
    global state_stored
    print_rubix(state_stored)
    path = solve_bfs_1(state_stored, [])
    print "done"
    print " "
    if path == None or len(path) == 0:
        print "Given layer is Solved"
    else:
        output = []
        node = TStar.NODE_CLASS(TStar.INITIAL_STATE)
        for i in range(len(path)):
            output += ["Step " + str(i+1) + ": " + path[i]]
            for o in TStar.OPERATORS:
                if o.id == path[i]:
                    TStar.TREE_DISP.selected_node = node
                    succ = o._apply(node.s)
                    new_node = TStar.TREE_DISP.node_class(succ)
                    TStar.TREE_DISP.state_node_hash[succ] = new_node
                    TStar.TREE_DISP.all_nodes.append(new_node)
                    TStar.ALL_STATES.append(succ)
                    node = new_node
                    break
        global last_sol_node
        last_sol_node = node
        for out in output:
            print out
        TStar.redraw_tree()
    return path

def solve_layer12():
    path = solve_layer1()
    path += solve_layer2()
    if len(path) == 0:
        print "Top 2 given layers are Solved."
    return path
    
def solve_cube():
    path = solve_layer12()
    path += solve_cube_layer3()
    if len(path) == 0:
        print "Cube Given is already Solved."
    return

def solve_layer2():
    global solution_1_stored, last_sol_node
    print_rubix(solution_1_stored)
    path = solve_bfs_2(solution_1_stored, [])
    print "done"
    print " "
    if path == None or len(path) == 0:
        print "Given layer is Solved"
    else:
        output = []
        node = last_sol_node
        for i in range(len(path)):
            temp = path.pop()
            path.append(temp)
            output += ["Step " + str(i+1) + ": " + temp]
            for o in TStar.OPERATORS:
                if o.id == path[i]:
                    TStar.TREE_DISP.selected_node = node
                    succ = o._apply(node.s)
                    new_node = TStar.TREE_DISP.node_class(succ)
                    TStar.TREE_DISP.state_node_hash[succ] = new_node
                    TStar.TREE_DISP.all_nodes.append(new_node)
                    TStar.ALL_STATES.append(succ)
                    node = new_node
                    break
        last_sol_node = node
        for out in output:
            print out
        TStar.redraw_tree()
    return path

def solve_cube_layer3():
    global solution_2_stored, last_sol_node
    print_rubix(solution_2_stored)
    path = solve_bfs_3(solution_2_stored, [])
    print "done"
    print " "
    if path == None or len(path) == 0:
        print "Given layer is Solved"
    else:
        output = []
        node = last_sol_node
        for i in range(len(path)):
            temp = path.pop()
            path.append(temp)
            output += ["Step " + str(i+1) + ": " + temp]
            for o in TStar.OPERATORS:
                if o.id == path[i]:
                    TStar.TREE_DISP.selected_node = node
                    succ = o._apply(node.s)
                    new_node = TStar.TREE_DISP.node_class(succ)
                    TStar.TREE_DISP.state_node_hash[succ] = new_node
                    TStar.TREE_DISP.all_nodes.append(new_node)
                    TStar.ALL_STATES.append(succ)
                    node = new_node
                    break
        for out in output:
            print out
        TStar.redraw_tree()
    return path

def succ_in_set(state, OorC):
    for i in range(len(OorC)):
        if state == OorC[i]:
            return True
    return False

def solve_bfs_1(thisState, path):
    OPEN = [([],thisState)]
    CLOSED = []
    while OPEN != []:
        thisS = OPEN[0]
        OPEN = OPEN[1:]
        CLOSED.append(thisS)
        s = thisS[1]
        p = thisS[0]
        path += [p]
        #print p
        if has_layer1(s):
            global solution_1_stored
            solution_1_stored = s
            print_rubix(s)
            return path[0]
        titles, lst = successors(s)
        for i in range(len(lst)):
            if succ_in_set(lst,CLOSED):
                lst.pop(i)
                titles.pop(i)
        for i in range(len(lst)):
            if succ_in_set(lst,OPEN):
                lst.pop(i)
                titles.pop(i)
        path.pop()
        # the new successors are added to the end of OPEN:
        newL = []
        for i in range(len(lst)):
            a = copy.deepcopy(p)
            a += [titles[i]]
            newP = a
            newL += [( newP, lst[i])]
        OPEN = OPEN + newL
    return path


def solve_bfs_2(thisState, path):
    OPEN = [([],thisState)]
    CLOSED = []
    while OPEN != []:
        thisS = OPEN[0]
        OPEN = OPEN[1:]
        CLOSED.append(thisS)
        s = thisS[1]
        p = thisS[0]
        path += [p]
        #print p
        if has_layer1(s) and has_layer2(s):
            global solution_2_stored
            solution_2_stored = s
            print_rubix(s)
            return path[0]
        titles, lst = successors(s)
        for i in range(len(lst)):
            if succ_in_set(lst,CLOSED):
                lst.pop(i)
                titles.pop(i)
        for i in range(len(lst)):
            if succ_in_set(lst,OPEN):
                lst.pop(i)
                titles.pop(i)
        path.pop()
        # the new successors are added to the end of OPEN:
        newL = []
        for i in range(len(lst)):
            a = copy.deepcopy(p)
            a += [titles[i]]
            newP = a
            newL += [( newP, lst[i])]
        OPEN = OPEN + newL
    return path

def solve_bfs_3(thisState, path):
    OPEN = [([],thisState)]
    CLOSED = []
    while OPEN != []:
        thisS = OPEN[0]
        OPEN = OPEN[1:]
        CLOSED.append(thisS)
        s = thisS[1]
        p = thisS[0]
        path += [p]
        #print p
        if has_won(s):
            print_rubix(s)
            return path[0]
        titles, lst = successors(s)
        for i in range(len(lst)):
            if succ_in_set(lst,CLOSED):
                lst.pop(i)
                titles.pop(i)
        for i in range(len(lst)):
            if succ_in_set(lst,OPEN):
                lst.pop(i)
                titles.pop(i)
        path.pop()
        # the new successors are added to the end of OPEN:
        newL = []
        for i in range(len(lst)):
            a = copy.deepcopy(p)
            a += [titles[i]]
            newP = a
            newL += [( newP, lst[i])]
        OPEN = OPEN + newL
    return path
            
##def solve1_recursive(thisState, CLOSED, path):
##    print_rubix(thisState)
##    if has_layer1(thisState):
##        return path
##    titles, sList = successors()
##    for i in range(len(sList)):
##        OPEN = []
##        if not succ_in_closed(sList[i],CLOSED):
##            OPEN.append((titles[i],sList[i]))
##            CLOSED.append(sList[i])
##        for thisSucc in OPEN:
##            if has_layer1(thisSucc[1]):
##                print_rubix(thisSucc[1])
##                path += [thisSucc[0]]
##                return path
##            path += [thisSucc[0]]
##            thisP = solve1_recursive(thisSucc[1],CLOSED,path)
##            if thisP != None:
##                path += thisP
##                return path
##    return

##
## Variables
################################################################################
utter = False

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

initial_state = [l_f, r_f, r_b, l_b, top, bottom]
newState = prepare()

##
##  T* Menus
################################################################################

def add_app_specific_menus(menubar):
  saveMenu = Menu(menubar)
  menubar.add_cascade(label="Cube I/O", menu=saveMenu)
  saveMenu.add_command(label="Load Initial State...", command=load_from_file)
  saveMenu.add_command(label="Save Initial State...", command=saveToFile)
  cubeMenu = Menu(menubar)
  menubar.add_cascade(label="Cube Patterns", menu=cubeMenu)
  cubeMenu.add_command(label="Completed Cube", command=completed_cube)
  cubeMenu.add_command(label="Randomize", command=randomize_global)
  cubeMenu.add_command(label="Cube in a Cube", command=cube_ina_cube)
  cubeMenu.add_command(label="Twisted Rings", command=twisted_rings)
  smartMenu = Menu(menubar)
  menubar.add_cascade(label="Smart Solve", menu=smartMenu)
  solveMenu = Menu(menubar)
  menubar.add_cascade(label="Solve with BDFS", menu=solveMenu)
  solveMenu.add_command(label="Solve 1st Layer", command=solve_layer1)
  solveMenu.add_command(label="Solve 1st & 2nd Layer",command=solve_layer12)
  solveMenu.add_command(label="Solve Cube", command=solve_cube)
#  extraMenu = Menu(menubar)
#  menubar.add_cascade(label="Extra", menu=extraMenu)
#  extraMenu.add_command(label="Print Successors", command=print_successors)
  

##
## T* Graphic Representation
################################################################################
def register_t_star_modifications():
  TStar.__dict__.update({
    'TITLE':" Rubix Cube Solver with T*",
    'NODE_CLASS': MySolver_Node,
    'INITIAL_DATA': INITIAL_DATA,
    'add_app_specific_menus': add_app_specific_menus
    })

INITIAL_DATA = newState
class MySolver_Node(TStar.Node):
    width = 85 ; height = 70
    def domain_specific_init(self, state):
        self.display_elements = []

    def paint_content(self,w,h,a_canvas):
        """Adds the node's blocks and labels to the canvas
           at the right place."""
        self.has_painted_content=True
        ##l_f
        x = 0
        y = 4
        for row in range(3):
          for col in range(3):
            letter = self.s.data[0][2-row][col]
            self.draw_block(letter, x, y, a_canvas, w, h)
            x += 1
            if x%3 == 0:
              x = 0
              y += 1
        ##r_f
        x = 4
        y = 4
        for row in range(3):
          for col in range(3):
            letter = self.s.data[1][2-row][col]
            self.draw_block(letter, x, y, a_canvas, w, h)
            x += 1
            if (x-1)%3 == 0:
              x = 4
              y += 1
        ##r_b
        x = 8
        y = 4
        for row in range(3):
          for col in range(3):
            letter = self.s.data[2][2-row][col]
            self.draw_block(letter, x, y, a_canvas, w, h)
            x += 1
            if (x-2)%3 == 0:
              x = 8
              y += 1
        ##l_b
        x = 12
        y = 4
        for row in range(3):
          for col in range(3):
            letter = self.s.data[3][2-row][col]
            self.draw_block(letter, x, y, a_canvas, w, h)
            x += 1
            if x%3 == 0:
              x = 12
              y += 1
        ##top
        x = 4
        y = 8
        for row in range(3):
          for col in range(3):
            letter = self.s.data[4][2-row][col]
            self.draw_block(letter, x, y, a_canvas, w, h)
            x += 1
            if (x-1)%3 == 0:
              x = 4
              y += 1
        ##bottom
        x = 4
        y = 0
        for row in range(3):
          for col in range(3):
            letter = self.s.data[5][2-row][col]
            self.draw_block(letter, x, y, a_canvas, w, h)
            x += 1
            if (x-1)%3 == 0:
              x = 4
              y += 1
        
    def unpaint_content(self,a_canvas):
        """deletes the node's blocks and labels from the canvas."""
        if self.has_painted_content:
            #a_canvas.delete(self.p)
            for elt in self.display_elements:
                a_canvas.delete(elt)
            self.display_elements = []
        self.has_painted_content=False
    def draw_block(self, letter, lx, ly, a_canvas, w, h):
        """Helper function for paint_content."""
        e = 5 # box spacing between centers
        m = 5 # size of box
        q = 5  # bottom margin
        if letter == "R":
            self.display_elements.append(
              a_canvas.create_rectangle(self.x+5-w/2   + lx*e, self.y+h/2-q-m - ly*e,
                                        self.x+5-w/2+m + lx*e, self.y+h/2-q   - ly*e,
                                        fill="Red"))
        if letter == "B":
            self.display_elements.append(
              a_canvas.create_rectangle(self.x+5-w/2   + lx*e, self.y+h/2-q-m - ly*e,
                                        self.x+5-w/2+m + lx*e, self.y+h/2-q   - ly*e,
                                        fill="Blue"))
        if letter == "G":
            self.display_elements.append(
              a_canvas.create_rectangle(self.x+5-w/2   + lx*e, self.y+h/2-q-m - ly*e,
                                        self.x+5-w/2+m + lx*e, self.y+h/2-q   - ly*e,
                                        fill="Green"))
        if letter == "W":
            self.display_elements.append(
              a_canvas.create_rectangle(self.x+5-w/2   + lx*e, self.y+h/2-q-m - ly*e,
                                        self.x+5-w/2+m + lx*e, self.y+h/2-q   - ly*e,
                                        fill="White"))
        if letter == "O":
            self.display_elements.append(
              a_canvas.create_rectangle(self.x+5-w/2   + lx*e, self.y+h/2-q-m - ly*e,
                                        self.x+5-w/2+m + lx*e, self.y+h/2-q   - ly*e,
                                        fill="Orange"))
        if letter == "Y":
            self.display_elements.append(
              a_canvas.create_rectangle(self.x+5-w/2   + lx*e, self.y+h/2-q-m - ly*e,
                                        self.x+5-w/2+m + lx*e, self.y+h/2-q   - ly*e,
                                        fill="Yellow"))
        return

register_t_star_modifications()

##
##  T* OPERATORS
################################################################################

hor_l_on_1 = TStar.Operator("hor_l_on_1",
                            "Horizontally Rotate Left on Row 1",
               lambda w: horizontal_rotate(w,1,"L"))
hor_l_on_2 = TStar.Operator("hor_l_on_2",
                            "Horizontally Rotate Left on Row 2",
               lambda w: horizontal_rotate(w,2,"L"))
hor_l_on_3 = TStar.Operator("hor_l_on_3",
                            "Horizontally Rotate Left on Row 3",
               lambda w: horizontal_rotate(w,3,"L"))
hor_r_on_1 = TStar.Operator("hor_r_on_1",
                            "Horizontally Rotate Right on Row 1",
               lambda w: horizontal_rotate(w,1,"R"))
hor_r_on_2 = TStar.Operator("hor_r_on_2",
                            "Horizontally Rotate Right on Row 2",
               lambda w: horizontal_rotate(w,2,"R"))
hor_r_on_3 = TStar.Operator("hor_r_on_3",
                            "Horizontally Rotate Right on Row 3",
               lambda w: horizontal_rotate(w,3,"R"))

ver_lr_u_on_1 = TStar.Operator("ver_lr_u_on_1",
                               "Vertically Rotate Up with LR on Row 1",
               lambda w: vertical_rotate(w, 1, "U", "LR"))
ver_lr_u_on_2 = TStar.Operator("ver_lr_u_on_2",
                               "Vertically Rotate Up with LR on Row 2",
               lambda w: vertical_rotate(w, 2, "U", "LR"))
ver_lr_u_on_3 = TStar.Operator("ver_lr_u_on_3",
                               "Vertically Rotate Up with LR on Row 3",
               lambda w: vertical_rotate(w, 3, "U", "LR"))
ver_lr_d_on_1 = TStar.Operator("ver_lr_d_on_1",
                               "Vertically Rotate Down with LR on Row 1",
               lambda w: vertical_rotate(w, 1, "D", "LR"))
ver_lr_d_on_2 = TStar.Operator("ver_lr_d_on_2",
                               "Vertically Rotate Down with LR on Row 2",
               lambda w: vertical_rotate(w, 2, "D", "LR"))
ver_lr_d_on_3 = TStar.Operator("ver_lr_d_on_3",
                               "Vertically Rotate Down with LR on Row 3",
               lambda w: vertical_rotate(w, 3, "D", "LR"))

ver_rl_u_on_1 = TStar.Operator("ver_rl_u_on_1",
                               "Vertically Rotate Up with RL on Row 1",
               lambda w: vertical_rotate(w, 1, "U", "RL"))
ver_rl_u_on_2 = TStar.Operator("ver_rl_u_on_2",
                               "Vertically Rotate Up with RL on Row 2",
               lambda w: vertical_rotate(w, 2, "U", "RL"))
ver_rl_u_on_3 = TStar.Operator("ver_rl_u_on_3",
                               "Vertically Rotate Up with RL on Row 3",
               lambda w: vertical_rotate(w, 3, "U", "RL"))
ver_rl_d_on_1 = TStar.Operator("ver_rl_d_on_1",
                               "Vertically Rotate Down with RL on Row 1",
               lambda w: vertical_rotate(w, 1, "D", "RL"))
ver_rl_d_on_2 = TStar.Operator("ver_rl_d_on_2",
                               "Vertically Rotate Down with RL on Row 2",
               lambda w: vertical_rotate(w, 2, "D", "RL"))
ver_rl_d_on_3 = TStar.Operator("ver_rl_d_on_3",
                               "Vertically Rotate Down with RL on Row 3",
               lambda w: vertical_rotate(w, 3, "D", "RL"))

TStar.register_operators([hor_l_on_1,hor_l_on_2,hor_l_on_3,
                          hor_r_on_1,hor_r_on_2,hor_r_on_3,
                          ver_lr_u_on_1,ver_lr_u_on_2,ver_lr_u_on_3,
                          ver_lr_d_on_1,ver_lr_d_on_2,ver_lr_d_on_3,
                          ver_rl_u_on_1,ver_rl_u_on_2,ver_rl_u_on_3,
                          ver_rl_d_on_1,ver_rl_d_on_2,ver_rl_d_on_3])

TStar.setup_and_run()
