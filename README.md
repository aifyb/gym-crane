# gym-crane

A gym environment for the crane scheduling problem.

## Installation

```bash
git clone https://github.com/aifyb/gym_crane.git
cd gym-crane
pip install -e .
```

## Usage

```python
import gymnasium as gym
import gym_crane

env = gym.make('CarneWorld-v0', render_mode='human')
```