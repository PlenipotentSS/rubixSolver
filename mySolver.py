'''
mySolver.py
Steven Stevenson


'''
import state_stored
import mostRecentPath
import rubixTStar as TStar
import rotations as rotate
import helpers
import bfs_solve
import astar_solve
#import algorithms
import sequences
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
    output = ""
    output += ""
    print output
    print ""
    state = state_stored.initial_state
    utter = True
    if utter: helpers.print_rubix(state)
    print "OK"
    state_stored.state = state
    return state



##
## HELPERS
################################################################################

def print_successors():
    titles, sList = bfs_solve.successors(state_stored.state)
    print titles
    for i in range(len(sList)):
        print titles[i]
        helpers.print_rubix(sList[i])

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
    state = state_stored.state
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

##
## FUNCTIONS TO LOAD CUBES
################################################################################

def randomize_global():
    global utter
    newState2 = copy.deepcopy(state_stored.initial_state)
    numRotations = random.choice(range(10,30))
    for i in range(numRotations):
        operators = ["vertical","horizontal"]
        choice = random.choice(operators)
        if choice == "vertical":
            UorD = random.choice(["U","D"])
            RLorLR = random.choice(["LR","RL"])
            col = random.choice([1,2,3])
            newState2 = rotate.vertical_rotate(newState2, col, UorD, RLorLR)
        if choice == "horizontal":
            LorR = random.choice(["L","R"])
            row = random.choice([1,2,3])
            newState2 = rotate.horizontal_rotate(newState2, row, LorR)
    if utter: helpers.print_rubix(newState2)
    TStar.INITIAL_DATA = newState2
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    state_stored.state = newState2
    mostRecentPath.path = []
    return 

def cube_ina_cube():
    global utter
    newState = state_stored.cube_ina_cube
    if utter: helpers.print_rubix(newState)
    TStar.INITIAL_DATA = newState
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    state_stored.state = newState
    return     

def twisted_rings():
    global utter
    newState = state_stored.twisted_rings
    if utter: helpers.print_rubix(newState)
    TStar.INITIAL_DATA = newState
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    state_stored.state = newState
    return

    mostRecentPath.path += "ver_"+LRorRL.lower()+"_"+UorD.lower()+"_on_"+str(col)

def completed_cube():
    global utter
    if utter: helpers.print_rubix(state_stored.initial_state)
    TStar.INITIAL_DATA = state_stored.initial_state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
    state_stored.state = newState
    return

def load_from_file():
    theFile = None
    theFile = tkFileDialog.askopenfile(mode='rb',title='Choose a file')
    if theFile != None:
        newState = readFromFile(state_stored.initial_state, theFile)
        TStar.INITIAL_DATA = newState
        TStar.create_initial_state()
        TStar.initialize_states_and_display()
        state_stored.state = newState
        return
    else:
        print "Failed Load."
        return

##
## SEQUENCES
################################################################################
def seq_top_corners():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    place = int(raw_input("Where is it?: "))
    state = sequences.top_corners(state, side, place)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def seq_top_sides():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    place = int(raw_input("Where is it?: "))
    state = sequences.top_sides(state, side, place)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def seq_middle_sides():
    mostRecentPath.path = []
    state = state_stored.state
    helpers.print_rubix(state)
    side = int(raw_input("What side is the face?: "))
    place = raw_input("Go Where?: ")
    state = sequences.middle_sides(state, side, place)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()
##    node = TStar.NODE_CLASS(TStar.INITIAL_STATE)
##    path = mostRecentPath.path
##    for i in range(len(path)):
##        for o in TStar.OPERATORS:
##                if o.id == path[i]:
##                    TStar.TREE_DISP.selected_node = node
##                    succ = o._apply(node.s)
##                    new_node = TStar.TREE_DISP.node_class(succ)
##                    TStar.TREE_DISP.state_node_hash[succ] = new_node
##                    TStar.TREE_DISP.all_nodes.append(new_node)
##                    TStar.ALL_STATES.append(succ)
##                    node = new_node
##                    break
##        global last_sol_node
##        last_sol_node = node
##        TStar.redraw_tree()

