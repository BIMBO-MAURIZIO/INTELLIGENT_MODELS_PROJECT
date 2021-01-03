import networkx as nx
from networkx.algorithms import bipartite
import random


def removeEdge(G,TestG):
   result = 0
   while result != 1:
      randUsr = str(random.randint(1,943))
      neighList = list(G.neighbors(randUsr))
      #verify if the node has more than 5 neighbor

      if(len(neighList) >= 5):
         randExt = random.randint(0,len(neighList)-1)
         filmEl = neighList[randExt]
         G.remove_edge(randUsr,filmEl)
         TestG.add_edge(randUsr,filmEl)
         result = 1

   return G, TestG

#makes a random extraction between the possibles neighbors of a node with this neighlist
def randomChoice(neighList):
   numberOfNeigh = len(neighList)
   if numberOfNeigh > 0:
      singleStep = 1/numberOfNeigh
   else :
      selectedNeighbor = "nonvalid"
      #print("not enough neighbor to compute value")
      return selectedNeighbor
   ranges = [0 for i in range(numberOfNeigh+1)]
   for i in range(numberOfNeigh):
      ranges[i+1] = singleStep*(i+1)

   randValue = random.random()
   selectedNeighbor = ''
   for i in range(len(ranges)-1):
      if ranges[i] <= randValue and randValue <= ranges[i+1]:
         selectedNeighbor = neighList[i]
         break 
                 
   return selectedNeighbor


#applicata su ogni nodo deve scegliere un link a caso in maniera equiprobabile e fare una random walk di lunghezza 3
def prediction(G, node, k, B):
   counter = {}
   for i in range(k):
      neighList1 = list(G.neighbors(node))
      #find a film
      selectedNeighbor1 = randomChoice(neighList1)
      if selectedNeighbor1 == "nonvalid":
         break
      neighList2 = list(G.neighbors(selectedNeighbor1))
      neighList2.remove(node)
      #find a user
      selectedNeighbor2 = randomChoice(neighList2)
      if selectedNeighbor2 == "nonvalid":
         break
      neighList3 = list(G.neighbors(selectedNeighbor2))
      neighList3.remove(selectedNeighbor1)
      #find a film and update the counter
      selectedNeighbor3 = randomChoice(neighList3)
      if selectedNeighbor3 == "nonvalid":
         break
      if selectedNeighbor3 in counter:
         counter[selectedNeighbor3] = counter[selectedNeighbor3]+1
      else :
         counter[selectedNeighbor3] = 1

   #verify if the dict is empty (if is not empty dict return true)
   if counter:
      #find the key correspondent to the max value
      MaxDictVal = max(counter, key = counter.get)
      B.add_edge(node,MaxDictVal)
   else :
      print("there were not enough edges to compute a prediction")
   return B


try:
   f = open("ml-100k\\ml-100k\\u.user")
   # perform file operations
   content = f.readlines()
   users = []
   for line in content:
      lineContent = line.split("|")
      users.append(lineContent[0])

finally:
   f.close()

try:
   f2 = open("ml-100k\\ml-100k\\u.data")
   # perform file operations
   content2 = f2.readlines()
   edges = []

   for line in content2:
      couple = []
      lineContent = line.split("\t")
      couple.append(lineContent[0])
      #adding 943 to have univoque ids
      couple.append(str(int(lineContent[1]) + 943))
      edges.append(couple)

finally:
   f.close()


try:
   f3 = open("ml-100k\\ml-100k\\u.item")
   # perform file operations
   content3 = f3.readlines()
   films = []
   for line in content3:
      lineContent = line.split("|")
      #adding 943 to have univoque ids
      lineContent[0] = str(int(lineContent[0]) + 943)
      films.append(lineContent[0])

finally:
   f.close()

G = nx.Graph()
TestG = nx.Graph()
TrainedG = nx.Graph()
k = 500


G.add_nodes_from(users,bipartite = 0)
G.add_nodes_from(films,bipartite = 1)
G.add_edges_from(edges)

TestG.add_nodes_from(users,bipartite = 0)
TestG.add_nodes_from(films,bipartite = 1)

TrainedG.add_nodes_from(users,bipartite = 0)
TrainedG.add_nodes_from(films,bipartite = 1)

for i in range(int(10/100*nx.number_of_edges(G))):
   G, TestG = removeEdge(G, TestG)

'''
for edge in G.edges:
   counter = counter = counter + 1
for edge in TestG.edges:
   counter2 = counter2 = counter2 + 1

print(counter)
print(counter2)
'''
top_nodes = {n for n, d in G.nodes(data=True) if d["bipartite"] == 0}
for node in top_nodes:
   TrainedG = prediction(G, node, k, TrainedG)

TrainedEdges = list(TrainedG.edges)
TestEdges = list(TestG.edges)
counter = 0
for i in range(len(TrainedEdges)):
   for j in range(len(TestEdges)):
      if TrainedEdges[i] == TestEdges[j]:
         counter = counter+1
print("the edges actually trained were",str(len(TrainedEdges)))         
print("the edges that were correctly predicted were",str(counter))
print("the percentage of success is ",str(counter/len(TrainedEdges)*100)+"%")