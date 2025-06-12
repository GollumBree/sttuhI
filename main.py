import serial
import pygame

x, y = pygame.init()
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()

ser = serial.Serial("COM3")


running=True
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    if not running:
        break
    
    ax, ay, az, gx, gy, gz = map(int, ser.read().decode("ascii").split(" "))
    
   
    
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()