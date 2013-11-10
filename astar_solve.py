import sequences
import random
import rotations as rotate
import copy
import helpers
import state_stored
import mostRecentPath
import rubixTStar as TStar

##
##  SUCCESSOR FUNCTION
#############################################################
def successors(state):
    newState = copy.deepcopy(state)
    sList = []
    value = this_value(state)
    if value <100: #no corners/sides (on layers) finished
        for i in range(4):
            for j in range(1,6):
                mostRecentPath.path = []
                thisSucc = sequences.top_corners(newState,i,j)
                thisPath = mostRecentPath.path
                sList += [[this_value(thisSucc),thisSucc,thisPath]]
                if this_value(thisSucc) > value:
                    value = this_value
        if value == this_value(state):
            for i in range(4):
                for j in range(1,5):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,3,"R")
                    thisSucc = sequences.top_corners(newState2,i,j)
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
                        value = this_value
        if value == this_value(state):
            for i in range(4):
                for j in range(1,5):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,3,"R")
                    newState2 = rotate.horizontal_rotate(newState2,3,"R")
                    thisSucc = sequences.top_corners(newState2,i,j)
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
                        value = this_value
        if value == this_value(state):
            for i in range(4):
                for j in range(1,5):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,3,"L")
                    thisSucc = sequences.top_corners(newState2,i,j)
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
                        value = this_value
        
    elif value >= 100 and value < 200: #a
        for i in range(4):
            for j in range(1,6):
                mostRecentPath.path = []
                thisSucc = sequences.top_sides(newState,i,j)
                thisPath = mostRecentPath.path
                sList += [[this_value(thisSucc),thisSucc,thisPath]]
                if this_value(thisSucc) > value:
                    value = this_value
        if value == this_value(state) and not value == 300:
            for i in range(4):
                for j in range(1,6):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,3,"R")
                    thisSucc = sequences.top_sides(newState2,i,j)
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        value = this_value
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
        if value == this_value(state) and not value == 300:
            for i in range(4):
                for j in range(1,6):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,3,"R")
                    newState2 = rotate.horizontal_rotate(newState2,3,"R")
                    thisSucc = sequences.top_sides(newState2,i,j)
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        value = this_value
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
        if value == this_value(state) and not value == 300:
            for i in range(4):
                for j in range(1,6):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,1,"R")
                    thisSucc = sequences.top_sides(newState2,i,j)
                    thisSucc = rotate.horizontal_rotate(thisSucc,1,"L")
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        value = this_value
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
        if value == this_value(state) and not value == 300:
            for i in range(4):
                for j in range(1,6):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,1,"R")
                    newState2 = rotate.horizontal_rotate(newState2,1,"R")
                    thisSucc = sequences.top_sides(newState2,i,j)
                    thisSucc = rotate.horizontal_rotate(thisSucc,1,"L")
                    thisSucc = rotate.horizontal_rotate(thisSucc,1,"L")
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        value = this_value
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
        if value == this_value(state) and not value == 300:
            for i in range(4):
                for j in range(1,6):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,2,"R")
                    thisSucc = sequences.top_sides(newState2,i,j)
                    thisSucc = rotate.horizontal_rotate(thisSucc,2,"L")
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        value = this_value
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
        if value == this_value(state) and not value == 300:
            for i in range(4):
                for j in range(1,6):
                    mostRecentPath.path = []
                    newState2 = rotate.horizontal_rotate(newState,2,"R")
                    newState2 = rotate.horizontal_rotate(newState2,2,"R")
                    thisSucc = sequences.top_sides(newState2,i,j)
                    thisSucc = rotate.horizontal_rotate(thisSucc,2,"L")
                    thisSucc = rotate.horizontal_rotate(thisSucc,2,"L")
                    thisPath = mostRecentPath.path
                    if this_value(thisSucc) > value:
                        value = this_value
                        sList += [[this_value(thisSucc),thisSucc,thisPath]]
    elif value >= 300 and value < 400: #1
        for i in range(4):
            #L
            mostRecentPath.path = []
            thisSucc = sequences.middle_sides(newState, i, "L")
            thisPath = mostRecentPath.path
            sList += [[this_value(thisSucc),thisSucc,thisPath]]
            if this_value(thisSucc) > value:
                value = this_value
            #R
            mostRecentPath.path = []
            thisSucc = sequences.middle_sides(newState, i, "R")
            thisPath = mostRecentPath.path
            sList += [[this_value(thisSucc),thisSucc,thisPath]]
            if this_value(thisSucc) > value:
                value = this_value
        if value == this_value(state) and not value == 400:
            for i in range(4):
                #L
                mostRecentPath.path = []
                thisSucc = rotate.horizontal_rotate(newState,3,"L")
                thisSucc = sequences.middle_sides(thisSucc, i, "L")
                thisSucc = sequences.middle_sides(thisSucc, i, "L")
                thisSucc = rotate.horizontal_rotate(thisSucc,3,"L")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
                #R
                mostRecentPath.path = []
                thisSucc = rotate.horizontal_rotate(newState,3,"R")
                thisSucc = sequences.middle_sides(thisSucc, i, "R")
                thisSucc = sequences.middle_sides(thisSucc, i, "R")
                thisSucc = rotate.horizontal_rotate(thisSucc,3,"R")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
        if value == this_value(state) and not value == 400:
           for i in range(4):
                #L
                mostRecentPath.path = []
                newState2 = rotate.horizontal_rotate(newState,3,"R")
                thisSucc = sequences.middle_sides(newState2, i, "L")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
                #R
                mostRecentPath.path = []
                newState2 = rotate.horizontal_rotate(newState,3,"R")
                thisSucc = sequences.middle_sides(newState2, i, "R")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
        if value == this_value(state) and not value == 400:
            for i in range(4):
                #L
                mostRecentPath.path = []
                newState2 = rotate.horizontal_rotate(newState,3,"R")
                newState2 = rotate.horizontal_rotate(newState2,3,"R")
                thisSucc = sequences.middle_sides(newState2, i, "L")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
                #R
                mostRecentPath.path = []
                newState2 = rotate.horizontal_rotate(newState,3,"R")
                newState2 = rotate.horizontal_rotate(newState2,3,"R")
                thisSucc = sequences.middle_sides(newState2, i, "R")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
        if value == this_value(state) and not value == 400:
            for i in range(4):
                #L
                mostRecentPath.path = []
                newState2 = rotate.horizontal_rotate(newState,3,"L")
                thisSucc = sequences.middle_sides(newState2, i, "L")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
                #R
                mostRecentPath.path = []
                newState2 = rotate.horizontal_rotate(newState,3,"L")
                thisSucc = sequences.middle_sides(newState2, i, "R")
                thisPath = mostRecentPath.path
                if this_value(thisSucc) > value:
                    sList += [[this_value(thisSucc),thisSucc,thisPath]]
                    value = this_value
    elif value >= 700 and value < 800: #1+2 (top two layers finished)
        for i in range(4):
            mostRecentPath.path = []
            thisSucc = sequences.pos_bottom_corners(newState, i)
            thisPath = mostRecentPath.path
            sList += [[this_value(thisSucc),thisSucc,thisPath]]
            if this_value(thisSucc) > value:
                value = this_value
    elif value >= 800 and value < 900: #3a (bottom corners)
        for i in range(4):
            mostRecentPath.path = []
            thisSucc = sequences.ori_bottom_corners(newState, i)
            thisPath = mostRecentPath.path
            sList += [[this_value(thisSucc),thisSucc,thisPath]]
            if this_value(thisSucc) > value:
                value = this_value

        step1 = []
        step2 = []
        step3 = []
        step4 = []
        stop = False
        finish = ""
        for i in range(4):
            if stop:
                finish += "i:"+str(i)
                break
            mostRecentPath.path = []
            thisSucc = copy.deepcopy(newState)
            thisSucc = sequences.ori_bottom_corners(thisSucc, i)
            step1 = mostRecentPath.path[-10:]
            if this_value(thisSucc) == 1600:
                sList += [[this_value(thisSucc),thisSucc,step1]]
                stop = True
            for j in range(4):
                if stop:
                    finish += "j:"+str(j)
                    break
                thisSucc1 = copy.deepcopy(thisSucc)
                thisSucc1 = sequences.ori_bottom_corners(thisSucc1, j)
                step2 = step1 + mostRecentPath.path[-10:]
                if this_value(thisSucc1) == 1600:
                    sList += [[this_value(thisSucc1),thisSucc1,step2]]
                    stop = True
                for h in range(4):
                    if stop:
                        finish += "h:"+str(h)
                        break
                    thisSucc2 = copy.deepcopy(thisSucc1)
                    thisSucc2 = sequences.ori_bottom_corners(thisSucc2, h)
                    step3 = step2 + mostRecentPath.path[-10:]
                    if this_value(thisSucc2) == 1600:
                        sList += [[this_value(thisSucc2),thisSucc2,step3]]
                        stop = True
                    for g in range(4):
                        if stop:
                            finish += "g:"+str(g)
                            break
                        thisSucc3 = copy.deepcopy(thisSucc2)
                        thisSucc3 = sequences.ori_bottom_corners(thisSucc3, g)
                        step4 = step3 + mostRecentPath.path[-10:]
                        if this_value(thisSucc3) == 1600:
                            sList += [[this_value(thisSucc3),thisSucc3,step4]]
                            stop = True
        if not stop:
            mostRecentPath.path = []
            thisSucc = copy.deepcopy(newState)
            num = [0,1,2,3]
            oriFace = random.choice(num)
            thisSucc = sequences.ori_bottom_corners(thisSucc, oriFace)
            thisSucc = sequences.ori_bottom_corners(thisSucc, oriFace)
            step = mostRecentPath.path
            sList += [[this_value(thisSucc)+10,thisSucc,step]]
    elif value >= 1600 and value < 1700: #3b (bottom corners finished)
        for i in range(4):
            mostRecentPath.path = []
            thisSucc = sequences.pos_bottom_sides(newState, i)
            thisPath = mostRecentPath.path
            sList += [[this_value(thisSucc),thisSucc,thisPath]]
            if this_value(thisSucc) > value:
                value = this_value
    elif value >= 3200 and value < 3300: #3+2+1 (H or F)
        for i in range(4):
            mostRecentPath.path = []
            thisSucc = sequences.H_pattern(newState, i)
            thisPath = mostRecentPath.path
            sList += [[this_value(thisSucc),thisSucc,thisPath]]
            if this_value(thisSucc) > value:
                value = this_value
        if value != 6400:
            for i in range(4):
                mostRecentPath.path = []
                thisSucc = sequences.F_pattern(newState, i)
                thisPath = mostRecentPath.path
                sList += [[this_value(thisSucc),thisSucc,thisPath]]
                if this_value(thisSucc) > value:
                    value = this_value
    ##if value == this_value(state):
    ##    print "repeat"
    return sList
