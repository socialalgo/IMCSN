import networkx as nx
import random
from random import sample
import sys
import math
import time
import Dijkstra
import main
def loadGraph(args):
	random.seed(123)
	G=nx.Graph()


	with open(args.input) as f:	
		for line in f:
			strlist = line.split()
			if (len(strlist)>1):
				u=int(strlist[0])
				v=int(strlist[1])
				G.add_edge(u,v)
				#G.add_edge(v,u)				

	targets=[]
	degrees=[]
	for u in G.nodes():
		degrees.append((u,G.degree(u)))

	degrees=sample(sorted(degrees, key=lambda x: x[1], reverse=True)[0:int(len(degrees)*0.1)],args.t)

	for u,degree in degrees:
		targets.append(u)



	choice=[0.1,0.01,0.001]
	for u,v in G.edges():
		G[v][u]['weight']=random.choice(choice)


	return G,targets




def G_dGenerator(G,targets,args,seed=123):

	for u in G.nodes():
		G.node[u]['threshold']=min(args.k,G.degree(u))

	G_d=nx.DiGraph()

	for target in targets:
		G_d.add_node(target)

	return G_d


def candidateInit(G,G_d,targets,args,ghost):
	G_r=nx.DiGraph()
	extraNodes=[]
	for u in G_d.nodes():
		G_r.add_node(u)

	for u in targets:
		G_r.add_node(u)

	for u in targets:
		G_d.add_edge(ghost,u,weight=1)

		for v in G.neighbors(u):
			if (not G_r.has_node(v)):
				extraNodes.append(v)
			G_r.add_edge(u,v)



	extraTriple=[]

	for v in extraNodes:
		inweight=0
		for u in G_r.predecessors(v):
			inweight+=G[u][v]['weight']
		extraTriple.append((v,inweight,G.degree(v)))

	rank=sorted(extraTriple, key=lambda ele: (-ele[1], -ele[2]))
	
	extraNodes=[]
	for u,inweight,degree in rank:
		extraNodes.append(u)



	return G_r,extraNodes

def candidateUpdate(G,G_d,G_r,extra,targets):
	extraNodes=[]
	for u in extra:
		for v in G.neighbors(u):
			if (not G_d.has_edge(u,v)):
				if (not G_r.has_node(v)):
					extraNodes.append(v)
				G_r.add_edge(u,v)

	extraTriple=[]

	for v in extraNodes:
		inweight=0
		for u in G_r.predecessors(v):
			inweight+=G[u][v]['weight']
		extraTriple.append((v,inweight,G.degree(v)))

	rank=sorted(extraTriple, key=lambda ele: (-ele[1], -ele[2]))

	extraNodes=[]
	for u,inweight,degree in rank:
		extraNodes.append(u)


	return extraNodes	


