from abc import ABCMeta, abstractmethod


class Detalhe(metaclass=ABCMeta):

    OCORRENCIA_LIQUIDADA = 1
    OCORRENCIA_BAIXADA = 2
    OCORRENCIA_ENTRADA = 3
    OCORRENCIA_ALTERACAO = 4
    OCORRENCIA_PROTESTADA = 5
    OCORRENCIA_OUTROS = 6
    OCORRENCIA_ERRO = 9

    @abstractmethod
    def getNossoNumero(self):
        pass

    @abstractmethod
    def getNumeroDocumento(self):
        pass

    @abstractmethod
    def getOcorrencia(self):
        pass

    @abstractmethod
    def getOcorrenciaDescricao(self):
        pass

    @abstractmethod
    def getOcorrenciaTipo(self):
        pass

    @abstractmethod
    def getDataOcorrencia(self, format='%d/%m/%Y'):
        pass

    @abstractmethod
    def getDataVencimento(self, format='%d/%m/%Y'):
        pass

    @abstractmethod
    def getDataCredito(self, format='%d/%m/%Y'):
        pass

    @abstractmethod
    def getValor(self):
        pass

    @abstractmethod
    def getValorTarifa(self):
        pass

    @abstractmethod
    def getValorIOF(self):
        pass

    @abstractmethod
    def getValorAbatimento(self):
        pass

    @abstractmethod
    def getValorDesconto(self):
        pass

    @abstractmethod
    def getValorRecebido(self):
        pass

    @abstractmethod
    def getValorMora(self):
        pass

    @abstractmethod
    def getValorMulta(self):
        pass

    @abstractmethod
    def getError(self):
        pass

    @abstractmethod
    def hasError(self):
        pass

    @abstractmethod
    def hasOcorrencia(self):
        pass

    @abstractmethod
    def toDict(self):
        pass
