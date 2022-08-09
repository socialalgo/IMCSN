import argparse
import sys
import math
import networkx as nx
import random
import time
import copy
import graphProcessor
import Dijkstra
import heapq
import sys
import numpy as np
#import Drawing
import ConvergeFill
import Influence
import os
from random import sample
if sys.version>'3':
	import queue as Queue
else:
	import Queue

random.seed(123)

def parse_args():
	parser = argparse.ArgumentParser(description="profit divergence minimization")

	parser.add_argument('--input', nargs='?', default='datasets/catster', help='input graph file')

	parser.add_argument('--t', type=int, default='50',help='the number of seed users')

	parser.add_argument('--k', type=int, default='20',help='the number of out neighbors per user')

	parser.add_argument('--epsilon', type=float, default='0.00001',help='convergence point')

	return parser.parse_args()
			

def EdgeInsertion(targets,G,G_d,G_r,extraNodes,nodeRank):

	
	count=0
	extra=[]
	
	
	start=time.time()
	# some nodes are full no need to process
	for v,score in nodeRank:
		maxprob=0
		maxnode=-1
		for u in G_r.predecessors(v):
			act=G_d.node[u]['prob']*G[u][v]['weight']
			if (act>maxprob):
				maxprob=act
				maxnode=u

		if (maxnode==-1):
			continue



		G_d.add_edge(maxnode,v,weight=G[maxnode][v]['weight'])
		G_r.remove_edge(maxnode,v)
		count=count+1

		if (G_d.out_degree(maxnode)==G.node[maxnode]['threshold']):
			for x in G_r.neighbors(maxnode):
				G_r.remove_edge(maxnode,x)
			#removeSet.add(maxnode)
	part1=time.time()-start
	start=time.time()


	for v in extraNodes:
		maxprob=0
		maxnode=-1
		
		if (len(G_r.predecessors(v))==0):
			G_r.remove_node(v)
			continue

		for u in G_r.predecessors(v):
			act=G_d.node[u]['prob']*G[u][v]['weight']
			if (act>maxprob):
				maxprob=act
				maxnode=u

		if (maxnode==-1):

			continue


		extra.append(v)
		G_d.add_edge(maxnode,v,weight=G[maxnode][v]['weight'])
		G_r.remove_edge(maxnode,v)
		count=count+1

		if (G_d.out_degree(maxnode)==G.node[maxnode]['threshold']):
			for x in G_r.neighbors(maxnode):
				G_r.remove_edge(maxnode,x)
			#removeSet.add(maxnode)





	return count,extra
def SNA(G,G_d,G_r,targets,ghost,extraNodes,args):
	start=time.time()
	preinf,parents=Dijkstra.MultipleMPPInf(ghost,G_d)
	
	nodeRank=[]
	iteration=0
	already=0

	conviter=0
	convtime=time.time()


	while (True):
		iteration=iteration+1
		nodeRank,treesize=Dijkstra.multiplegetRank(ghost,parents,targets)


		count,extraNodes=EdgeInsertion(targets,G,G_d,G_r,extraNodes,nodeRank)
		already=already+count

		curinf,parents=Dijkstra.MultipleMPPInf(ghost,G_d)
		

		if ( (curinf-preinf)/preinf<args.epsilon):
			if (conviter==0):
				conviter=iteration
				convtime=time.time()-convtime

			filltime=time.time()

			ConvergeFill.bruteforceGreedy(G,G_d,G_r,nodeRank,extraNodes,args.k)

			filltime=time.time()-filltime
			break

			

		preinf=curinf
		extraNodes=graphProcessor.candidateUpdate(G,G_d,G_r,extraNodes,targets)

	G_d.remove_node(ghost)
	return G_d,conviter,convtime,filltime

def generation(args):
	ghost=sys.maxsize
	G,targets=graphProcessor.loadGraph(args)

	G_d=graphProcessor.G_dGenerator(G,targets,args)
	G_r,extraNodes=graphProcessor.candidateInit(G,G_d,targets,args,ghost)

	G_d,conviter,convtime,filltime=SNA(G,G_d,G_r,targets,ghost,extraNodes,args)	
	
	inf,etime=Influence.MonteCarlo(G_d,targets,5)
	
	
	
	output="inf:"+str(inf)+" converge iter:"+str(conviter)+" converge time:"+str(convtime)+" filling time:"+str(filltime)

	print (output)


def main(args):

	
	generation(args)


if __name__ == "__main__":
	args = parse_args()
	main(args)
