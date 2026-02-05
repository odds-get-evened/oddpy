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


class Feeder:
    """
    Represents a generic data supplier for the simulation.

    This class serves as a base for more specific simulation modules such
    as the potassium pump simulation.
    """
    
    def fetch_data(self):
        """
        Abstract method for data retrieval. Should be implemented by subclasses.
        
        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("fetch_data must be implemented by subclasses")


class PotassiumPumpFeeder(Feeder):
    """
    Simulates a potassium pump via the Goldman-Hodgkin-Katz (GHK) equation.
    """

    def __init__(self, k_in=140.0, k_out=5.0, membrane_potential=-70.0):
        """
        Initialize a potassium pump using the GHK equation parameters.
        
        Args:
            k_in (float): Intracellular concentration of potassium in mM.
            k_out (float): Extracellular concentration of potassium in mM.
            membrane_potential (float): Membrane potential in mV. Defaults to -70 mV.
        """
        self.k_in = k_in
        self.k_out = k_out
        self.membrane_potential = membrane_potential

    def calculate_ghk(self):
        """
        Calculate the ion flux using the GHK equation approximation.

        Returns:
            float: A value representing ion flux through the potassium pump.
        """
        # Constants used in GHK Equation
        F = 96485.3329  # Faraday's constant (C/mol)
        R = 8.314       # Universal gas constant (J/mol/K)
        T = 310.15      # Temperature in Kelvin (~37°C)

        # Calculate the exponent to avoid ValueError if the exponent is too large (e.g., very negative or very positive).
        exponent = -self.membrane_potential * F / (R * T)

        # Prevent overflow errors by clamping the exponent value
        if exponent < -700:
            exponent = -700  # Safeguard for very negative exponents (avoids math range error)
        if exponent > 700:
            exponent = 700  # Safeguard for very large positive exponents

        # GHK equation: Flux as a function of concentrations and potential
        numerator = self.k_out - self.k_in * math.exp(exponent)
        denominator = 1 - math.exp(exponent)
        flux = numerator / denominator if abs(denominator) > 1e-9 else 0  # Avoid division by zero

        return flux


class Heartbeat:
    """
    Represents a dynamic heartbeat movement powered by a fuel source and optionally
    enhanced by a potassium pump's influence.
    """

    def __init__(self, initial_fuel=10, increment=0.01, potassium_pump=None):
        """
        Initialize heartbeat with initial fuel and movement increment.
        
        Args:
            initial_fuel (float, optional): Starting fuel value. Higher values allow
                longer simulation runs. Defaults to 10.
            increment (float, optional): Base movement speed increment. Defaults to 0.01.
            potassium_pump: An optional PotassiumPumpFeeder instance to influence the heartbeat dynamics.
        """
        self.low_end = -1
        self.high_end = 1
        self.position = 0
        self.direction = 0  # 1 for up/right, 0 for down/left
        self.fuel = initial_fuel
        self.base_increment = increment
        self.potassium_pump = potassium_pump  # Optional potassium pump integration

    async def start(self):
        """
        Start the motorized heartbeat simulation with fuel dependency and dynamic movement.
        """
        start = random.uniform(-1, 1)
        threshold = random.uniform(0.3, 0.9)
        print(f"Initial start: {start:.4f}")
        print(f"Threshold: {threshold:.4f}")

        self.direction = 1 if start >= 0 else 0
        self.position = start
        self.low_end = max(-1, start - threshold)
        self.high_end = min(1, start + threshold)

        while self.fuel > 0:
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
            print(
                f"Direction: {'up' if self.direction else 'down'} @ {self.position:.4f}, "
                f"Speed: {increment:.4f}, Fuel: {self.fuel:.3f}, Flux: {flux:.6f}"
            )

            await asyncio.sleep(1)

        print("Out of fuel! Heartbeat stopped.")

    def dynamic_increment(self):
        """
        Compute the movement increment dynamically based on fuel level and environmental factors.

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


async def do_heartbeat(initial_fuel, increment, k_in, k_out, membrane_potential):
    """
    Run a heartbeat simulation instance.
    """
    pump = PotassiumPumpFeeder(k_in, k_out, membrane_potential)
    heartbeat = Heartbeat(initial_fuel=initial_fuel, increment=increment, potassium_pump=pump)
    await heartbeat.start()


def main():
    """
    Entry point to run the heartbeat simulation from the command line.

    This function ensures compatibility in both interactive and non-interactive
    environments by explicitly creating the event loop.
    """
    parser = argparse.ArgumentParser(description="Run the Heartbeat Simulation with Potassium Pump dynamics.")
    parser.add_argument("--fuel", type=float, default=10, help="Initial fuel level")
    parser.add_argument("--increment", type=float, default=0.01, help="Base movement speed increment")
    parser.add_argument("--k_in", type=float, default=140.0, help="Intracellular potassium concentration (mM)")
    parser.add_argument("--k_out", type=float, default=5.0, help="Extracellular potassium concentration (mM)")
    parser.add_argument("--mem_pot", type=float, default=-70, help="Membrane potential (mV)")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(do_heartbeat(
            args.fuel, args.increment, args.k_in, args.k_out, args.mem_pot
        ))
    except KeyboardInterrupt:
        print("\nSimulation interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
