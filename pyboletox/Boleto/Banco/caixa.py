from pyboletox.Boleto.abstractBoleto import AbstractBoleto
from pyboletox.util import Util
from pyboletox.calculoDV import CalculoDV


class Caixa(AbstractBoleto):
    def __init__(self, **kwargs):
        super().__init__()
        self.init(**kwargs)
        self.setCamposObrigatorios('numero', 'agencia', 'carteira', 'codigoCliente')

        # Código do banco
        self._codigo_banco = self.COD_BANCO_CEF

        # Define as carteiras disponíveis para este banco
        self._carteiras = ['RG']

        # Espécie do documento, coódigo para remessa
        self._especiesCodigo = {
            'DM': '01',
            'NP': '02',
            'DS': '03',
            'NS': '05',
            'LC': '06',
        }

        # Codigo do cliente junto ao banco.
        self._codigoCliente = None

    # Seta o codigo do cliente.
    def setCodigoCliente(self, codigoCliente):
        self._codigoCliente = codigoCliente
        return self

    # Retorna o codigo do cliente.
    def getCodigoCliente(self):
        return self._codigoCliente

    """
    Retorna o codigo do cliente como se fosse a conta
    ja que a caixa não faz uso da conta para nada.
    """
    def getConta(self):
        return self.getCodigoCliente()

    # Gera o Nosso Número.
    def gerarNossoNumero(self):
        numero_boleto = Util.numberFormatGeral(self.getNumero(), 15)
        composicao = '1'
        if self.getCarteira() == 'SR':
            composicao = '2'

        carteira = composicao + '4'
        # As 15 próximas posições no nosso número são a critério do beneficiário, utilizando o sequencial
        # Depois, calcula-se o código verificador por módulo 11
        numero = carteira + Util.numberFormatGeral(numero_boleto, 15)
        return numero

    # Método que retorna o nosso numero usado no boleto. alguns bancos possuem algumas diferenças.
    def getNossoNumeroBoleto(self):
        return self.getNossoNumero() + '-' + CalculoDV.cefNossoNumero(self.getNossoNumero())

    # Na CEF deve retornar agência (sem o DV) / código beneficiário (com DV)
    def getAgenciaCodigoBeneficiario(self):
        return self.getAgencia() + ' / ' + \
               self.getCodigoCliente() + '-' + \
               Util.modulo11(self.getCodigoCliente())

    # Seta dias para baixa automática
    def setDiasBaixaAutomatica(self, baixaAutomatica):
        if self.getDiasProtesto() > 0:
            raise Exception('Você deve usar dias de protesto ou dias de baixa, nunca os 2')
        baixaAutomatica = int(baixaAutomatica)
        self._diasBaixaAutomatica = baixaAutomatica if baixaAutomatica > 0 else 0
        return self

    def getCampoLivre(self):
        if self._campoLivre:
            return self._campoLivre

        nossoNumero = Util.numberFormatGeral(self.gerarNossoNumero(), 17)
        beneficiario = Util.numberFormatGeral(self.getCodigoCliente(), 6)
        beneficiario += Util.modulo11(beneficiario)
        if self.getCodigoCliente() > 1100000:
            beneficiario = Util.numberFormatGeral(self.getCodigoCliente(), 7)

        campoLivre = beneficiario
        campoLivre += nossoNumero[2:2+3]
        campoLivre += nossoNumero[0:0+1]
        campoLivre += nossoNumero[5:5+3]
        campoLivre += nossoNumero[1:1+1]
        campoLivre += nossoNumero[8:8+9]
        campoLivre += Util.modulo11(campoLivre)
        self._campoLivre = campoLivre
        return self._campoLivre

    @staticmethod
    def parseCampoLivre(campoLivre):
        return {
            'convenio': None,
            'agencia': None,
            'agenciaDv': None,
            'contaCorrente': None,
            'contaCorrenteDv': None,
            'codigoCliente7': campoLivre[0:0+7],
            'codigoCliente': campoLivre[0:0+6],
            'carteira': campoLivre[10:10+1],
            'nossoNumero': campoLivre[7:7+3] + campoLivre[11:11+3] + campoLivre[15:15+8],
            'nossoNumeroDv': campoLivre[23:23+1],
            'nossoNumeroFull': campoLivre[7:7+3] + campoLivre[11:11+3] + campoLivre[15:15+8],
        }
