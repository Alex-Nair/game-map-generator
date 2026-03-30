from lib.utils import *

import pygame
import random
import math

# Main Application
class App:
    def __init__(self):
        self.distance = None
        self.spread = None

        self.screen = None
        self.isDone = False

        self.nodes = []
        self.connections = []

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
        
        # Highlighting Nodes
        left, middle, right = pygame.mouse.get_pressed()

        yOffset = 0
        for nodes in self.nodes:
            nodeSize = 60 if self.nodes.index(nodes) == len(self.nodes) - 1 else 30

            for node in nodes:
                hitRect = pygame.Rect(-1 * self.cameraX - (nodeSize / 2) + 80 * node[1], self.cameraY - (nodeSize / 2) - yOffset, nodeSize, nodeSize)

                if hitRect.collidepoint(pygame.mouse.get_pos()):
                    if left:
                        node[2] = 1
                    elif middle:
                        node[2] = 2
                    elif right:
                        node[2] = 0
            
            yOffset += 150

    def draw(self):
        self.screen.fill((100, 100, 100))

        # Drawing the map.
        yOffset = 150

        for connectionSet in self.connections:
            for connection in connectionSet:
                pygame.draw.line(self.screen, (0, 0, 0), (-1 * self.cameraX + 80 * connection[0], self.cameraY - yOffset + 150), (-1 * self.cameraX + 80 * connection[1], self.cameraY - yOffset), 3)

            yOffset += 150
        
        yOffset = 0
        for nodes in self.nodes:
            nodeSize = 60 if self.nodes.index(nodes) == len(self.nodes) - 1 else 30

            for node in nodes:
                # Draw Hightlight
                if node[2] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(-1 * self.cameraX- ((nodeSize + 10) / 2) + 80 * node[1], self.cameraY - ((nodeSize + 10) / 2) - yOffset, nodeSize + 10, nodeSize + 10))

                pygame.draw.rect(self.screen, node[0] if node[2] != 2 else (255, 255, 255), pygame.Rect(-1 * self.cameraX- (nodeSize / 2) + 80 * node[1], self.cameraY - (nodeSize / 2) - yOffset, nodeSize, nodeSize))


            # Adjust y-offset to prevent overlaps.
            yOffset += 150

        pygame.display.flip()


    def logic(self):
        pass


    def start(self):
        # Generate the map.
        lastNode = (255, 0, 0)
        penultimateNodes = (0, 200, 0)

        nodeTypes = [ # Colour, Distribution
            [(200, 0, 0), 3], # Regular Battles
            [(120, 0, 0), 1], # Elite Battles
            [(200, 200, 0), 0.5], # Treasures
            [(0, 200, 0), 0.5], # Rest Sites
            [(0, 170, 255), 1] # Shops
        ]

        # The first and second set of notes are pre-set.
        self.nodes.append([[lastNode, 0, 0]])

        penultimateNodeCount = random.choice(range(0, self.spread)) * 2 + 1

        nodes = []
        connections = []
        for i in range(penultimateNodeCount):
            position = math.ceil(i / 2) * (-1 if i % 2 == 0 else 1)

            nodes.append([penultimateNodes, position, 0])
            connections.append([position, 0])
        
        nodes = sorted(nodes, key = lambda x: x[1])
        self.nodes.append(nodes)
        self.connections.append(connections)

        # The maximum number of nodes is "distance * spread * 2", so distribute across that.
        maxNodes = self.distance * self.spread * 2

        possibleNodes = {}
        totalDistribution = sum(node[1] for node in nodeTypes)

        for node in nodeTypes:
            possibleNodes[node[0]] = math.ceil(maxNodes * (node[1] / totalDistribution))

        # Generate the rest of the layers.
        for i in range(self.distance - 2):
            nodes = []
            connections = []

            for node in self.nodes[-1]:
                possibleDirections = [node[1]]

                for direction in [-1, 1]:
                    if abs(node[1] + direction) <= self.spread and not [node[1], node[1] + direction] in connections:
                        possibleDirections.append(node[1] + direction)
                
                random.shuffle(possibleDirections)

                nodeCount = random.choice([x for x in [1, 1, 1, 1, 2, 2, 3] if x <= len(possibleDirections)])
                for j in range(nodeCount):
                    nextPosition = possibleDirections[j]

                    foundNode = False
                    for cNode in nodes:
                        if cNode[1] == nextPosition:
                            foundNode = True
                            break

                    if not foundNode:
                        possibleColours = []

                        for colour in possibleNodes.keys():
                            possibleColours += [colour] * possibleNodes[colour]

                        chosenColour = random.choice(possibleColours)
                        nodes.append([chosenColour, nextPosition, 0])

                        possibleNodes[chosenColour] -= 1
                    
                    connections.append([nextPosition, node[1]]) # We write this in reverse order so that when we flip the tree, this is easier to work with.
            
            self.nodes.append(nodes)
            self.connections.append(connections)
        
        # Flip the tree since we've been building it top-down.
        self.nodes.reverse()
        self.connections.reverse()

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

    app.distance = get_input("Enter the length of the map: ", minimum = 2)
    previousLines.append(f"Map Distance: {app.distance}")

    app.spread = get_input("Enter the maximum spread of the map: ", previousLines, minimum = 0)

    app.start()