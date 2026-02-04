# oddpy

## Overview
**`oddpy`** is a Python application that simulates a dynamic heartbeat movement powered by a fuel source using an interactive simulation model. It demonstrates concepts such as:

- Dynamic movement controlled by the amount of fuel.
- Environmental factors affecting speed and direction.
- Mathematical functions (`sigmoid` and `ReLU`) for non-linear dynamics.
- Asynchronous programming using Python's `asyncio` module.


The main program is implemented in the file `odds/engine.py`.

---

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Contributing](#contributing)
5. [License](#license)

---

## Installation

To use this app, follow the steps below:

1. Clone this repository:
   ```bash
   git clone https://github.com/odds-get-evened/oddpy.git
   ```
2. Navigate to the repository folder:
   ```bash
   cd oddpy
   ```
3. Ensure you have Python 3.8+ installed.
4. (Optional) Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate  # For Windows
   ```
5. Install required libraries if needed:
   ```bash
   pip install -r requirements.txt  # (if dependencies are listed)
   ```

---

## Usage

To run the `heartbeat` simulation, execute:
```bash
python odds/engine.py
```

### Key Parameters
You can modify the behavior by changing the initialization parameters in the `Heartbeat` class:

- `initial_fuel`: Set the starting fuel (default: 10).
- `increment`: Define the base speed increment (default: 0.01).

Example:
```python
from odds.engine import Heartbeat

# Initialize heartbeat with custom parameters
heartbeat_simulation = Heartbeat(initial_fuel=20, increment=0.05)
```

---

## Features

1. **Dynamic Movement**:
    - Simulated positional change in a 2D range from -1 to 1.
    - Value oscillates based on fuel and environmental dynamics.

2. **Fuel and Environmental Dependency**:
    - Fuel levels directly impact speed; a sigmoid curve optimizes fuel usage.
    - Environmental factors like resistance/amplification impact movement.

3. **Asynchronous Programming**:
    - Uses Python's `asyncio` to simulate real-world time intervals between movements.

---

## Contributing

Contributions are welcome! If you'd like to contribute, follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss your idea.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.