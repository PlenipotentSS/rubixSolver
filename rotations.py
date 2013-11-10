import copy
import mostRecentPath

utter = False   ##for debugging

## row is   1: panel
##          2: middle
##          3: bottom
def horizontal_rotate(state, row, LorR):
    global utter
    if utter:
        print "Rotating Horizontally \"" + LorR + "\" with row " + \
              str(row) + "."
    mostRecentPath.path += ["hor_"+LorR.lower()+"_on_"+str(row)]
    row = row-1
    newState = copy.deepcopy(state)
    if LorR == "L":
        tmp = newState[0][row]
        for i in range(3):
            newState[i][row] = newState[i+1][row]
        newState[3][row] = tmp
        #move top/bottom
        if row == 0 or row == 2:
            if row == 0:
                panel = newState[4]
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
    if LorR == "R":
        tmp = newState[3][row]
        for i in range(3):
            j = 3-i
            newState[j][row] = newState[j-1][row]
        newState[0][row] = tmp
        #move top/bottom
        if row == 0 or row == 2:
            if row == 0:
                panel = newState[4]
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
    mostRecentPath.path += ["ver_"+LRorRL.lower()+"_"+UorD.lower()+"_on_"+str(col)]
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
