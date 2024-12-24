import socket
import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # отключаем пакетирование
main_socket.bind(("localhost", 10000))  # айпи и порт привязываем к порту
main_socket.setblocking(False)  # не прирывность , не ждем ответа
main_socket.listen(5)  # прослушка 5 одновременных входящих соединений
print("сокет создался")

players = []
while True:
    try:
        # проверяем желающих войти в игру
        new_socket, addr = main_socket.accept()  # принимаем входящий
        print("подключился", addr)
        new_socket.setblocking(False)
        players.append(new_socket)

    except BlockingIOError:
        pass

    # Считываем команды игроков
    for sock in players:
        try:
            sock.send("игра".encode())
        except:
            players.remove(sock)
            sock.close()
            print("сокет закрыт")
    time.sleep(1)
