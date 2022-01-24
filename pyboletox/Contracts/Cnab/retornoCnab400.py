from abc import ABCMeta, abstractmethod
from pyboletox.Contracts.Cnab.retorno import Retorno


class RetornoCnab400(Retorno):
    
    @abstractmethod
    def getCodigoBanco(self):
        pass

    @abstractmethod
    def getBancoNome(self):
        pass

    @abstractmethod
    def getDetalhes(self):
        pass

    @abstractmethod
    def getDetalhe(self, i):
        pass

    @abstractmethod
    def getHeader(self):
        pass

    @abstractmethod
    def getTrailer(self):
        pass

    @abstractmethod
    def processar(self):
        pass

    @abstractmethod
    def toDict(self):
        pass
