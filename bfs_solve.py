import helpers
import rubixTStar as TStar
import state_stored
import rotations as rotate
import copy


def successors(s):
    original = copy.deepcopy(s)
    sList = []
    sList += [rotate.horizontal_rotate(original,1,"L")]
    sList += [rotate.horizontal_rotate(original,2,"L")]
    sList += [rotate.horizontal_rotate(original,3,"L")]
    sList += [rotate.horizontal_rotate(original,1,"R")]
    sList += [rotate.horizontal_rotate(original,2,"R")]
    sList += [rotate.horizontal_rotate(original,3,"R")]

    sList += [rotate.vertical_rotate(original, 1, "U", "LR")]
    sList += [rotate.vertical_rotate(original, 2, "U", "LR")]
    sList += [rotate.vertical_rotate(original, 3, "U", "LR")]
    sList += [rotate.vertical_rotate(original, 1, "D", "LR")]
    sList += [rotate.vertical_rotate(original, 2, "D", "LR")]
    sList += [rotate.vertical_rotate(original, 3, "D", "LR")]
    
    sList += [rotate.vertical_rotate(original, 1, "U", "RL")]
    sList += [rotate.vertical_rotate(original, 2, "U", "RL")]
    sList += [rotate.vertical_rotate(original, 3, "U", "RL")]
    sList += [rotate.vertical_rotate(original, 1, "D", "RL")]
    sList += [rotate.vertical_rotate(original, 2, "D", "RL")]
    sList += [rotate.vertical_rotate(original, 3, "D", "RL")]
    titles = ["hor_l_on_1","hor_l_on_2","hor_l_on_3",
                "hor_r_on_1","hor_r_on_2","hor_r_on_3",
                "ver_lr_u_on_1","ver_lr_u_on_2","ver_lr_u_on_3",
                "ver_lr_d_on_1","ver_lr_d_on_2","ver_lr_d_on_3",
                "ver_rl_u_on_1","ver_rl_u_on_2","ver_rl_u_on_3",
                "ver_rl_d_on_1","ver_rl_d_on_2","ver_rl_d_on_3"]
    return [titles, sList]


##
## FUNCTIONS TO SOLVE CUBES WITH BREADTH FIRST SEARCH
################################################################################

def solve_layer1():
    helpers.print_rubix(state_stored.state)
    path = solve_bfs_1(state_stored.state, [])
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
    helpers.print_rubix(solution_1_stored)
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
    helpers.print_rubix(solution_2_stored)
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
        if helpers.has_layer1(s):
            global solution_1_stored
            solution_1_stored = s
            helpers.print_rubix(s)
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
        if helpers.has_layer1(s) and helpers.has_layer2(s):
            global solution_2_stored
            solution_2_stored = s
            helpers.print_rubix(s)
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
        if helpers.has_won(s):
            helpers.print_rubix(s)
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
