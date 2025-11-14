import sys
import math
import random
import pygame
from pygame.math import Vector2
from .car import Car
from .ai import AIController

WIDTH, HEIGHT = 1280, 720
FPS = 60


def draw_road(surface):
    surface.fill((80, 170, 90))  # grass
    road_color = (40, 40, 40)
    pygame.draw.rect(surface, road_color, (200, 0, 400, 2000))
    pygame.draw.rect(surface, road_color, (0, 200, 2000, 400))
    # draw straight cross


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Freeplay Racing Prototype")
    clock = pygame.time.Clock()

    # big world surface
    world_width, world_height = 2000, 2000
    world = pygame.Surface((world_width, world_height))
    draw_road(world)

    # player car
    car = Car(Vector2(world_width // 2, world_height // 2))

    # AI cars
    ai_cars = []
    for i in range(6):
        pos = Vector2(world_width // 2 + random.randint(-150, 150), world_height // 2 + random.randint(-300, -50 - i * 50))
        ai_car = Car(pos, color=(200, 80, 80))
        ai_car.controller = AIController(ai_car, world)
        ai_cars.append(ai_car)

    show_debug = True
    running = False
    elapsed_test = 0.0
    import os
    try:
        test_seconds = float(os.getenv('GAME_TEST_SECONDS', '0'))
    except Exception:
        test_seconds = 0.0

    while True:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    car.reset(Vector2(world_width // 2, world_height // 2))
                if event.key == pygame.K_d:
                    show_debug = not show_debug
                if event.key == pygame.K_t:
                    # spawn new AI
                    pos = car.pos + Vector2(random.randint(-300, 300), random.randint(-300, 300))
                    new_ai = Car(pos, color=(random.randint(80,255),random.randint(80,255),random.randint(80,255)))
                    new_ai.controller = AIController(new_ai, world)
                    ai_cars.append(new_ai)

        # inputs
        keys = pygame.key.get_pressed()
        car.update(dt, keys)

        for ai in ai_cars:
            ai.update(dt)

        # collisions between cars
        all_cars = ai_cars + [car]
        for i in range(len(all_cars)):
            for j in range(i + 1, len(all_cars)):
                a = all_cars[i]
                b = all_cars[j]
                try:
                    a.collide_with(b)
                except Exception:
                    pass

        # world bounds clamp
        for c in all_cars:
            if c.pos.x < 0:
                c.pos.x = 0
                c.velocity.x *= -0.3
            if c.pos.y < 0:
                c.pos.y = 0
                c.velocity.y *= -0.3
            if c.pos.x > world_width:
                c.pos.x = world_width
                c.velocity.x *= -0.3
            if c.pos.y > world_height:
                c.pos.y = world_height
                c.velocity.y *= -0.3

        # camera — center on player
        cam_x = int(car.pos.x - WIDTH / 2)
        cam_y = int(car.pos.y - HEIGHT / 2)

        screen.fill((80, 170, 90))
        screen.blit(world, (-cam_x, -cam_y))

        # draw cars
        for ai in ai_cars:
            ai.draw(screen, offset=Vector2(-cam_x, -cam_y))
        car.draw(screen, offset=Vector2(-cam_x, -cam_y))

        # minimap
        minimap_w, minimap_h = 220, 140
        minimap = pygame.Surface((minimap_w, minimap_h))
        minimap.fill((30, 30, 30))
        # sample scaled world (fast approximate)
        scale_x = minimap_w / world_width
        scale_y = minimap_h / world_height
        # draw cars as dots
        for c in ai_cars:
            x = int(c.pos.x * scale_x)
            y = int(c.pos.y * scale_y)
            pygame.draw.circle(minimap, (200, 80, 80), (x, y), 3)
        x = int(car.pos.x * scale_x)
        y = int(car.pos.y * scale_y)
        pygame.draw.circle(minimap, (70, 130, 255), (x, y), 4)
        screen.blit(minimap, (WIDTH - minimap_w - 10, 10))

        if show_debug:
            font = pygame.font.SysFont(None, 20)
            debug_surf = font.render(f"Speed: {car.velocity.length():.1f} | Pos: {int(car.pos.x)} {int(car.pos.y)} | DT: {dt:.3f}", True, (255,255,255))
            screen.blit(debug_surf, (10, 10))

        pygame.display.flip()

        if test_seconds > 0:
            elapsed_test += dt
            if elapsed_test >= test_seconds:
                pygame.quit()
                return


if __name__ == "__main__":
    main()
