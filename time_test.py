# time_test.py for Python 3  - スリープ前後で時刻を記録し、経過時間（秒）を表示。
#
import time

# ＜経過時間の測り方＞
#  time.time() は「1970年1月1日からの経過秒数」（いわゆるUNIX時刻）を返す関数で、
#  「今が何年何月何日の何時何分か」を知りたいときに使う。
#  しかしこの値は、NTPによる時刻合わせや利用者による時計の変更で
#  飛んだり巻き戻ったりすることがあるため、
#  「ある処理に何秒かかったか」を測る用途には向かない。
#
#  経過時間の計測には time.perf_counter() を使う。
#  これは必ず増加する（巻き戻らない）高分解能のカウンタの値を返す。
#  返る値そのものには意味が無く、2つの値の差だけに意味がある。


def main() -> None:
    start_time = time.perf_counter()

    time.sleep(3.75)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # start_time, end_time の値自体には意味が無いので、差だけを見ること
    print(f'Start: {start_time:.6f}, End: {end_time:.6f}, '
          f'Elapsed: {elapsed_time:.6f} seconds')


if __name__ == '__main__':
    main()
