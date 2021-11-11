import pygame
from collections import deque
import random
import uuid
from pygame import gfxdraw

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.id = uuid.uuid4()

class Connection:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

points = []
connections = []
def distance_between_points(point1, point2):
    return ((point1[0] - point2.x)**2 + (point1[1] - point2.y)**2)**0.5

def create_random_point(x, y):
    global points
    minimum_distance = 80
    x_margin = x - minimum_distance
    y_margin = y - minimum_distance
    while True:
        random_point = (random.randint(minimum_distance, x_margin), random.randint(minimum_distance, y_margin))
        toggle = True
        for point in points:
            if distance_between_points(random_point, point) < minimum_distance:
                toggle = False

        if toggle:
            return random_point
                
def remove_unconnected_points():
    global points
    global connections
    for point in points:
        for connection in connections:
            if point == connection.point1 or point == connection.point2:
                break
        else:
            points.remove(point)
        toggle = False


def randomize_playfield():
    global points
    global connections
    points = []
    connections = []
    for i in range(20):
        x, y = create_random_point(WINDOW_WIDTH, WINDOW_HEIGHT)
        color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        points.append(Point(x, y, color))
    for i in range(random.randrange(len(points))*5):
        random_point = random.choice(points)
        other_random_point = random.choice(points)
        connections.append(Connection(random_point, other_random_point))

    remove_unconnected_points()

def longest_path(point1, point2):
    global connections
    global points
    visited = []
    queue = deque([point1])
    while queue:
        current_point = queue.popleft()
        visited.append(current_point)
        for connection in connections:
            if current_point == connection.point1 and connection.point2 not in visited:
                queue.append(connection.point2)
            elif current_point == connection.point2 and connection.point1 not in visited:
                queue.append(connection.point1)
    return visited


def color_subset(point):
    global connections
    global points
    visited = []
    queue = deque([point])
    while queue:
        current_point = queue.popleft()
        visited.append(current_point)
        for connection in connections:
            if current_point == connection.point1 and connection.point2 not in visited:
                queue.append(connection.point2)
            elif current_point == connection.point2 and connection.point1 not in visited:
                queue.append(connection.point1)
    return visited

def click_to_circle(x,y):
    for point in points:
        if distance_between_points((x,y), point) < 20:
            return point
    return None


def main():
    global connections
    global points
    pygame.init()
    pygame.display.set_caption("Minimum Spanning Trees")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.flip()
    running = True
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20)

    drag_circle = False
    randomize_playfield()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    randomize_playfield()
                    print(longest_path(random.choice(points), random.choice(points)))

            if event.type == pygame.MOUSEBUTTONDOWN:
                circle = click_to_circle(event.pos[0], event.pos[1])
                if circle:
                    coll = color_subset(circle)
                    for collection in list(set(coll)):
                        if collection.color == (255, 0, 0):
                            collection.color = (0, 255, 0)
                        elif collection.color == (0, 255, 0):
                            collection.color = (0, 0, 255)
                        elif collection.color == (0, 0, 255): 
                            collection.color = (0, 255, 255)
                        else: 
                            collection.color = (255, 0, 0)

                drag_circle = click_to_circle(event.pos[0], event.pos[1])

            if event.type == pygame.MOUSEMOTION:
                if drag_circle:
                    drag_circle.x = event.pos[0]
                    drag_circle.y = event.pos[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if drag_circle is not None:
                    drag_circle.x = event.pos[0]
                    drag_circle.y = event.pos[1]
                    drag_circle = False

        screen.fill((255, 255, 255))
        knoten = len(points)
        kanten = len(connections)
        written_text = font.render("Knoten: {} Kanten: {}".format(knoten, kanten), False, (0,0,0))
        screen.blit(written_text, (10, 10))

        for connection in connections:
            gfxdraw.line(screen, connection.point1.x, connection.point1.y, connection.point2.x, connection.point2.y, connection.color)
        for point in points:
            gfxdraw.aacircle(screen,  point.x, point.y, 20, point.color)
            gfxdraw.filled_circle(screen,  point.x, point.y, 20, point.color)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()