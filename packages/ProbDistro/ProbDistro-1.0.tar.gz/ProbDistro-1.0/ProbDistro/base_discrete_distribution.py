import abc
import typing

import ProbDistro.base_distribution as base_distribution


class BaseDiscreteDistribution(base_distribution.BaseDistribution, abc.ABC):
    @abc.abstractmethod
    def pmf(self, x: float) -> float:
        pass

    def equals(self, x: float) -> float:
        self._check_supported(x)
        return self.pmf(x)

    def less_than(self, x: float) -> float:
        self._check_supported(x)
        return self.cdf(x) - self.equals(x)

    def less_than_equals(self, x: float) -> float:
        self._check_supported(x)
        return self.cdf(x)

    def greater_than(self, x: float) -> float:
        self._check_supported(x)
        return 1 - self.less_than_equals(x)

    def greater_than_equals(self, x: float) -> float:
        self._check_supported(x)
        return 1 - self.less_than(x)

    def between(self, upper: float, lower: float):
        return self.equals(upper) - self.equals(lower)

    def pmf_range(self, x: typing.Iterable):
        return self._equals_range(x, self.pmf)
