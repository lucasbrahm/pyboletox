from abc import abstractmethod
import re
from pyboletox.util import Util
from pyboletox.Contracts.Boleto.boleto import Boleto as BoletoContract


class AbstractRetorno:
    def __init__(self, file) -> None:
        # Se Cnab ja foi processado
        self._processado = False

        # Código do banco
        self._codigoBanco = ''

        # Incremento de detalhes
        self._increment = 0

        # Arquivo transformado em array por linha
        self._file = None

        self._header = ''

        self._trailer = ''

        self._detalhe = {}

        #  Helper de totais.
        self._totais = []

        self._position = 1

        self._file = Util.file2array(file)

        bancosDisponiveis = []
        for name, value in vars(BoletoContract).items():
            if re.match(r"^COD_BANCO.*", name):
                bancosDisponiveis.append(value)

        if not Util.isHeaderRetorno(self._file[0]):
            raise Exception("Arquivo de retorno inválido")

        banco = self._file[0][76:79] if Util.isCnab400(self._file[0]) else self._file[0][0:3]
        if banco not in bancosDisponiveis:
            raise Exception(f"Banco: {banco}, inválido")

    # Retorna o código do banco
    def getCodigoBanco(self):
        return self._codigoBanco
    
    def getBancoNome(self):
        return Util.bancos[self._codigoBanco]

    def getTipo(self):
        return 400 if Util.isCnab400(self._file[0]) else 240

    def getFileContent(self):
        return ''.join(self._file)

    def getDetalhes(self):
        return self._detalhe

    def getDetalhe(self, i):
        return self._detalhe.get(i)

    def getHeader(self):
        return self._header

    def getTrailer(self):
        return self._trailer

    def getTotais(self):
        return self._totais

    def detalheAtual(self):
        return self._detalhe[self._increment]

    def isProcessado(self):
        return self._processado

    def setProcessado(self):
        self._processado = True
        return self

    @abstractmethod
    def incrementDetalhe(self):
        pass

    @abstractmethod
    def processar(self):
        pass

    @abstractmethod
    def toDict(self):
        pass

    def rem(self, i, f, array):
        return Util.remove(i, f, array)

    def current(self):
        return self._etalhe[self._position]

    def next(self):
        self._position += 1

    def key(self):
        return self._position

    def valid(self):
        return True if self._detalhe.get(self._position) else False

    def rewind(self):
        self._position = 1

    def count(self):
        return len(self._detalhe)

    def seek(self, position):
        self._position = position
        if self.valid():
            raise KeyError(f"Posição inválida {position}")
