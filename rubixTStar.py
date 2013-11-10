""" TStar05.py       Steve Tanimoto, December 9, 2005.

    The T* module, Version 0.5.  It builds on version 0.4b.
    V 0.5 adds (1) menus, (2) load-save options for files,
    (3) a menu option to automatically generate a subtree.


    PURPOSE OF THIS MODULE:
        
    This module supports what we can call "interactive state
    space search".  Whereas traditional search algorithms in the
    context of artificial intelligence work completely automatically,
    this module lets the user make the moves.  It provides support
    to the user in terms of computing new states, displaying that
    portion of the state space that the user has embodied, and
    providing controls to permit the user to adapt the presentation
    to his or her needs.  This type of tool could ultimately be a
    powerful problem solving tool, useful in several different
    modes of use: interactive processing of individual objects,
    programming by demonstration (the path from the root to any
    other node in the state space represents a way of processing
    any object similar in structure to that of the root object.)
    By showing any number of states simultaneously, the user has
    the ability to compare, relatively easily, a large number of
    alternative versions (or derived states), and so it becomes
    convenient to compare large numbers of variations on processing
    sequences.

    The default domain here is simple (some trivial arithmetic)

    To use this code for a different application domain, certain
    methods and values need to be redefined. This can all be done
    in another file.  For an example of the use of T* in simple
    image processing, see the file TRAIPSE01.py.
      
    NOTES:
    For Version V0.4: Minor changes to simplify using the module
        in other programs.  The code for INITIAL_DATA for the
        demo application has been moved into the conditional code
        at the end. That means most applications that load the module
        will not have to redefine the method create_initial_state.
        They should not need to redefine get_full_root_data either.
    New Features for V0.3 are working
    New in Version 0.3:
        a. Option to apply only a single operator to a state.
        b. Automatic detection that an operator has already been applied
           to a state, with a warning about it.
        c. When generating "all children" of a state that already has at least
           one child, repetitions are automatically avoided.

    New in Version 0.2:
        A new Desc field for states.  This is separate from the Data field,
          but it can be used, in conjunction with the Python type of the
          data, in precondition testing. The Desc field is assumed to have
          a string as its value.  For example, if the data is of type Image,
          the Desc field might be "edges" to indicate that the state
          represents the resulting image after an edge-detection step.
        Preconditions for operators. A precondition is a predicate
          that can be applied to a state. If the result is true, then
          the operator can be applied to the state.
          If the precondition is None, then a default is used:
             lambda s: True.
        "Postconditions" for operators. What this means is that each
          operator can have a Python function that, when applied to
          the parent state, produces the Desc string for the new node.
          If the postcondition is None, then a default is used:
             lambda s: s.desc  # The parent's description is copied down.
        Code for the testing of precondition satisfaction within search.

    """
from Tkinter import *

# Note: It is very important that ImageTk be imported AFTER Tkinter
# Otherwise the constructor ImageTk.PhotoImage will not work.
from math import log

import state_stored

# Create some global variables:
TK_ROOT = None; SP_CANVAS = None; TREE_DISP = None
X_SCROLLBAR = None; Y_SCROLLBAR = None
COMMANDS_POPUP = None; COMMANDS_POPUP_FRAME = None
OPS_POPUP = None; OPS_POPUP_FRAME = None; LAST_EVENT=None
INITIAL_STATE=None; ALL_STATES=[]
OPERATORS=[]
PRODUCED_OBJECT=None
TINY_SIZE = 6

# The following 5 globals should normally be modified within
# an importing application of TStar:
TITLE=" T* Transparent STate-space search ARchitecture"
HEADLINE = "###TStar Version 05 Tree Description File"
TREE_FILE_TYPE="tst"
ROOT_DATA_FILE_TYPE="int"
ROOT_DATA_TYPE_DESCRIPTION="Files containing one integer"

USER="Unknown" # Used in the headers of any tree files that are saved.

def setup_and_run():
  global TK_ROOT, SP_CANVAS, TREE_DISP, INITIAL_STATE,\
         X_SCROLLBAR, Y_SCROLLBAR
  TK_ROOT = Tk(className=TITLE)
  TK_ROOT.grid_rowconfigure(0, weight=1)
  TK_ROOT.grid_columnconfigure(0, weight=1)

  # add scrollbars
  X_SCROLLBAR = Scrollbar(TK_ROOT, orient=HORIZONTAL)
  Y_SCROLLBAR = Scrollbar(TK_ROOT)
  X_SCROLLBAR.grid(row=1, column=0, sticky='ew')
  Y_SCROLLBAR.grid(row=0, column=1, sticky='ns')

  # Set up the canvas for drawing the tree diagrams
  SP_CANVAS = Canvas(TK_ROOT, xscrollcommand=X_SCROLLBAR.set,
                     yscrollcommand=Y_SCROLLBAR.set)
  SP_CANVAS.grid(row=0,column=0,sticky='nesw')
  SP_CANVAS.bind("<Button-1>", left_click)
  SP_CANVAS.bind("<Button-3>", right_click)
  X_SCROLLBAR.config(command=SP_CANVAS.xview)
  Y_SCROLLBAR.config(command=SP_CANVAS.yview)
  X_SCROLLBAR.set(0.1, 0.5)
  Y_SCROLLBAR.set(0.1, 0.5)
  create_menus()
  create_commands_popup() # Used when the user right-clicks on a node.
  create_initial_state()  # Create the initial state and display it.
  initialize_states_and_display()
  TK_ROOT.mainloop()

