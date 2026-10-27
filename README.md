# net_samples

このリポジトリには、ネットワークプログラミング学習のためのサンプルプログラムが格納されています。

## 動作環境

- Python 3.10 以降
- 追加のライブラリは不要です（標準ライブラリのみを使用しています）

各プログラムは次のように実行します。

```
python3 プログラム名.py
```

サーバとクライアントの組になっているものは、**先にサーバを起動**し、
別の端末（ターミナル）からクライアントを起動してください。
サーバは Ctrl-C で停止します。

## 第4回 演習2: TCPによる通信プログラム

- `tcp_server.py`
- `tcp_client.py`

```
# 端末1
python3 tcp_server.py

# 端末2
python3 tcp_client.py
```

## 第4回 演習3: ファイル転送プログラム〜大きなデータの送受信

- `filetrans_server.py`
- `filetrans_client.py`

あらかじめ、サーバが送信するファイル `random_1M.dat` を用意しておきます
（このファイル名は `filetrans_server.py` の `FILE_NAME` で指定されています）。

```
# 1MB（1048576バイト）のランダムなバイナリファイルを作る
head -c 1048576 /dev/urandom > random_1M.dat

# 端末1
python3 filetrans_server.py

# 端末2 （引数は要求するバイト数）
python3 filetrans_client.py 1048576
```

受信した内容は `received_data.dat` に保存されます。
正しく転送できたかは次のコマンドで確認できます（何も表示されなければ一致）。

```
cmp random_1M.dat received_data.dat
```

## 第4回 補足資料: 大きなファイルをバイナリモードで読み書きする方法について

- `readfile.py`

第3引数でコピー方式を選べます（省略時は `with`）。

```
python3 readfile.py random_1M.dat copy.dat with      # withで少しずつコピー
python3 readfile.py random_1M.dat copy.dat at_once   # withで一度にコピー
python3 readfile.py random_1M.dat copy.dat try       # try〜finallyでコピー
```

- 参考: ランダムなバイナリファイルを作る方法（例: 1MBのランダムバイナリファイルを作る）

```
head -c 1048576 /dev/urandom > random_file.bin
```

- 参考: ランダムなテキストファイルを作る方法（例: 1kBのランダムテキストファイルを作る）

```
tr -dc '0-9a-zA-Z' < /dev/urandom | head -c 1024 > random_text.txt
```

（macOS の `head` は `1M` のような単位付きの指定を受け付けないため、
バイト数で指定しています。）

## 第5回 演習1: マルチスレッドを使ったサーバプログラム/UDPの通信/時間計測

- `tcp_server_thread.py` — クライアントごとにスレッドを作って応対するサーバ
- `tcp_server_nothread.py` — スレッドを作らず1つずつ順番に応対するサーバ
- `udp_server.py`
- `udp_client.py`
- `time_test.py`

スレッドの効果は、サーバに2つのクライアントをほぼ同時に接続させると分かります。

```
# 端末1
python3 tcp_server_thread.py     # もしくは tcp_server_nothread.py

# 端末2・端末3 からそれぞれ
python3 tcp_client.py
```

スレッドを使う版では両方とも約15秒で応答が返りますが、
使わない版では2つめのクライアントは約30秒待たされます。

UDPのサンプルは次のように実行します。

```
# 端末1
python3 udp_server.py

# 端末2
python3 udp_client.py
```

サーバを起動せずにクライアントだけを実行すると、
5秒後にタイムアウトのメッセージが表示されます（UDPには再送の仕組みがないため）。
