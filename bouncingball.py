import pygame
import math
import sys

# Initialize Pygame and set up the display
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Bouncing Inside a Tesseract")
clock = pygame.time.Clock()

# Global variables for projection
screen_center_x = width // 2
screen_center_y = height // 2
scale = 200  # scale factor for projection

# Simulation parameters
restitution = 0.9       # how much energy is retained at each bounce
gravity = 0.001         # acceleration along the y-axis (index 1)

# Ball parameters in 4D
ball_radius = 0.1       # radius of the ball (in 4D units)
ball_pos = [0.0, 0.0, 0.0, 0.0]   # initial 4D position
ball_vel = [0.01, 0.015, 0.012, 0.008]  # initial 4D velocity

# Define the tesseract (4D hypercube) vertices:
# A tesseract has 16 vertices with coordinates at all combinations of -1 and 1.
tesseract_vertices = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w in [-1, 1]:
                tesseract_vertices.append([x, y, z, w])

# Define the edges of the tesseract:
# Two vertices are connected if they differ in exactly one coordinate.
tesseract_edges = []
num_vertices = len(tesseract_vertices)
for i in range(num_vertices):
    for j in range(i + 1, num_vertices):
        diff = 0
        for k in range(4):
            if tesseract_vertices[i][k] != tesseract_vertices[j][k]:
                diff += 1
        if diff == 1:
            tesseract_edges.append((i, j))

# --- 4D Rotation Functions ---
# In 4D there are 6 independent planes of rotation. Here we define a helper that rotates
# a 4D point in the plane spanned by two coordinate axes (given by indices i and j).
def rotate4d(point, angle, i, j):
    new_point = point.copy()
    temp_i = new_point[i]
    temp_j = new_point[j]
    new_point[i] = temp_i * math.cos(angle) - temp_j * math.sin(angle)
    new_point[j] = temp_i * math.sin(angle) + temp_j * math.cos(angle)
    return new_point

# For display we apply two rotations. For example, we rotate in:
# • the XW plane (indices 0 and 3) and
# • the YZ plane (indices 1 and 2).
def apply_rotation(point, angle1, angle2):
    p = rotate4d(point, angle1, 0, 3)  # rotate in X-W
    p = rotate4d(p, angle2, 1, 2)       # rotate in Y-Z
    return p

# --- Projection Functions ---
# We project from 4D → 3D using a simple perspective projection (using w as “depth”)
# and then from 3D → 2D (using z as “depth”).
def project_point(point4d):
    # 4D to 3D projection
    d4 = 3  # distance from the viewer in 4D
    # Avoid division by zero if w gets too close to d4
    factor4 = d4 / (d4 - point4d[3])
    x3 = point4d[0] * factor4
    y3 = point4d[1] * factor4
    z3 = point4d[2] * factor4

    # 3D to 2D projection
    d3 = 3  # distance from the viewer in 3D
    factor3 = d3 / (d3 - z3)
    x2 = x3 * factor3
    y2 = y3 * factor3

    # Translate to screen coordinates
    screen_x = screen_center_x + x2 * scale
    screen_y = screen_center_y + y2 * scale
    return (int(screen_x), int(screen_y))

# --- Main Loop Rotation Angles for Display ---
angle1 = 0.0
angle2 = 0.0
rotation_speed1 = 0.01
rotation_speed2 = 0.008

# --- Main Loop ---
running = True
while running:
    dt = clock.tick(60)  # run at 60 FPS

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update the 4D simulation for the ball ---
    for i in range(4):
        ball_pos[i] += ball_vel[i]
        # Apply a tiny gravity along the y-axis (index 1)
        if i == 1:
            ball_vel[i] -= gravity

        # Check for collisions with the axis-aligned tesseract boundaries
        if ball_pos[i] + ball_radius > 1:
            ball_pos[i] = 1 - ball_radius
            ball_vel[i] = -ball_vel[i] * restitution
        if ball_pos[i] - ball_radius < -1:
            ball_pos[i] = -1 + ball_radius
            ball_vel[i] = -ball_vel[i] * restitution

    # --- Drawing ---
    screen.fill((30, 30, 30))  # dark background

    # First, compute the rotated and projected vertices of the tesseract.
    projected_vertices = []
    for vertex in tesseract_vertices:
        rotated_vertex = apply_rotation(vertex, angle1, angle2)
        proj = project_point(rotated_vertex)
        projected_vertices.append(proj)

    # Draw each tesseract edge
    for edge in tesseract_edges:
        p1 = projected_vertices[edge[0]]
        p2 = projected_vertices[edge[1]]
        pygame.draw.line(screen, (200, 200, 200), p1, p2, 1)

    # Rotate and project the ball’s 4D position for display
    rotated_ball = apply_rotation(ball_pos, angle1, angle2)
    ball_screen = project_point(rotated_ball)
    pygame.draw.circle(screen, (255, 100, 100), ball_screen, 8)

    pygame.display.flip()

    # Update display rotation angles
    angle1 += rotation_speed1
    angle2 += rotation_speed2

pygame.quit()
sys.exit()