def create_menus():
  menu_bar = Menu(TK_ROOT)
  TK_ROOT.config(menu=menu_bar)
  fileMenu = Menu(menu_bar)
  menu_bar.add_cascade(label="File", menu=fileMenu)
  fileMenu.add_command(label="Open Tree...", command=open_tree_file)
  fileMenu.add_command(label="Save Tree As...", command=save_tree_file)
  fileMenu.add_separator()
  fileMenu.add_command(label="Exit", command=TK_ROOT.destroy)

  add_app_specific_menus(menu_bar)
  
  helpMenu = Menu(menu_bar)
  menu_bar.add_cascade(label="Help", menu=helpMenu)
  helpMenu.add_command(label="Instructions", command=show_instructions)
  helpMenu.add_command(label="About", command=show_about)

def add_app_specific_menus(menubar): pass # Redefine this in your application.

def open_tree_file():
  import tkFileDialog
  FILE_NAME = tkFileDialog.askopenfilename(
    filetypes=[("T-Star Tree Files", TREE_FILE_TYPE)])
  try:
    f = open(FILE_NAME, "r")
    temp_headline = f.readline()[:-1]
    if temp_headline[:16] != HEADLINE[:16]:
        print "This file is incompatible with this version of TStar"
        return None
    temp_body = f.read()
    f.close()
  except:
    print "Could not load new data from file: ", FILE_NAME
  else:
    create_initial_state()
    initialize_states_and_display()
    current_state = INITIAL_STATE
    try:
      import string
      for line in string.split(temp_body, "\n"):
        if line[0]=="#": continue
        if line[0]=="v":
            line = line[2:]
            opidx = get_int_param(line,"op")
            op = applicable_ops(current_state)[opidx]
            current_state = TREE_DISP.try_to_create_new_child(current_state, op)
        if line[0]=="^":
            if current_state.p:
              current_state = current_state.p
            continue
        try:
          h = get_int_param(line,"h")
          if h: current_state.hidden = True
          current_state.display_version = get_int_param(line,"d")
          current_state.n = get_int_param(line,"n")
        except:
          print "could not find parameter (maybe h, d, or n) for state in the line:" + line
    except:
      print "Parsing error in line: " + line
      raise
    redraw_tree()
    app_specific_tree_load(FILE_NAME)
    return temp_body

def get_int_param(line, param_name):
    """Retrieve an integer parameter in the given line of text,
    directly following the first occurrence of param_name and the
    equals sign (=)."""
    j = line.index(param_name + "=")
    start = j + len(param_name) + 1
    end = line.index(";", start)
    strparam = line[start: end]
    val = int(strparam)
    return val

def save_tree_file():
  """Brings up a file dialog box, so the user can choose a
  file for saving the current tree configuration. Then saves it."""
  global TK_ROOT, USER
  import tkFileDialog
  savefile = tkFileDialog.asksaveasfilename(
    filetypes=[("T-Star Tree Files", TREE_FILE_TYPE)],
    defaultextension=TREE_FILE_TYPE)
  if savefile:
    try:
      tree_desc_str = INITIAL_STATE.get_tree_desc_str()
      f = open(savefile, "w")
      f.write(HEADLINE+"\n")
      f.write("###USER="+USER+"\n")
      import time
      f.write("###TIME="+str(time.asctime())+"\n")
      f.write(tree_desc_str)
      f.close()
      app_specific_tree_save(savefile)
    except:
        print "Couldn't write the file: ", savefile
        raise

def app_specific_tree_save(fn): pass
def app_specific_tree_load(fn): pass

def show_instructions():
  import tkMessageBox
  tkMessageBox.showinfo("Help","Instructions:\n\n"
        "Right-clicking on a node opens a pop-up menu of node options.\n"
        "Left-clicking re-applies the most recent command to the node clicked on.\n\n"
        "T-Star's main purpose is to facilitate user exploration of a space "
        'of possible "states" of a design or problem. '
        "It keeps track of what states have been explored, and it displays this "
        "information in a flexible way on the screen. "
        "A tree can be saved to or loaded from a disk file, in order to "
        "checkpoint a session or to prepare a demonstration.")

def show_about():
  import tkMessageBox
  tkMessageBox.showinfo("About","TStar Version 0.5\nCopyright 2006 Steven Tanimoto\n"
        "University of Washington, Seattle, WA\n\n"
        "T-Star is an experimental design and problem-solving tool.")

def initialize_states_and_display():
    global ALL_STATES, TREE_DISP
    ALL_STATES = [INITIAL_STATE]
    initial_node = NODE_CLASS(INITIAL_STATE)
    TREE_DISP = tree_display(SP_CANVAS,NODE_CLASS)
    TREE_DISP.state_node_hash = {}
    TREE_DISP.state_node_hash[INITIAL_STATE] = initial_node
    TREE_DISP.all_nodes = [initial_node]
    redraw_tree()

