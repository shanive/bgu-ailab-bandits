
import matplotlib.pyplot as plt
import matplotlib.axes

class PlotCreator:
	"creates a plot of experiment results"
	
	def __init__(self):
		"""initialize
		basex is the logarithm base scale of the x axis 
		basey is the logarithm base scale of the y axis
		default is linear axes
		 """
		self.linestyle = ('k-', 'k--', 'k-.', 'k:', 'ko', 'k^', 'kv') 
		
	def create(self, matrix, outputfile, xbase = 0, ybase = 0, xlabel = 'x axis', ylabel = 'y axis'):
		"""receives a matrix of results. 
		first row is the x scale.
		first column are the labes (each row has it's own lable)
		creates a file with name outputfile with the created plot"""
		graphs = len(matrix) 					#number of graphs
		
		labels = [matrix[row][0] for row in range(graphs)]
		data = [matrix[row][1:] for row in range(graphs)]			
		
		for graph in range(1, graphs):
			plt.plot(data[0], data[graph], self.linestyle[graph], label = labels[graph])
		 
		if xbase > 1:
			plt.gca().set_xscale('log', basex = xbase)
		if ybase > 1:
			plt.gca().set_yscale('log', basey = ybase)
		
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		
		plt.legend()
		
		plt.savefig(outputfile)