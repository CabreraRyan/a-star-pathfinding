import sys
import pygame


# G cost is the current node distance to start node
# H cost is the current node heuristic distance to the end node
# F cost = G + H // Lower Fcost = Better

# TODO: IMPLEMENT WALLS TO THE GRID
# TODO: GAME STATES AND KEYBINDINGS
# TODO: WHEN PATH IS NOT FOUND

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
        size = self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode(size)

        # COLORS
        self.WHITE = 255, 255, 255
        self.BLACK = 0, 0, 0
        self.ORANGE = 255, 165, 0
        self.GREEN = 0, 128, 0
        self.RED = 255, 0, 0
        self.BLUE = 0, 0, 255

        self.screen.fill(self.WHITE)

        # Grid
        self.cols = 20
        self.rows = 20

        self.cell_width = self.WIDTH // self.cols
        self.cell_height = self.HEIGHT // self.rows

        self.grid = self.init_grid()
        self.found = False
        self.draw_grid()

        # FPS
        self.max_fps = 60
        self.clock = pygame.time.Clock()

        # Nodes
        self.open_list = []
        self.closed_list = []

        # Initialize the start and end node
        start = (3, 5)
        end = (13, 5)

        self.start_node = Node(None, start)
        self.start_node.g = self.start_node.h = self.start_node.f = 0
        self.end_node = Node(None, end)
        self.end_node.g = self.end_node.h = self.end_node.f = 0

        self.start_node_pos = list(self.start_node.position)
        self.show(self.ORANGE, self.start_node_pos[0], self.start_node_pos[1], 0)
        self.end_node_pos = list(self.end_node.position)
        self.show(self.ORANGE, self.end_node_pos[0], self.end_node_pos[1], 0)

        self.open_list.append(self.start_node)

        self.test_wall()

        # 0 = Player Control
        # 1 = Run
        # 2 = Pause
        self.game_state = 0

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
                self.show(self.BLACK, i, j, 1)

    def draw_wall(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.grid[i][j] == 1:
                    self.show(self.BLACK, i, j, 0)

    def update_grid(self):
        if not self.found:
            for i in self.open_list:
                if i in self.closed_list:
                    continue
                open_pos = list(i.position)
                self.show(self.GREEN, open_pos[0], open_pos[1], 0)
            for j in self.closed_list:
                closed_pos = list(j.position)
                self.show(self.RED, closed_pos[0], closed_pos[1], 0)

    def test_wall(self):
        self.grid[8][5] = 1
        self.grid[8][6] = 1
        self.grid[8][7] = 1
        self.grid[8][4] = 1
        self.grid[8][3] = 1

    def show(self, color, x, y, st):
        """ Draw singular rectangle """
        pygame.draw.rect(self.screen, color, (x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height), st) # width or height // cols or rows = 40
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
            #self.open_list.pop(current_index)
            del self.open_list[current_index]
            self.closed_list.append(current_node)

            # If the algorithm is finished checking
            if current_node == self.end_node:
                path = []
                current = current_node
                while current is not None:
                    pos = list(current.position)
                    path.append(pos)
                    self.show(self.BLUE, pos[0], pos[1], 0)
                    current = current.parent
                    # for i in self.open_list:
                    self.found = True
                print("Shortest path is " + str(current_node.f) + " blocks away")
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
                if child in self.closed_list:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = self.heuristics(child.position[0], child.position[1])
                child.f = child.g + child.h

                # Child is already in the open list
                # for open_node in self.open_list:
                #     if child == open_node and child.g > open_node.g:
                #         continue

                if child in self.open_list:
                    continue

                # Add the child to the open list
                self.open_list.append(child)

    def cell_onclick(self):
        pass

    def run(self):
        """ Main loop of the game """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif self.game_state == 0:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        try:
                            pos = pygame.mouse.get_pos()
                            self.grid[(pos[0]) // self.cell_width][(pos[1]) // self.cell_height] = 1
                            #print(pos[0] // self.cell_height)
                            self.draw_wall()
                        except AttributeError:
                            pass
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            print("You pressed space")
                            self.game_state = 1


            if self.game_state == 1 and not self.found:
                self.a_star()
                self.update_grid()

            pygame.display.flip()
            self.clock.tick(self.max_fps)

if __name__ == '__main__':
    game = Board()
    game.run()
