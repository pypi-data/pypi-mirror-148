# gym-stopping

Brief description:
- control space: discrete {0,1}, continue or stop
- state space: continuous (0, \infty), [0,1], stock price and time to maturity
- default parameters: spot = 90.0, strike = 100.0, drift = 0.02, sigma = 0.20, maturity = 1.0, periods = 365   


To install:
- pip install gym-stopping
- import gym_stopping

To load:
- env = gym.make("stopping-v0")

To update version after changes:
- change version to, e.g., 1.0.7 from setup.py file
- git clone https://github.com/claudia-viaro/gym-stopping.git
- cd gym-update
- python setup.py sdist bdist_wheel
- twine check dist/*
- twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
