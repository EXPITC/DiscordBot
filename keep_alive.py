import time
import urllib.error
import urllib.request
from threading import Thread

from flask import Flask, send_from_directory

# def sleep(timeout, retry=3):
#     def the_real_decorator(function):
#         def wrapper(*args, **kwargs):
#             retries = 0
#             while retries < retry:
#                 try:
#                     value = function(*args, **kwargs)
#                     if value is None:
#                         return
#                 except:
#                     print(f'Sleeping for {timeout} seconds')
#                     time.sleep(timeout)
#                     retries += 1
#         return wrapper
#     return the_real_decorator

# @sleep(1)
# def uptime_bot(url):
#     try:
#         conn = urllib.request.urlopen(url)
#     except urllib.error.HTTPError as e:
#         # Email admin / log
#         print(f'HTTPError: {e.code} for {url}')
#         # Re-raise the exception for the decorator
#         raise urllib.error.HTTPError
#     except urllib.error.URLError as e:
#         # Email admin / log
#         print(f'URLError: {e.code} for {url}')
#         # Re-raise the exception for the decorator
#         raise urllib.error.URLError
#     else:
#         # Website is up
#         print(f'{url} is up')


url = [""]
loop = 0


def worker():
    global loop
    while True:
        try:
            # pass
            conn = urllib.request.urlopen(url[loop])
        except urllib.error.HTTPError as e:
            # Email admin / log
            print(f"HTTPError: {e.code} for {url[loop]}")
        except urllib.error.URLError as e:
            # Email admin / log
            print(f"URLError: {e.code} for {url[loop]}")
        else:
            # Website is up
            print(f"{url[loop]} is up")
        if loop == 0:
            loop = 1
        else:
            loop = 0
        time.sleep(60)


def main():
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(relativeCreated)6d %(threadName)s %(message)s"
    # )
    info = {"stop": False}
    thread = Thread(target=worker, args=(info,))
    thread_two = Thread(target=worker, args=(info,))
    thread.start()
    thread_two.start()

    while True:
        try:
            # logging.debug("Checking in from main thread")
            time.sleep(0.75)
        except KeyboardInterrupt:
            info["stop"] = True
            # logging.debug('Stopping')
            break
    thread.join()
    thread_two.join()


# print("IS THIS HIT??????")
app = Flask("")


@app.route("/")
def home():
    # print("HIT HOME?")
    return send_from_directory("", "hello.html")


def run():
    # print("hit this?")
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    w = Thread(target=worker)
    t.start()
    w.start()
    # uptime_bot(url)


# def uptime_bot(url):
#     while True:
#         try:
#             conn = urllib.request.urlopen(url)
#         except urllib.error.HTTPError as e:
#             # Email admin / log
#             print(f'HTTPError: {e.code} for {url}')
#         except urllib.error.URLError as e:
#             # Email admin / log
#             print(f'URLError: {e.code} for {url}')
#         else:
#             # Website is up
#             print(f'{url} is up')
#         time.sleep(60)

# if __name__ == '__main__':
#     url = 'http://www.google.com/py'
#     uptime_bot(url)