##
##  HELPERS
#############################################################
def p_succ():
    print ""
    print ""
    print "SUCCESSORS:"
    state= state_stored.state
    sList = successors(state)
    maxPossible = [0,[],[]]
    thisValue = 0
    oldValue = 0
    print len(sList)
    for succ in sList:
        thisValue = this_value(succ[1])
        #print thisValue
        if thisValue > oldValue:
            maxPossible = [thisValue,succ[1],succ[2]]
        #helpers.print_rubix(succ[0])
    print maxPossible[0]
    if len(maxPossible[1]) != 0:
        helpers.print_rubix(maxPossible[1])
        state_stored.state = maxPossible[1]
        TStar.INITIAL_DATA = maxPossible[1]
        TStar.create_initial_state()
        TStar.initialize_states_and_display()
    for p in maxPossible[2]:
        print p

def get_corner_colors(state, cornerInd,TorB):
    if TorB == "T":
        leftSide = (cornerInd - 1) % 4
        leftColor = state[leftSide][0][2]
        rightColor = state[cornerInd][0][0]
        indices = []
        if cornerInd == 0: indices = [0,0]
        if cornerInd == 1: indices = [2,0]
        if cornerInd == 2: indices = [2,2]
        if cornerInd == 3: indices = [0,2]
        otherColor = state[4][indices[0]][indices[1]]
    if TorB == "B":
        leftSide = (cornerInd - 1) % 4
        leftColor = state[leftSide][2][2]
        rightColor = state[cornerInd][2][0]
        indices = []
        if cornerInd == 0: indices = [2,0]
        if cornerInd == 1: indices = [0,0]
        if cornerInd == 2: indices = [0,2]
        if cornerInd == 3: indices = [2,2]
        otherColor = state[5][indices[0]][indices[1]]
    return [leftColor, rightColor, otherColor]

