import time
import os
import shutil
from collections import deque
from collections import defaultdict
import subprocess
from random import random as rd


def MonteCarlo(initGraph,targets,simulation):
	start=time.time()
	#simulation=1000
	
	inf=simulation*len(targets)

	for target in targets:
		
		for i in range(simulation):
			q=deque()
			visited=set()
			visited.add(target)
			
			q.append(target)
			while (q):
				u=q.popleft()

				for v in initGraph.neighbors(u):
					
					if (not v in visited and rd()<=initGraph[u][v]['weight']):
						visited.add(v)
						q.append(v)
						inf=inf+1

	inf=int(float(inf)/simulation)

	return inf,time.time()-start