import socket
import select

TRUE = 1
FALSE = 0

def main():
    host = "localhost"
    port = 65001

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print("Server is Live now...")

    main_fd = [server]
    done = FALSE

    while not done:
        read_fd, _, _ = select.select(main_fd, [], [])

        for fd in read_fd:
            if fd == server:
                clientfd, _ = server.accept()
                main_fd.append(clientfd)

                buffer = f"\nVISHWAKRAMA LABS> Welcome {clientfd.getpeername()} to Vishwakarma Labs!"
                clientfd.send(buffer.encode('utf-8'))

                buffer = f"\nVISHWAKARMA LABS> {clientfd.getpeername()} has joined the server\n"
                for x in main_fd:
                    if x != server:
                        try:
                            x.send(buffer.encode('utf-8'))
                        except BrokenPipeError:
                            pass
                print(buffer)

            else:
                try:
                    peername = fd.getpeername()
                    buffer = fd.recv(1024).decode('utf-8')
                except (ConnectionResetError, OSError):
                    buffer = None
                    peername = None

                if not buffer:
                    fd.close()
                    main_fd.remove(fd)

                    if peername:
                        disconnect_msg = f"\nVISHWAKARMA LABS> {peername} disconnected\n"
                        for x in main_fd:
                            if x != server:
                                try:
                                    x.send(disconnect_msg.encode('utf-8'))
                                except BrokenPipeError:
                                    pass
                        print(disconnect_msg)

                else:
                    if buffer == "shutdown\n":
                        done = TRUE
                    else:
                        sendstr = f"{peername}> {buffer}"

                        for x in main_fd:
                            if x != server:
                                try:
                                    x.send(sendstr.encode('utf-8'))
                                except BrokenPipeError:
                                    pass
                        print(sendstr)

    print("\nVISHWAKRMA LABS> Shutdown issued; cleaning up")
    server.close()

if __name__ == "__main__":
    main()
