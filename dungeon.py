from lib.utils import *

import pygame
import random
import math

# Main Application
class App:
    def __init__(self):
        self.mainPathLength = None
        self.sidePathCount = None
        self.sidePathMaximumSize = None

        self.nodes = []
        self.connections = []

        self.screen = None
        self.isDone = False

        self.cameraX = -400
        self.cameraY = 400

    def input(self):
        keys = pygame.key.get_pressed()

        # Camera Movement
        cameraSpeed = 15 if keys[pygame.K_LSHIFT] else 5

        if keys[pygame.K_w]:
            self.cameraY += cameraSpeed

        elif keys[pygame.K_s]:
            self.cameraY -= cameraSpeed

        if keys[pygame.K_a]:
            self.cameraX -= cameraSpeed

        elif keys[pygame.K_d]:
            self.cameraX += cameraSpeed


        # Highlighting Nodes and Connections
        left, middle, right = pygame.mouse.get_pressed()

        nodeSize = 40
        connectorSize = 20
        distance = 120

        for node in self.nodes:
            hitRect = pygame.Rect(distance * node[0] - self.cameraX - (nodeSize / 2), self.cameraY - distance * node[1] - (nodeSize / 2), nodeSize, nodeSize)

            if hitRect.collidepoint(pygame.mouse.get_pos()):
                if left:
                    node[3] = 1
                elif middle:
                    node[3] = 2
                elif right:
                    node[3] = 0


        for connection in self.connections:
            centerSpace = [distance * connection[0][0] + (distance * connection[1][0] - distance * connection[0][0]) / 2,
                           ((distance * connection[0][1] - distance * connection[1][1]) / 2) - distance * connection[0][1]]

            hitRect = pygame.Rect(centerSpace[0] - self.cameraX - (connectorSize / 2), centerSpace[1] + self.cameraY - (connectorSize / 2), connectorSize, connectorSize)

            if hitRect.collidepoint(pygame.mouse.get_pos()):
                if left:
                    connection[3] = 1
                elif middle:
                    connection[3] = 2
                elif right:
                    connection[3] = 0


    def draw(self):
        self.screen.fill((100, 100, 100))

        # General variables.
        nodeSize = 40
        connectorSize = 20
        distance = 120

        # Draw the connections first.
        for connection in self.connections:
            pygame.draw.line(self.screen, (0, 0, 0),
                             (distance * connection[0][0] - self.cameraX, self.cameraY - distance * connection[0][1]),
                             (distance * connection[1][0] - self.cameraX, self.cameraY - distance * connection[1][1]), 3)

            centerSpace = [distance * connection[0][0] + (distance * connection[1][0] - distance * connection[0][0]) / 2,
                           ((distance * connection[0][1] - distance * connection[1][1]) / 2) - distance * connection[0][1]]

            if connection[3] == 1:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(centerSpace[0] - self.cameraX - ((connectorSize + 10) / 2), centerSpace[1] + self.cameraY - ((connectorSize + 10) / 2), connectorSize + 10, connectorSize + 10))

            pygame.draw.rect(self.screen, connection[2] if connection[3] != 2 else (255, 255, 255), pygame.Rect(centerSpace[0] - self.cameraX - (connectorSize / 2), centerSpace[1] + self.cameraY - (connectorSize / 2), connectorSize, connectorSize))

        # Then draw the nodes so that they're above the connections.
        for node in self.nodes:
            if node[3] == 1:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(distance * node[0] - self.cameraX - ((nodeSize + 10) / 2), self.cameraY - distance * node[1] - ((nodeSize + 10) / 2), nodeSize + 10, nodeSize + 10))

            pygame.draw.rect(self.screen, node[2] if node[3] != 2 else (255, 255, 255), pygame.Rect(distance * node[0] - self.cameraX - (nodeSize / 2), self.cameraY - distance * node[1] - (nodeSize / 2), nodeSize, nodeSize))

        pygame.display.flip()


    def logic(self):
        pass


    def start(self):
        # Create dungeon.
        startNode = (0, 255, 0)
        bossNode = (255, 0, 0)

        nodeTypes = [ # Colour, Distribution
            [(200, 200, 200), 3], # Empty Space
            [(200, 200, 0), 1], # Treasures
            [(0, 200, 0), 1], # Rest Sites
            [(0, 170, 255), 1] # Shops
        ]

        connectionTypes = [ # Colour, Distribution
            [(0, 0, 0), 3], # Empty Connection
            [(200, 0, 0), 2], # Enemy Connection
            [(100, 0, 0), 1] # Elite Connection
        ]

        # Create the node distribution for later.
        maxNodes = self.mainPathLength + self.sidePathCount
        possibleNodes = {}
        maxNodes *= 3
        totalDistribution = sum(node[1] for node in nodeTypes)

        for node in nodeTypes:
            possibleNodes[node[0]] = math.ceil(maxNodes * (node[1] / totalDistribution))

        # Also create the connection distribution.
        maxConnections = self.mainPathLength + self.sidePathCount
        maxConnections *= 3
        possibleConnections = {}
        totalDistribution = sum(connection[1] for connection in connectionTypes)

        for connection in connectionTypes:
            possibleConnections[connection[0]] = math.ceil(maxConnections * (connection[1] / totalDistribution))

        # Start by constructing the main path.
        previousNode = [0, 0, startNode, 0]
        self.nodes.append(previousNode)

        takenSpaces = [[0, 0]]
        nextMoves = [[0, 1], [1, 0], [-1, 0], [0, -1]]


        # Helper Function - Generates new paths and connections.
        def generate_node(node, direction):
            # Generate the next node...
            possibleColours = []

            for colour in possibleNodes.keys():
                possibleColours += [colour] * possibleNodes[colour]

            chosenColour = random.choice(possibleColours)

            newNode = [node[0] + direction[0], node[1] + direction[1], chosenColour, 0]
            self.nodes.append(newNode)

            possibleNodes[chosenColour] -= 1

            # ...As well as a connection between this new room and the next one.
            possibleColours = []

            for colour in possibleConnections.keys():
                possibleColours += [colour] * possibleConnections[colour]

            chosenConnectionColour = random.choice(possibleColours)

            self.connections.append([node[:2], newNode[:2], chosenConnectionColour, 0])

            possibleConnections[chosenConnectionColour] -= 1

            return newNode


        while len(nextMoves) > 0 and self.mainPathLength > 0: # The main path is just a straight path with no branching paths or shortcuts, at least for now.
            self.mainPathLength -= 1
            nextMove = random.choice(nextMoves)

            newNode = generate_node(previousNode, nextMove)

            # Our next possible moves branch off of the node we just added.
            nextMoves = []

            for adjustment in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                cLocation = [newNode[0] + adjustment[0], newNode[1] + adjustment[1]]

                if not cLocation in takenSpaces:
                    # To prevent the main path from ending early, we perform a surrounded check. We only consider this direction if it won't lead to the node being "surrounded".
                    clearDirections = [True, True, True, True] # Up, Down, Left, Right

                    for space in takenSpaces:
                        if space[1] > cLocation[1]:
                            clearDirections[0] = False
                        elif space[1] < cLocation[1]:
                            clearDirections[1] = False

                        if space[0] < cLocation[0]:
                            clearDirections[2] = False
                        elif space[0] > cLocation[0]:
                            clearDirections[3] = False

                    if sum(clearDirections) != 0:
                        nextMoves.append(adjustment)

            takenSpaces.append(newNode[:2])
            previousNode = newNode

        # The last node should be the boss node.
        previousNode[2] = bossNode

        # For the side paths, pick random nodes and keep constructing until we connect two paths or hit the maximum.
        currentLocation = None

        while self.sidePathCount > 0:
            currentLocation = random.choice(takenSpaces)

            pathLength = 0
            self.sidePathCount -= 1
            nextMoves = [None]

            while pathLength < self.sidePathMaximumSize and self.sidePathCount > 0 and len(nextMoves) > 0:
                nextMoves = []

                for adjustment in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                    cLocation = [currentLocation[0] + adjustment[0], currentLocation[1] + adjustment[1]]

                    if not cLocation in takenSpaces:
                        nextMoves.append(adjustment)

                pathLength += 1

                if len(nextMoves) <= 0:
                    break
    
                chosenMove = random.choice(nextMoves)

                if [currentLocation[0] + adjustment[0], currentLocation[1] + adjustment[1]] in takenSpaces:
                    pathLength = self.sidePathMaximumSize # Instantly end this side path here.

                    possibleColours = []

                    for colour in possibleConnections.keys():
                        possibleColours += [colour] * possibleConnections[colour]

                    chosenConnectionColour = random.choice(possibleColours)

                    self.connections.append([currentLocation, [currentLocation[0] + adjustment[0], currentLocation[1] + adjustment[1]], chosenConnectionColour, 0])

                    possibleConnections[chosenConnectionColour] -= 1


                newNode = generate_node(currentLocation, chosenMove)
                takenSpaces.append(newNode[:2])

                currentLocation = newNode[:2]

        # Start the actual pygame loop.
        pygame.init()
        self.screen = pygame.display.set_mode([800, 800])
        clock = pygame.time.Clock()

        self.isDone = False
        while not self.isDone:
            self.input()
            self.draw()
            self.logic()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isDone = True

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = App()

    previousLines = []
    app.mainPathLength = get_input("Enter the maximum length of the main path: ", minimum = 1)
    previousLines.append(f"Main path length: {app.mainPathLength}")

    app.sidePathCount = get_input("Enter the number of space the side paths should use: ", previousLines, minimum = 0)
    previousLines.append(f"Side path count: {app.sidePathCount}")

    app.sidePathMaximumSize = get_input("Enter the maximum number of spaces a side path can use: ", previousLines, minimum = 1)

    app.start()