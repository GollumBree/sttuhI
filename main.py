import serial  # noqa: F401
import pygame
import math

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

rotation = [0, 0, 0]
p_racket = pygame.rect.Rect(30, 100, 20, 100)
e_racket = pygame.rect.Rect(screen.get_width() - 50, 100, 20, 100)

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    if not running:
        break

    ax, ay, az, gx, gy, gz = (
        7,
        7,
        7,
        7,
        7,
        7,
    )  # map(int, ser.read().decode("ascii").split(" "))

    # TODO: Tisch sprite, Netz collision, höhe simulieren, (gegner)
    rotation[0] = (rotation[0] + gx) % 360
    rotation[1] = (rotation[1] + gy) % 360
    rotation[2] = (rotation[2] + gz) % 360
    # Calculate sidewards (left) and forward movement based on accelerometer and rotation

    # Convert rotation angles to radians
    pitch_rad = math.radians(rotation[0])
    roll_rad = math.radians(rotation[1])

    # Project accelerometer values onto the screen axes
    # Assuming ax is forward/backward, ay is sidewards, az is up/down
    # Adjust according to your sensor orientation

    # Forward movement: project ax onto the screen considering pitch
    forward = int(ax * math.cos(pitch_rad))

    # Sidewards movement: project ay onto the screen considering roll
    left = int(ay * math.cos(roll_rad))
    p_racket.y = max(0, min(screen.get_height() - p_racket.height, p_racket.y + left))
    p_racket.x = max(0, min(screen.get_width() - p_racket.width, p_racket.x + forward))

    screen.fill(0)
    pygame.draw.rect(screen, (255, 255, 255), p_racket)
    pygame.draw.rect(screen, (255, 255, 255), e_racket)

    text = font.render(f"Rotation: {rotation}", True, (255, 255, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, 40))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
