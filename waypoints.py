from lib.utils import *

import pygame
import random
import math

# Main Application
class App:
    def __init__(self):
        self.nodes = []
        self.connections = []

        self.maximumDistance = 0
        self.sideNodes = 0

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

        # Highlighting Nodes
        left, middle, right = pygame.mouse.get_pressed()
        nodeSize = 20

        for node in self.nodes:
            hitRect = pygame.Rect(node[0] - self.cameraX - (nodeSize / 2), node[1] + self.cameraY - (nodeSize / 2), nodeSize, nodeSize)

            if hitRect.collidepoint(pygame.mouse.get_pos()):
                if left:
                    node[3] = 1
                elif middle:
                    node[3] = 2
                elif right:
                    node[3] = 0


    def draw(self):
        self.screen.fill((100, 100, 100))

        # First the connections for proper z-order.
        for connection in self.connections:
            node1 = self.nodes[connection[0]]
            node2 = self.nodes[connection[1]]

            pygame.draw.line(self.screen, (0, 0, 0), (node1[0] - self.cameraX, node1[1] + self.cameraY), (node2[0] - self.cameraX, node2[1] + self.cameraY), 3)

        # Now draw the actual nodes.
        nodeSize = 20

        for node in self.nodes:
            if node[3] == 1:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(node[0] - self.cameraX - ((nodeSize + 6) / 2), node[1] + self.cameraY - ((nodeSize + 6) / 2), nodeSize + 6, nodeSize + 6))

            pygame.draw.rect(self.screen, node[2] if node[3] != 2 else (255, 255, 255), pygame.Rect(node[0] - self.cameraX - (nodeSize / 2), node[1] + self.cameraY - (nodeSize / 2), nodeSize, nodeSize))

        pygame.display.flip()


    def logic(self):
        pass


    def start(self):
        # Create dungeon.
        startNode = (0, 255, 0)
        bossNode = (255, 0, 0)

        # Setting up node distributions. We'll only calculate the scaled distributions once we've placed every node, however.
        nodeTypes = [ # Colour, Distribution
            [(200, 200, 200), 3], # Empty Space
            [(200, 0, 0), 2], # Regular Battles
            [(120, 0, 0), 1], # Elite Battles
            [(200, 200, 0), 0.5], # Treasures
            [(0, 200, 0), 0.5], # Rest Sites
            [(0, 170, 255), 1] # Shops
        ]

        # Initial Node.
        previousNode = [0, 0, startNode, 0]
        self.nodes.append(previousNode)

        # Keep branching forwards until we hit the limit, at which point we can call that the final node.
        cIndex = 0
        
        while previousNode[0] <= self.maximumDistance:
            angle = random.uniform(math.pi / -4, math.pi / 4)

            newNode = [
                previousNode[0] + (math.cos(angle) * 100),
                previousNode[1] + (math.sin(angle) * 100),
                None,
                0
            ]

            self.nodes.append(newNode)
            self.connections.append([cIndex, cIndex + 1])

            previousNode = newNode
            cIndex += 1
        
        previousNode[2] = bossNode

        # Now generate all of the side nodes.
        possibleChoices = [x for x in range(len(self.nodes) - 1)] # We don't want any nodes branching only from the boss node, which would make them inaccessible.

        while self.sideNodes > 0:
            targetIndex = random.choice(possibleChoices)
            chosenAngle = random.uniform(0, 2 * math.pi)
            chosenDistance = random.uniform(50, 150)

            newNode = [
                self.nodes[targetIndex][0] + (math.cos(chosenAngle) * chosenDistance),
                self.nodes[targetIndex][1] + (math.sin(chosenAngle) * chosenDistance),
                None,
                0
            ]

            newConnections = [[targetIndex, len(self.nodes)]]
            validPlacement = True

            for node in self.nodes:
                distance = (node[0] - newNode[0])**2 + (node[1] - newNode[1])**2

                if distance < 50**2: # Making sure that no two nodes are too close to each other.
                    validPlacement = False
                    break
                
                elif 50**2 <= distance <= 150**2:
                    newConnections.append([self.nodes.index(node), len(self.nodes)])
            
            if validPlacement:
                possibleChoices.append(len(self.nodes))
                self.nodes.append(newNode)
                self.connections = self.connections + newConnections
                self.sideNodes -= 1

        # Now that we have every node, we can colour them all in.
        possibleNodes = {}
        totalDistribution = sum(node[1] for node in nodeTypes)

        for node in nodeTypes:
            possibleNodes[node[0]] = math.ceil((len(self.nodes) - 1) * (node[1] / totalDistribution))

        possibleColours = []

        for colour in possibleNodes.keys():
            possibleColours += [colour] * possibleNodes[colour]

        for node in self.nodes:
            if node[2] == None:
                chosenColour = random.choice(possibleColours)
                node[2] = chosenColour
                possibleColours.remove(chosenColour)          

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
    app.maximumDistance = get_input("Enter the maximum distance that the board should progress before ending the map: ", minimum = 0)
    previousLines.append(f"Maximum Distance: {app.maximumDistance}")

    app.sideNodes = get_input("Enter the number of side nodes that should be present: ", previousLines, minimum = 0)

    app.start()