def seq_pos_bottom_corners():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    state = sequences.pos_bottom_corners(state, side)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def seq_ori_bottom_corners():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    state = sequences.ori_bottom_corners(state, side)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def seq_pos_bottom_sides():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    state = sequences.pos_bottom_sides(state, side)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def seq_H_pattern():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    state = sequences.H_pattern(state, side)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def seq_F_pattern():
    state = state_stored.state
    side = int(raw_input("What side is the face?: "))
    state = sequences.F_pattern(state, side)
    #state = state_stored.test
    helpers.print_rubix(state)
    layer1 = astar_solve.value_state(state,1)
    layer2 = astar_solve.value_state(state,2)
    layer3 = astar_solve.value_state(state,3)
    print "VALUE: " + str(layer1 + layer2+layer3)
    state_stored.state = state
    TStar.INITIAL_DATA = state
    TStar.create_initial_state()
    TStar.initialize_states_and_display()

def run_layer1():
    mostRecentPath.path = []
    state = state_stored.state
    value,newState,path = astar_solve.AStar1(state)
    print "1st layer done"
    helpers.print_rubix(newState)
    node = TStar.NODE_CLASS(TStar.INITIAL_STATE)
    for i in range(len(path)):
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

def run_layer2():
    mostRecentPath.path = []
    state = state_stored.state
    value,newState,path = astar_solve.AStar12(state)
    print "2nd layer done"
    helpers.print_rubix(newState)
    node = TStar.NODE_CLASS(TStar.INITIAL_STATE)
    for i in range(len(path)):
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

def run_layer3():
    mostRecentPath.path = []
    state = state_stored.state
    value,newState,path = astar_solve.AStar123(state)
    print "Cube done"
    helpers.print_rubix(newState)
    node = TStar.NODE_CLASS(TStar.INITIAL_STATE)
    for i in range(len(path)):
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

##
## Variables
################################################################################
utter = rotate.utter   ##for debugging

newState = prepare()

##
##  T* Menus
################################################################################

def add_app_specific_menus(menubar):
  saveMenu = Menu(menubar) #I/O
  menubar.add_cascade(label="Cube I/O", menu=saveMenu)
  saveMenu.add_command(label="Load Initial State...", command=load_from_file)
  saveMenu.add_command(label="Save Initial State...", command=saveToFile)
  cubeMenu = Menu(menubar) #patterns
  menubar.add_cascade(label="Cube Patterns", menu=cubeMenu)
  cubeMenu.add_command(label="Completed Cube", command=completed_cube)
  cubeMenu.add_command(label="Randomize", command=randomize_global)
  cubeMenu.add_command(label="Cube in a Cube", command=cube_ina_cube)
  cubeMenu.add_command(label="Twisted Rings", command=twisted_rings)
  solveMenu = Menu(menubar) #BDFS
  menubar.add_cascade(label="Solve with BDFS", menu=solveMenu)
  solveMenu.add_command(label="Solve 1st Layer", command=bfs_solve.solve_layer1)
  solveMenu.add_command(label="Solve 1st & 2nd Layer",command=bfs_solve.solve_layer12)
  solveMenu.add_command(label="Solve Cube", command=bfs_solve.solve_cube)
  solve2Menu = Menu(menubar) #A Star
  menubar.add_cascade(label="Solve with A Star", menu=solve2Menu)
  solve2Menu.add_command(label="Solve 1st Layer", command=run_layer1)
  solve2Menu.add_command(label="Solve 1st & 2nd Layer",command=run_layer2)
  solve2Menu.add_command(label="Solve Cube", command=run_layer3)
  algMenu = Menu(menubar) #algorithms
  menubar.add_cascade(label="Algorithms", menu=algMenu)
  algMenu.add_command(label="Rotate Top Corner", command = seq_top_corners)
  algMenu.add_command(label="Put Top Sides", command = seq_top_sides)
  algMenu.add_command(label="Middle_Sides", command = seq_middle_sides)
  algMenu.add_command(label="Switch Bottom Face Corners", command = seq_pos_bottom_corners)
  algMenu.add_command(label="Attempt Orient Bottom Corners", command = seq_ori_bottom_corners)
  algMenu.add_command(label="Position Bottom Sides", command = seq_pos_bottom_sides)
  algMenu.add_command(label="Dedmore's \"H\"", command = seq_H_pattern)
  algMenu.add_command(label="Dedmore's \"Fish\"", command = seq_F_pattern)

  extraMenu = Menu(menubar)
  menubar.add_cascade(label="Extras", menu=extraMenu)
  extraMenu.add_command(label="Value", command=astar_solve.value)
  extraMenu.add_command(label="Print Successors", command=astar_solve.p_succ)
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
               lambda w: rotate.horizontal_rotate(w,1,"L"))
