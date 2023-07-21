import itertools
from collections import Counter

class Tree:
  def __init__(self, name, can_repeat):
    self.name = name
    self.taken = False
    self.children = []
    self.can_repeat = can_repeat
  def __repr__(self):
    return self.name

  def childrenwalk(self):
    for item in self.children:
      yield item, "{}".format(item.name)

  def doesnt_contain(self, name):
    found = False
    for child in self.children:
      if child.name == name:
        found = True
        break

    return not found
  
  def order(self, visited, recurse=False):
    if self.taken:
      yield self, "{}".format(self.name)
    if recurse:
      for item in self.children:
        myvisited = list(visited)
        if item.name in visited:
          myvisited.append(item.name)
          yield from item.order(myvisited, False)
        else:
          myvisited.append(item.name)
          yield from item.order(myvisited, True)

      
  def walk(self, indent=0, visited=[], recurse=False):
    tag = ""
    if self.can_repeat:
      tag = "(recursive)"
    
    # print("{}{}{}".format(((indent * 2)) * " ", self, tag))
    
      
    if recurse:
      for child in self.children:
    
        myvisited = list(visited)
        yield (child, "{}{}".format((1 + (indent * 2)) * " ", child))
        if child.name in visited:
          myvisited.append(child.name)
          yield from child.walk(indent + 1, myvisited, False)
        else:
          myvisited.append(child.name)
          yield from child.walk(indent + 1, myvisited, True)
          
        
      # visited[self] = True
        
  def add_child(self, name, can_repeat):
    new_node = Tree(name, can_repeat)
    new_children = []    
    for child in self.children:
      new_children.append(Tree(child.name, child.can_repeat))
    new_node.children = new_children
    self.children.append(new_node)

    return new_node

definitions = [
  ("windows", False),
  ("mac", False),
  ("linux", False),
  ("enter_scope", True),
  ("exit_scope", True)
]

root = Tree("root", True)
for event in definitions:
  root.add_child(event[0], event[1])
defs = root.walk(0, {}, True)
for item in defs:
  print(item[1])
events = [
  ("+", "windows", False),
  ("+", "mac", False),
  ("+", "linux", False),
  ("+", "enter_scope", True),
  ("+", "exit_scope", True),
  ("+", "windows", True)
]
gap = Tree("gap", True)
gaproot = gap
last_position = gap
for event in events:
  found = False
  my_children = list(last_position.childrenwalk())
  print(my_children)
  for item in my_children:
    
    if item[0].name == event[1]:
      print(item[0].name, "is already in the gap")
      
      child = last_position.add_child(item[0].name, item[0].can_repeat)
      child.taken = True
      last_position = child
      
      found = True
      break
  if not found:
    for item in root.childrenwalk():
      
      if item[0].name == event[1]:
        print(item[0].name, "found in root")
       
        
       

        
        child = last_position.add_child(item[0].name, item[0].can_repeat)
        last_position = child
        child.taken = True
        found = True
        break
      else:
        if last_position.doesnt_contain(item[0].name):
          last_position.add_child(item[0].name, item[0].can_repeat)

    
  
  print(event)

print("### GAP OUTPUT")

defs = gap.walk(0, {}, True)
for item in defs:
  #if item[0].taken:
  print(item[1])

print("### TRAVESAL OF INTERACTION SPACE")

for item in gaproot.order([], True):
  print(item[1])

# interactions between disperate things

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
# merge behaviour

# orderings