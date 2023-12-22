import pygame as pg
import numpy as np
import sys


rotate_x_z = []
rotate_y_z = []
cos = []
sin = []

for angle in range(360):
    angle = np.deg2rad(angle)
    c = np.cos(angle)
    s = np.sin(angle)
    cos.append(c)
    sin.append(s)
    rotate_x_z.append(np.array([
        [c, 0, -s],
        [0, 1, 0],
        [s, 0, c]
    ]))
    rotate_y_z.append(np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ]))


def generate_point_of_cube(center, size):
    half_size = size / 2
    points = np.array([
        [-1, -1, -1, 1],
        [1, -1, -1, 1],
        [1, 1, -1, 1],
        [-1, 1, -1, 1],
        [-1, -1, 1, 1],
        [1, -1, 1, 1],
        [1, 1, 1, 1],
        [-1, 1, 1, 1]
    ]).T
    transform_martice = np.array([
        [half_size, 0, 0, center[0]],
        [0, half_size, 0, center[1]],
        [0, 0, half_size, center[2]]
    ])
    return np.dot(transform_martice, points).T


def transform_points(points, f):
    points_x = points[..., 0]
    points_y = points[..., 1]
    points_z = (points[..., 2] - f)
    points_z[points_z < 0.001] = 0.001
    return np.column_stack((points_x/points_z, points_y/points_z, np.ones(len(points))))


def save_surfaces(transformed_coordinates):
    return sorted([
        [[0, np.linalg.norm(transformed_coordinates[0]), transformed_coordinates[0][2]], [1, np.linalg.norm(transformed_coordinates[1]), transformed_coordinates[1][2]], [2, np.linalg.norm(transformed_coordinates[2]), transformed_coordinates[2][2]],
         [3, np.linalg.norm(transformed_coordinates[3]), transformed_coordinates[3][2]]],
        [[4, np.linalg.norm(transformed_coordinates[4]), transformed_coordinates[4][2]], [5, np.linalg.norm(transformed_coordinates[5]), transformed_coordinates[5][2]], [6, np.linalg.norm(transformed_coordinates[6]), transformed_coordinates[6][2]],
         [7, np.linalg.norm(transformed_coordinates[7]), transformed_coordinates[7][2]]],
        [[0, np.linalg.norm(transformed_coordinates[0]), transformed_coordinates[0][2]], [1, np.linalg.norm(transformed_coordinates[1]), transformed_coordinates[1][2]], [5, np.linalg.norm(transformed_coordinates[5]), transformed_coordinates[5][2]],
         [4, np.linalg.norm(transformed_coordinates[4]), transformed_coordinates[4][2]]],
        [[2, np.linalg.norm(transformed_coordinates[2]), transformed_coordinates[2][2]], [3, np.linalg.norm(transformed_coordinates[3]), transformed_coordinates[3][2]], [7, np.linalg.norm(transformed_coordinates[7]), transformed_coordinates[7][2]],
         [6, np.linalg.norm(transformed_coordinates[6]), transformed_coordinates[6][2]]],
        [[1, np.linalg.norm(transformed_coordinates[1]), transformed_coordinates[1][2]], [2, np.linalg.norm(transformed_coordinates[2]), transformed_coordinates[2][2]], [6, np.linalg.norm(transformed_coordinates[6]), transformed_coordinates[6][2]],
         [5, np.linalg.norm(transformed_coordinates[5]), transformed_coordinates[5][2]]],
        [[0, np.linalg.norm(transformed_coordinates[0]), transformed_coordinates[0][2]], [3, np.linalg.norm(transformed_coordinates[3]), transformed_coordinates[3][2]], [7, np.linalg.norm(transformed_coordinates[7]), transformed_coordinates[7][2]], [4, np.linalg.norm(transformed_coordinates[4]), transformed_coordinates[4][2]]]
    ], key=lambda x: np.mean(x, axis=0)[1], reverse=True)[-3:]


def draw_cube(screen, points, angle_x_z, angle_y_z, player_position, f, K, color):
    global rotate_x_z, rotate_y_z
    transformed_points = np.dot(np.dot(points - player_position, rotate_x_z[int(angle_x_z)]), rotate_y_z[int(angle_y_z)])
    surfaces = save_surfaces(transformed_points)
    points_2d = np.dot(transform_points(transformed_points, f), K)
    f = 0
    for surface in surfaces:
        if surface[0][2] > f and surface[1][2] > f and surface[2][2] > f and surface[3][2] > f:
            p = []
            depth = np.mean([surface[i][1] for i in range(len(surface))])+0.00001
            color = min(255,max(0,10*color[0]/depth)), min(255,max(0,10*color[1]/depth)), min(255,max(0,10*color[2]/depth))
            for point, _, _ in surface:
                p.append(points_2d[point])
            pg.draw.polygon(screen, color, p)


