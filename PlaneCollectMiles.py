import pygame
import random
import sys

# initialise Pygame
pygame.init()


WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane collecting miles mini game")

WHITE = (255, 255, 255)

# game photos
plane = pygame.image.load("plane.png")
plane = pygame.transform.scale(plane, (100, 80))
plane_x, plane_y = 50, HEIGHT // 2
plane_speed_y = 0

cloud_image = pygame.image.load("cloud.png")
cloud_image = pygame.transform.scale(cloud_image, (200, 180))


mileage = 0
clouds = []
mileage_points = []
cloud_speed_x = 3
gravity = 0.2
lift = -5

font = pygame.font.Font(None, 36)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            plane_speed_y = lift  # plane goes up when tap
        elif event.type == pygame.MOUSEBUTTONUP:
            plane_speed_y = 0  # plane falls when not tapping
    
    # plane movements with gravity
    plane_speed_y += gravity
    plane_y += plane_speed_y

    # plane height limit
    if plane_y < 0:
        plane_y = 0
    elif plane_y > HEIGHT - 40:
        plane_y = HEIGHT - 40

    # generate clouds
    if random.randint(1, 60) == 1:
        cloud_x = WIDTH
        cloud_y = random.randint(50, HEIGHT - 100)
        clouds.append((cloud_x, cloud_y))
    
    # update position of clouds
    clouds = [(x - cloud_speed_x, y) for x, y in clouds if x > -120]

    # generate miles point
    if random.randint(1, 200) == 1:
        mileage_x = WIDTH
        mileage_y = random.randint(50, HEIGHT - 100)
        mileage_value = random.choice([20, 50])  # choose 20 or 50 miles randomly
        mileage_points.append((mileage_x, mileage_y, mileage_value))
    
    mileage_points = [(x - cloud_speed_x, y, value) for x, y, value in mileage_points if x > -80]


    plane_rect = pygame.Rect(plane_x, plane_y, 60, 40)
    for cloud_x, cloud_y in clouds:
        cloud_rect = pygame.Rect(cloud_x, cloud_y, 120, 90)
        if plane_rect.colliderect(cloud_rect):
            running = False  # game ends if touches cloud

    for mileage_x, mileage_y, mileage_value in mileage_points[:]:
        mileage_rect = pygame.Rect(mileage_x, mileage_y, 30, 30)
        if plane_rect.colliderect(mileage_rect):
            mileage += mileage_value  # increase mile
            mileage_points.remove((mileage_x, mileage_y, mileage_value))  # remove collected miles point
    
    for cloud_x, cloud_y in clouds:
        screen.blit(cloud_image, (cloud_x, cloud_y))

    for mileage_x, mileage_y, mileage_value in mileage_points:
        mileage_text = font.render(f"{mileage_value} miles", True, (0, 100, 0))
        screen.blit(mileage_text, (mileage_x, mileage_y))

    # fix plane position
    screen.blit(plane, (plane_x, plane_y))
    
    # show miles
    score_text = font.render(f"Miles: {mileage}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # win if
    if mileage >= 300:
        print("Win！")
        running = False
    
    pygame.display.flip()
    clock.tick(60)
