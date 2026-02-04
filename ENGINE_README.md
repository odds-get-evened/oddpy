# Engine Module - User Guide

## Overview

The `engine.py` module is the core simulation component of oddpy. It implements a dynamic heartbeat simulation powered by a fuel-based system. The simulation demonstrates advanced concepts including:

- **Dynamic Movement**: Position oscillates within a bounded range based on available fuel
- **Fuel Dynamics**: Fuel consumption affects speed using sigmoid functions for realistic efficiency curves
- **Environmental Factors**: Simulated resistance/amplification using mathematical functions (ReLU applied to sine waves)
- **Asynchronous Programming**: Utilizes Python's `asyncio` for time-based updates

The heartbeat simulation runs continuously until the fuel is depleted, with real-time status updates showing position, direction, speed, and remaining fuel.

---

## Installation

### Prerequisites

- Python 3.8 or higher (Python 3.12+ recommended)
- No external dependencies required (uses Python standard library only)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/odds-get-evened/oddpy.git
   cd oddpy
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate     # On Windows
   ```

3. Install the package (optional):
   ```bash
   pip install -e .
   ```

---

## Usage

### Running from Command Line

#### Basic Usage

Run the heartbeat simulation with default parameters:

```bash
python odds/engine.py
```

Or if installed as a package:

```bash
python -m odds.engine
```

#### With Custom Parameters

Customize the simulation using command-line arguments:

```bash
# Set initial fuel to 20
python odds/engine.py --initial-fuel 20

# Set both initial fuel and increment
python odds/engine.py --initial-fuel 15 --increment 0.1

# Lower fuel for shorter simulation
python odds/engine.py --initial-fuel 5 --increment 0.02
```

#### Getting Help

View all available options:

```bash
python odds/engine.py --help
```

### Using as a Python Module

You can also import and use the engine components in your own Python code:

```python
from odds.engine import Heartbeat, sigmoid, relu

# Create a heartbeat simulation with custom parameters
heartbeat = Heartbeat(initial_fuel=20, increment=0.1)

# The simulation starts automatically and runs until fuel is depleted
```

---

## Command-Line Arguments

### `--initial-fuel`

- **Type**: Float
- **Default**: 10
- **Description**: Sets the starting fuel value for the simulation. Higher values result in longer-running simulations.
- **Valid Range**: Must be greater than 0
- **Example**: `--initial-fuel 25`

### `--increment`

- **Type**: Float  
- **Default**: 0.05
- **Description**: Sets the base movement speed increment. This controls how fast the heartbeat position changes. Higher values mean faster movement.
- **Valid Range**: Must be greater than 0
- **Example**: `--increment 0.1`

---

## Understanding the Simulation

### Heartbeat Class

The `Heartbeat` class is the main simulation component. When initialized, it:

1. Sets a random starting position between -1 and 1
2. Calculates movement bounds based on a random threshold
3. Begins oscillating within those bounds
4. Consumes fuel with each movement cycle
5. Adjusts speed dynamically based on fuel levels and environmental factors
6. Stops when fuel is depleted

### Key Concepts

#### Fuel Efficiency

The simulation uses a sigmoid function to model fuel efficiency:
- Most efficient at moderate fuel levels (around 5)
- Less efficient at very high or very low fuel levels
- Fuel consumption is proportional to movement speed

#### Environmental Resistance

Environmental factors affect movement speed:
- Resistance varies with position using `ReLU(sin(position))`
- Creates realistic speed variations during the simulation
- Simulates real-world physical constraints

#### Dynamic Speed

The actual movement speed at each step is calculated as:
```
speed = base_increment × fuel_efficiency × (1 - environment_factor)
```

This ensures the simulation never stalls completely (minimum speed: 0.001).

### Simulation Output

The simulation outputs status information every 2 seconds:

```
Initial start: 0.3245
Threshold: 0.6789
Direction: up @ 0.3345, Speed: 0.0450, Fuel: 9.9850
Direction: up @ 0.3795, Speed: 0.0449, Fuel: 9.9701
Direction: up @ 0.4243, Speed: 0.0448, Fuel: 9.9551
...
Direction: down @ 0.2156, Speed: 0.0021, Fuel: 0.0034
Out of fuel! Heartbeat stopped.
```

Each line shows:
- **Direction**: "up" (moving toward high_end) or "down" (moving toward low_end)
- **Position**: Current position value (between low_end and high_end)
- **Speed**: Current movement increment (affected by fuel and environment)
- **Fuel**: Remaining fuel value

---

## Examples

### Example 1: Quick Simulation

For a short test run:

```bash
python odds/engine.py --initial-fuel 3 --increment 0.05
```

This will run for approximately 30-60 seconds.

### Example 2: Extended Simulation

For a longer observation period:

```bash
python odds/engine.py --initial-fuel 50 --increment 0.02
```

This could run for several minutes depending on environmental factors.

### Example 3: Fast-Paced Simulation

For rapid movement and quick fuel consumption:

```bash
python odds/engine.py --initial-fuel 10 --increment 0.2
```

This creates dramatic speed changes and faster fuel depletion.

### Example 4: Using in Python Code

```python
from odds.engine import Heartbeat

