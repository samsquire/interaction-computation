import itertools
from collections import Counter


class Versions:

  def __init__(self):
    self.version = 0
    self.index = {}

  def next_version(self, item):
    current_version = self.version
    self.index[current_version] = item
    self.version = self.version + 1
    return current_version


class Tree:

  def __init__(self, name, can_repeat, version, version_generator):
    self.name = name
    self.taken = False
    self.children = []
    self.can_repeat = can_repeat
    self.version = version
    self.version_generator = version_generator

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

  def order(self, visited, visited_list, recurse=False):

    if self.taken:
      vs = list(map(lambda x: x.version, visited_list))
      yield self, "{}".format(self.name), vs
    if recurse:
      for item in self.children:
        myvisited = list(visited)
        myvisitedlist = list(visited_list)
        myvisitedlist.append(item)
        if item.name in visited:
          myvisited.append(item.name)
          yield from item.order(myvisited, myvisitedlist, False)
        else:
          myvisited.append(item.name)
          yield from item.order(myvisited, myvisitedlist, True)

  def walk(self, indent=0, visited=[], visited_items=[], identifier=[], recurse=False):
    tag = ""
    identifier = list(identifier)
    identifier.append(self.version)
    if self.can_repeat:
      tag = "(recursive)"

    # print("{}{}{}".format(((indent * 2)) * " ", self, tag))

    if recurse:
      for child in self.children:

        myvisited = list()
        myvisited_items = list()
        yield (child, "{}{}".format((1 + (indent * 2)) * " ",
                                    child), identifier)
        if child.name in visited:
          myvisited_items.append(child.version)
          myvisited.append(child.name)
          yield from child.walk(indent + 1,
                                myvisited,
                                identifier,
                          myvisited_items, recurse=False)
        else:
          myvisited_items.append(child.version)
          myvisited.append(child.name)
          yield from child.walk(indent + 1,
                                myvisited,
                                identifier,
                                myvisited_items,  recurse=True)

      # visited[self] = True

  def add_child(self, name, can_repeat, copy=True):

    new_node = Tree(name, can_repeat, 0, self.version_generator)
    new_node.version = self.version_generator.next_version(new_node)
    new_children = []
    if copy:
      for child in self.children:
        new_child = Tree(child.name, child.can_repeat, 0,
                         self.version_generator)
        new_children.append(new_child)
        new_child.version = self.version_generator.next_version(new_child)
      new_node.children = new_children
    self.children.append(new_node)

    return new_node


definitions = [("windows", False), ("mac", False), ("linux", False),
               ("enter_scope", True), ("exit_scope", True),
               ("create_thread", True)]

versions = Versions()
root = Tree("root", True, 0, versions)
root.version = versions.next_version(root)
for event in definitions:
  root.add_child(event[0], event[1])
defs = root.walk(0, {}, [], recurse=True)
for item in defs:
  print(item[1])
events = [("+", "windows", False),
          ("+", "enter_scope", True), ("+", "exit_scope", True),
          ("+", "create_thread", True)]
gap = Tree("gap", True, 0, versions)
gap.version = versions.next_version(gap)
gaproot = gap
last_position = gap
for event in events:
  found = False
  my_children = list(last_position.childrenwalk())
  print(my_children)
  for item in my_children:

    if item[0].name == event[1] and last_position.doesnt_contain(item[0].name):
      print(item[0].name, "is already in the gap")

      child = last_position.add_child(item[0].name, item[0].can_repeat)
      child.taken = True
      last_position = child

      found = True
      break
  if not found:
    for item in root.childrenwalk():

      if item[0].name == event[1]:
        if not last_position.doesnt_contain(item[0].name):
          for child in last_position.children:
            if child.name == item[0].name:
              child.taken = True
              last_position = child
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

defs = gap.walk(0, {}, [], recurse=True)
for item in defs:
  #if item[0].taken:
  print(item[1], item[2])

print("### TRAVESAL OF INTERACTION SPACE")

for item in gaproot.order([], [], True):
  print(item[1], item[2])

# interactions between disperate things

operating_systems = ["windows", "mac", "linux"]

print(
    list(
        itertools.permutations(
            ["scope_enter", "initialize_variable", "scope_exit"])))

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

A = {"B": "One", "C": "Two", "D": "Three"}
C = {"B": "Two", "C": "Three", "D": "Four"}


def recur(root, lefts, excepts):
  for key, item in lefts.items():
    if key in excepts:
      continue
    myexcepts = list(excepts)
    myexcepts.append(key)

    for v in item:
      child = root.add_child("{}={}".format(key, v), False, copy=False)
      recur(child, lefts, myexcepts)

  return root


def create_tree(lefts):
  root = Tree("root", False, 0, versions)
  root.version = versions.next_version(root)
  recur(root, lefts, [])
  return root


def multiply(left, right):
  lefts = {}
  for key, value in left.items():
    if key not in lefts:
      lefts[key] = []
    lefts[key].append(value)

  for key, value in right.items():
    if key not in lefts:
      lefts[key] = []
    lefts[key].append(value)
  output = ""
  for key, value in lefts.items():
    output += "{} =[{}] ".format(key, ",".join(value))
  root = create_tree(lefts)

  return "A×C = {}".format(output), root


r, t = multiply(A, C)
print(r)
print(t)
defs = t.walk(0, {}, [], recurse=True)
for item in defs:
  print(item[1])

from subprocess import Popen, PIPE


class Graph():

  def __init__(self, name):
    self.adjacency = {}
    self.backwards = {}
    self.name = name
    self.nodes = []

  def search(self, node):
    found = set()
    if node in self.nodes:
      for out in self.adjacency[node]:
        found.add(out)
      
      for backward in self.backwards[node]:
        found.add(backward)
    return found
  
  def add_edge(self, start, end):

    if start not in self.adjacency:
      self.adjacency[start] = []
      self.backwards[start] = []
      self.nodes.append(start)
    if end not in self.adjacency:
      self.adjacency[end] = []
      self.backwards[end] = []
      self.nodes.append(end)
    self.adjacency[start].append(end)
    self.adjacency[end].append(start)

  def draw(self):
    dot = Popen(["dot", "-Tpng", "-o", "graphs/{}.png".format(self.name)],
                stdin=PIPE,
                stdout=PIPE)
    graph = "digraph G {"
    for item, value in self.adjacency.items():
      for link in value:
        graph += "\"{}\" -> \"{}\";".format(item, link)
    graph += "}"

    dot.communicate(graph.encode("utf8"))


interactions = Graph("root")
interactions.add_edge("windows", "create_thread")

interactions.draw()


def find_abstractions(versions, interactions, gap):
  found = []
  visited = {}
  for item in gap.order([], [], True):
    
    vs = item[2]
    strr = item[0].name
    
    print(vs)
    for version in vs:
      link = versions.index[version]
      if link.name not in visited:
        strr = link.name
        visited[strr] = True
        found.append(strr)
  return found

items = find_abstractions(versions, interactions, gap)
for item in items:
  print(item)
