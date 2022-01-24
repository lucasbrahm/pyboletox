from datetime import datetime
from pyboletox.Contracts.Cnab.Retorno.Cnab400.header import Header as HeaderContract
from pyboletox.magicTrait import MagicTrait


class Header(MagicTrait, HeaderContract):
    
    def __init__(self) -> None:
        super().__init__()
        self._operacaoCodigo = None
        self._operacao = None
        self._servicoCodigo = None
        self._servico = None
        self._agencia = None
        self._agenciaDv = None
        self._conta = None
        self._contaDv = None
        self._data = None
        self._convenio = None
        self._codigoCliente = None

    def getOperacaoCodigo(self):
        return self._operacaoCodigo

    def setOperacaoCodigo(self, operacaoCodigo):
        self._operacaoCodigo = operacaoCodigo
        return self

    def getOperacao(self):
        return self._operacao

    def setOperacao(self, operacao):
        self._operacao = operacao
        return self

    def getServicoCodigo(self):
        return self._servicoCodigo

    def setServicoCodigo(self, servicoCodigo):
        self._servicoCodigo = servicoCodigo
        return self

    def getServico(self):
        return self._servico

    def setServico(self, servico):
        self._servico = servico
        return self

    def getAgencia(self):
        return self._agencia

    def setAgencia(self, agencia):
        self._agencia = str(agencia).strip(' ').lstrip('0')
        return self

    def getAgenciaDv(self):
        return self._agenciaDv

    def setAgenciaDv(self, agenciaDv):
        self._agenciaDv = agenciaDv
        return self

    def getConta(self):
        return self._conta

    def setConta(self, conta):
        self._conta = str(conta).strip(' ').lstrip('0')
        return self

    def getContaDv(self):
        return self._contaDv

    def setContaDv(self, contaDv):
        self._contaDv = contaDv
        return self

    def getData(self, format='%d/%m/%Y'):
        return self._data.strftime(format) if self._data else None

    def setData(self, data, format='%d%m%y'):
        self._data = datetime.strptime(data, format)
        return self

    def getConvenio(self):
        return self._convenio

    def setConvenio(self, convenio):
        self._convenio = convenio
        return self

    def getCodigoCliente(self):
        return self._codigoCliente

    def setCodigoCliente(self, codigoCliente):
        self._codigoCliente = str(codigoCliente).strip(' ').lstrip('0')
        return self
