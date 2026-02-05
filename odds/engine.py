"""
Engine module for oddpy.

This module provides a dynamic heartbeat simulation powered by a fuel source.
It demonstrates concepts such as:
- Dynamic movement controlled by fuel levels
- Environmental factors affecting speed and direction
- Mathematical functions (sigmoid and ReLU) for non-linear dynamics
- Asynchronous programming using Python's asyncio module

Classes:
    Heartbeat: A dynamic heartbeat movement simulator with fuel-based dynamics.
    Feeder: A real-time data supplier simulator (experimental).

Functions:
    sigmoid(x): Sigmoid activation function.
    relu(x): ReLU activation function.
    do_heartbeat(): Run a heartbeat simulation instance.
    main(): Entry point for command-line execution.
"""

import argparse
import asyncio
import math
import random
import sys
from io import BytesIO

def sigmoid(x):
    """
    Sigmoid activation function to map values to a range of 0 to 1.
    
    The sigmoid function is used to normalize values and create smooth transitions.
    It's particularly useful for modeling fuel efficiency in the heartbeat simulation.
    
    Args:
        x (float): Input value to transform.
    
    Returns:
        float: Output value in range (0, 1).
    
    Example:
        >>> sigmoid(0)
        0.5
        >>> sigmoid(5)
        0.9933...
    """
    return 1.0 / (1 + (math.e ** -x))

def relu(x):
    """
    ReLU (Rectified Linear Unit) activation function.
    
    Used to model resistance or amplification effects in the environment.
    Returns the input if positive, otherwise returns 0.
    
    Args:
        x (float): Input value to transform.
    
    Returns:
        float: max(0, x) - the input value if positive, otherwise 0.
    
    Example:
        >>> relu(5)
        5
        >>> relu(-3)
        0
    """
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
        
        The heartbeat simulation starts automatically upon initialization and runs
        until the fuel is depleted. The simulation uses asyncio for time-based updates.
        
        Args:
            initial_fuel (float, optional): Starting fuel value. Higher values allow
                longer simulation runs. Defaults to 10.
            increment (float, optional): Base movement speed increment. Controls how
                fast the heartbeat position changes. Defaults to 0.01.
        
        Raises:
            KeyboardInterrupt: Can be raised to stop the simulation early.
        
        Example:
            >>> heartbeat = Heartbeat(initial_fuel=20, increment=0.05)
            Initial start: 0.5432
            Threshold: 0.7821
            ...
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
        Start the motorized heartbeat simulation with fuel dependency and dynamic movement.
        
        This async method runs the main simulation loop. It:
        1. Initializes a random starting position and movement threshold
        2. Oscillates position between calculated bounds
        3. Consumes fuel with each movement cycle
        4. Adjusts speed based on fuel levels and environmental factors
        5. Stops when fuel is depleted
        
        The simulation outputs status information at each step, including direction,
        position, speed, and remaining fuel.
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
        Compute the movement increment dynamically based on fuel and environment.
        
        The increment (speed) is calculated using:
        1. Fuel efficiency: Sigmoid function normalized around fuel level 5
        2. Environmental factor: ReLU applied to sine of current position
        3. Combined effect: base_increment * fuel_efficiency * (1 - environment_factor)
        
        This creates realistic speed variations where:
        - Movement is most efficient at moderate fuel levels
        - Environmental resistance varies with position
        - Speed never drops below a minimum threshold (0.001)
        
        Returns:
            float: The calculated movement increment (speed) for this cycle.
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
    """
    Experimental data feed simulator.
    
    This class mimics a real-time data supplier that could be used for various
    purposes such as user input processing or computational work simulation.
    Currently in experimental stage.
    
    Attributes:
        feed (BytesIO): Internal byte stream for data storage.
    """
    
    def __init__(self, init_data=b"", run_forever=True):
        """
        Initialize the Feeder with optional initial data.
        
        Args:
            init_data (bytes, optional): Initial data for the feed. Defaults to b"".
            run_forever (bool, optional): If True, runs the feed continuously using
                asyncio. If False, runs once (currently not fully implemented).
                Defaults to True.
        
        Note:
            This class is experimental and not currently used in the main heartbeat
            simulation. It demonstrates concepts for future enhancement.
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
        
        Creates two concurrent tasks:
        1. handle_in(): Accepts user input
        2. handle_out(): Outputs feed content
        
        Both tasks run indefinitely until interrupted.
        """
        input_task = asyncio.create_task(self.handle_in())
        feed_task = asyncio.create_task(self.handle_out())

        await asyncio.gather(input_task, feed_task)  # Run both tasks concurrently

    def run_once(self):
        """
        Execute a single run sequence.
        
        Note:
            This method is currently not implemented and serves as a placeholder
            for future functionality.
        """
        pass

    async def handle_in(self):
        """
        Continuously accept user input and append it to the feed.
        
        Prompts the user with "> " and appends their input to the internal
        BytesIO feed. Runs indefinitely in an async loop with a small delay
        between iterations.
        """
        while True:
            user_input = input("> ")  # Prompt user for input
            in_len = len(self.feed.getvalue())
            self.feed.seek(in_len)  # Seek to end of the current feed
            self.feed.write((" " + user_input).encode())  # Append user input to feed

            await asyncio.sleep(0.1)  # Simulate slight processing delay

    async def handle_out(self):
        """
        Continuously output the current feed content for demonstration.
        
        Retrieves and prints the entire feed content at regular intervals.
        Runs indefinitely in an async loop with a small delay between iterations.
        """
        while True:
            chunk = self.feed.getvalue()  # Retrieve feed content
            print(chunk)  # Output the content
            await asyncio.sleep(0.1)  # Simulate slight processing delay


