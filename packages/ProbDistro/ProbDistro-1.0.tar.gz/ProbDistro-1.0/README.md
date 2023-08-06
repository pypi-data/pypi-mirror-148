# ProbDistro
A Python package for handling various continuous and discrete random variables, including normal/gauss, binomial, poisson, and more!

## Usage
Simply instantiate the desired distribution, and use its methods to perform the desired calculations.

For example, with a Poisson distribution

```python
import ProbDistro

p = ProbDistro.Poisson(0.75)

# print the probability 5 or fewer events will occur
print(p.less_than_equals(5))

# print the probability exactly 2 events will occur
print(p(5))
```

Or, to convert one distribution to another:

```python
import ProbDistro

p = ProbDistro.Binomial(200, 0.02)

# convert the binomial distribution to normal distribution
n = ProbDistro.conversion.binomial_to_normal(p)

# calculate the value of the normal distro at 5 on the CDF and PDF functions
print(n.cdf(5))
print(n.pdf(5))
```

## Bug Tracker
To report bugs or leave feedback, please visit our bug tracker at 
https://github.com/CPSuperstore/ProbDistro/issues

Thanks for using ProbDistro