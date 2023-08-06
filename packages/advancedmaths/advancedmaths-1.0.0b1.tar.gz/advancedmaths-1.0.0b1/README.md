[![Downloads](https://static.pepy.tech/personalized-badge/find-primes?period=total&units=none&left_color=grey&right_color=yellowgreen&left_text=Downloads)](https://pepy.tech/project/find-primes)

Advanced Math is a library to calculate math problems.

**Install**

Stable Version:
```shell
pip install -U advanced-math
```
Beta Version:
```shell
pip install --pre -U advanced-math
```

**[Fractions](https://en.wikipedia.org/wiki/Twin_prime)**

A twin prime is a prime number that is either 2 less or 2 more than another prime number.

Example: Find all twin primes below 1000.
```python
from find_primes import find_twins
print(find_twins(1000))
```