def right_click(event):
  """If the user clicked on a node,
     make it the selected node, and perform the
     current command on it, if legal."""
  x = SP_CANVAS.canvasx(event.x)
  y = SP_CANVAS.canvasy(event.y)
  for nd in TREE_DISP.all_nodes:
      if nd.clicked_on(x,y):
          update_node_selection(nd)
          perform_last_command()
          break

def update_node_selection(nd):
  """Modify the display to highlight the correct
     selected node."""
  sn = TREE_DISP.selected_node
  if sn:
    sn.unselect()
    if not sn.s.hidden:
      sn.unpaint()
      sn.paint()
  TREE_DISP.selected_node = nd
  nd.select()
  nd.unpaint()
  nd.paint()

def left_click(event):
  temp_object = get_full_root_data()
  global PRODUCED_OBJECT # make available in case user wants to save it.
  global THIS_STATE
  THIS_STATE = temp_object
  PRODUCED_OBJECT = Wrapped_string(convert_toLine(temp_object))
  """If the user right-clicked on a node, select it,
     and bring up the popup menu"""
  x = SP_CANVAS.canvasx(event.x)
  y = SP_CANVAS.canvasy(event.y)
  global LAST_EVENT
  LAST_EVENT = event
  for nd in TREE_DISP.all_nodes:
      if nd.clicked_on(x,y):
          update_node_selection(nd)
          show_popup_menu(COMMANDS_POPUP,event)
          break

def make_initial():
  global INITIAL_DATA
  this_state = TREE_DISP.selected_node.s
  op_sequence = this_state.get_op_sequence()
  function_sequence = this_state.get_fn_sequence()
  temp_object = get_full_root_data()
  for fn in function_sequence:
    temp_object = fn(temp_object)
  INITIAL_DATA = temp_object
  create_initial_state()
  initialize_states_and_display()
  state_stored.state = temp_object

def create_commands_popup():
  global COMMANDS_POPUP, COMMANDS_POPUP_FRAME, TK_ROOT
  COMMANDS_POPUP_FRAME = Frame(TK_ROOT, width=200, height=200)
  COMMANDS_POPUP = Menu(COMMANDS_POPUP_FRAME, tearoff=0)
  P = COMMANDS_POPUP
  P.add_command(label="Grow all children", command=make_children)
  P.add_command(label="Apply one operator...", command=apply_one_op)
  P.add_command(label="Make Tiny", command=make_tiny)
  P.add_command(label="Make Normal", command=make_normal)
  P.add_command(label="Make Descendants Tiny", command=make_descendants_tiny)
  P.add_command(label="Make Descendants Mini", command=make_descendants_mini)
  P.add_command(label="Make Descendants Normal", command=make_descendants_normal)
  P.add_command(label="Make Ancestors Normal", command=make_ancestors_normal)
  P.add_command(label="Hide Subtree", command=hide_subtree)
  P.add_command(label="Show Details", command=show_details)
  P.add_command(label="Unhide Children", command=unhide_children)
  P.add_command(label="Save This Node", command=do_save)
  P.add_command(label="Make Initial State", command=make_initial)

def show_popup_menu(pm, event):
    x = SP_CANVAS.canvasx(event.x)
    y = SP_CANVAS.canvasy(event.y)
    pm.post(event.x, event.y)

class temp_op_callable:
    """Objects in this class are used as temporary functions,
       similar to closures in functional languages. They are used
       as the 'command' argument to entries in the popup menu for
       applicable operators.  This list is regenerated each time
       the user wants to apply a single operator to the selected
       state."""
    def __init__(self, op, s):
        self.op = op; self.s = s
    def __call__(self):
        if TREE_DISP.try_to_create_new_child(self.s, self.op):
            redraw_tree()
        else: print "No new state created."
        
def create_operators_popup():
  global OPS_POPUP, OPS_POPUP_FRAME, TK_ROOT
  OPS_POPUP_FRAME = Frame(TK_ROOT, width=200, height=200)
  OPS_POPUP = Menu(OPS_POPUP_FRAME, tearoff=0)
  count = 0; temp_func = []
  for op in applicable_ops(TREE_DISP.selected_node.s):
      temp = temp_op_callable(op, TREE_DISP.selected_node.s)
      OPS_POPUP.add_command(label=op.name,
                            command=temp )

def perform_last_command():
    """This is invoked when the user clicks the left mouse button
       on a node."""
    last_command()

def set_last_command(the_last_command):
    global last_command
    last_command = the_last_command

def redraw_tree():
    TREE_DISP.draw_tree_inorder(INITIAL_STATE)
    SP_CANVAS.config(scrollregion=SP_CANVAS.bbox(ALL))
    
def make_children():
    """Generate the children of the selected node. If any
       children already exist, only generate those children
       using other operators than those used to create the
       existing children."""
    set_last_command(make_children)
    sn = TREE_DISP.selected_node
    print sn
    #if sn.is_leaf():
    TREE_DISP.grow_successors_and_their_nodes(sn)
    redraw_tree()
      
last_command = make_children # Default command for left mouse button.