hor_l_on_2 = TStar.Operator("hor_l_on_2",
                            "Horizontally Rotate Left on Row 2",
               lambda w: rotate.horizontal_rotate(w,2,"L"))
hor_l_on_3 = TStar.Operator("hor_l_on_3",
                            "Horizontally Rotate Left on Row 3",
               lambda w: rotate.horizontal_rotate(w,3,"L"))
hor_r_on_1 = TStar.Operator("hor_r_on_1",
                            "Horizontally Rotate Right on Row 1",
               lambda w: rotate.horizontal_rotate(w,1,"R"))
hor_r_on_2 = TStar.Operator("hor_r_on_2",
                            "Horizontally Rotate Right on Row 2",
               lambda w: rotate.horizontal_rotate(w,2,"R"))
hor_r_on_3 = TStar.Operator("hor_r_on_3",
                            "Horizontally Rotate Right on Row 3",
               lambda w: rotate.horizontal_rotate(w,3,"R"))

ver_lr_u_on_1 = TStar.Operator("ver_lr_u_on_1",
                               "Vertically Rotate Up with LR on Row 1",
               lambda w: rotate.vertical_rotate(w, 1, "U", "LR"))
ver_lr_u_on_2 = TStar.Operator("ver_lr_u_on_2",
                               "Vertically Rotate Up with LR on Row 2",
               lambda w: rotate.vertical_rotate(w, 2, "U", "LR"))
ver_lr_u_on_3 = TStar.Operator("ver_lr_u_on_3",
                               "Vertically Rotate Up with LR on Row 3",
               lambda w: rotate.vertical_rotate(w, 3, "U", "LR"))
ver_lr_d_on_1 = TStar.Operator("ver_lr_d_on_1",
                               "Vertically Rotate Down with LR on Row 1",
               lambda w: rotate.vertical_rotate(w, 1, "D", "LR"))
ver_lr_d_on_2 = TStar.Operator("ver_lr_d_on_2",
                               "Vertically Rotate Down with LR on Row 2",
               lambda w: rotate.vertical_rotate(w, 2, "D", "LR"))
ver_lr_d_on_3 = TStar.Operator("ver_lr_d_on_3",
                               "Vertically Rotate Down with LR on Row 3",
               lambda w: rotate.vertical_rotate(w, 3, "D", "LR"))

ver_rl_u_on_1 = TStar.Operator("ver_rl_u_on_1",
                               "Vertically Rotate Up with RL on Row 1",
               lambda w: rotate.vertical_rotate(w, 1, "U", "RL"))
ver_rl_u_on_2 = TStar.Operator("ver_rl_u_on_2",
                               "Vertically Rotate Up with RL on Row 2",
               lambda w: rotate.vertical_rotate(w, 2, "U", "RL"))
ver_rl_u_on_3 = TStar.Operator("ver_rl_u_on_3",
                               "Vertically Rotate Up with RL on Row 3",
               lambda w: rotate.vertical_rotate(w, 3, "U", "RL"))
ver_rl_d_on_1 = TStar.Operator("ver_rl_d_on_1",
                               "Vertically Rotate Down with RL on Row 1",
               lambda w: rotate.vertical_rotate(w, 1, "D", "RL"))
ver_rl_d_on_2 = TStar.Operator("ver_rl_d_on_2",
                               "Vertically Rotate Down with RL on Row 2",
               lambda w: rotate.vertical_rotate(w, 2, "D", "RL"))
ver_rl_d_on_3 = TStar.Operator("ver_rl_d_on_3",
                               "Vertically Rotate Down with RL on Row 3",
               lambda w: rotate.vertical_rotate(w, 3, "D", "RL"))

TStar.register_operators([hor_l_on_1,hor_l_on_2,hor_l_on_3,
                          hor_r_on_1,hor_r_on_2,hor_r_on_3,
                          ver_lr_u_on_1,ver_lr_u_on_2,ver_lr_u_on_3,
                          ver_lr_d_on_1,ver_lr_d_on_2,ver_lr_d_on_3,
                          ver_rl_u_on_1,ver_rl_u_on_2,ver_rl_u_on_3,
                          ver_rl_d_on_1,ver_rl_d_on_2,ver_rl_d_on_3])

TStar.setup_and_run()