def get_top_side_color(state,face):
    top = state[4]
    if face==0: return top[1][0]
    if face==1: return top[2][1]
    if face==2: return top[1][2]
    if face==3: return top[0][1]

def get_bottom_side_color(state,face):
    bottom = state[5]
    if face==0: return bottom[1][0]
    if face==1: return bottom[0][1]
    if face==2: return bottom[1][2]
    if face==3: return bottom[2][1]

##
##  VALUE OF STATE
############################################################# 
##a  100s = first row corners finished
##b  200s = first row sides finished
##1  300s = +1 finished
##
##2  400s = +2 finished
##
##2a 500s = second row finished, and top corners finished
##2b 600s = second row finished, and first row sides finished
##3  700s = +1+2 finished
##
##3c 800s = third row corners finished
## 900-1200 = combos
## 1200 = first row corners +2 and third row corners finished
## 1300-1500 = combos
## 1500s = third row sides finished
## 1600-3100 = combos
## 3100 = +1+2+3 finished!!
def value():
    state = state_stored.state
    helpers.print_rubix(state)
    layer1 = value_state(state,1)
    layer2 = value_state(state,2)
    layer3 = value_state(state,3)
    print "layer1: ", str(layer1)
    print "layer2: ", str(layer2)
    print "layer2: ", str(layer3)
    return layer1+layer2+layer3