def apply_one_op():
    """Populate a popup menu with the names of currently applicable
       operators, and let the user choose which one to apply."""
    set_last_command(apply_one_op)
    currently_applicable_ops = applicable_ops(TREE_DISP.selected_node.s)
    #print "Applicable operators: ",\
    #    map(lambda o: o.name, currently_applicable_ops)
    global OPS_POPUP
    create_operators_popup()
    show_popup_menu(OPS_POPUP, LAST_EVENT)

def make_tiny():
    """Make the selected node as small as possible."""
    set_last_command(make_tiny)
    TREE_DISP.selected_node.s.display_version = 0
    redraw_tree()

def make_mini():
    """Make the selected node relatively small."""
    set_last_command(make_mini)
    TREE_DISP.selected_node.s.display_version = 1
    redraw_tree()

def make_normal():
    """Restore the selected node to normal size."""
    set_last_command(make_normal)
    TREE_DISP.selected_node.s.display_version = 2
    redraw_tree()

def make_descendants_tiny():
    """Minimize the selected node and all of its descendants."""
    set_last_command(make_descendants_tiny)
    descendants = preorder_collect(TREE_DISP.selected_node.s, root=True)
    map(lambda s: s.set_display_version(0), descendants)
    redraw_tree()

def make_descendants_mini():
    """Set the selected node and all of its descendants to the middle size."""
    set_last_command(make_descendants_mini)
    descendants = preorder_collect(TREE_DISP.selected_node.s, root=True)
    map(lambda s: s.set_display_version(1), descendants)
    redraw_tree()

def make_descendants_normal():
    """Restore the selected node and all of its descendants
       to normal size, but do not change the hidden status
       of any nodes."""
    set_last_command(make_descendants_normal)
    descendants = preorder_collect(TREE_DISP.selected_node.s, root=True)
    map(lambda s: s.set_display_version(2), descendants)
    redraw_tree()

def make_ancestors_normal():
    """Restore the selected node and those on the path from it to
       the root."""
    set_last_command(make_ancestors_normal)
    ancestors = collect_ancestors(TREE_DISP.selected_node.s)
    map(lambda s: s.set_display_version(2), ancestors)
    redraw_tree()

def hide_subtree():
    """Hide the selected node (provided it is not the root node).
       The node will not be displayed when its status is 'hidden'.
       Its descendants will not be displayed, either, although they
       do not necessarily have the hidden status directly."""
    set_last_command(hide_subtree)
    if TREE_DISP.selected_node.s == INITIAL_STATE:
        print "Cannot hide the root,",\
              "because there would be no way to unhide it."
    else:
      TREE_DISP.selected_node.s.hidden = True
      redraw_tree()

def unhide_children():
    set_last_command(unhide_children)
    these_children = children(TREE_DISP.selected_node.s)
    map(lambda s: s.unhide(), these_children)
    redraw_tree()

# The following is a domain-dependent display generator.
def show_details():
    set_last_command(show_details)
    this_state = TREE_DISP.selected_node.s
    op_sequence = this_state.get_op_sequence()
    function_sequence = this_state.get_fn_sequence()
    op_seq_desc = map(lambda o: o.name, op_sequence)
    description = [str(this_state)]
    description += ["Operator sequence for this state is:"]
    count = 0
    for op in op_seq_desc:
        count += 1
        description += ["Step " + str(count) + ": " +str(op)]
    top = Toplevel(TK_ROOT)
    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)
    temp_object = get_full_root_data()
    for fn in function_sequence:
       temp_object = fn(temp_object)
    global PRODUCED_OBJECT # make available in case user wants to save it.
    PRODUCED_OBJECT = Wrapped_string(convert_toLine(temp_object))

    # add scrollbars
    s = Scrollbar(top)
    TEXT = Text(top)
    TEXT.focus_set()
    s.pack(side=RIGHT,fill=Y)
    TEXT.pack(side=LEFT)
    s.config(command=TEXT.yview)
    TEXT.config(yscrollcommand=s.set)
    oS = str(convert_toLine(temp_object))
    oS = "   "+oS[:3]+"\n"+"   "+oS[3:6]+"\n"+"   "+oS[6:9]+"\n"+ \
         oS[9:21]+"\n"+oS[21:33]+"\n"+oS[33:45]+"\n"+ \
         "   "+oS[45:48]+"\n"+"   "+oS[48:51]+"\n"+"   "+oS[51:54]+"\n"
    description += ["State data:"]
    description += [oS]
    for i in range(len(description)):
      TEXT.insert(END, str(description[i])+"\n")
##    info_label = Label(top, text="State type = "+this_state.desc)
##    info_label.grid(row=1,column=0)
##    
##    save_button = Button(top, text="Save object as...", command=do_save)
##    save_button.grid(row=2,column=0)

    mainloop()

    #display_data_in_detail(detail_canvas, description, op_seq_desc, temp_object, this_state)
    #detail_canvas.create_image(0,0,image=new_image,anchor=NW)
    #new_image.width = new_image.width # Dummy op that makes image show up.

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

