##
## HELPERS
################################################################################

def printUtterances(default):
    global utter
    if default:
        utter = True
    else:
        utter = False

##used for deubgging in terminal / console
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
