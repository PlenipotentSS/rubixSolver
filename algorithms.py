import state_stored
import mostRecentPath
import helpers
import rotations as rotate
import rubixTStar as TStar
import copy
import sequences


##
## FUNCTIONS TO SOLVE CUBES WITH ALGORITHMS
################################################################################

'''
def start_solve(state):        #Get one side cubie matching top, and 2nd layer centers
    top = state[4]
    if top[1][1] == top[0][1] and top[1][1] == top[1][0] and \
                    top[1][1] == top[2][1] and top[1][1] == top[1][2]:
        


def get_top_sides:      #match all sides for layer 1
    sum = 0
    while sum < 4:
        if top[1][1] == top[0][1]:
            sum += 1
        if top[1][1] == top[1][0]:
            sum += 1
        if top[1][1] == top[2][1]:
            sum += 1
        if top[1][1] == top[1][2]:
            sum += 1
    

def find_top_corners   #get current corner in right place 

def find_middle_sides  #find current middle side

def get_middle_sides   #put the middle side in place (finishes 2nd layer)

def position_bottom_corners   #switch corners around

def orient_bottom_corners     #

def position_sides

def finish_cube
'''

def top_corners_finished(state):
    top = state[4]
    if top[1][1] == top[0][0] == top[0][2] == top[2][0] == top[2][2]:
        if state[0][0][0] == state[0][0][2] and state[1][0][0]== state[1][0][2] \
                and state[2][0][0]== state[2][0][2] and state[3][0][0]== state[3][0][2]:
            return True
    return False

def top_corners():
    state = copy.deepcopy(state_stored.state)
    newState = copy.deepcopy(state)
    helpers.print_rubix(state)
    global pulls
    pulls = -4
    repeats = 0
    path = []
    while not top_corners_finished(state):
        mostRecentPath.path = []
        helpers.print_rubix(state)
        top = state[4]
        if top[1][1] == top[2][0] and state[0][1][1] == state[0][0][2]:
            print "First Corner Situated"
        else:
            print "Situating first Corner..."
            newState = get_top_corners(state, 0)
            if newState[0][1][1] == newState[0][0][2]:
                path += mostRecentPath.path
                mostRecentPath.path = []
                state = newState
        if top[1][1] == top[2][2] and state[1][1][1] == state[1][0][2]:
            print "Second Corner Situated"
        else:
            print "Situating second Corner..."
            newState = get_top_corners(state, 1)
            if newState[1][1][1] == newState[1][0][2]:
                path += mostRecentPath.path
                mostRecentPath.path = []
                state = newState
        if top[1][1] == top[0][2] and state[2][1][1]== state[2][0][2]:
            print "Third Corner Situated"
        else:
            print "Situating third Corner..."
            newState = get_top_corners(state, 2)
            if newState[2][1][1] == newState[2][0][2]:
                path += mostRecentPath.path
                mostRecentPath.path = []
                state = newState
        if top[1][1] == top[0][0] and state[3][1][1]== state[3][0][2]:
            print "Last Corner Situated"
        else:
            print "Situating Last Corner..."
            newState = get_top_corners(state, 3)
            if newState[3][1][1] == newState[3][0][2]:
                path += mostRecentPath.path
                mostRecentPath.path = []
                state = newState
        state = rotate.horizontal_rotate(state,3,"R")
        path += mostRecentPath.path
    helpers.print_rubix(state)
    helpers.print_rubix(newState)
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
        TStar.redraw_tree()
    mostRecentPath.path = []

def cubie_bottom_right(front_face):
    if front_face == 0:
        return [0,0]
    if front_face == 1:
        return [0,2]
    if front_face == 2:
        return [2,2]
    if front_face == 3:
        return [2,0]

def count_top_corners(state):
    count = 0
    if state[4][0][0] == state[4][1][1]:
        count += 1
    if state[4][0][2] == state[4][1][1]:
        count += 1
    if state[4][2][0] == state[4][1][1]:
        count += 1
    if state[4][2][2] == state[4][1][1]:
        count += 1
    return count

def get_top_corners(state, face): #put cubie in right corner for layer 1
    if face >= 4:
        print "error: wrong face number"
    else:
        top = state[4]
        topColor = top[1][1]
        front = state[face]
        right = state[(face+1) % 4]
        bottom = state[5]
        seq = 0
        row,col = cubie_bottom_right(face)
        if top_corners_finished(state): 
            return state
        if front[0][2] == topColor:
            seq = 4
            state = sequences.top_corners(state, face, 4)
        if top_corners_finished(state): 
            return state
        if front[2][2] == topColor:
            seq = 2
            state = sequences.top_corners(state, face, 2)
        if top_corners_finished(state): 
            return state
        if right[0][0] == topColor:
            seq = 5
            state = sequences.top_corners(state, face, 5)
        if top_corners_finished(state): 
            return state
        if right[2][0] == topColor:
            seq = 1
            state = sequences.top_corners(state, face, 1)
        if top_corners_finished(state): 
            return state
        if bottom[row][col] == topColor:
            seq = 3
            state = sequences.top_corners(state, face, 3)
        if top_corners_finished(state): 
            return state
    return state