def this_value(state):
    total = value_state(state,1)
    if total >= 300:
        total += value_state(state,2)
    if total >= 700:
        total += value_state(state,3)
    return total

def value_state(state,layer):
    value = 0
    if layer == 1:
            #top corners
            tempvalue = 0
            for i in range(4):
                corner_colors = get_corner_colors(state, i,"T")
                expectedColors = []
                expectedColors += state[(i-1)%4][1][1]
                expectedColors += state[i][1][1]
                expectedColors += state[4][1][1]
                if corner_colors == expectedColors:
                    tempvalue +=5
                else:
                    tempvalue += 1  #assume its position is right
                    for j in range(3):
                        if corner_colors.count(expectedColors[j]) == 0:
                            tempvalue -= 1  #if not right position, adjust
                            break
            if tempvalue == 20:
                value += 100
            else:
                value += tempvalue
            #top sides
            tempvalue = 0
            if value == 100:
                for i in range(4):
                    expectedColors = []
                    expectedColors += state[i][0][0]
                    expectedColors += state[4][1][1]
                    top_side_colors = [state[i][0][1],get_top_side_color(state,i)]
                    if top_side_colors == expectedColors:
                        tempvalue +=5
                    else:
                        tempvalue += 1  #assume its position is right
                        for j in range(2):
                            if top_side_colors.count(expectedColors[j]) == 0:
                                tempvalue -= 1  #if not right position, adjust
                                break
                if tempvalue == 20:
                    value += 200
                else:
                    value += tempvalue
    elif layer == 2:
            tempvalue = 0
            for i in range(4):
                expectedColors = []
                expectedColors += state[(i-1)%4][1][1]
                expectedColors += state[i][1][1]
                leftColor = state[(i-1)%4][1][2]
                rightColor = state[i][1][0]
                side_colors = [leftColor,rightColor]
                if side_colors == expectedColors:
                    tempvalue +=5
                else:
                    tempvalue += 1
                    for j in range(2):
                        if side_colors.count(expectedColors[j]) == 0:
                            tempvalue -= 1
                            break
            if tempvalue == 20:
                value += 400
            else:
                value += tempvalue
    elif layer == 3:
            #bottom corners
            tempvalue = 0
            for i in range(4):
                corner_colors = get_corner_colors(state, i,"B")
                expectedColors = []
                expectedColors += state[(i-1)%4][1][1]
                expectedColors += state[i][1][1]
                expectedColors += state[5][1][1]
                tempvalue += 1  #assume its position is right
                for j in range(3):
                    if corner_colors.count(expectedColors[j]) == 0:
                        tempvalue -= 1  #if not right position, adjust
                        break
            if tempvalue == 4: #corners in right place
                value += 100
                tempvalue = 0
                for i in range(4):
                    corner_colors = get_corner_colors(state, i,"B")
                    expectedColors = []
                    expectedColors += state[(i-1)%4][1][1]
                    expectedColors += state[i][1][1]
                    expectedColors += state[5][1][1]
                    if corner_colors == expectedColors:
                        tempvalue += 1
                if tempvalue == 4:#corners oriented correctly
                    value += 800
                else:
                    value +=tempvalue
            else:
                value += tempvalue
            #bottom sides
            if tempvalue == 4:
                tempvalue = 0
                finished_side = 0
                for i in range(4):
                    expectedColors = []
                    expectedColors += state[i][2][0]
                    expectedColors += state[5][1][1]
                    bottom_side_colors = [state[i][2][1],get_bottom_side_color(state,i)]
                    tempvalue += 1  #assume its position is right
                    if bottom_side_colors == expectedColors:
                        finished_side +=1
                    for j in range(2):
                        if bottom_side_colors.count(expectedColors[j]) == 0:
                            tempvalue -= 1  #if not right position, adjust
                            break
                if tempvalue != 4:
                    value += tempvalue
                elif tempvalue == 4 or finished_side == 4:
                    value += 1600
                    tempvalue = 0
                    for i in range(4):
                        expectedColors = []
                        expectedColors += state[i][2][0]
                        expectedColors += state[5][1][1]
                        bottom_side_colors = [state[i][2][1],get_bottom_side_color(state,i)]
                        if expectedColors == bottom_side_colors:
                            tempvalue +=1
                    if tempvalue == 4:
                        value += 3200
    return value

