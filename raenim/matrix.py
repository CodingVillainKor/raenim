from manim import *

class zeros(DecimalMatrix):
    def __init__(self, *shape, **kwargs):
        self._val = np.zeros(shape)
        super().__init__(self.val, **kwargs)

    @property
    def val(self):
        return self._val
    
class ones(DecimalMatrix):
    def __init__(self, *shape, **kwargs):
        self._val = np.ones(shape)
        super().__init__(self.val, **kwargs)

    @property
    def val(self):
        return self._val
    
class eye(DecimalMatrix):
    def __init__(self, n, **kwargs):
        self._val = np.eye(n)
        super().__init__(self.val, **kwargs)

    @property
    def val(self):
        return self._val

class randn(DecimalMatrix):
    def __init__(self, *shape, **kwargs):
        self._val = np.random.randn(*shape)
        super().__init__(self.val, **kwargs)

    @property
    def val(self):
        return self._val

class Mat:
    @staticmethod
    def zeros(*shape, **kwargs):
        return zeros(*shape, **kwargs)

    @staticmethod
    def ones(*shape, **kwargs):
        return ones(*shape, **kwargs)

    @staticmethod
    def eye(n, **kwargs):
        return eye(n, **kwargs)

    @staticmethod
    def randn(*shape, **kwargs):
        return randn(*shape, **kwargs)