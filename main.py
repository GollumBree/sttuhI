import serial
import pygame

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

# ser = serial.Serial("COM3")

p_racket = pygame.rect.Rect(30, 100, 20, 100)
e_racket = pygame.rect.Rect(screen.get_width()-50, 100, 20, 100)

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

    #TODO: Tisch sprite, Netz collision, höhe simulieren, sensor werte anwenden

    screen.fill(0)
    pygame.draw.rect(screen, (255, 255, 255), p_racket)
    pygame.draw.rect(screen, (255, 255, 255), e_racket)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
