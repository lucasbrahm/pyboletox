from abc import ABCMeta, abstractmethod


class Trailer(metaclass=ABCMeta):
    
    @abstractmethod
    def getValorTitulos(self):
        pass

    @abstractmethod
    def getAvisos(self):
        pass

    @abstractmethod
    def getQuantidadeTitulos(self):
        pass

    @abstractmethod
    def getQuantidadeLiquidados(self):
        pass

    @abstractmethod
    def getQuantidadeBaixados(self):
        pass

    @abstractmethod
    def getQuantidadeEntradas(self):
        pass

    @abstractmethod
    def getQuantidadeAlterados(self):
        pass

    @abstractmethod
    def getQuantidadeErros(self):
        pass

    @abstractmethod
    def toDict(self):
        pass
