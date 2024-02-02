import socket
import threading
import time
import csv

TRUE = 1
FALSE = 0

def replace(s):
    return s.replace('\n', '_')

def wait_1_min():
    remaining_time = 60  # 1 minute countdown

    while remaining_time > 0:
        print("\rTime remaining: {} seconds".format(remaining_time), end="")
        time.sleep(1)
        remaining_time -= 1

    print("\rYou are done!                       \n")

def receive_data(sock):
    while True:
        try:
            buffer = sock.recv(1024).decode('utf-8')
            if not buffer:
                print("Connection closed by peer")
                break
            print(buffer, end='')
        except Exception as e:
            print("Error receiving data:", e)
            break

def record_attendance(data):
    with open('attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty (i.e., no header present)
            writer.writerow(['Name', 'Class', 'Roll No.'])
        writer.writerows(data)
    print("Attendance recorded in 'attendance.csv'")

def main():
    host = "localhost"
    port = 65001

    print("\nLooking for Vishwakarma Labs on {}...".format(host))

    try:
        sockfd = socket.create_connection((host, port))
    except Exception as e:
        print("Connection failed:", e)
        exit(1)

    print("\nVishwakarma Labs found!")
    print("\nEnter your Name, Class and Roll no. [AI&DS_A_Siddhesh_27]")

    counter = 0
    attendance_data = []

    receive_thread = threading.Thread(target=receive_data, args=(sockfd,), daemon=True)
    receive_thread.start()

    done = FALSE

    try:
        while not done:
            buffer = input()
            if not buffer:
                print()
            else:
                buffer = replace(buffer)
                sockfd.send(buffer.encode('utf-8'))

                if buffer == "close":
                    done = TRUE
                else:
                    counter += 1
                    print("\nYour timer has started!")
                    wait_1_min()
                    buffer = replace(buffer)
                    buffer += "Present\n"
                    attendance_data.append(buffer.split('_')[:3])  # Keep only the first three elements
                    sockfd.send(buffer.encode('utf-8'))
                    print("\nYour Attendance has been marked! Bye!")
                    done = TRUE
    except KeyboardInterrupt:
        pass

    print("\nDisconnected")
    sockfd.close()
    record_attendance(attendance_data)

if __name__ == "__main__":
    main()
