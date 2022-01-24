from datetime import datetime
from pyboletox.Contracts.Cnab.Retorno.Cnab400.detalhe import Detalhe as DetalheContract
from pyboletox.magicTrait import MagicTrait


class Detalhe(MagicTrait, DetalheContract):
    
    def __init__(self) -> None:
        super().__init__()

        self._carteira = None
        self._nossoNumero = None
        self._numeroDocumento = None
        self._numeroControle = None
        self._codigoLiquidacao = None
        self._ocorrencia = None
        self._ocorrenciaTipo = None
        self._ocorrenciaDescricao = None
        self._dataOcorrencia = None
        self._rejeicao = None
        self._dataVencimento = None
        self._dataCredito = None
        self._valor = None
        self._valorTarifa = None
        self._valorOutrasDespesas = None
        self._valorIOF = None
        self._valorAbatimento = None
        self._valorRecebido = None
        self._valorMora = None
        self._valorMulta = None
        self._error = None

    def getCarteira(self):
        return self._carteira

    def setCarteira(self, carteira):
        self._carteira = carteira
        return self

    def getNossoNumero(self):
        return self._nossoNumero

    def setNossoNumero(self, nossoNumero):
        self._nossoNumero = nossoNumero
        return self

    def getNumeroDocumento(self):
        return self._numeroDocumento

    def setNumeroDocumento(self, numeroDocumento):
        self._numeroDocumento = str(numeroDocumento).strip(' ').lstrip('0')
        return self

    def getNumeroControle(self):
        return self._numeroControle

    def setNumeroControle(self, numeroControle):
        self._numeroControle = numeroControle
        return self

    def getCodigoLiquidacao(self):
        return self._codigoLiquidacao

    def setCodigoLiquidacao(self, codigoLiquidacao):
        self._codigoLiquidacao = codigoLiquidacao
        return self

    def hasOcorrencia(self, *args):
        ocorrencias = args

        if len(ocorrencias) == 0 and not self.getOcorrencia():
            return True

        if len(ocorrencias) == 1 and type(ocorrencias[0]) is list:
            ocorrencias = ocorrencias[0]

        if self.getOcorrencia() in ocorrencias:
            return True

        return False

    def getOcorrencia(self):
        return self._ocorrencia

    def setOcorrencia(self, ocorrencia):
        self._ocorrencia = "{0:0>2s}".format(ocorrencia)
        return self

    def getOcorrenciaDescricao(self):
        return self._ocorrenciaDescricao

    def setOcorrenciaDescricao(self, ocorrenciaDescricao):
        self._ocorrenciaDescricao = ocorrenciaDescricao
        return self

    def getOcorrenciaTipo(self):
        return self._ocorrenciaTipo

    def setOcorrenciaTipo(self, ocorrenciaTipo):
        self._ocorrenciaTipo = ocorrenciaTipo
        return self

    def getDataOcorrencia(self, format='%d/%m/%Y'):
        return self._dataOcorrencia.strftime(format) if self._dataOcorrencia else None
    
    def setDataOcorrencia(self, dataOcorrencia, format='%d%m%y'):
        self._dataOcorrencia = datetime.strptime(dataOcorrencia, format) if dataOcorrencia.strip("0 ") else None
        return self

    def getRejeicao(self):
        return self._rejeicao

    def setRejeicao(self, rejeicao):
        self._rejeicao = rejeicao
        return self

    def getDataVencimento(self, format='%d/%m/%Y'):
        return self._dataVencimento.strftime(format) if self._dataVencimento else None

    def setDataVencimento(self, dataVencimento, format='%d%m%y'):
        self._dataVencimento = datetime.strptime(dataVencimento, format) if dataVencimento.strip("0 ") else None
        return self

    def getDataCredito(self, format='%d/%m/%Y'):
        return self._dataCredito.strftime(format) if self._dataCredito else None

    def setDataCredito(self, dataCredito, format='%d%m%y'):
        self._dataCredito = datetime.strptime(dataCredito, format) if dataCredito.strip("0 ") else None
        return self

    def getValor(self):
        return self._valor

    def setValor(self, valor):
        self._valor = valor
        return self

    def getValorTarifa(self):
        return self._valorTarifa

    def setValorTarifa(self, valorTarifa):
        self._valorTarifa = valorTarifa
        return self

    def getValorOutrasDespesas(self):
        return self._valorOutrasDespesas

    def setValorOutrasDespesas(self, valorOutrasDespesas):
        self._valorOutrasDespesas = valorOutrasDespesas
        return self

    def getValorIOF(self):
        return self._valorIOF

    def setValorIOF(self, valorIOF):
        self._valorIOF = valorIOF
        return self

    def getValorAbatimento(self):
        return self._valorAbatimento

    def setValorAbatimento(self, valorAbatimento):
        self._valorAbatimento = valorAbatimento
        return self

    def getValorDesconto(self):
        return self._valorDesconto

    def setValorDesconto(self, valorDesconto):
        self._valorDesconto = valorDesconto
        return self

    def getValorRecebido(self):
        return self._valorRecebido

    def setValorRecebido(self, valorRecebido):
        self._valorRecebido = valorRecebido
        return self

    def getValorMora(self):
        return self._valorMora

    def setValorMora(self, valorMora):
        self._valorMora = valorMora
        return self

    def getValorMulta(self):
        return self._valorMulta

    def setValorMulta(self, valorMulta):
        self._valorMulta = valorMulta
        return self

    def hasError(self):
        return self.getOcorrencia == self.OCORRENCIA_ERRO

    def getError(self):
        return self._error

    def setError(self, error):
        self._ocorrenciaTipo = self.OCORRENCIA_ERRO
        self._error = error
        return self