def load():
    global FILE_NAME, ROOT_DATA_FILE_TYPE, ROOT_DATA_TYPE_DESCRIPTION
    import tkFileDialog
    FILE_NAME = tkFileDialog.askopenfilename(
        filetypes=[(ROOT_DATA_TYPE_DESCRIPTION, ROOT_DATA_FILE_TYPE)])
    try:
        temp = read_data_from_file(FILE_NAME)
    except:
        print "Could not load new data from file: ", FILE_NAME
    else:
        global INITIAL_DATA
        INITIAL_DATA = build_data_object(temp)
        create_initial_state()
        initialize_states_and_display()

def do_save():
    global TK_ROOT, PRODUCED_OBJECT
    import FileDialog
    sfd = FileDialog.SaveFileDialog(TK_ROOT)
    savefile = sfd.go(key="test")
    if savefile:
        PRODUCED_OBJECT.save(savefile)

class State:
    """encapsulates the state-space element, together with
    any possible annotations, strategy or history info.
    """
    number = 0
    tiny_size_factor = 0.12 # used by the size_needed method
    def __init__(self, data, parent, last_operator, desc=""):
        self.p = parent
        self.last_operator = last_operator # This is used to
        # keep track of how this state was obtained from its parent.
        self.first_child = None
        self.last_child = None
        self.right_sibling = None

        left_sibling = None # temporary assignment.
        # Figure out the depth of the state and its left sibling,
        # if any, using the parent's last_child reference:
        if not parent:
            self.d = 0
        else:
            self.d = parent.d + 1
            left_sibling = parent.last_child
            parent.last_child = self
        # Let the left sibling know about its new right sibling:
        if left_sibling:
            left_sibling.right_sibling = self
        else:
            if parent:
                # If it has no left sibling, then it is a first
                # child. If it also has a parent, then the parent
                # should be updated:
                parent.first_child = self
        # Assign this state a unique number:
        self.n = State.number
        State.number += 1
        self.hidden = False
        self.display_version=2 # 0=tiny, 1=miniature, 2=normal, 3=expanded. 
    # Here is the domain dependent component of the state:
        self.data = data
        self.desc = desc
    def __str__(self):
        return "[state %d]" % self.n
    def space_needed(self):
        if self.display_version==0: #return 0.12 # "tiny" # NOTE: NO LONGER USED
            return State.tiny_size_factor
        if self.display_version==1: return 0.3 # "mini"
        if self.display_version==2: return 1.0 # "normal"
        if self.display_version==3: return 2.0 # "double" (not in use as of Nov.14)
        else: return 1
    def set_display_version(self,dv):
        self.display_version = dv;
    def unhide(self):
        self.hidden = False
    def get_op_sequence(self):
        if not self.p: return []
        else: return self.p.get_op_sequence() + [self.last_operator]
    def get_fn_sequence(self):
        if not self.p: return []
        else: return self.p.get_fn_sequence() + [self.last_operator.function]
    def has_hidden_children(self):
        this_child = self.first_child
        while this_child:
            if this_child.hidden: return True
            this_child = this_child.right_sibling
        return False
    def get_tree_desc_str(self):
        tds = "n="+str(self.n)
        tds += ";h="
        if self.hidden: tds += '1'
        else: tds += '0'
        tds += ";d="+str(self.display_version)+";"
        this_child = self.first_child
        while this_child:
            applicables = applicable_ops(self)
            print "applicable ops for state "+str(self)+" are:", applicables
            tds += "\nv:" + "op=" + str(applicables.index(this_child.last_operator))+";"
            tds += this_child.get_tree_desc_str()
            this_child = this_child.right_sibling
        tds += "\n^"
        return tds


def default_precondition(s): return True
def default_postcondition(s): return s.desc

class Operator:
    """encapsulates a transformation on states.
    """
    def __init__(self, thisID, name, data_function,
                 precondition=default_precondition,
                 postcondition=default_postcondition):
        self.id = thisID
        self.name = name
        self.function = data_function
        self.precondition = precondition
        self.postcondition = postcondition
        
    def __str__(self):
        s = "<operator: %s>" % (self.name)        
        return s
    
    def is_applicable(self, old_state):
        return apply(self.precondition, [old_state])
    
    def _apply(self, old_state):
        #print "Applying operator named ", self.name
        return State(apply(self.function, [old_state.data]),
                     old_state,
                     self,
                     desc=apply(self.postcondition, [old_state])
                     )


