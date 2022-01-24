from abc import ABCMeta, abstractmethod


class IPessoa(metaclass=ABCMeta):
    @abstractmethod
    def getNome(self):
        pass

    @abstractmethod
    def getNomeDocumento(self):
        pass

    @abstractmethod
    def getDocumento(self):
        pass

    @abstractmethod
    def getBairro(self):
        pass

    @abstractmethod
    def getEndereco(self):
        pass

    @abstractmethod
    def getCepCidadeUf(self):
        pass

    @abstractmethod
    def getEnderecoCompleto(self):
        pass

    @abstractmethod
    def getCep(self):
        pass

    @abstractmethod
    def getCidade(self):
        pass

    @abstractmethod
    def getUf(self):
        pass

    @abstractmethod
    def toDict(self):
        pass
