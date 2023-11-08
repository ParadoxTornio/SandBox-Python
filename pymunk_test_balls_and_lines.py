__docformat__ = "reStructuredText"

import pygame

import pymunk
from pymunk import Vec2d

X, Y = 0, 1
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_BALL = 2


def flipy(y):
    return -y + 600


def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    space = pymunk.Space()
    space.gravity = 0.0, -900.0

    balls = []

    line_point1 = None
    static_lines = []
    run_physics = True

    image = pygame.image.load('images/water_frame.png')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "balls_and_lines.png")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(10):
                    p = event.pos[X], flipy(event.pos[Y])
                    body = pymunk.Body(10, 100)
                    body.position = p
                    shape = pymunk.Circle(body, 2, (0, 0))
                    shape.friction = 0.5
                    shape.collision_type = COLLTYPE_BALL
                    space.add(body, shape)
                    balls.append(shape)

            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #     if line_point1 is None:
            #         line_point1 = Vec2d(event.pos[X], flipy(event.pos[Y]))
            # elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            #     if line_point1 is not None:

            #         line_point2 = Vec2d(event.pos[X], flipy(event.pos[Y]))
            #         shape = pymunk.Segment(
            #             space.static_body, line_point1, line_point2, 0.0
            #         )
            #         shape.friction = 0.99
            #         space.add(shape)
            #         static_lines.append(shape)
            #         line_point1 = None
            line_point1 = Vec2d(0, flipy(599))
            line_point2 = Vec2d(600, flipy(599))
            left_line_point1_y = Vec2d(500, flipy(0))
            left_line_point2_y = Vec2d(500, flipy(600))
            right_line_point1_y = Vec2d(599, flipy(0))
            right_line_point2_y = Vec2d(599, flipy(600))
            shape1 = pymunk.Segment(
                space.static_body, line_point1, line_point2, 0.0
            )
            shape2 = pymunk.Segment(
                space.static_body, left_line_point1_y, left_line_point2_y, 0.0
            )
            shape3 = pymunk.Segment(
                space.static_body, right_line_point1_y, right_line_point2_y,
                0.0)
            shape1.friction = 0.99
            shape2.friction = 0.99
            shape3.friction = 0.99
            space.add(shape1)
            space.add(shape2)
            space.add(shape3)
            static_lines.append(shape1)
            static_lines.append(shape2)
            static_lines.append(shape3)
            line_point1 = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_physics = not run_physics

        p = pygame.mouse.get_pos()
        mouse_pos = Vec2d(p[X], flipy(p[Y]))

        # if pygame.key.get_mods() and \
        #         pygame.mouse.get_pressed()[0]:
        #     body = pymunk.Body(10, 10)
        #     body.position = mouse_pos
        #     shape = pymunk.Circle(body, 4, (0, 0))
        #     shape.collision_type = COLLTYPE_BALL
        #     space.add(body, shape)
        #     balls.append(shape)

        if run_physics:
            dt = 1.0 / 60.0
            for x in range(1):
                space.step(dt)

        screen.fill(pygame.Color("white"))

        for ball in balls:
            r = ball.radius
            v = ball.body.position
            rot = ball.body.rotation_vector
            p = int(v.x), int(flipy(v.y))
            p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
            p2 = int(p2.x), int(p2.y)
            pygame.draw.circle(screen, pygame.Color("blue"), p, int(r), 8)
            water_surface = pygame.Surface((8, 8))
            water_surface.blit(image, (0, 0))
            screen.blit(water_surface, (p[0] - r, p[1] - r))

        if line_point1 is not None:
            p1 = int(line_point1.x), int(flipy(line_point1.y))
            p2 = mouse_pos.x, flipy(mouse_pos.y)
            pygame.draw.lines(screen, pygame.Color("black"), False, [p1, p2])

        for line in static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = int(pv1.x), int(flipy(pv1.y))
            p2 = int(pv2.x), int(flipy(pv2.y))
            pygame.draw.lines(screen, pygame.Color(
                "black"), False, [p1, p2])

        pygame.display.flip()
        clock.tick(60)
        pygame.display.set_caption("fps: " + str(clock.get_fps()) +
                                   " quantity: " + str(len(balls)))


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
    else:
        import cProfile
        import pstats

        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats("cumulative", "time", "calls")
        stats.print_stats(30)
