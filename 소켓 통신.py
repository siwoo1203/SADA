import socket

def main():
    target_ip = '192.168.117.182'
    target_port = 12345

    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # 사용자로부터 메시지 입력
        message = input("송신할 메시지를 입력하세요: ")

        # 메시지를 바이트로 인코딩하여 송신
        sock.sendto(message.encode(), (target_ip, target_port))

        if message == "exit":
            break

    # 소켓 닫기
    sock.close()

if __name__ == '__main__':
    main()