# The node object consists of a state plus some display coordinates.
# It's sort of the graphical embodiment of the state.
class Node:
    width=64; height=64 # Dimensions of the node (actually the image)
    def __init__(self, state):
        self.s = state
        self.selected = False
        self.rect = None
        self.text = None
        self.qin = 0 # quasi-inorder number for inorder display
        self.has_painted_content=False
        self.domain_specific_init(state)
        self.x = 0

    def set_coords(self, x, y):
        self.x = x
        self.y = y
    def paint(self):
        if self.s.display_version==0:
            w=TINY_SIZE; h=TINY_SIZE
        else:
            sn = self.s.space_needed()
            w = self.width*sn; h = self.height*sn
        # Display a box (which will appear behind the state's image):
        node_color = "light blue"
        if self.s.has_hidden_children(): node_color = "light gray"
        if self.selected:
          self.rect = \
            SP_CANVAS.create_rectangle(self.x-w/2-3,self.y-h/2-3,
               self.x+w/2+2,self.y+h/2+2,fill="light green")
        else:
          self.rect = \
            SP_CANVAS.create_rectangle(self.x-w/2-1,self.y-h/2-1,
              self.x+w/2+1,self.y+h/2+1,fill=node_color)
        # Display the image itself:
        if self.s.display_version > 1:
            self.paint_label(w,h)
            self.paint_content(w,h,SP_CANVAS)
        
    def paint_label(self,w,h):
        # Display the state identifying string:
        self.text=SP_CANVAS.create_text(self.x,self.y-h/2-12,
                                        text=str(self.s))
    def unpaint(self):
        if self.rect: 
          SP_CANVAS.delete(self.rect)
        if self.text:
          SP_CANVAS.delete(self.text)
        self.unpaint_content(SP_CANVAS)

    def clicked_on(self, x,y):
        if self.s.hidden: return False
        sn = self.s.space_needed()
        w = self.width*sn; h = self.height*sn
        return (self.x - w/2 < x < self.x + w/2 and
                self.y - h/2 < y < self.y + h/2)
    def select(self):
        self.selected = True
    def unselect(self):
        self.selected = False
    def is_leaf(self):
        if self.s.first_child: return False
        else: return True

    # Override the following 3 methods in a child class to
    # change the application domain for the program.
    def domain_specific_init(self, state):
        pass
    def paint_content(self,w,h,a_canvas):
        self.has_painted_content=True
        self.p=a_canvas.create_text(self.x,self.y,
                                        text=str(self.s.data))
    def unpaint_content(self,a_canvas):
        if self.has_painted_content:
            a_canvas.delete(self.p)
        self.has_painted_content=False

NODE_CLASS=Node

# A kind of object to represent a tree display.
# It references a Tkinter canvas.
# It provide a method to draw a tree from a list of states.
LAST_INCR = 0
class tree_display:
    left_margin = 50
    top_margin = 50
    deltax = 0  # horiz. scaling factor for values from quasi-inorder-tr.
    deltay = 0 # vertical dist. betw. node centers, level-to-level.
    def __init__(self, acanvas, node_class_to_use):
        self.tdcanvas = acanvas
        self.state_node_hash = {}
        self.all_nodes = [];
        self.selected_node = None
        self.running_x = 0
        self.node_class = node_class_to_use

    def draw_tree_inorder(self, root):
        self.tdcanvas.delete(ALL) # remove any existing display. 
        # Assign x coordinates to the nodes by performing 
        # a quasi-inorder traversal of the tree.
        root_node = self.state_node_hash[root]
        tree_display.deltax = int((root_node.width + 2)*1.2)
        tree_display.deltay = int((root_node.height + 2)*1.2)+10
        nodes_to_draw = self.get_nodes_quasi_inorder(root,[],first_state=True)
        for n in nodes_to_draw:
          n.x = tree_display.left_margin + \
                tree_display.deltax*(n.qin + 0.5)
          n.y = tree_display.top_margin + n.s.d * \
                tree_display.deltay
          n.set_coords(n.x,n.y)
        for n in nodes_to_draw:
          if n.s.d > 0:
              parent_node = self.state_node_hash[n.s.p]
              self.tdcanvas.create_line(
                  n.x, n.y, parent_node.x, parent_node.y)
        # Finally, paint all the nodes:
        for n in nodes_to_draw:
          n.paint()

    def get_nodes_quasi_inorder(self, a_state, nodelist_so_far,
                                first_state = False):
      """This performs something like inorder traversal starting at
         the given state. Its most important job is to compute
         an x coordinate value for each node. (The canvas x
         will be obtained by multiplying this by a constant.)
         If the state is hidden, skip it."""
      if a_state.hidden: return nodelist_so_far
      if first_state: self.running_x = 0
      global LAST_INCR
      a_node = self.state_node_hash[a_state] # get tree node assoc. with this state.
      epsilon = 0.02 # enough to separate nodes in tiny mode.
      a_node.w2 = (a_state.space_needed()/2.0)+epsilon # half the display width of the node.
      #children_states = children(a_state)
      #nchildren = len(children)
      unhidden_children_states = unhidden_children(a_state) # get the list of children.
      n_unhidden_children = len(unhidden_children_states)
      if n_unhidden_children==0:        # if a_state has no unhidden children...
        self.running_x += a_node.w2     # add half the display width to running_x.
        a_node.qin = self.running_x     # the node's quasi-inorder position is saved.
        self.running_x += a_node.w2     # the other half of the node-width is added to running_x
        return nodelist_so_far + [a_node] # return, with this node appended to the given node list.
      else:
        nleft = min(n_unhidden_children, (1 + n_unhidden_children) / 2) # the number to show hanging to the left.
        nright = n_unhidden_children - nleft        # the number to show hanging to the right.
        next_child = a_state.first_child            # prepare to iterate through the left kids.
        starting_x = self.running_x
        for i in range(nleft):
            if not next_child:
                print "Error, expected another unhidden child in state",\
                      a_state; break
            if next_child.hidden: next_child = next_child.right_sibling
            LAST_INCR = next_child.space_needed() # amount of horiz space most recently used for a child at this level. 
            temp = self.get_nodes_quasi_inorder(next_child,[]) # recursive call on the child.
            nodelist_so_far += temp
            last_child = next_child
            #last_incr = next_child.space_needed() # amount of horiz space most recently used for a child at this level. 
            next_child = next_child.right_sibling
        if self.running_x < starting_x + a_node.w2:
            self.running_x = starting_x + a_node.w2
        a_node.qin = self.running_x  # Let's use the running_x value after all left-hanging children for their parent.
        if n_unhidden_children == 1: # special case of one child -- use the same running x value across generations.
            a_node.qin = self.state_node_hash[last_child].qin
            self.running_x = max(self.running_x, a_node.qin + a_node.w2)
        elif n_unhidden_children%2 == 1:  # Case of an odd number of children -- adjust parent position to be between two children.
            #if a_node.w2 <= last_incr: # Not exactly the correct condition
            if a_node.w2 <= LAST_INCR: # Not exactly the correct condition
                # but it works in all except a few configs of large and small nodes.
               a_node.qin -= a_node.w2
        nodelist_so_far.append(a_node)
        if nright==0: return nodelist_so_far 
        for i in range(nright): # Now process the right-hanging children...
            if not next_child:
                print "Error, expected another unhidden child in state",\
                      a_state; break
            if next_child.hidden: next_child = next_child.right_sibling
            LAST_INCR = next_child.space_needed()
            temp = self.get_nodes_quasi_inorder(next_child, [])
            nodelist_so_far += temp
            #last_incr = next_child.space_needed()
            next_child = next_child.right_sibling
        # Handle a possible situation in which the right children take up less horizontal space than half the parent.
        if self.running_x < a_node.qin + a_node.w2:
            self.running_x = a_node.qin + a_node.w2 + epsilon
        return nodelist_so_far
    def grow_successors_and_their_nodes(self, a_node):
        these_children = successors(a_node.s)
        for c in these_children:
            self.register_state_and_node(c)
    def register_state_and_node(self, s):
        ALL_STATES.append(s)
        new_node = self.node_class(s)
        self.state_node_hash[s] = new_node
        self.all_nodes.append(new_node)
        
    def try_to_create_new_child(self, a_state, an_operator):
        existing_child = a_state.first_child
        op_is_redundant = False
        while existing_child:
            if existing_child.last_operator == an_operator:
                op_is_redundant = True; break
            existing_child = existing_child.right_sibling
        if op_is_redundant:
            user_response_num = warn_about_redundancy()
            if user_response_num == 1: return None
        this_child = an_operator._apply(a_state)
        if not this_child: return None
        self.register_state_and_node(this_child)
        return this_child

