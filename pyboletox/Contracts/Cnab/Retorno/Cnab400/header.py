from abc import ABCMeta, abstractmethod


class Header(metaclass=ABCMeta):
    
    @abstractmethod
    def getOperacaoCodigo(self):
        pass

    @abstractmethod
    def getOperacao(self):
        pass

    @abstractmethod
    def getServicoCodigo(self):
        pass

    @abstractmethod
    def getServico(self):
        pass

    @abstractmethod
    def getAgencia(self):
        pass

    @abstractmethod
    def getAgenciaDv(self):
        pass

    @abstractmethod
    def getConta(self):
        pass

    @abstractmethod
    def getContaDv(self):
        pass

    @abstractmethod
    def getData(self, format='%d/%m/%Y'):
        pass

    @abstractmethod
    def getConvenio(self):
        pass

    @abstractmethod
    def getCodigoCliente(self):
        pass

    @abstractmethod
    def toDict(self):
        pass
