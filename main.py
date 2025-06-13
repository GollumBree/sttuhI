import math

import numpy as np
import pygame
import serial  # noqa: F401

π = math.pi

pygame.init()
screen = pygame.display.set_mode(
    tuple(
        map(
            lambda x: x[1] - 150 if x[0] else x[1] - 75,
            enumerate(pygame.display.get_desktop_sizes()[0]),
        )
    )
)
pygame.display.set_caption("Nudelholz")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ser = serial.Serial("COM3")

rotation_matrix = np.eye(3)
rotation_speed = (0, 0, 0)
p_racket = pygame.rect.Rect(30, 100, 20, 100)
e_racket = pygame.rect.Rect(screen.get_width() - 50, 100, 20, 100)


def matrix_to_euler(R):
    # ZYX order
    sy = math.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0
    return (math.degrees(x), math.degrees(y), math.degrees(z))

def draw_rectangle(x, y, width, height, color, rotation:float=0):
    """Draw a rectangle, centered at x, y.

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
    """
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]


    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rotation)
        x_offset = radius * math.cos(angle + rotation)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)

running = True
while True:
    buttons = pygame.key.get_pressed()
    ax, ay, az, gx, gy, gz = (
        buttons[pygame.K_UP] - buttons[pygame.K_DOWN],
        buttons[pygame.K_SPACE] - buttons[pygame.K_LSHIFT],
        buttons[pygame.K_RIGHT] - buttons[pygame.K_LEFT],
        buttons[pygame.K_d] - buttons[pygame.K_a],
        buttons[pygame.K_q] - buttons[pygame.K_e],
        buttons[pygame.K_w] - buttons[pygame.K_s],
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    if not running:
        break

    # map(int, ser.read().decode("ascii").split(" "))

    # TODO: Tisch sprite, Netz collision, höhe simulieren, (gegner)
    rotation_speed = (
        rotation_speed[0] + gx / 180 * π,
        rotation_speed[1] + gy / 180 * π,
        rotation_speed[2] + gz / 180 * π,
    )
    # Assume gx, gy, gz are angular velocities in degrees per frame
    # Create small rotation matrices for each axis
    Rx = np.array(
        [
            [1, 0, 0],
            [0, math.cos(rotation_speed[0]), -math.sin(rotation_speed[0])],
            [0, math.sin(rotation_speed[0]), math.cos(rotation_speed[0])],
        ]
    )
    Ry = np.array(
        [
            [math.cos(rotation_speed[1]), 0, math.sin(rotation_speed[1])],
            [0, 1, 0],
            [-math.sin(rotation_speed[1]), 0, math.cos(rotation_speed[1])],
        ]
    )
    Rz = np.array(
        [
            [math.cos(rotation_speed[2]), -math.sin(rotation_speed[2]), 0],
            [math.sin(rotation_speed[2]), math.cos(rotation_speed[2]), 0],
            [0, 0, 1],
        ]
    )

    # Combine the rotations in the correct order (ZYX is common for IMUs)
    dR = Rz @ Ry @ Rx

    # Update the rotation matrix
    rotation_matrix = dR @ rotation_matrix
    # Calculate sidewards (left) and forward movement based on accelerometer and rotation

    # Project accelerometer values onto the screen axes
    # Assuming ax is forward/backward, ay is sidewards, az is up/down
    # Adjust according to your sensor orientation

    movement = np.array([ax, ay, az]) @ rotation_matrix
    p_racket.y = max(
        0, min(screen.get_height() - p_racket.height, p_racket.y + movement[2])
    )
    p_racket.x = max(
        0, min(screen.get_width() - p_racket.width, p_racket.x + movement[0])
    )

    screen.fill(0)
    #pygame.draw.rect(screen, (255, 255, 255), p_racket)
    pygame.draw.rect(screen, (255, 255, 255), e_racket)
    draw_rectangle(p_racket.x,p_racket.y,p_racket.width,p_racket.height,(0,0,0),matrix_to_euler(rotation_matrix)[1])

    text = font.render(
        f"Rotation: {', '.join(f'{x:.5}' for x in matrix_to_euler(rotation_matrix))}",
        True,
        (255, 255, 0),
    )
    text_rect = text.get_rect(center=(screen.get_width() // 2, 40))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