def warn_about_redundancy():
    import Dialog
    d = Dialog.Dialog(None, {'title': 'Duplicate An Existing State?',
        'text': 'The operator you have chosen has already been applied to'
                ' the selected state. Really create an identical twin?',
        'bitmap': 'questhead',
        'default': 0,
        'strings': ('Create twin',
                    'Cancel reapplication')})
    return d.num

def preorder_collect(r, root=False):
    """Traverses the subtree rooted at state r with preorder,
       and places each state reached into the list of states to
       be returned.  When calling from top level (non-recursively),
       be sure to use root=True, so that the method will not try
       to access its right sibling, which would take it out of its
       own subtree."""
    states_found = [r]
    if r.first_child:
        states_found += preorder_collect(r.first_child)
    if not root:
        if r.right_sibling:
            states_found += preorder_collect(r.right_sibling)
    return states_found

def collect_ancestors(a_state):
    if not a_state.p:
        return [a_state]
    else:
        return collect_ancestors(a_state.p)+[a_state]


def children(state):
    """Returns the existing children of the given state by
       traversing links."""
    if state.first_child:
        return [state.first_child] + right_siblings(state.first_child)
    else:
        return []

def unhidden_children(state):
    return filter(lambda s: not s.hidden, children(state))

def right_siblings(state):
    """Returns the siblings to the right of the given state by
       traversing links."""
    if state.right_sibling:
        return [state.right_sibling] + right_siblings(state.right_sibling)
    else:
        return []

def applicable_ops(s):
    """Returns the subset of OPERATORS whose preconditions are
       satisfied by the state s."""
    return filter(lambda o: o.is_applicable(s), OPERATORS)
    
def successors(s):
    """Generates and returns the successors of the state s by
       applying to it all those operators in the list OPERATORS
       that are applicable to the state s."""
    ops_already_applied_here = map(lambda c: c.last_operator, children(s))
    nonredundant_ops = filter(lambda op: not op in ops_already_applied_here,
                              applicable_ops(s))
    return map(lambda o: o._apply(s), nonredundant_ops)

def register_operators(ops):
    """Takes the given list ops of operators and assigns it to
       the global variable OPERATORS. Also computes the length
       of the list and assigned it to the global BRANCHING_FACTOR."""
    global OPERATORS
    OPERATORS = ops
    global BRANCHING_FACTOR
    BRANCHING_FACTOR = len(OPERATORS)

