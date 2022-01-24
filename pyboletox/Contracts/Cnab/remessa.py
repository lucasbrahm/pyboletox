from abc import abstractmethod
from pyboletox.Contracts.Cnab.cnab import Cnab


class Remessa(Cnab):

    @abstractmethod
    def gerar(self):
        pass