def do_heartbeat(initial_fuel=10, increment=0.05):
    """
    Run an instance of the heartbeat simulation with fuel-enabled dynamics.
    
    This function creates and runs a Heartbeat instance with the specified parameters.
    The simulation can be interrupted with Ctrl+C (KeyboardInterrupt).
    
    Args:
        initial_fuel (float, optional): Starting fuel value for the simulation.
            Defaults to 10.
        increment (float, optional): Base movement speed increment. Defaults to 0.05.
    
    Raises:
        KeyboardInterrupt: Caught and handled gracefully to exit the simulation.
    
    Example:
        >>> do_heartbeat(initial_fuel=20, increment=0.1)
        Initial start: 0.3245
        Threshold: 0.8123
        ...
    """
    try:
        Heartbeat(initial_fuel=initial_fuel, increment=increment)
    except KeyboardInterrupt:
        print("\nHeartbeat interrupted.")
        sys.exit(0)


def main():
    """
    Main entry point for command-line execution of the heartbeat simulation.
    
    Parses command-line arguments and runs the heartbeat simulation with the
    specified parameters. If no arguments are provided, uses default values.
    
    Command-line Arguments:
        --initial-fuel: Starting fuel value (default: 10)
        --increment: Base movement speed increment (default: 0.05)
    
    Example:
        $ python engine.py --initial-fuel 20 --increment 0.1
        $ python engine.py --help
    """
    parser = argparse.ArgumentParser(
        description='Run a dynamic heartbeat simulation powered by fuel.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python engine.py
  python engine.py --initial-fuel 20
  python engine.py --initial-fuel 15 --increment 0.1
  
The simulation will run until fuel is depleted or interrupted with Ctrl+C.
        """
    )
    
    parser.add_argument(
        '--initial-fuel',
        type=float,
        default=10,
        help='Starting fuel value for the heartbeat simulation (default: 10)'
    )
    
    parser.add_argument(
        '--increment',
        type=float,
        default=0.05,
        help='Base movement speed increment (default: 0.05)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.initial_fuel <= 0:
        parser.error("initial-fuel must be greater than 0")
    
    if args.increment <= 0:
        parser.error("increment must be greater than 0")
    
    do_heartbeat(initial_fuel=args.initial_fuel, increment=args.increment)


if __name__ == "__main__":
    main()