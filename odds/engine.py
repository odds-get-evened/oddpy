import asyncio
import math
import random
import sys
from io import BytesIO


def sigmoid(x):
    return 1.0 / (1 + (math.e ** -x))


def relu(x):
    return x * (x > 0)


def leaky_relu(x, alpha=0.01):
    return max(alpha * x, x)


def tanh(x):
    return math.tanh(x)


def softmax(x):
    ex = []
    [ex.append(math.exp(y)) for y in x]
    t = sum(ex)

    ex = [ex[i] / t for i in range(len(ex))]

    return ex


class Heartbeat:
    """
    idea: use math to determine divisor of any given number between 0 and 9 maybe
    0, 1, 2 correspond to x, y, z movement
    """

    def __init__(self, increment=0.01):
        """
        how much to increment the position
        :param increment:
        """
        # 1 is up/right and 0 is down/left
        self.low_end = -1
        self.high_end = 1
        self.direction = 0
        self.position = 0
        self.increment = increment

        asyncio.run(self.start())

    async def start(self):
        start = random.uniform(-1, 1)
        threshold = random.uniform(0, 0.9)
        print(f"start: {start}")
        print(f"threshold: {threshold}")

        self.direction = 1 if start >= 0 else 0
        self.position = start

        low_end = start - threshold
        high_end = start + threshold
        print(f"low {low_end} - high {high_end}", end="\n\n")
        print("#################################", end="\n\n")

        # offset thresholds so that direction is changed before hitting them
        self.low_end = low_end if low_end > -1 else -1 + self.increment
        self.high_end = high_end if high_end < 1 else 1 - self.increment

        while True:
            # positioning
            if self.position <= low_end:
                self.direction = 1

            if self.position >= high_end:
                self.direction = 0

            # direction based on position
            if self.direction == 1:
                self.position += self.optimized_increment()
            else:
                self.position -= self.optimized_increment()

            print(f"direction {'up' if self.direction == 1 else 'down'} @ {self.position} w/pace {self.increment}")

            await asyncio.sleep(2)

    def optimized_increment(self):
        # determine if we are moving down or up and get delta from low or high, dependent on what we're nearing
        delta = self.position - self.low_end if self.direction == 0 else self.high_end - self.position

        return self.increment


class Feeder:
    def __init__(self, init_data=b"", run_forever=True):
        self.signing_key = None
        self.feed = BytesIO(init_data)

        if run_forever:
            asyncio.run(self.run_forever())
        else:
            self.run_once()

        self.feed.close()

    async def run_forever(self):
        input_task = asyncio.create_task(self.handle_in())
        feed_task = asyncio.create_task(self.handle_out())

        await asyncio.gather(input_task, feed_task)

    def run_once(self):
        pass

    async def handle_in(self):
        while True:
            user_input = input("> ")
            in_len = len(self.feed.getvalue())
            self.feed.seek(in_len)  # seek to end of stream
            self.feed.write((" " + user_input).encode())

            await asyncio.sleep(0.1)

    async def handle_out(self):
        while True:
            chunk = self.feed.getvalue()
            print(chunk)
            await asyncio.sleep(0.1)


def do_heartbeat():
    try:
        Heartbeat(increment=0.1)
    except KeyboardInterrupt:
        sys.exit(0)


def do_enginio():
    engio = Feeder(init_data=b"hello, world =)", run_forever=True)


def main():
    # do_enginio()

    '''
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key = kdf.derive(b"test")
    based_key = base64.urlsafe_b64encode(key)
    print(f"base64 key: {based_key}")
    f = Fernet(based_key)
    token = f.encrypt(b"secret message")
    print(f"secret message: {token}")
    print(f"decrypted message: {f.decrypt(token)}")
    '''

    do_heartbeat()
    '''lin = np.linspace(-1, 1, 10)
    print(lin)
    lin = np.pad(lin, len(lin) + 8, mode='constant')
    print(lin)'''


if __name__ == "__main__":
    main()
