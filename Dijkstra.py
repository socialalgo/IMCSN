import heapq
import networkx as nx


def getRank(target, parents):
	
	tree=nx.DiGraph()

	for (u,parent) in parents.items():
		if (not parent==-1):
			tree.add_edge(parent,u)



	count1={}


	# Function to calculate no. of
	# nodes in subtree
	def numberOfNodes(s, e):

		count1[s] = 1
		for u in tree.neighbors(s):
			
			# Condition to omit reverse path
			# path from children to parent
			if u == e:
				continue
			
			# recursive call for DFS
			numberOfNodes(u, s)
			
			# update count[] value of parent
			# using its children
			count1[s] += count1[u]


	# Function to print result
	def printNumberOfNodes():

		for u in tree.nodes():
			print("Nodes in subtree of", u,
							":", count1[u])


	numberOfNodes(target, -1)
		
	# print result
	#printNumberOfNodes()
	count1.pop(target)
	nodeRank=list(count1.items())
	nodeRank=sorted( nodeRank, key=lambda ele: (-ele[-1]) )

	return nodeRank,count1


def multiplegetRank(ghost,parents,targets):
	
	tree=nx.DiGraph()

	for (u,parent) in parents.items():
		if (not parent==-1):
			tree.add_edge(parent,u)



	count1={}


	# Function to calculate no. of
	# nodes in subtree
	def numberOfNodes(s, e):

		count1[s] = 1
		for u in tree.neighbors(s):
			
			# Condition to omit reverse path
			# path from children to parent
			if u == e:
				continue
			
			# recursive call for DFS
			numberOfNodes(u, s)
			
			# update count[] value of parent
			# using its children
			count1[s] += count1[u]


	# Function to print result
	def printNumberOfNodes():

		for u in tree.nodes():
			print("Nodes in subtree of", u,
							":", count1[u])


	numberOfNodes(ghost, -1)
		
	# print result
	#printNumberOfNodes()
	count1.pop(ghost)
	#for target in targets:
		#count1.pop(target)
	nodeRank=list(count1.items())
	nodeRank=sorted( nodeRank, key=lambda ele: (-ele[-1]) )
	

	return nodeRank,count1

def SingleMPPInf(target, G_d):
	for u in G_d.nodes():
		G_d.node[u]['prob']=0

	G_d.node[target]['prob'] = 1
	parents={target:-1}
	pq = [(-1, target,target)]
	while (pq):
		current_pr, current_vertex,parent = heapq.heappop(pq)

		# Nodes can get added to the priority queue multiple times. We only
		# process a vertex the first time we remove it from the priority queue.
		if current_pr > -G_d.node[current_vertex]['prob']:
			continue

		parents[current_vertex]=parent
		for v in G_d.neighbors(current_vertex):
			pr=current_pr*G_d[current_vertex][v]['weight']
			if (pr < -G_d.node[v]['prob']):
				G_d.node[v]['prob']=-pr
				heapq.heappush(pq, (pr, v,current_vertex))
	inf=0 

	for u in G_d.nodes():
		inf=inf+G_d.node[u]['prob']

	return inf,parents

def MultipleMPPInf(ghost, G_d):
	for u in G_d.nodes():
		G_d.node[u]['prob']=0

	G_d.node[ghost]['prob'] = 1
	parents={ghost:-1}
	pq = [(-1, ghost,ghost)]
	while (pq):
		current_pr, current_vertex,parent = heapq.heappop(pq)

		# Nodes can get added to the priority queue multiple times. We only
		# process a vertex the first time we remove it from the priority queue.
		if current_pr > -G_d.node[current_vertex]['prob']:
			continue

		parents[current_vertex]=parent
		for v in G_d.neighbors(current_vertex):
			pr=current_pr*G_d[current_vertex][v]['weight']
			if (pr < -G_d.node[v]['prob']):
				G_d.node[v]['prob']=-pr
				heapq.heappush(pq, (pr, v,current_vertex))
	inf=0 

	for u in G_d.nodes():
		inf=inf+G_d.node[u]['prob']

	return inf,parents	
	