# Custom simulation
try:
    simulation = Heartbeat(initial_fuel=15, increment=0.08)
except KeyboardInterrupt:
    print("\nSimulation stopped by user")
```

---

## Stopping the Simulation

To stop the simulation before fuel is depleted:

- Press `Ctrl+C` (or `Cmd+C` on macOS)
- The program will catch the interrupt and exit gracefully

---

## Troubleshooting

### Issue: "SyntaxError" when running

**Solution**: Ensure you're using Python 3.8 or higher:
```bash
python3 --version
```

### Issue: "ModuleNotFoundError: No module named 'odds'"

**Solution**: Run from the repository root directory or install the package:
```bash
cd /path/to/oddpy
python odds/engine.py
```

### Issue: Simulation runs too quickly/slowly

**Solution**: Adjust the `--increment` parameter:
- For slower: Use smaller values (e.g., `--increment 0.01`)
- For faster: Use larger values (e.g., `--increment 0.1`)

### Issue: Simulation ends too quickly

**Solution**: Increase the initial fuel:
```bash
python odds/engine.py --initial-fuel 30
```

### Issue: Invalid argument values

**Solution**: Ensure both `--initial-fuel` and `--increment` are positive numbers:
```bash
# This will fail:
python odds/engine.py --initial-fuel -5

# This will work:
python odds/engine.py --initial-fuel 5
```

---

## Technical Details

### Mathematical Functions

#### Sigmoid Function

```python
def sigmoid(x):
    return 1.0 / (1 + (math.e ** -x))
```

Maps any input to a value between 0 and 1. Used for fuel efficiency calculations.

#### ReLU Function

```python
def relu(x):
    return max(0, x)
```

Returns the input if positive, otherwise 0. Used for environmental resistance modeling.

### Asynchronous Design

The simulation uses Python's `asyncio` module for non-blocking time delays:
- Main loop runs with 2-second intervals between updates
- Allows for potential future enhancements (multiple concurrent simulations, real-time input, etc.)

---

## Advanced Usage

### Modifying the Code

The engine module is designed to be extensible. You can:

1. **Add new environmental factors**: Modify the `dynamic_increment()` method
2. **Change fuel consumption rate**: Adjust the fuel consumption line in the `start()` method
3. **Modify output format**: Change the print statements in the main loop
4. **Add data logging**: Capture position/fuel data for analysis

### Example: Custom Environmental Factor

```python
def dynamic_increment(self):
    # Original calculation
    fuel_efficiency = sigmoid(self.fuel - 5)
    environment_factor = relu(math.sin(self.position))
    
    # Add custom factor (e.g., wind resistance)
    wind_resistance = 0.1 * abs(self.position)
    
    effective_increment = self.base_increment * fuel_efficiency * (1 - environment_factor - wind_resistance)
    return max(0.001, effective_increment)
```

---

## Future Enhancements

The `Feeder` class in the module is experimental and demonstrates potential future features:
- Real-time data input integration
- External control of simulation parameters
- Multi-threaded data processing

These features are not currently used in the main heartbeat simulation but may be developed in future versions.

---

## Support

For issues, questions, or contributions:

1. Visit the GitHub repository: https://github.com/odds-get-evened/oddpy
2. Open an issue or pull request
3. Check the main README.md for project-wide information

---

## License

This module is part of the oddpy project, licensed under the MIT License. See the LICENSE file in the repository root for details.
