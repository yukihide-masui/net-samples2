# udp_server.py for Python 3
# トランスポート層にUDPを用いるサーバプログラム

import socket

SERVER_PORT = 50004

# 一度に受信するバイト数
#  ＜注意＞UDPでは、これより大きなデータグラムが届くと、あふれた分は捨てられる。
#  TCPと違って、残りを後からもう一度受信することはできない。
BUFSIZE = 2048


def main() -> None:
    # socket()の第2引数はSOCK_DGRAM（TCPの場合はSOCK_STREAM）
    #  with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('', SERVER_PORT))
        print('The server is ready to receive.')

        # UDPを使う場合は、listen(), accept()は使用しない

        while True:
            # recvfrom()で受信。受信データとクライアントアドレスのタプルが戻り値
            message, client_address = server_socket.recvfrom(BUFSIZE)

            # 受信した文字列を大文字に変換して返送する
            sentence = message.decode()
            print(f'Received from {client_address}: {sentence}')
            modified_message = sentence.upper()

            # sendto()で送信 明示的に相手のアドレスとポートを指定
            #  ここでのclient_addressはIPアドレスとポート番号のタプルになっている
            server_socket.sendto(modified_message.encode(), client_address)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl-Cで止めたときにエラー表示（トレースバック）を出さずに終了する
        print('\nThe server was stopped.')
