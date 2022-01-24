from abc import ABCMeta, abstractmethod


class Boleto(metaclass=ABCMeta):

    COD_BANCO_BB = '001'
    COD_BANCO_SANTANDER = '033'
    COD_BANCO_CEF = '104'
    COD_BANCO_BRADESCO = '237'
    COD_BANCO_ITAU = '341'
    COD_BANCO_HSBC = '399'
    COD_BANCO_SICREDI = '748'
    COD_BANCO_BANRISUL = '041'
    COD_BANCO_BANCOOB = '756'
    COD_BANCO_BNB = '004'

    STATUS_REGISTRO = 1
    STATUS_ALTERACAO = 2
    STATUS_BAIXA = 3
    STATUS_ALTERACAO_DATA = 4
    STATUS_CUSTOM = 99

    @abstractmethod
    def renderPDF(self, print=False):
        pass

    @abstractmethod
    def renderHTML(self):
        pass

    @abstractmethod
    def toDict(self):
        pass

    @abstractmethod
    def getLinhaDigitavel(self):
        pass

    @abstractmethod
    def getCodigoBarras(self):
        pass

    @abstractmethod
    def getBeneficiario(self):
        pass

    @abstractmethod
    def getLogoBase64(self):
        pass

    @abstractmethod
    def getLogo(self):
        pass

    @abstractmethod
    def getLogoBancoBase64(self):
        pass

    @abstractmethod
    def getLogoBanco(self):
        pass

    @abstractmethod
    def getCodigoBanco(self):
        pass

    @abstractmethod
    def getMoeda(self):
        pass

    @abstractmethod
    def getDataVencimento(self):
        pass

    @abstractmethod
    def getDataVencimentoApos(self):
        pass

    @abstractmethod
    def getDataDesconto(self):
        pass

    @abstractmethod
    def getDataProcessamento(self):
        pass

    @abstractmethod
    def getDataDocumento(self):
        pass

    @abstractmethod
    def getValor(self):
        pass

    @abstractmethod
    def getDesconto(self):
        pass

    @abstractmethod
    def getMulta(self):
        pass

    @abstractmethod
    def getJuros(self):
        pass

    @abstractmethod
    def getMoraDia(self):
        pass

    @abstractmethod
    def getJurosApos(self):
        pass

    @abstractmethod
    def getDiasProtesto(self, default=0):
        pass

    @abstractmethod
    def getDiasBaixaAutomatica(self, default=0):
        pass

    @abstractmethod
    def getSacadorAvalista(self):
        pass

    @abstractmethod
    def getPagador(self):
        pass

    @abstractmethod
    def getDescricaoDemonstrativo(self):
        pass

    @abstractmethod
    def getInstrucoes(self):
        pass

    @abstractmethod
    def getLocalPagamento(self):
        pass

    @abstractmethod
    def getNumero(self):
        pass

    @abstractmethod
    def getNumeroDocumento(self):
        pass

    @abstractmethod
    def getNumeroControle(self):
        pass

    @abstractmethod
    def getAgenciaCodigoBeneficiario(self):
        pass

    @abstractmethod
    def getNossoNumero(self):
        pass

    @abstractmethod
    def getNossoNumeroBoleto(self):
        pass

    @abstractmethod
    def getEspecieDoc(self):
        pass

    @abstractmethod
    def getEspecieDocCodigo(self, default=99, tipo=240):
        pass

    @abstractmethod
    def getAceite(self):
        pass

    @abstractmethod
    def getCarteira(self):
        pass

    @abstractmethod
    def getCarteiraNome(self):
        pass

    @abstractmethod
    def getUsoBanco(self):
        pass

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def alterarBoleto(self):
        pass

    @abstractmethod
    def baixarBoleto(self):
        pass

    @abstractmethod
    def alterarDataDeVencimento(self):
        pass

    @abstractmethod
    def comandarInstrucao(self, instrucao):
        pass

    @abstractmethod
    def getComando(self):
        pass

    @staticmethod
    @abstractmethod
    def parseCampoLivre(self, campoLivre):
        pass

    @abstractmethod
    def getMostrarEnderecoFichaCompensacao(self):
        pass
