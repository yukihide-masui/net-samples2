# tcp_server_thread.py for Python 3
#
# クライアントごとにスレッドを作って応対するサーバ。
# スレッドを作らない版（tcp_server_nothread.py）と見比べてください。
#

import socket
import threading  # for Thread()
import time  # for time.sleep()

SERVER_PORT = 50000
BUFSIZE = 1024


def interact_with_client(s: socket.socket, addr: tuple[str, int]) -> None:
    # with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with s:
        sentence = s.recv(BUFSIZE).decode()
        print(f'Received from {addr}: {sentence}')

        time.sleep(15.0)  # 時間のかかる処理をしているつもりで15秒待つ

        capitalized_sentence = sentence.upper()
        print(f'Sending to {addr}: {capitalized_sentence}')
        s.sendall(capitalized_sentence.encode())


def main() -> None:
    # with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # サーバを再起動したときにbind()が
        # 「Address already in use」で失敗するのを防ぐための設定
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', SERVER_PORT))
        server_socket.listen(5)  # 引数は保留できる接続の数（バックログ）
        print('The server is ready to receive')

        while True:
            connection_socket, addr = server_socket.accept()

            # スレッドを作り、そこで動かす関数と引数をスレッドに与える
            #   argsに与えるのはタプル(xxx, xxx, ...)でないといけないので、
            #   たとえ引数が一つであっても、括弧で囲い、かつ、ひとつめの要素のあとにカンマを入れる。
            #
            #   daemon=Trueを指定すると、メインのプログラムが終了するときに
            #   スレッドの終了を待たずにプログラム全体が終了する。
            #   これを指定しないと、Ctrl-Cで止めても処理中のスレッドが
            #   終わるまで（最大15秒）プログラムが終了しない。
            client_handler = threading.Thread(
                target=interact_with_client,
                args=(connection_socket, addr),
                daemon=True)
            client_handler.start()  # スレッドを開始


# 発展: 複数のクライアントを同時に扱うサーバの書き方は他にもあります。
#   - socketserver.ThreadingTCPServer : 定型的な処理を標準ライブラリに任せる
#   - concurrent.futures.ThreadPoolExecutor : 作るスレッドの数に上限を設ける
#   - asyncio : スレッドを作らずに、1つのスレッドで多数の接続を扱う
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl-Cで止めたときにエラー表示（トレースバック）を出さずに終了する
        print('\nThe server was stopped.')
