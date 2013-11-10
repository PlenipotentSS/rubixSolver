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

def get_top_corners    

def find_middle_sides  #find current middle side

def get_middle_sides   #put the middle side in place (finishes 2nd layer)

def position_bottom_corners   #switch corners around

def orient_bottom_corners     #

def position_sides

def finish_cube




def get_top_corners(state, face): #put cubie in right corner for layer 1
    if face >= 4:
        print "error: wrong face number"
    else:
        topColor = state[4][1][1]
        front = state[face]
        right = state[(face+1) % 4]
        bottom = state[5]
        if front[0][2] == topColor:
            seq_move_corners(state, face, 4)
        elif front[2][2] == topColor:
            seq_move_corners(state, face, 2)
        elif right[0][0] == topColor:
            seq_move_corners(state, face, 5)
        elif right[2][0] == topColor:
            seq_move_corners(state, face, 1)
        elif bottom[0][2] == topColor:
            seq_move_corners(state, face, 3)
        
