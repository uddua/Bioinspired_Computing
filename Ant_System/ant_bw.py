


distance_matrix = [ [0, 35, 71, 99, 71, 75, 41],
					[35, 0, 42, 80, 65, 82, 47],
					[71, 42, 0, 45, 49, 79, 55],
					[99, 80, 45, 0, 36, 65, 65],
					[71, 65, 49, 36, 0, 31, 32],
					[75, 82, 79, 65, 31, 0, 36],
					[41, 47, 55, 65, 32, 36, 0] ]

flow_matrix = [ [0, 2, 0, 0, 0, 0, 2],
				[2, 0, 3, 0, 0, 1, 0],
				[0, 3, 0, 0, 0, 1, 0],
				[0, 0, 0, 0, 3, 0, 1],
				[0, 0, 0, 3, 0, 0, 0],
				[0, 1, 1, 0, 0, 0, 0],
				[2, 0, 0, 1, 0, 0, 0] ]

n_ants = 4

def print_matrix( matrix, text ):
	print( text )
	for i in range( n_units ):
		if(i==0):
			print("\tA\tB\tC\tD" )
		for j in range( n_units ):
			if(j==0):
				print(units[i], end='\t')
			print( "{:.3f}".format(matrix[i][j]), end='\t')
		print()

if __name__ == "__main__":

	print("Hi") 