import os
from subprocess import Popen, PIPE
import time

PIPE_PATH = "/tmp/my_pipe"

if not os.path.exists(PIPE_PATH):
    os.mkfifo(PIPE_PATH)

Popen(['xterm', '-e', 'tail', '-f', PIPE_PATH])
count = 0
while count != 0:
    with open(PIPE_PATH, "w") as p:
        count += 1
        p.write("Hello {}\n".format(count))
        time.sleep(1)
