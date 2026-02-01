import asyncio
import math
import random
import sys
from io import BytesIO

def sigmoid(x):
    """ Sigmoid function to map values to a range of 0 to 1 """
    return 1.0 / (1 + (math.e ** -x))

def relu(x):
    """ ReLU function to model resistance or amplification """
    return max(0, x)

class Heartbeat:
    """
    Represents a dynamic heartbeat movement powered by a fuel source.
    The movement speed is controlled by the amount of fuel available
    and affected non-linearly by environmental factors.
    """

    def __init__(self, initial_fuel=10, increment=0.01):
        """
        Initialize heartbeat with initial fuel and movement increment.
        :param initial_fuel: starting fuel value.
        :param increment: base movement increment.
        """
        # Define position and movement range
        self.low_end = -1
        self.high_end = 1
        self.position = 0
        self.direction = 0  # 1 for up/right, 0 for down/left

        # Properties affecting movement dynamics
        self.fuel = initial_fuel  # initial fuel value
        self.base_increment = increment  # base speed increment
        
        asyncio.run(self.start())

    async def start(self):
        """
        Start motorized heartbeat simulation with fuel dependency and dynamic movement.
        """
        start = random.uniform(-1, 1)  # Random initial position
        threshold = random.uniform(0.3, 0.9)  # Random movement range threshold
        
        print(f"Initial start: {start}")
        print(f"Threshold: {threshold}")

        self.direction = 1 if start >= 0 else 0  # Initial direction
        self.position = start

        low_end = start - threshold
        high_end = start + threshold

        # Setting movement bounds with offset thresholds
        self.low_end = low_end if low_end > -1 else -1 + self.base_increment
        self.high_end = high_end if high_end < 1 else 1 - self.base_increment

        while self.fuel > 0:  # Continue as long as there's fuel
            # Adjust direction based on position bounds
            if self.position <= self.low_end:
                self.direction = 1

            if self.position >= self.high_end:
                self.direction = 0

            # Determine dynamic increment based on fuel and environmental factors
            increment = self.dynamic_increment()

            # Update position value based on direction and dynamic increment
            if self.direction == 1:
                self.position += increment
            else:
                self.position -= increment

            # Consume fuel each cycle based on movement increment
            self.fuel -= sigmoid(increment) * 0.1  # Fuel burns slower on small increments

            # Log the current status
            print(f"Direction: {'up' if self.direction == 1 else 'down'} @ {self.position:.4f}, Speed: {increment:.4f}, Fuel: {self.fuel:.4f}")

            await asyncio.sleep(2)  # Simulate time delay between movements

        print("Out of fuel! Heartbeat stopped.")

    def dynamic_increment(self):
        """
        Compute the increment dynamically based on fuel efficiency and environmental factors.
        """
        # Normalize fuel to determine efficiency with sigmoid
        fuel_efficiency = sigmoid(self.fuel - 5)  # Efficient at moderate fuel levels

        # Environmental influence (e.g., resistance based on position)
        environment_factor = relu(math.sin(self.position))

        # Effective increment combines base increment, fuel, and environment
        effective_increment = self.base_increment * fuel_efficiency * (1 - environment_factor)

        # Ensure increment is not negative or zero
        return max(0.001, effective_increment)

class Feeder:
    def __init__(self, init_data=b", run_forever=True):
        """
        Feeder mimics a real-time data supplier (e.g., user input or computational work).
        It can simulate input data that, in our current system, might be used to fuel the heartbeat.
        :param init_data: Initial data for the feed (e.g., bytes).
        :param run_forever: Determines if the feed runs continuously.
        """
        self.feed = BytesIO(init_data)  # Initializes input stream

        if run_forever:
            asyncio.run(self.run_forever())
        else:
            self.run_once()

        self.feed.close()  # Close feed after usage

    async def run_forever(self):
        """
        Run the input/output handlers repeatedly in asynchronous tasks.
        """
        input_task = asyncio.create_task(self.handle_in())
        feed_task = asyncio.create_task(self.handle_out())

        await asyncio.gather(input_task, feed_task)  # Run both tasks concurrently

    def run_once(self):
        """
        Method for single run sequence (currently not implemented).
        """
        pass

    async def handle_in(self):
        """
        Continuously accept user input as input to the feed.
        """
        while True:
            user_input = input("> ")  # Prompt user for input
            in_len = len(self.feed.getvalue())
            self.feed.seek(in_len)  # Seek to end of the current feed
            self.feed.write((" " + user_input).encode())  # Append user input to feed

            await asyncio.sleep(0.1)  # Simulate slight processing delay

    async def handle_out(self):
        """
        Continuously output the current feed value for demonstration purposes.
        """
        while True:
            chunk = self.feed.getvalue()  # Retrieve feed content
            print(chunk)  # Output the content
            await asyncio.sleep(0.1)  # Simulate slight processing delay


def do_heartbeat():
    """
    Run an instance of the heartbeat simulation with fuel-enabled dynamics.
    """
    try:
        Heartbeat(initial_fuel=10, increment=0.05)
    except KeyboardInterrupt:
        print("Heartbeat interrupted.")
        sys.exit(0)


def main():
    """
    Main function to execute the Heartbeat.
    """
    do_heartbeat()


if __name__ == "__main__":
    main()