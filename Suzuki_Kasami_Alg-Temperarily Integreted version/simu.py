import threading
import time


class TestThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.switch = False

    def run(self):

        while True:

            if not self.switch:
                print("running")
                print(self.switch)
                time.sleep(1)

    def change(self):
        self.switch = not self.switch
        print("change")


if __name__ == '__main__':

    ts = TestThread()
    ts.start()

    while True:
        inp = input()

        if inp == "":
            print("ch")
            ts.change()