import ProbDistro.base_discrete_distribution as base_discrete_distribution


class Geometric(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, p: float):
        """
         A discrete random variable which can be used to represent the number of Bernoulli trials which are needed
         to obtain exactly 1 success.

         For example, if the probability is 0.25 for an x value of 3, this indicates there is a 25% chance of receiving
         no successes until the third trial where the first success is obtained

        :param p: probability of success
        """
        self.p = p
        self.q = 1 - p

    def pmf(self, x: float) -> float:
        return self.p * self.q ** (x - 1)

    def cdf(self, x: float) -> float:
        return 1 - self.q ** x

    def _is_supported(self, x: float) -> bool:
        if isinstance(x, float):
            if not x.is_integer():
                return False

        return x >= 1

    def expected_value(self) -> float:
        return 1 / self.p

    def variance(self) -> float:
        return (1 - self.p) / (self.p ** 2)
