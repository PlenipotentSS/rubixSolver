l_f = [
        ["G","G","G"],
        ["G","G","G"],
        ["G","G","G"]]
        
r_f = [
        ["W","W","W"],
        ["W","W","W"],
        ["W","W","W"]]
r_b = [
        ["B","B","B"],
        ["B","B","B"],
        ["B","B","B"]]
l_b = [
        ["Y","Y","Y"],
        ["Y","Y","Y"],
        ["Y","Y","Y"]]
top = [
        ["O","O","O"],
        ["O","O","O"],
        ["O","O","O"]]
bottom = [
        ["R","R","R"],
        ["R","R","R"],
        ["R","R","R"]]


l_f1 = [
        ["B","R","R"],
        ["B","R","R"],
        ["B","B","B"]]

r_f1 = [
        ["B","B","O"],
        ["B","B","O"],
        ["O","O","O"]]

r_b1 = [
        ["W","W","W"],
        ["W","G","G"],
        ["W","G","G"]]

l_b1 = [
        ["Y","Y","Y"],
        ["W","W","Y"],
        ["W","W","Y"]]
top1 = [
        ["R","R","R"],
        ["O","O","R"],
        ["O","O","R"]]
bottom1 = [
        ["G","G","G"],
        ["G","Y","Y"],
        ["G","Y","Y"]]

l_f2 = [
        ["R","B","R"],
        ["R","B","B"],
        ["R","R","R"]]

r_f2 = [
        ["B","O","B"],
        ["O","O","B"],
        ["B","B","B"]]

r_b2 = [
        ["G","G","G"],
        ["G","W","W"],
        ["G","W","G"]]

l_b2 = [
        ["W","W","W"],
        ["Y","Y","W"],
        ["W","Y","W"]]
top2 = [
        ["O","O","O"],
        ["R","R","O"],
        ["O","R","O"]]
bottom2 = [
        ["Y","Y","Y"],
        ["Y","G","G"],
        ["Y","G","Y"]]


## testing the cube
l_f3 = [
        ["G","G","G"],
        ["G","G","G"],
        ["G","G","G"]]
        
r_f3 = [
        ["W","W","W"],
        ["W","W","W"],
        ["W","R","W"]]
r_b3 = [
        ["B","B","B"],
        ["B","B","B"],
        ["B","B","B"]]
l_b3 = [
        ["Y","Y","Y"],
        ["Y","Y","Y"],
        ["Y","R","Y"]]
top3 = [
        ["O","O","O"],
        ["O","O","O"],
        ["O","O","O"]]
bottom3 = [
        ["R","W","R"],
        ["R","R","R"],
        ["R","Y","R"]]
test = [l_f3, r_f3, r_b3, l_b3, top3, bottom3]
#initial_state = test

##GLOBALS
initial_state = [l_f, r_f, r_b, l_b, top, bottom]
state = initial_state
cube_ina_cube = [l_f1, r_f1, r_b1, l_b1, top1, bottom1]
twisted_rings = [l_f2, r_f2, r_b2, l_b2, top2, bottom2]

