import rotations as rotate


################ GET OPERATION VARIABLES:
##
def other_UD(UorD):
    if UorD == "U":
        return "D"
    elif UorD == "D":
        return "U"

def face_rotate_LR(LorR):
    if LorR == "L":
        return "U"
    elif LorR == "R":
        return "D"
    
def other_face_rotate_LR(LorR):
    if LorR == "L":
        return "D"
    elif LorR == "R":
        return "U"

def get_vert(front_face):
    if front_face == 0:
        return lambda w, UorD, col: rotate.vertical_rotate(w, col, UorD, "LR")
    if front_face == 1:
        return lambda w, UorD, col: rotate.vertical_rotate(w, col, UorD, "RL")
    if front_face == 2:
        return lambda w, UorD, col: rotate.vertical_rotate(w, 4-col, other_UD(UorD), "LR")
    if front_face == 3:
        return lambda w, UorD, col: rotate.vertical_rotate(w, 4-col, other_UD(UorD), "RL")

def get_face_rotate(front_face):
    if front_face == 0:
        return lambda w,LorR: rotate.vertical_rotate(w, 1, face_rotate_LR(LorR), "RL")
    if front_face == 1:
        return lambda w,LorR: rotate.vertical_rotate(w, 3, other_face_rotate_LR(LorR), "LR")
    if front_face == 2:
        return lambda w,LorR: rotate.vertical_rotate(w, 3, other_face_rotate_LR(LorR), "RL")
    if front_face == 3:
        return lambda w,LorR: rotate.vertical_rotate(w, 1, face_rotate_LR(LorR), "LR")
    
###############################################################################
################ SEQUENCES: ###################################################
##

################ TOP ROW:
def top_corners(state, front_face, alg_num):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    if alg_num == 1:
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state, 3 , "L")
        state = vert_function(state, "U", 3)
    if alg_num == 2:
        state = rotate.horizontal_rotate(state, 3 , "L")
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = vert_function(state, "U", 3)
    if alg_num == 3:
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = vert_function(state, "U", 3)
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = vert_function(state, "D", 3)
        state = state = rotate.horizontal_rotate(state, 3 , "L")
        state = vert_function(state, "U", 3)
    if alg_num == 4:
        state = rotate_face(state,"R")
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = rotate_face(state,"L")
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = vert_function(state, "U", 3)
    if alg_num == 5:
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state, 3 , "L")
        state = vert_function(state, "U", 3)
        state = rotate.horizontal_rotate(state, 3 , "R")
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state, 3 , "L")
        state = vert_function(state, "U", 3)
    return state

def top_sides(state, front_face, alg_num):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    if alg_num == 1:
        state = vert_function(state, "D", 2)
        state = rotate.horizontal_rotate(state,3, "L")
        state = rotate.horizontal_rotate(state,3, "L")
        state = vert_function(state, "U", 2)
    if alg_num == 2:
        state = rotate.horizontal_rotate(state,3, "L")
        state = vert_function(state, "D", 2)
        state = rotate.horizontal_rotate(state,3, "R")
        state = vert_function(state, "U", 2)
    if alg_num == 3:
        state = rotate.horizontal_rotate(state, 2, "R")
        state = rotate_face(state, "R")
        state = rotate.horizontal_rotate(state, 2, "L")
        state = rotate_face(state, "L")
    if alg_num == 4:
        state = rotate.horizontal_rotate(state, 2, "R")
        state = rotate_face(state, "L")
        state = rotate.horizontal_rotate(state, 2, "L")
        state = rotate.horizontal_rotate(state, 2, "L")
        state = rotate_face(state, "R")
    if alg_num == 5:
        state = vert_function(state, "D", 2)
        state = rotate.horizontal_rotate(state,3, "L")
        state = rotate.horizontal_rotate(state,3, "L")
        state = vert_function(state, "U", 2)
        state = rotate.horizontal_rotate(state,3, "L")
        state = vert_function(state, "D", 2)
        state = rotate.horizontal_rotate(state,3, "R")
        state = vert_function(state, "U", 2)
    return state


################ MIDDLE ROW:
def middle_sides(state, front_face, LorR):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    if LorR == "L":
        state = rotate.horizontal_rotate(state,3, "R")
        state = vert_function(state, "D", 1)
        state = rotate.horizontal_rotate(state,3, "L")
        state = vert_function(state, "U", 1)
        state = rotate.horizontal_rotate(state,3, "L")
        state = rotate_face(state, "L")
        state = rotate.horizontal_rotate(state,3, "R")
        state= rotate_face(state, "R")
    if LorR == "R":
        state = rotate.horizontal_rotate(state,3, "L")
        state = vert_function(state, "D", 3)
        state = rotate.horizontal_rotate(state,3, "R")
        state = vert_function(state, "U", 3)
        state = rotate.horizontal_rotate(state,3, "R")
        state = rotate_face(state, "R")
        state = rotate.horizontal_rotate(state,3, "L")
        state = rotate_face(state, "L")
    return state

################ BOTTOM ROW:
def pos_bottom_corners(state, front_face):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    state = vert_function(state, "D", 3)
    state = rotate.horizontal_rotate(state,3, "L")
    state = vert_function(state, "U", 3)
    state = rotate_face(state, "R")
    state = rotate.horizontal_rotate(state,3, "R")
    state = rotate_face(state, "L")
    state = vert_function(state, "D", 3)
    state = rotate.horizontal_rotate(state,3, "R")
    state = vert_function(state, "U", 3)
    state = rotate.horizontal_rotate(state,3, "R")
    state = rotate.horizontal_rotate(state,3, "R")
    return state

def ori_bottom_corners(state, front_face):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    state = vert_function(state,"D",3)
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"U",3)
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"D",3)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"U",3)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    return state

def pos_bottom_sides(state,front_face):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    state = vert_function(state,"D",2)
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"U",2)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"D",2)
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"U",2)
    return state

################ H or FISH!
def H_pattern(state,front_face):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,2,"R")
    state = vert_function(state,"U",1)
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,2,"R")
    state = rotate.horizontal_rotate(state,2,"R")
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"D",1)
    state = rotate.horizontal_rotate(state,2,"L")
    state = rotate.horizontal_rotate(state,2,"L")
    state = vert_function(state,"U",1)
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,2,"L")
    state = vert_function(state,"D",1)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    return state

def F_pattern(state,front_face):
    vert_function = get_vert(front_face)
    rotate_face = get_face_rotate(front_face)
    state = rotate_face(state,"L")
    state = vert_function(state,"D",3)
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,2,"R")
    state = vert_function(state,"U",1)
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,2,"R")
    state = rotate.horizontal_rotate(state,2,"R")
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"D",1)
    state = rotate.horizontal_rotate(state,2,"L")
    state = rotate.horizontal_rotate(state,2,"L")
    state = vert_function(state,"U",1)
    state = vert_function(state,"U",1)
    state = rotate.horizontal_rotate(state,2,"L")
    state = vert_function(state,"D",1)
    state = rotate.horizontal_rotate(state,3,"L")
    state = rotate.horizontal_rotate(state,3,"L")
    state = vert_function(state,"U",3)
    state = rotate_face(state,"R")
    return state
                                     
