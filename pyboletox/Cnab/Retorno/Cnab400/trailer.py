from pyboletox.Contracts.Cnab.Retorno.Cnab400.trailer import Trailer as TrailerContract
from pyboletox.magicTrait import MagicTrait


class Trailer(MagicTrait, TrailerContract):
    
    def __init__(self) -> None:
        super().__init__()

        self._valorTitulos = None
        self._avisos = 0
        self._quantidadeTitulos = None
        self._quantidadeLiquidados = 0
        self._quantidadeBaixados = 0
        self._quantidadeEntradas = 0
        self._quantidadeAlterados = 0
        self._quantidadeErros = 0

    def getValorTitulos(self):
        return self._valorTitulos

    def setValorTitulos(self, valorTitulos):
        self._valorTitulos = valorTitulos
        return self

    def getAvisos(self):
        return self._avisos

    def setAvisos(self, avisos):
        self._avisos = avisos
        return self

    def getQuantidadeTitulos(self):
        return self._quantidadeTitulos

    def setQuantidadeTitulos(self, quantidadeTitulos):
        self._quantidadeTitulos = quantidadeTitulos
        return self

    def getQuantidadeLiquidados(self):
        return self._quantidadeLiquidados

    def setQuantidadeLiquidados(self, quantidadeLiquidados):
        self._quantidadeLiquidados = quantidadeLiquidados
        return self

    def getQuantidadeBaixados(self):
        return self._quantidadeBaixados

    def setQuantidadeBaixados(self, quantidadeBaixados):
        self._quantidadeBaixados = quantidadeBaixados
        return self

    def getQuantidadeEntradas(self):
        return self._quantidadeEntradas

    def setQuantidadeEntradas(self, quantidadeEntradas):
        self._quantidadeEntradas = quantidadeEntradas
        return self

    def getQuantidadeAlterados(self):
        return self._quantidadeAlterados

    def setQuantidadeAlterados(self, quantidadeAlterados):
        self._quantidadeAlterados = quantidadeAlterados
        return self

    def getQuantidadeErros(self):
        return self._quantidadeErros

    def setQuantidadeErros(self, quantidadeErros):
        self._quantidadeErros = quantidadeErros
        return self
