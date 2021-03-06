import random
import numpy as np

distance_matrix = [ [0, 50, 50, 94, 50],
					[50, 0, 22, 50, 36],
					[50, 22, 0, 44, 14],
					[94, 50, 44, 0 ,50],
					[50, 36, 14, 50, 0] ]

flow_matrix = [ [0, 0, 2, 0, 3],
			    [0, 0, 0, 3, 0],
			    [2, 0, 0, 0, 0],
			    [0, 3, 0, 0, 1],
			    [3, 0, 0, 1, 0] ]

n_ants = 4
n_units = 5
initial_pheromones = .1

alpha = 1
beta = 1
p = 0.99
Q = 1
q_0 = 0.7
phi = 0.5

n_iterations = 100
initial_unit = random.randint( 0, n_units-1 )

best_global = {'path':[], 'cost': np.inf}

pheromone_matrix = np.zeros(( n_units, n_units ))
visibility_matrix = np.zeros(( n_units, n_units ))

units = ['A', 'B', 'C', 'D', 'E']

def print_matrix( matrix, text ):
	print( text )
	for i in range( n_units ):
		if(i==0):
			print("\tA\tB\tC\tD\tE" )
		for j in range( n_units ):
			if(j==0):
				print(units[i], end='\t')
			print( "{:.3f}".format(matrix[i][j]), end='\t')
		print()

def initialize_pheromone_matrix():
	for i in range( n_units ):
		for j in range( n_units ):
			if(i!=j):
				pheromone_matrix[i][j] = initial_pheromones

def initialize_visibility_matrix():
	tmp = np.matmul( flow_matrix, distance_matrix )
	for i in range( len(tmp) ):
		for j in range( len(tmp) ):
			if i != j :
				if tmp[i][j] == 0 :
					visibility_matrix[i][j] = 10e-10
				else :
					visibility_matrix[i][j] = 1 / tmp[i][j]
			else :
				visibility_matrix[i][j]

def next_city( m_prob, random_number):
	probabilty_sum = 0
	for i in range( len(m_prob) ):
		if( m_prob[i] != -1 ):
			probabilty_sum += m_prob[i]
			if( random_number <= probabilty_sum ):
				return i

def update_pheromone_trace( i, j):
	print("(1-"+str(phi)+")*"+str(pheromone_matrix[i][j])+"+"+str(phi)+"*"\
				+str(initial_pheromones)+"=",end='')
	pheromone_matrix[i][j] *=(1-phi) + phi*initial_pheromones
	print(pheromone_matrix[i][j])

def send_ants():
	path_list = []
	for i in range( n_ants ):
		path = []
		current_unit = initial_unit
		path.append( current_unit )
		print("Ant # ",i )
		print("Starting at: ", current_unit)
		while( len(path) < n_units ):
			m_sum = 0.
			sums_list = []
			n_index = -1
			q = random.random()
			print("Value of q: ", q)
			if q <= q_0 :
				print("Travel by diversification")

				for j in range( n_units ):
					if j not in path :
						t = (pheromone_matrix[current_unit][j]) ** alpha
						n = (visibility_matrix[current_unit][j]) ** beta
						tn = t*n
						sums_list.append( tn )
						m_sum += tn
						print( units[current_unit] + "-" + units[j], end=' ' )
						print( "t = ", t, end=' ' )
						print( "n = ", n, end=' ' )
						print( "t*n = ", tn )
					else:
						sums_list.append( -1 )
				print( "Sum: ", m_sum )
				m_prob = []
				for k in range( n_units ):
					if k not in path :
						m_prob.append( sums_list[k] / m_sum )
						print( units[current_unit] + "-" + units[k], end=' ' )
						print( "Probabilty = ", sums_list[k] / m_sum)
					else:
						m_prob.append(-1)
				random_number = random.random()
				print( "Random number: ", random_number )
				n_index = next_city( m_prob, random_number )
				print("Next city: ", units[n_index] )


			else:
				print("Travel by Intensification")
				prev_tn = -1
				for j in range( n_units ):
					if j not in path :
						t = (pheromone_matrix[current_unit][j]) ** alpha
						n = (visibility_matrix[current_unit][j]) ** beta
						tn = t*n
						sums_list.append( tn )
						m_sum += tn
						print( units[current_unit] + "-" + units[j], end=' ' )
						print( "t = ", t, end=' ' )
						print( "n = ", n, end=' ' )
						print( "t*n = ", tn )
						if prev_tn < tn :
							n_index = j
				print("Next city: ", units[n_index] )

			print("Updating arc "+str(path[-1])+"-"+str(n_index)+": ",end='')
			update_pheromone_trace(path[-1], n_index)
			current_unit = n_index
			path.append( n_index )
		print("Ant # "+str(i)+": ", end='')
		for i in range( n_units ):
			if( i == n_units-1 ):
				print( units[path[i]])
			else:	
				print( units[path[i]] + "-", end='')
		path_list.append( path )
	return path_list

