from abc import ABCMeta, abstractmethod
from email.policy import default
from pyboletox.Cnab.Retorno.abstractRetorno import AbstractRetorno as AbstractRetornoGeneric
from pyboletox.Cnab.Retorno.Cnab400.header import Header
from pyboletox.Cnab.Retorno.Cnab400.trailer import Trailer
from pyboletox.Cnab.Retorno.Cnab400.detalhe import Detalhe


class AbstractRetorno(AbstractRetornoGeneric, metaclass=ABCMeta):
    def __init__(self, file) -> None:
        super().__init__(file)
        self._header = Header()
        self._trailer = Trailer()

    @abstractmethod
    def processarHeader(self, header):
        pass

    @abstractmethod
    def processarDetalhe(self, detalhe):
        pass

    @abstractmethod
    def processarTrailer(self, trailer):
        pass

    def incrementDetalhe(self):
        self._increment += 1
        self._detalhe[self._increment] = Detalhe()

    def processar(self):
        if self.isProcessado():
            return self

        f = getattr(self, 'init', None)
        if f:
            f()

        for linha in self._file:
            inicio = self.rem(1, 1, linha)

            if inicio == '0':
                self.processarHeader(linha)
            elif inicio == '9':
                self.processarTrailer(linha)
            else:
                self.incrementDetalhe()
                if not self.processarDetalhe(linha):
                    self._detalhe.pop(self._increment)
                    self._increment -= 1

        f = getattr(self, 'finalize', None)
        if f:
            f()

        ret = self.setProcessado()
        return ret

    def toDict(self):
        d = {
            'header': self._header.toDict(),
            'trailer': self._trailer.toDict(),
            'detalhes': []
        }

        for key, value in self._detalhe.items():
            d['detalhes'].append(value.toDict())

        return d
