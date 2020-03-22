import sys
import pygame

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Board():
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        size = self.WIDTH, self.HEIGHT = 400, 400
        self.screen = pygame.display.set_mode(size)

        # COLORS
        self.WHITE = 255, 255, 255
        self.BLACK = 0, 0, 0
        self.ORANGE = 255, 165, 0
        self.GREEN = 0, 128, 0
        self.RED = 255, 0, 0

        # Grid
        self.cols = 10
        self.rows = 10

        self.grid = self.init_grid()
        self.found = False
        self.draw_grid()

        # FPS
        self.max_fps = 5
        self.clock = pygame.time.Clock()

        # Nodes
        self.open_list = []
        self.closed_list = []

        # Initialize the start and end node

        start = (1, 1)
        end = (8, 5)

        self.start_node = Node(None, start)
        self.start_node.g = self.start_node.h = self.start_node.f = 0
        self.end_node = Node(None, end)
        self.end_node.g = self.end_node.h = self.end_node.f = 0

        self.start_node_pos = list(self.start_node.position)
        self.show(self.ORANGE, self.start_node_pos[0], self.start_node_pos[1], 0)
        self.end_node_pos = list(self.end_node.position)
        self.show(self.ORANGE, self.end_node_pos[0], self.end_node_pos[1], 0)

        self.open_list.append(self.start_node)


    def init_grid(self):
        """"
        Initialize the 2D List
        """
        grid = [0 for i in range(self.cols)]
        for i in range(self.cols):
            grid[i] = [0 for i in range(self.rows)]
        return grid

    def draw_grid(self):
        """ Initialize the grid to the screen """
        for i in range(self.cols):
            for j in range(self.rows):
                self.show(self.WHITE, i, j, 1)

    def show(self, color, x, y, st):
        """ Draw singular rectangle """
        pygame.draw.rect(self.screen, color, (x * 40, y * 40, 40, 40), st) # width or height // cols or rows = 40
        pygame.display.update()

    def heuristics(self, x, y):
        """ Returns a value for the H cost of the Node """
        return ((x - self.end_node.position[0]) ** 2) + ((y - self.end_node.position[1]) ** 2)

    def a_star(self):
        """ Algorithm of the game """

        # start = (1, 1)
        if len(self.open_list) > 0:
            # Get the current node
            current_node = self.open_list[0]
            current_index = 0
            for index, item in enumerate(self.open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            # self.open_list.pop(current_index)
            del self.open_list[current_index]
            self.closed_list.append(current_node)

            for i in self.open_list:
                open_pos = list(i.position)
                self.show(self.GREEN, open_pos[0], open_pos[1], 0)
            for j in self.closed_list:
                closed_pos = list(j.position)
                self.show(self.RED, closed_pos[0], closed_pos[1], 0)

            if current_node == self.end_node:
                path = []
                current = current_node
                while current is not None:
                    pos = list(current.position)
                    path.append(pos)
                    self.show(self.WHITE, pos[0], pos[1], 0)
                    current = current.parent
                    # for i in self.open_list:
                    self.found = True
                print("Shortest path is " + str(current_node.f) + "blocks away")
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.grid) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(self.grid[len(self.grid) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.grid[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in self.closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = self.heuristics(child.position[0], child.position[1])
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in self.open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                self.open_list.append(child)

    def run(self):
        """ Main loop of the game """

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            if self.found is False:
                self.a_star()

            pygame.display.flip()
            self.clock.tick(self.max_fps)

if __name__ == '__main__':
    game = Board()
    game.run()
