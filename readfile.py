# readfile.py

# ファイルをコピーする
#   このサンプルは、以下の処理の実装例を示しています。
#   - バイナリモードでファイルを読み込んで処理する。
#   - 決まった大きさのデータを読み込みながら、処理をする。
#   - ファイル全体を一度にまとめて読み込み、まとめて書き出す。
#
# 使い方:
#   python3 readfile.py コピー元 コピー先 [コピー方式]
#     コピー方式: with（省略時） / at_once / try
#
#   例: python3 readfile.py random_1M.dat copy.dat try

import sys

# 一度に読み書きするデータサイズ[バイト]
CHUNK_SIZE = 4096


# with 構文を使ったファイルの入出力の例
#  with 構文を使ってファイルをオープンすると、
#  close()を明示的に書かなくても、withのブロックの外側に処理が移った時点で
#  ファイルはクローズされます。
#  複数のファイルを扱うときは、カンマで区切って1つのwith文にまとめられます。
#
#  ＜よくある誤解＞
#  withが保証するのは「途中で例外が起きた場合でも確実にクローズされること」で、
#  例外そのものを処理してくれるわけではありません。
#  たとえばコピー元のファイルが存在しなければ、この関数はFileNotFoundErrorを
#  そのまま呼び出し元に送出します（下のcopy_file_try()と比べてみてください）。
#
#  なお、読み込み用のファイルを先に開いています。
#  書き込み用のファイルは開いた時点で中身が空にされてしまうので、
#  コピー元が開けないときにコピー先を壊さないようにするためです。
def copy_file_with(from_file_name: str, to_file_name: str) -> None:
    with open(from_file_name, 'rb') as f_in, open(to_file_name, 'wb') as f_out:
        while True:
            data = f_in.read(CHUNK_SIZE)
            if not data:  # 読み込めたデータが空ならファイルの終わり
                break
            f_out.write(data)


# withを使って入出力をするが、
# ファイル全体を一度に読み込んでコピーするバージョン
# 書くのはこちらの方がずっと簡単
# 大きなファイル（何十Mbyteもあるような）を扱うときは、
# それだけメモリも沢山使うので注意
def copy_file_with_at_once(from_file_name: str, to_file_name: str) -> None:
    with open(from_file_name, 'rb') as f_in, open(to_file_name, 'wb') as f_out:
        data = f_in.read()
        f_out.write(data)


# try〜except〜finallyを使って例外処理をするバージョン
# ファイルの読み書きは CHUNK_SIZEで指定したサイズ単位
#  ＜重要＞開いたファイルは、途中で例外が起きた場合でも必ず閉じる必要があります。
#  そのためにfinallyブロックを使います。
#  finallyの中身は、例外が起きても起きなくても必ず実行されます。
#  ……このように自分で書くと面倒なので、通常はwith構文を使います。
def copy_file_try(from_file_name: str, to_file_name: str) -> None:
    f_in = None
    f_out = None
    try:
        f_in = open(from_file_name, 'rb')
        f_out = open(to_file_name, 'wb')
        while True:
            data = f_in.read(CHUNK_SIZE)
            if not data:
                break
            f_out.write(data)
    except OSError as e:
        # OSErrorはファイル入出力の失敗を表す例外。
        #  （かつてIOErrorと呼ばれていたもの。Python 3.3以降は両者は同じもので、
        #    現在はOSErrorと書くのが普通）
        sys.exit(e)  # 例外の情報を表示して終了
    finally:
        # 例外が起きても起きなくても、開いたファイルを必ず閉じる。
        #  open()自体が失敗した場合は変数がNoneのままなので、それを確かめてから閉じる。
        if f_out is not None:
            f_out.close()
        if f_in is not None:
            f_in.close()


# 発展: 単にファイルをコピーするだけなら、標準ライブラリの
#       shutil.copyfile(コピー元, コピー先) を使うのが簡単です。

# コピー方式の名前と関数の対応表
COPY_METHODS = {
    'with': copy_file_with,
    'at_once': copy_file_with_at_once,
    'try': copy_file_try,
}


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(f'Usage: {sys.argv[0]} from_file_name to_file_name '
                 f'[{"|".join(COPY_METHODS)}]')

    from_file_name = sys.argv[1]
    to_file_name = sys.argv[2]
    method = sys.argv[3] if len(sys.argv) > 3 else 'with'

    if method not in COPY_METHODS:
        sys.exit(f'知らないコピー方式です: {method} '
                 f'（使えるのは {", ".join(COPY_METHODS)}）')

    COPY_METHODS[method](from_file_name, to_file_name)


if __name__ == '__main__':
    main()
