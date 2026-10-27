# udp_client.py for Python 3
# トランスポート層にUDPを用いるクライアントプログラム

import socket
import sys

SERVER_NAME = 'localhost'
SERVER_PORT = 50004

# 一度に受信するバイト数
#  ＜注意＞UDPでは、これより大きなデータグラムが届くと、あふれた分は捨てられる。
BUFSIZE = 2048

TIMEOUT = 5.0  # 応答を待つ秒数


def main() -> None:
    # ソケット作成  socket()の第2引数はSOCK_DGRAM
    #  with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # 応答待ちの上限時間を設定する。
        #  ＜重要＞UDPには再送の仕組みが無いので、送ったパケットや
        #  返ってくるはずの応答が途中で失われると、応答は永久に返ってこない。
        #  この設定が無いと、プログラムはそこで待ち続けたままになってしまう。
        client_socket.settimeout(TIMEOUT)

        # 送信メッセージ入力
        message = input('Input lowercase sentence: ')

        # UDPの場合は、connect()をしなくて良い
        #  (TCPとは異なりコネクションを作らない）
        # サーバ名とポートを指定して、sendto()で送るだけ
        client_socket.sendto(message.encode(), (SERVER_NAME, SERVER_PORT))

        # 受信にはソケットのrecvfrom()を使う
        #  戻り値は受信データと送信元アドレスのタプル
        try:
            modified_message, server_address = client_socket.recvfrom(BUFSIZE)
        except TimeoutError:
            # settimeout()で指定した時間を過ぎても応答が無かった場合。
            #  （Python 3.9以前では socket.timeout という名前の例外）
            sys.exit(f'{TIMEOUT}秒待ちましたが応答がありませんでした。'
                     'サーバが起動していないか、パケットが失われた可能性があります。')

        print(modified_message.decode())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
