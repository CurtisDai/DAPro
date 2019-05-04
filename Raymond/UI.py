import tkinter as tk

class UI:
	def __init__(self, window):
		window.title('Mutual Exclusion Demo')

		self.node_name = []
		self.canvas_node_id = {}
		self.node_position = {0: (450, 140),
							  1: (830, 140),
							  2: (130, 350),
							  3: (1150, 350),
							  4: (450, 560),
							  5: (830, 560)}
		self.node_color = ['lightgoldenrod', 'seashell', 'skyblue1', 'pink3', 'thistle1', 'palegreen']

		self.edge_id = {}
		self.radius = 100

		self.canvas = tk.Canvas(window, width=1280, height=800)
		self.canvas.pack()

	def add_edge(self, node0, node1, message):
		x0 = self.node_position[self.node_name.index(node0)][0]
		y0 = self.node_position[self.node_name.index(node0)][1]
		x1 = self.node_position[self.node_name.index(node1)][0]
		y1 = self.node_position[self.node_name.index(node1)][1]

		radius = self.radius
		if x0 != x1:
			delta = radius / (x1 - x0) * (y1 - y0)
			if x0 < x1:
				self.canvas.create_line(x0 + radius, y0 + delta + 10, x1 - radius, y1 - delta + 10, arrow=tk.LAST,
										fill='orangered')
				return self.canvas.create_text(x0 + radius, y0 + delta + 10, text=message, width=200, fill='orangered',
											   anchor=tk.NW)
			else:
				self.canvas.create_line(x0 - radius, y0 - delta - 10, x1 + radius, y1 + delta - 10, arrow=tk.LAST,
										fill='forestgreen')
				return self.canvas.create_text(x0 - radius, y0 - delta - 10, text=message, width=200,
											   fill='forestgreen', anchor=tk.SE)
		else:
			if y0 < y1:
				self.canvas.create_line(x0 - 10, y0 + radius, x1 - 10, y1 - radius, arrow=tk.LAST, fill='gold1')
				return self.canvas.create_text(x0 - 10, y0 + radius, text=message, width=200, fill='gold1',
											   anchor=tk.NW)
			else:
				self.canvas.create_line(x0 + 10, y0 - radius, x1 + 10, y1 + radius, arrow=tk.LAST, fill='cyan2')
				return self.canvas.create_text(x0 + 10, y0 - radius, text=message, width=200, fill='cyan2',
											   anchor=tk.SW)

	def update_edge(self, first_node, second_node, target_message):
		self.canvas.insert(self.edge_id[first_node, second_node], tk.END, '\n' + target_message)

	def render_node(self, i):
		radius = self.radius
		x0 = self.node_position[i][0]
		y0 = self.node_position[i][1]
		self.canvas.create_rectangle(x0 - radius, y0 - radius, x0 + radius, y0 + radius, fill=self.node_color[i])
		self.canvas_node_id[self.node_name[i]] = self.canvas.create_text(x0, y0, text='\n ' + str(self.node_name[i]),
																		 font=("Purisa", 16), width=200)

	def add_node(self, name):
		if len(self.node_name) >= 6:
			return 'reach capacity'
		self.node_name.append(name)
		self.render_node(len(self.node_name) - 1)

	def update_node(self, target_name, target_message):
		self.canvas.insert(self.canvas_node_id[target_name], tk.END, '\n' + target_message)



