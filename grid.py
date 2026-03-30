from lib.utils import *

import pygame
import random
import math

# Main Application
class App:
    def __init__(self):
        self.minimumSize = None
        self.maximumSize = None

        self.screen = None
        self.isDone = False

        self.grid = []

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

        squareSize = 30
        padding = 40
        for square in self.grid:
            hitRect = pygame.Rect(padding * square[0] - self.cameraX - (squareSize / 2), self.cameraY - padding * square[1] - (squareSize / 2), squareSize, squareSize)

            if hitRect.collidepoint(pygame.mouse.get_pos()):
                if left:
                    square[3] = 1
                elif middle:
                    square[3] = 2
                elif right:
                    square[3] = 0


    def draw(self):
        self.screen.fill((100, 100, 100))

        squareSize = 30
        padding = 40

        for square in self.grid:
            if square[3] == 1:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(padding * square[0] - self.cameraX - ((squareSize + 10) / 2), self.cameraY - padding * square[1] - ((squareSize + 10) / 2), squareSize + 10, squareSize + 10))

            pygame.draw.rect(self.screen, square[2] if square[3] != 2 else (255, 255, 255), pygame.Rect(padding * square[0] - self.cameraX - (squareSize / 2), self.cameraY - padding * square[1] - (squareSize / 2), squareSize, squareSize))

        pygame.display.flip()


    def logic(self):
        pass


    def start(self):
        # Create grid.
        gridSize = random.choice(range(self.minimumSize, self.maximumSize + 1)) - 1

        bossNode = (255, 0, 0)
        keyNode = (240, 240, 0)
        startNode = (0, 255, 0)

        nodeTypes = [ # Colour, Distribution
            [(200, 200, 200), 4], # Empty Space
            [(120, 0, 0), 1], # Elite Battles
            [(200, 200, 0), 0.5], # Treasures
            [(0, 200, 0), 0.5], # Rest Sites
            [(0, 170, 255), 1] # Shops
        ]

        # Create the node distribution for later.
        maxNodes = gridSize
        possibleNodes = {}
        totalDistribution = sum(node[1] for node in nodeTypes)

        for node in nodeTypes:
            possibleNodes[node[0]] = math.ceil(maxNodes * (node[1] / totalDistribution))

        # Generate the actual grid.
        possibleNextMoves = []
        previousMoves = []

        while gridSize > 0:
            gridSize -= 1

            if len(self.grid) <= 0:
                self.grid.append([0, 0, startNode, 0])
                possibleNextMoves = [[1, 0], [0, 1], [-1, 0], [0, -1]]
                previousMoves = [[0, 0]]
            
            else:
                nextSpot = random.choice(possibleNextMoves)
                possibleColours = []

                for colour in possibleNodes.keys():
                    possibleColours += [colour] * possibleNodes[colour]

                chosenColour = random.choice(possibleColours)
                self.grid.append(nextSpot + [chosenColour, 0])

                possibleNodes[chosenColour] -= 1

                # Update the set of possible moves.
                possibleNextMoves.remove(nextSpot)
                previousMoves.append(nextSpot)

                for adjustment in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                    if not [nextSpot[0] + adjustment[0], nextSpot[1] + adjustment[1]] in possibleNextMoves + previousMoves:
                        possibleNextMoves.append([nextSpot[0] + adjustment[0], nextSpot[1] + adjustment[1]])
        
        # Generate spots for the key and boss room. Start wit the key.
        keySpot = random.choice(possibleNextMoves)
        self.grid.append(keySpot + [keyNode, 0])

        # The boss room should be as far away from the key spot as posslble. Use manhattan distance for efficiency.
        bestChoice = None

        for spot in possibleNextMoves:
            distance = abs(spot[0] - keySpot[0]) + abs(spot[1] - keySpot[1])
            
            if bestChoice == None or distance > bestChoice[2]:
                bestChoice = spot + [distance]
        
        self.grid.append(bestChoice[:2] + [bossNode, 0])

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
    app.minimumSize = get_input("Enter the minimum number of squares: ", minimum = 2)
    previousLines.append(f"Minimum Amount: {app.minimumSize}")

    app.maximumSize = get_input("Enter the maximum number of squares: ", previousLines, minimum = app.minimumSize)

    app.start()