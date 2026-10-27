# filetrans_server.py
#
# 決められたファイルの指定されたサイズまでを転送するシステムのサーバ
#

import socket

BUFSIZE = 4096  # 一度に読み込み・送信処理するデータサイズ

FILE_NAME = 'random_1M.dat'  # 読み出すファイルの名前
SERVER_PORT = 50001
MAX_REQUEST_SIZE = 1024  # 要求メッセージの長さの上限[バイト]


# 要求メッセージ（末尾が改行）を1行受信する
#  ＜重要＞TCPはバイトの流れ（ストリーム）を運ぶ仕組みで、
#  「メッセージの切れ目」という考え方を持たない。
#  相手が1回のsendall()で送ったデータが、こちらでは複数回のrecv()に分かれて
#  届くこともあれば、複数回に分けて送られたデータが1回のrecv()で
#  まとめて届くこともある。
#  そのため「どこまでが1つのメッセージか」はアプリケーション側で決める必要がある。
#  ここでは「改行まで」を1つのメッセージと決め、改行が現れるまで受信を繰り返す。
def receive_request_line(s: socket.socket) -> str:
    buffer = b''
    while b'\n' not in buffer:
        data = s.recv(BUFSIZE)
        if not data:  # 空のバイト列が返るのは、相手がソケットを閉じたということ
            raise ValueError('要求メッセージが届く前に接続が切れました')
        buffer += data
        if len(buffer) > MAX_REQUEST_SIZE:
            # いつまでも改行が来ない相手に付き合ってメモリを使い切らないようにする
            raise ValueError('要求メッセージが長すぎます')

    # 最初の改行までを取り出して文字列にする
    line, _separator, _rest = buffer.partition(b'\n')
    return line.decode()


# クライアントとやりとりする処理
def interact_with_client(s: socket.socket) -> None:
    req_msg = receive_request_line(s)

    # 最初の空白文字までに書かれているのがサイズなのでそれを解釈する
    fields = req_msg.split()
    if not fields:
        raise ValueError('要求メッセージが空です')
    send_size = int(fields[0])  # 数字でなければValueErrorが送出される
    if send_size < 0:
        raise ValueError(f'サイズに負の値が指定されました: {send_size}')

    # ファイルを少しずつ読みながら、読んだ分だけ送信する
    #   ファイル全体を一度にメモリへ読み込むと、大きなファイルを扱うときに
    #   それだけ大量のメモリを使ってしまうので、BUFSIZEずつ処理する。
    #   （readfile.py の copy_file_with() と同じ考え方）
    #
    #   with 構文を使って書いているので、close()を書かなくても
    #   ブロックを抜けた時点でファイルはクローズされます。
    #   （途中で例外が起きた場合もクローズされます。ただし例外そのものは
    #     withでは処理されないので、下のmain()の中で受け止めています）
    remaining = send_size
    with open(FILE_NAME, 'rb') as f:  # 'rb'は「バイナリファイルを読み込みモードで」の意味
        while remaining > 0:
            data = f.read(min(BUFSIZE, remaining))
            if not data:  # ファイルの終わりに達した（要求サイズよりファイルが小さい）
                break

            s.sendall(data)
            remaining -= len(data)

    print(f'Sent {send_size - remaining} bytes')


# メインルーチン
def main() -> None:
    # 待ち受け用ソケットを作ってポートに関連付け、待ち受けを開始
    #  with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # サーバを再起動したときにbind()が
        # 「Address already in use」で失敗するのを防ぐための設定
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', SERVER_PORT))
        server_socket.listen(1)
        print('The server is ready to receive')

        while True:
            # 接続されたら、そのクライアントとのソケットを作って、クライアントと通信する
            s, addr = server_socket.accept()
            print(f'Connected from {addr}')
            with s:
                try:
                    interact_with_client(s)  # クライアントとの処理は別関数にて
                except (ValueError, OSError) as e:
                    # 1つのクライアントの処理で問題が起きても（変な要求が来た、
                    # 送るファイルが無い、など）、サーバ全体は止めずに次の接続を待つ。
                    #  OSErrorはファイル入出力や通信の失敗を表す例外。
                    print(f'Error: {e}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl-Cで止めたときにエラー表示（トレースバック）を出さずに終了する
        print('\nThe server was stopped.')