def main():
    cubes = [
        {
            'center': np.array((0, 0, 0)),
            'points': generate_point_of_cube((0, 0, 0), 2),
            'color': (255, 255, 255)
        },
        {
            'center': np.array((0, 0, 2)),
            'points': generate_point_of_cube((0, 0, 2), 2),
            'color': (255, 255, 255)
        },
        {
            'center': np.array((0, 0, -2)),
            'points': generate_point_of_cube((0, 0, -2), 2),
            'color': (255, 255, 255)
        },
        {
            'center': np.array((0, 2, 2)),
            'points': generate_point_of_cube((0, 2, 2), 2),
            'color': (255, 255, 255)
        },
        {
            'center': np.array((0, 2, -2)),
            'points': generate_point_of_cube((0, 2, -2), 2),
            'color': (255, 70, 70)
        },
        {
            'center': np.array((0, -2, 2)),
            'points': generate_point_of_cube((0, -2, 2), 2),
            'color': (255, 255, 255)
        },
        {
            'center': np.array((2, 0, 0)),
            'points': generate_point_of_cube((2, 0, 0), 2),
            'color': (0, 0, 0)
        },
        {
            'center': np.array((-2, 0, 2)),
            'points': generate_point_of_cube((-2, 0, 2), 2),
            'color': (255, 0, 255)
        },
        {
            'center': np.array((2, 2, 2)),
            'points': generate_point_of_cube((2, 2, 2), 2),
            'color': (255, 255, 0)
        },
        {
            'center': np.array((0, 4, -8)),
            'points': generate_point_of_cube((0, 4, -8), 2),
            'color': (255, 255, 0)
        },
        {
            'center': np.array((0, 4, -6)),
            'points': generate_point_of_cube((0, 4, -6), 2),
            'color': (255, 255, 0)
        },
        {
            'center': np.array((0, 4, -4)),
            'points': generate_point_of_cube((0, 4, -4), 2),
            'color': (255, 255, 0)
        },
        {
            'center': np.array((0, 4, -2)),
            'points': generate_point_of_cube((0, 4, -2), 2),
            'color': (255, 255, 0)
        },
        {
            'center': np.array((2, 4, -8)),
            'points': generate_point_of_cube((2, 4, -8), 2),
            'color': (255, 0, 0)
        },
        {
            'center': np.array((2, 4, -6)),
            'points': generate_point_of_cube((2, 4, -6), 2),
            'color': (0, 0, 0)
        },
        {
            'center': np.array((2, 4, -4)),
            'points': generate_point_of_cube((2, 4, -4), 2),
            'color': (255, 0, 0)
        },
        {
            'center': np.array((2, 4, -2)),
            'points': generate_point_of_cube((2, 4, -2), 2),
            'color': (255, 0, 255)
        },
        {
            'center': np.array((-2, 4, -8)),
            'points': generate_point_of_cube((-2, 4, -8), 2),
            'color': (255, 0, 255)
        },
        {
            'center': np.array((-2, 4, -6)),
            'points': generate_point_of_cube((-2, 4, -6), 2),
            'color': (200, 200, 200)
        }]

    player_position = [0, 0, -15]
    f = 2
    alpha = 100
    beta = 100
    angle_x_z = 0
    angle_y_z = 0
    movement_speed = .05
    rotation_speed = .5
    jump_force = 0
    jump_reduce = 0.05
    gravity = 1
    pg.init()
    width, height = 1024, 1024
    screen = pg.display.set_mode((width, height))
    u0 = width//2
    v0 = height//2
    K = np.array([[f * alpha, 0, u0], [0, f * beta, v0]]).T
    clock = pg.time.Clock()

    while True:
        screen.fill((100, 100, 100))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()

        if keys[pg.K_q]:
            player_position[2] -= movement_speed * sin[int(angle_x_z)]
            player_position[0] -= movement_speed * cos[int(angle_x_z)]
        if keys[pg.K_d]:
            player_position[2] += movement_speed * sin[int(angle_x_z)]
            player_position[0] += movement_speed * cos[int(angle_x_z)]
        if keys[pg.K_z]:
            player_position[2] += movement_speed * cos[int(angle_x_z)]
            player_position[0] -= movement_speed * sin[int(angle_x_z)]
        if keys[pg.K_s]:
            player_position[2] -= movement_speed * cos[int(angle_x_z)]
            player_position[0] += movement_speed * sin[int(angle_x_z)]
        if keys[pg.K_SPACE]:
            # player_position[1] -= movement_speed
            if jump_force == 0:
                jump_force = 2
        if pg.key.get_mods() & pg.KMOD_SHIFT:
            player_position[1] += movement_speed
        if keys[pg.K_LEFT]:
            angle_x_z += rotation_speed
        if keys[pg.K_RIGHT]:
            angle_x_z -= rotation_speed
        if keys[pg.K_UP]:
            angle_y_z += rotation_speed
        if keys[pg.K_DOWN]:
            angle_y_z -= rotation_speed
        jump_force = max(0, jump_force-jump_reduce)
        player_position[1] = min(0, player_position[1]-jump_force+gravity)
        angle_x_z %= 360
        angle_y_z %= 360
        cubes.sort(key=lambda x: np.linalg.norm(np.dot(np.dot(x.get('center') - player_position, rotate_x_z[int(angle_x_z)]), rotate_y_z[int(angle_y_z)])), reverse=True)
        for cube in cubes:
            draw_cube(screen, cube.get('points'), angle_x_z, angle_y_z, player_position, f, K, cube.get('color'))
        clock.tick(600)
        print(clock.get_fps())
        pg.display.update()


if __name__ == '__main__':
    main()