import itertools
from collections import Counter

class Tree:
  def __init__(self, name, can_repeat):
    self.name = name
    self.children = []
    self.can_repeat = can_repeat
  def __repr__(self):
    return self.name
  def walk(self, indent=0, visited=[], recurse=False):
    tag = ""
    if self.can_repeat:
      tag = "(recursive)"
    
    # print("{}{}{}".format(((indent * 2)) * " ", self, tag))
    
      
    if recurse:
      for child in self.children:
    
        myvisited = list(visited)
        print("{}{}".format((1 + (indent * 2)) * " ", child))
        if child in visited:
          myvisited.append(child)
          child.walk(indent + 1, myvisited, False)
        else:
          myvisited.append(child)
          child.walk(indent + 1, myvisited, True)
          
        
      # visited[self] = True
        
  def add_child(self, name, can_repeat):
    new_node = Tree(name, can_repeat)
    
    if self.can_repeat:
        new_node.children.append(self)
    elif not self.can_repeat:
      new_node.children = self.children
    self.children.append(new_node)

events = [
  ("+", "windows", False),
  ("+", "mac", False),
  ("+", "linux", False),
  ("+", "enter_scope", True)
]

root = Tree("root", True)
for event in events:
  if event[0] == "+":
    root.add_child(event[1], event[2])

root.walk(0, {}, True)

operating_systems = ["windows", "mac", "linux"]


print(list(itertools.permutations(["scope_enter", "initialize_variable", "scope_exit"])))

# scope_enter -> scope_exit
# scope_enter -> initialize_variable ->

# useful interaction creator
# useful permutations
# pluralities
# the gap is where interactions happen

# type the gap

# neurons, dendrites

# token stream


# multidimensional AST
# graph is already in order if it is directed

# create a context
# mashup generator
# CRDT + megatree + smol_world