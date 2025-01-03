# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
# sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
# sock.connect(("localhost", 10000))
#
# while True:
#     sock.send("""Сижу за решеткой в темнице сырой.
# Вскормленный в неволе орел молодой,
# Мой грустный товарищ, махая крылом,
# Кровавую пищу клюет под окном,
# Клюет, и бросает, и смотрит в окно,
# Как будто со мною задумал одно.
# Зовет меня взглядом и криком своим
# И вымолвить хочет: «Давай улетим!
# Мы вольные птицы; пора, брат, пора!c
# Туда, где за тучей белеет гора,
# Туда, где синеют морские края,
# Туда, где гуляем лишь ветер… да я!..""""".encode())


# Размести на бактерии свой никнейм. Для этого тебе нужно будет вспомнить, как работают шрифты в PyGame.

import socket
import pygame
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 10000))

pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)
radius = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")
font = pygame.font.Font(None, 36)
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0] - CC[0], pos[1] - CC[1]
        lenv = math.sqrt(vector[0]**2 + vector[1]**2)
        vector = vector[0] / lenv, vector[1] / lenv
        if lenv <= radius:
            vector = 0, 0
        if vector != old:
            old = vector
            msg = f"<{vector[0]}, {vector[1]}>"
            sock.send(msg.encode())

    try:
        data = sock.recv(1024).decode()
        print("получил:", data)
    except socket.error as e:
        print("Ошибка приема данных:", e)

    screen.fill("gray")
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    text_surface = font.render("Наполеон", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    pygame.display.update()

pygame.quit()