##
##  A STAR ALGORITHMS
#############################################################
def h(n):  
    return this_value(n)

def listDifference(list1, list2):
    newList = []
    for i in range(len(list1)):
        if list2.count(list1[i]) == 0:
            newList += [list1[i]]
    return newList

def deleteBest(sList):
    countList = []
    for succ in sList:
        countList += [succ[0]]
    succ = sList.pop(countList.index(max(countList)))
    return succ


def AStar1(theStart):
    start = [this_value(theStart),theStart,[]]
    OPEN = [start] # Step 1 
    CLOSED = [] 
    while OPEN != []: # Step 2 
        n = deleteBest(OPEN) # Step 3
        CLOSED.append(n) 
        if this_value(n[1]) >= 300:
            return n
        lst = successors(n[1]) # Step 4
        for succ in lst:
            succ[2] = n[2]+ succ[2]
        lst = listDifference(lst, CLOSED)
        OPEN = lst + listDifference(OPEN, lst) # Step 5

def AStar12(theStart):
    start = [this_value(theStart),theStart,[]]
    OPEN = [start] # Step 1 
    CLOSED = [] 
    while OPEN != []: # Step 2 
        n = deleteBest(OPEN) # Step 3
        CLOSED.append(n) 
        if this_value(n[1]) >= 700:
            return n
        lst = successors(n[1]) # Step 4
        for succ in lst:
            succ[2] = n[2]+ succ[2]
        lst = listDifference(lst, CLOSED)
        OPEN = lst + listDifference(OPEN, lst) # Step 5

##  800  bottom corners positioned
##  1600 bottom corners oriented
##  3200 partial bottom sides
##  6400 finished!!!
##
def AStar123(theStart):
    start = [this_value(theStart),theStart,[]]
    OPEN = [start] # Step 1 
    CLOSED = [] 
    while OPEN != []: # Step 2 
        n = deleteBest(OPEN) # Step 3
        CLOSED.append(n)
        if n[0] >= 6400:
            return n
        lst = successors(n[1]) # Step 4
        for succ in lst:
            succ[2] = n[2]+ succ[2]
        lst = listDifference(lst, CLOSED)
        OPEN = lst + listDifference(OPEN, lst) # Step 5


