# filetrans_client.py
#
# 決められたファイルの指定されたサイズまでを転送するシステムのクライアント

import socket
import sys

BUFSIZE = 4096  # 一度に受信処理するデータサイズ

FILE_NAME = 'received_data.dat'  # 受信した内容を書き込むファイルの名前
SERVER_NAME = 'localhost'
SERVER_PORT = 50001


# サーバとやりとりする処理。受信できたバイト数を返す。
def interact_with_server(s: socket.socket, size: int) -> int:
    # 要求メッセージを作る  例: '4096\n' ... 4096バイト要求
    #  末尾の改行が「ここまでが1つのメッセージ」という区切りの印になる。
    #  サーバ側は改行が現れるまで受信を繰り返す（filetrans_server.py を参照）。
    req_msg = f'{size:d}\n'

    # 要求メッセージの文字列をバイト列にして送信
    s.sendall(req_msg.encode())

    # 書き込み用ファイルをオープンして処理
    #   with 構文を使って書いているので、close()を書かなくても
    #   ブロックを抜けた時点でファイルはクローズされます。
    #   （途中で例外が起きた場合もクローズされます）
    received = 0
    with open(FILE_NAME, 'wb') as f:  # 'wb' は「バイナリファイルを書き込みモードで」という意味
        while True:
            data = s.recv(BUFSIZE)  # 最大BUFSIZEバイトずつ受信
            if not data:  # 空のバイト列が返るのは、相手からの送信が全て終了したということ
                break
            f.write(data)  # 受け取ったデータをファイルに書き込む
            received += len(data)

    return received


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f'Usage: {sys.argv[0]} size_in_bytes')

    # 発展: 引数が増えてきたら、標準ライブラリのargparseモジュールを使うと、
    #       使い方の表示や引数のエラー処理を自動で用意してくれる。
    try:
        size = int(sys.argv[1])
    except ValueError:
        sys.exit(f'サイズには数値を指定してください: {sys.argv[1]}')

    # ソケットを作ってサーバに接続
    #  with構文を使うと、ブロックを抜けるときに自動的にclose()される
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_NAME, SERVER_PORT))
        received = interact_with_server(s, size)  # サーバとのデータのやりとりは別関数に

    print(f'Received {received} bytes -> {FILE_NAME}')
    if received != size:
        # 要求したサイズと受信できたサイズが食い違ったら知らせる。
        #  （サーバ側のファイルが要求サイズより小さい場合などに起こる）
        print(f'注意: 要求したサイズ({size}バイト)と受信したサイズが異なります。')


if __name__ == '__main__':
    try:
        main()
    except ConnectionRefusedError:
        # サーバが起動していないときに出る例外
        sys.exit(f'サーバ({SERVER_NAME}:{SERVER_PORT})に接続できませんでした。'
                 'サーバは起動していますか？')
    except KeyboardInterrupt:
        print()
