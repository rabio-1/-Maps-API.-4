import math
import os
import sys

import pygame

from Samples.geocoder import get_coordinates, get_ll_span
from Samples.mapapi_PG import show_map

LON_STEP = 0.01
LAN_STEP = 0.025
print('Что вы хотите найти?')
t = input()
gl = 'map'


if __name__ == '__main__':
    toponym_to_find = t
    if toponym_to_find:
        zoom = 15
        lat, lon = get_coordinates(toponym_to_find)
        ll_spn = f'll={lat},{lon}&z={zoom}'
        point_param = f'pt={lat},{lon}'
        show_map(ll_spn, 'map')
    else:
        print('Нет данных для поиска')

    map_file = 'map.png'
    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_PAGEUP:
                    if zoom < 23:
                        zoom += 1
                elif event.key == pygame.K_PAGEDOWN:
                    if zoom > 1:
                        zoom -= 1

                elif event.key == pygame.K_UP:
                    lon += LON_STEP * math.pow(2, 15 - zoom)
                    if lon > 85:
                        lon = 85
                elif event.key == pygame.K_DOWN:
                    lon -= LON_STEP * math.pow(2, 15 - zoom)
                    if lon < -85:
                        lon = -85
                elif event.key == pygame.K_RIGHT:
                    lat += LAN_STEP * math.pow(2, 15 - zoom)
                    if lat > 180:
                        lat = 180
                elif event.key == pygame.K_LEFT:
                    lat -= LAN_STEP * math.pow(2, 15 - zoom)
                    if lat < -180:
                        lat = -180

                elif event.key == pygame.K_1:
                    gl = 'map'
                elif event.key == pygame.K_2:
                    gl = 'sat'
                elif event.key == pygame.K_3:
                    gl = 'sat,skl'

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:
                    if zoom < 23:
                        zoom += 1
                if event.button == 5:
                    if zoom > 1:
                        zoom -= 1

        ll_spn = f'll={lat},{lon}&z={zoom}'
        show_map(ll_spn, f'{gl}', point_param)
        screen.blit(pygame.image.load(map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)