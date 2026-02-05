"""
Engine module for oddpy.

This module provides a dynamic heartbeat simulation powered by a fuel source and additionally integrates
a potassium pump simulation powered by the Goldman-Hodgkin-Katz (GHK) Equation.

It demonstrates concepts such as:
- Dynamic movement controlled by fuel levels
- Environmental factors affecting speed and direction
- Mathematical functions (sigmoid and ReLU) for non-linear dynamics
- Asynchronous programming using Python's asyncio module
- Biological modeling of ion transport via a potassium pump

Classes:
    Heartbeat: A dynamic heartbeat movement simulator with fuel-based and potassium pump dynamics.
    Feeder: A real-time data supplier simulator (experimental).
    PotassiumPumpFeeder: A subclass of Feeder that simulates a potassium pump using GHK equation.

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
    return 1.0 / (1 + math.exp(-x))


def relu(x):
    """
    ReLU (Rectified Linear Unit) activation function.
    
    Used to model resistance or amplification effects in the environment. Returns
    the input if positive or zero.
    
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
    Represents a dynamic heartbeat movement powered by a fuel source and optionally
    enhanced by a potassium pump's influence.
    """

    def __init__(self, initial_fuel=10, increment=0.01, potassium_pump=None):
        """
        Initialize heartbeat with initial fuel and movement increment.
        
        The heartbeat simulation starts automatically upon initialization and runs
        until the fuel is depleted. The simulation uses asyncio for time-based updates.

        Args:
            initial_fuel (float, optional): Starting fuel value. Higher values allow
                longer simulation runs. Defaults to 10.
            increment (float, optional): Base movement speed increment. Controls how
                fast the heartbeat position changes. Defaults to 0.01.
            potassium_pump (PotassiumPumpFeeder, optional): An instance of PotassiumPumpFeeder
                to influence the heartbeat dynamics. Defaults to None.
        """
        self.low_end = -1
        self.high_end = 1
        self.position = 0
        self.direction = 0  # 1 for up/right, 0 for down/left
        self.fuel = initial_fuel
        self.base_increment = increment
        self.potassium_pump = potassium_pump  # Optional potassium pump integration
        
        asyncio.run(self.start())

    async def start(self):
        """
        Start the motorized heartbeat simulation with fuel dependency and dynamic movement.

        This async method runs the main simulation loop. It:
        1. Initializes a random starting position and movement threshold
        2. Oscillates position between calculated bounds
        3. Consumes fuel with each movement cycle
        4. Adjusts speed based on fuel levels and optional potassium pump influence
        5. Stops when fuel is depleted
        """
        start = random.uniform(-1, 1)  # Random initial position
        threshold = random.uniform(0.3, 0.9)  # Random movement range threshold
        print(f"Initial start: {start:.4f}")
        print(f"Threshold: {threshold:.4f}")

        self.direction = 1 if start >= 0 else 0  # Initial direction
        self.position = start
        self.low_end = max(-1, start - threshold)
        self.high_end = min(1, start + threshold)

        while self.fuel > 0:  # Continue as long as there's fuel
            # Update direction
            if self.position <= self.low_end:
                self.direction = 1
            if self.position >= self.high_end:
                self.direction = 0

            # Calculate increment
            increment = self.dynamic_increment()

            # Update position
            self.position += increment if self.direction == 1 else -increment

            # Burn fuel
            self.fuel -= sigmoid(increment) * 0.1

            # Log state
            flux = self.potassium_pump.calculate_ghk() if self.potassium_pump else 0
            print(f"Direction: {'up' if self.direction else 'down'} @ {self.position:.4f}, Speed: {increment:.4f}, "
                  f"Fuel: {self.fuel:.3f}, Flux: {flux:.6f}")

            await asyncio.sleep(1)  # Delay for the effect

        print("Out of fuel! Heartbeat stopped.")

    def dynamic_increment(self):
        """
        Compute the movement increment dynamically based on fuel level and environmental factors.

        If a potassium pump is integrated, its ion flux (calculated from GHK equation) is factored into
        the increment computation to reflect a biological influence.

        Returns:
            float: The calculated movement increment.
        """
        fuel_efficiency = sigmoid(self.fuel - 5)
        environment_factor = relu(math.sin(self.position))  # Environment-based resistance

        increment = self.base_increment * fuel_efficiency * (1 - environment_factor)

        if self.potassium_pump:
            flux = self.potassium_pump.calculate_ghk()
            increment *= 1 + flux  # Increase or decrease speed based on flux effect

        return max(0.001, increment)
