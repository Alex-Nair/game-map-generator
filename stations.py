from lib.utils import *

import pygame
import random
import math

# Main Application
class App:
    def __init__(self):
        self.distance = None
        self.spread = None
        self.elementsPerStation = None

        self.stations = []
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

        stationSize = 60

        for layer in range(len(self.stations)):
            for station in self.stations[layer]:
                hitRect = pygame.Rect(station[0] * 150 - self.cameraX - (stationSize / 2), layer * 150 + self.cameraY - (stationSize / 2), stationSize, stationSize)

                if hitRect.collidepoint(pygame.mouse.get_pos()):
                    if left:
                        station[2] = 1
                    elif middle:
                        clear_screen()

                        print("EVENTS:")
                        for event in station[1]:
                            print(f"- {event}")
                    elif right:
                        station[2] = 0


    def draw(self):
        self.screen.fill((100, 100, 100))

        stationSize = 60
        stationInsideSize = 50

        # Draw the connections first for z-order.
        for connection in self.connections:
            pygame.draw.line(self.screen, (0, 0, 0), 
                             (connection[0][1] * 150 - self.cameraX, connection[0][0] * 150 + self.cameraY),
                             (connection[1][1] * 150 - self.cameraX, connection[1][0] * 150 + self.cameraY), 3)

        # Now draw all of the stations.
        for layer in range(len(self.stations)):
            for station in self.stations[layer]:
                pygame.draw.rect(self.screen, (255, 255, 255) if station[2] != 1 else (0, 255, 0), pygame.Rect(station[0] * 150 - self.cameraX - (stationSize / 2), layer * 150 + self.cameraY - (stationSize / 2), stationSize, stationSize))
                pygame.draw.rect(self.screen, (100, 100, 100), pygame.Rect(station[0] * 150 - self.cameraX - (stationInsideSize / 2), layer * 150 + self.cameraY - (stationInsideSize / 2), stationInsideSize, stationInsideSize))
        
        pygame.display.flip()


    def logic(self):
        pass


    def start(self):
        # Create the stations.
        startEvent = "Entry Station"
        finalEvent = "Boss Fight"

        stationCount = 2 # Start and end stations.

        # Start with the actual distribution of elements that will be in each station. We'll calculate their real distribution later.
        eventTypes = {
            "Fight": 3,
            "Elite Fight": 1,
            "Treasure": 0.5,
            "Rest": 0.5,
            "Shop": 1
        }

        # Helper Functions
        def get_station(location):
            try:
                for station in self.stations[location[0]]:
                    if station[0] == location[1]:
                        return station
                
                return None
            except IndexError:
                return None
        
        def add_station(location):
            while len(self.stations) <= location[0]:
                self.stations.append([])
            
            self.stations[location[0]].append([location[1], [], 0])

        # Generate a top-down map, similar to scroll.
        self.stations.append([[0, [finalEvent], 0]])

        toConsider = [[0, 0]] # Which layer, what location in layer.

        while len(toConsider) > 0:
            newConsiderations = []

            for stationLocation in toConsider:
                possibleDirections = [[1, 0]] * 5 + [[1, -1], [1, 1]] * 2 + [[0, 1], [0, -1]] # Side-to-side movement should be less likely than downard movement.
                movementAttempts = random.choice([1] * 3 + [2] * 2 + [3])

                connectionsMade = 0
                while len(possibleDirections) > 0 and connectionsMade < movementAttempts:
                    chosenDirection = random.choice(possibleDirections)
                    possibleDirections = [direction for direction in possibleDirections if direction != chosenDirection] # Filter out this direction.

                    newPosition = [stationLocation[0] + chosenDirection[0], stationLocation[1] + chosenDirection[1]]

                    if newPosition[0] > self.distance or abs(newPosition[1]) > self.spread:
                        continue

                    if get_station(newPosition) == None:
                        add_station(newPosition)
                        stationCount += 1

                        newConsiderations.append(newPosition)
                    
                    self.connections.append([stationLocation, newPosition])
                    connectionsMade += 1
            
            toConsider = newConsiderations.copy()

        # Add the last node, which is the start node and connects to every possible node above it.
        self.stations.append([[0, [startEvent], 0]])

        # Now that we have every station, we can add events to them.
        events = []
        totalDistribution = sum(eventTypes.values())

        for eventType in eventTypes.keys():
            events = events + [eventType] * math.ceil(stationCount * self.elementsPerStation * (eventTypes[eventType] / totalDistribution))
        
        for layer in self.stations:
            for station in layer:
                if len(station[1]) <= 0:
                    for _ in range(self.elementsPerStation):
                        chosenElement = random.choice(events)
                        events.remove(chosenElement)

                        station[1].append(chosenElement)
        

        for node in self.stations[-2]:
            self.connections.append([[len(self.stations) - 1, 0], [len(self.stations) - 2, node[0]]])

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
    previousLines.append(f"Spread: {app.spread}")

    app.elementsPerStation = get_input("Enter the number of elements there should be at each station: ", previousLines, minimum = 1)

    app.start()