def path_cost( path ):
	cost = 0.
	for i in range( n_units ):
		for j in range( n_units ):
			if i != j :
				cost += flow_matrix[i][j]*distance_matrix[path[i]][path[j]]
	return cost

def print_ant_results( path_list ):
	print("\nResults")
	costs_lists = []
	for j in range( len( path_list ) ):
		print("Ant # "+str(j)+": ", end='') 
		for i in range( n_units ):
			if( i == n_units-1 ):
				print( units[path_list[j][i]], end=' ')
			else:
				print( units[ path_list[j][i]] + "-", end='')
		costs_lists.append( path_cost(path_list[j]) ) 
		print( "Cost: ", costs_lists[j])
	index_ant = costs_lists.index( min(costs_lists) )
	print("------------------------------------------------------")
	print("Best Local Ant: ", end='')
	for i in range( n_units ):
		if( i == n_units-1 ):
			print( units[path_list[index_ant][i]], end=' ')
		else:
			print( units[path_list[index_ant][i]] + "-", end='')
	print("Cost: ", costs_lists[index_ant])
	print("------------------------------------------------------")

	if best_global['cost'] > costs_lists[index_ant] :
		best_global['path'] = list(path_list[index_ant])
		best_global['cost'] = costs_lists[index_ant]

	print("------------------------------------------------------")
	print("Best Global Ant: ", end='')
	for i in range( n_units ):
		if( i == n_units-1 ):
			print( units[best_global['path'][i]], end=' ')
		else:
			print( units[best_global['path'][i]] + "-", end='')
	print("Cost: ", best_global['cost'])
	print("------------------------------------------------------")

	return costs_lists, index_ant

def get_delta( i, j):
	for k in range( len(best_global['path']) -1 ):
		if ( best_global['path'][k] == i and best_global['path'][k+1] == j) or \
			( best_global['path'][k+1] == i and best_global['path'][k] == j):
			return 1 / best_global['cost']
	return 0

def update_pheromone_matrix( path_list, costs_lists ):
	for i in range( n_units ):
		for j in range( n_units ):
			tmp = 0
			if i != j :
				print(units[i]+" "+units[j]+": Pheromone = ", end='')
				delta = get_delta(i, j)
				print( str(1-p)+"*"+str(pheromone_matrix[i][j])+\
									"+"+str(delta)+" = ", end='')
				pheromone_matrix[i][j] *= p+(1-p)*delta
				print( pheromone_matrix[i][j] )

def ACS_algorithm():
	initialize_pheromone_matrix()
	initialize_visibility_matrix()

	for i in range( n_iterations ):
		print("Iteration # ", i)
		if(i == 0):
			print_matrix( distance_matrix, " Distance Matrix " )
			print_matrix( pheromone_matrix, " Pheromone Matrix" )
			print_matrix( visibility_matrix, "Visibility Matrix" )
		path_list = send_ants()
		cost_list = print_ant_results( path_list )
		update_pheromone_matrix( path_list, cost_list )

	# print_matrix( pheromone_matrix, " Updated Pheromone Matrix " )


if __name__ == "__main__":

	ACS_algorithm()
