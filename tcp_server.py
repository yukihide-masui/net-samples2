# tcp_server.py for Python 3
#

import socket

SERVER_PORT = 50000  # 接続待ち受けポート番号
BUFSIZE = 1024  # 一度に受信を試みるバイト数


def main() -> None:
    # TCPを使う待ち受け用のソケットを作る
    #  with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # サーバを再起動したときにbind()が
        # 「Address already in use」で失敗するのを防ぐための設定。
        #  通信を終えた接続はしばらくOSの中に残る（TIME_WAIT状態）ため、
        #  この設定が無いと、サーバを止めた直後は同じポートを使えない。
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ポート番号をソケットに対応づける
        #  ホスト名に空文字列''を指定すると、この計算機が持つ全てのIPアドレス宛の
        #  接続を受け付ける。自分自身からの接続だけを受け付けたい場合は
        #  '127.0.0.1' を指定する。
        server_socket.bind(('', SERVER_PORT))

        # クライアントからの接続を待つ
        #  引数の1はaccept()がまだ呼ばれていない接続を
        #  何個まで保留しておくか（バックログ）を表す。
        server_socket.listen(1)
        print('The server is ready to receive')

        while True:
            # クライアントからの接続があったら、それを受け付け、
            # そのクライアントとの通信のためのソケットを作る
            connection_socket, addr = server_socket.accept()
            print(f'Connected from {addr}')

            # 通信用のソケットもwith構文で扱う（ブロックを抜けると自動的に閉じる）
            with connection_socket:
                # クライアントからバイト列を最大BUFSIZEバイト受信し、
                # 文字列に変換（decode()）する。
                #  ＜注意＞TCPはバイトの流れ（ストリーム）を運ぶ仕組みなので、
                #  相手が送ったデータが1回のrecv()で全部届く保証は無い。
                #  きちんとした受信のしかたは演習3（filetrans_*.py）で学ぶ。
                sentence = connection_socket.recv(BUFSIZE).decode()

                # 受け取った文字列を大文字に変換する
                capitalized_sentence = sentence.upper()

                # 大文字になった文字列をバイト列に変換して送信する。
                connection_socket.sendall(capitalized_sentence.encode())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl-Cで止めたときにエラー表示（トレースバック）を出さずに終了する
        print('\nThe server was stopped.')
