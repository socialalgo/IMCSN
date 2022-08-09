import random
from random import choice
from random import random as rd
from random import sample
import networkx as nx


def bruteforceGreedy(G,G_d,G_r,nodeRank,extraNodes,k):
	
	newRank=[]

	for u,score in nodeRank:
		newRank.append(u)

	newRank.extend(extraNodes)
	
	sortedNeighbors={}
	neighborIndex={}
	
	for v in newRank:
		neighborIndex[v]=0
		sortedN=[]

		for u in G_r.predecessors(v):
			sortedN.append((u,G_d.node[u]['prob']*G[u][v]['weight']))

		sortedNeighbors[v]=sorted(sortedN,key=lambda ele: (-ele[1]))


	iteration=0
	#print ("rank length",len(newRank))
	while(len(newRank)>0):
		tempRank=[]
		iteration+=1

		for v in newRank:
			for i in range(neighborIndex[v],len(sortedNeighbors[v])):
				inNode=sortedNeighbors[v][i][0]
				if (not G_r.has_edge( inNode,v ) ):
					continue

				if (not i== len(sortedNeighbors[v])-1):
					tempRank.append(v)

				neighborIndex[v]=i
				G_d.add_edge(inNode,v,weight=G[inNode][v]['weight'])
				G_r.remove_edge(inNode,v)
			

				if (G_d.out_degree(inNode)==G.node[inNode]['threshold']):
					for x in G_r.neighbors(inNode):
						G_r.remove_edge(inNode,x)				
				break
		
		
		newRank=tempRank
		#print ("rank length",len(newRank))
		