def gen_subtree():
    print "You have the selected the (unimplemented) command gen_subtree."
    # Get selected node.
    # Get number of levels requested (default: 2) and display mode (default: tiny)
    # Use Breadth-First approach to generating the requested subtree,
    #   automatically avoiding duplicates.
    # Set the display mode on all the new states (but not on subtree components
    #   that existed before the command was executed).
    sn = TREE_DISP.selected_node
    if not sn:
        print "No state has been selected, so we will use the root state."
        sn = TREE_DISP.state_node_hash[INITIAL_STATE]
    n_new_levels = 2 # hardcoded for now
    new_states_display_mode = 0 # hardcoded for now
    pending = [sn] # list of nodes whose successors must be generated.
    for i in range(n_new_levels):
        new_pending = []
        for node in pending:
            these_children = successors(node.s)
            for c in these_children:
                global ALL_STATES
                ALL_STATES.append(c)
                new_node = TREE_DISP.node_class(c)
                TREE_DISP.state_node_hash[c] = new_node
                TREE_DISP.all_nodes.append(new_node)
                new_pending.append(new_node)
        pending = new_pending
    redraw_tree()

# Domain-dependent part of setup:
"""
The following parts of this program are specific to the
domain of simple operations on numbers.
The data component of each state is a Wrapped_int which
is an int that knows how to save itself to a file.
Saving is not really important for an int, but we do that
here for consistency with what one would want if the data
were more complicated, such as with an image."""

class Wrapped_obj:
  """Provides objects with a method to save themselves."""
  def save(self,filename):
    print "Preparing to save the data ",self
    try: 
      f = open(filename, "w")
      f.write(self)
      f.close()
    except: print "Couldn't write the file: ", filename
    else: print "Saved the number ", self, " to file ", filename

class Wrapped_int(int,Wrapped_obj):
  """Provides int data with a method to save themselves."""
  pass

class Wrapped_string(str,Wrapped_obj):
  """Provides string data with a method to save themselves."""
  pass

def create_initial_state():
  """(Re)initializes the counter for states, and
     create a new state, assigning it to the global
     variable INITIAL_STATE."""
  global INITIAL_STATE
  State.number = 0 # Start state numbering from 0.
  INITIAL_STATE = State(INITIAL_DATA,None,None,desc='number')

def read_data_from_file(filename):
    """Gets information from a file."""
    f = open(filename, "r")
    temp = f.read()
    f.close()
    return temp

def build_data_object(data):
  """Converts the information read in from a file to the
     form needed within an initial state."""
  return Wrapped_int(data)

def f1(n):return Wrapped_int(n+1)
def f2(n):return Wrapped_int(n*2)
def f3(n):return Wrapped_int(n*7)
def f4(n):return Wrapped_int(n / 10)
def f5(n): return Wrapped_string(num_to_string(n))
def f6(strng): return Wrapped_string(strng.swapcase())
def f7(strng): return Wrapped_string(str_rot(strng))

def num_to_string(n):
    """Converts, for example, 475 to 'four-seven-five' """
    if n<10: return {0:'zero',1:'one',2:'two',3:'three',4:'four',
                     5:'five',6:'six',7:'seven',8:'eight',9:'nine'}[n]
    else: return num_to_string(n/10)+'-'+num_to_string(n%10)

def str_rot(strng):
    """Moves the last character of the string to the front."""
    if len(strng)<2: return strng
    else: return strng[-1]+strng[:-1]
    
def needs_num(s):
    """Returns True if the data for state s is a Wrapped_int."""
    return isinstance(s.data, Wrapped_int)

def needs_str(s):
    """Returns True if the data for state s is a Wrapped_string."""
    return isinstance(s.data, Wrapped_string)

# Note that six of our seven operators use the default postcondition,
# which is for the child state to receive the same desc value as
# its parent.  Only op5 changes it (from 'number' to 'string')
arithmetic_operators = map(
    lambda name,fun:Operator("",name,fun,precondition=needs_num),
    ['Add-1', 'Times-2', 'Times-7', 'Div-10'],
    [f1, f2, f3, f4])

convert_operators = [
    Operator("",'Convert',f5,
             precondition=needs_num,
             postcondition=lambda s: 'string') ]
string_operators = [
    Operator("",'SwapCase',f6, precondition=needs_str),
    Operator("",'Rotate',f7, precondition=needs_str) ]

register_operators(arithmetic_operators +
                   convert_operators +
                   string_operators)

def get_full_root_data():
    return INITIAL_STATE.data
  
def display_data_in_detail(detail_canvas, desc, op_seq, temp_object, the_state):
    # temp_object is ignored in this default application.
    # op_seq is not used explicitly, since desc, which embeds it in
    #  a string, is being used here instead.
    # It is important in TRAIPSE and other applications.
    detail_canvas.create_text(200,200,text=desc)

# The following is only executed if this module is being run as the main
# program, rather than imported from another one.
if __name__ == '__main__':
  print "Setting up..."
  global INITIAL_DATA
  INITIAL_DATA = Wrapped_int(1)
  setup_and_run()
  print "The session is finished."



