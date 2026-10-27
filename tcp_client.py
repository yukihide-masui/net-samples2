# tcp_client.py for Python 3

import socket
import sys

SERVER_NAME = 'localhost'  # サーバのホスト名あるいはIPアドレスを表す文字列
SERVER_PORT = 50000  # サーバのポート
BUFSIZE = 1024  # 一度に受信を試みるバイト数


def main() -> None:
    # ソケットを作る
    #  with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # サーバのソケットに接続する
        client_socket.connect((SERVER_NAME, SERVER_PORT))

        # キーボードから入力された文字列を受け取る
        sentence = input('Input lowercase sentence: ')

        # 文字列をバイト列に変換後、送信する。
        client_socket.sendall(sentence.encode())

        # 最大BUFSIZEバイトを受け取る。受け取った内容はバイト列として格納される。
        modified_sentence = client_socket.recv(BUFSIZE)

        # バイト列を文字列に変換して表示する
        print(f'From Server: {modified_sentence.decode()}')


if __name__ == '__main__':
    try:
        main()
    except ConnectionRefusedError:
        # サーバが起動していないときに出る例外。
        #  トレースバックの代わりに分かりやすいメッセージを出して終了する。
        sys.exit(f'サーバ({SERVER_NAME}:{SERVER_PORT})に接続できませんでした。'
                 'サーバは起動していますか？')
    except KeyboardInterrupt:
        print()
