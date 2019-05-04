import tkinter as tk


class UI:
    def __init__(self, window):
        window.title('Mutual Exclusion Demo')

        self.node_name = []
        self.canvas_node_id = {}
        self.node_position = {0: (550, 120),
                              1: (930, 120),
                              2: (230, 400),
                              3: (1250, 400),
                              4: (550, 680),
                              5: (930, 680)}
        self.color_list = ['lightgoldenrod', 'seashell', 'skyblue1', 'pink3', 'thistle1', 'palegreen', 'LightPink',
                           'HotPink', 'Plum', 'Purple', 'BlueViolet', 'LightSlateGray', 'LightSkyBlue', 'CadetBlue',
                           'MediumTurquoise', 'MediumSpringGreen', 'LawnGreen']

        self.edge_id = {}
        self.radius = 100
        self.tiny_radius = 20

        self.canvas = tk.Canvas(window, width=1380, height=800)
        self.canvas.pack()
        self.color_index = 0

        self.tiny_node_position = {}
        for pos in self.node_position.items():
            x = pos[1][0] / 1380 * 400
            y = pos[1][1] / 800 * 300
            self.tiny_node_position[pos[0]] = (x, y)
        self.tiny_edge_id = {}

    def render_node(self, i, position, radius):
        x0 = position[i][0]
        y0 = position[i][1]

        if radius == self.tiny_radius:

            self.canvas.create_oval(x0 - radius, y0 - radius, x0 + radius, y0 + radius, fill=self.color_list[i])
            self.canvas.create_text(x0, y0, text=str(self.node_name[i]), font=("Purisa", 16), width=200)
        else:
            self.canvas.create_rectangle(x0 - radius, y0 - radius, x0 + radius, y0 + radius, fill=self.color_list[i])
            self.canvas_node_id[self.node_name[i]] = self.canvas.create_text(x0, y0,
                                                                             text='\n ' + str(self.node_name[i]),
                                                                             font=("Purisa", 16), width=200)

    def add_node(self, name):
        self.color_index += 1

        if len(self.node_name) >= 6:
            return 'reach capacity'
        self.node_name.append(name)

        self.render_node(len(self.node_name) - 1, self.node_position, self.radius)
        self.render_node(len(self.node_name) - 1, self.tiny_node_position, self.tiny_radius)

    def update_node(self, target_name, target_message):
        # self.canvas.insert(self.canvas_node_id[target_name], tk.END, '\n'+target_message)
        x0 = self.node_position[self.node_name.index(target_name)][0]
        y0 = self.node_position[self.node_name.index(target_name)][1]

        self.canvas.delete(self.canvas_node_id[target_name])

        self.canvas_node_id[target_name] = self.canvas.create_text(x0, y0, text='\n ' + str(
            target_name) + '\n' + target_message, font=("Purisa", 16), width=200)

    def add_edge(self, node0, node1, message):
        self.color_index += 1
        color = self.color_list[self.color_index % len(self.color_list)]
        x0 = self.node_position[self.node_name.index(node0)][0]
        y0 = self.node_position[self.node_name.index(node0)][1]
        x1 = self.node_position[self.node_name.index(node1)][0]
        y1 = self.node_position[self.node_name.index(node1)][1]

        line = None
        text = None
        radius = self.radius
        if x0 != x1:
            delta = radius / (x1 - x0) * (y1 - y0)
            if x0 < x1:

                line = self.canvas.create_line(x0 + radius, y0 + delta + 10, x1 - radius, y1 - delta + 10,
                                               arrow=tk.LAST, fill=color, width=2)
                text = self.canvas.create_text(x0 + radius, y0 + delta + 10, text=message, width=200, fill=color,
                                               anchor=tk.NW)

            else:
                line = self.canvas.create_line(x0 - radius, y0 - delta - 10, x1 + radius, y1 + delta - 10,
                                               arrow=tk.LAST, fill=color, width=2)
                text = self.canvas.create_text(x0 - radius, y0 - delta - 10, text=message, width=200, fill=color,
                                               anchor=tk.SE)
        else:
            if y0 < y1:
                line = self.canvas.create_line(x0 - 10, y0 + radius, x1 - 10, y1 - radius, arrow=tk.LAST, width=2,
                                               fill=color)
                text = self.canvas.create_text(x0 - 10, y0 + radius, text=message, width=200, fill=color, anchor=tk.NW)
            else:
                line = self.canvas.create_line(x0 + 10, y0 - radius, x1 + 10, y1 + radius, arrow=tk.LAST, width=2,
                                               fill=color)
                text = self.canvas.create_text(x0 + 10, y0 - radius, text=message, width=200, fill=color, anchor=tk.SW)
        self.edge_id[node0, node1] = (line, text)

    def update_edge(self, first_node, second_node, target_message):
        self.canvas.insert(self.edge_id[first_node, second_node][1], tk.END, '\n' + target_message)

    def delete_all_edge(self):
        for edge in self.edge_id.items():
            self.canvas.delete(edge[1][0])
            self.canvas.delete(edge[1][1])

        self.edge_id = {}

    def add_parent(self, node0, node1):
        if node0 != node1:
            if (node1, node0) in self.tiny_edge_id:
                self.canvas.delete(self.tiny_edge_id[(node1, node0)])

            x0 = self.tiny_node_position[self.node_name.index(node0)][0]
            y0 = self.tiny_node_position[self.node_name.index(node0)][1]
            x1 = self.tiny_node_position[self.node_name.index(node1)][0]
            y1 = self.tiny_node_position[self.node_name.index(node1)][1]

            if x0 != x1:
                if x0 < x1:

                    line = self.canvas.create_line(x0 + self.tiny_radius, y0, x1 - self.tiny_radius, y1, arrow=tk.LAST,
                                                   width=2)

                else:
                    line = self.canvas.create_line(x0 - self.tiny_radius, y0, x1 + self.tiny_radius, y1, arrow=tk.LAST,
                                                   width=2)
            else:
                if y0 < y1:
                    line = self.canvas.create_line(x0, y0 + self.tiny_radius, x1, y1 - self.tiny_radius, arrow=tk.LAST,
                                                   width=2)
                else:
                    line = self.canvas.create_line(x0, y0 - self.tiny_radius, x1, y1 + self.tiny_radius, arrow=tk.LAST,
                                                   width=2)
            self.tiny_edge_id[node0, node1] = line