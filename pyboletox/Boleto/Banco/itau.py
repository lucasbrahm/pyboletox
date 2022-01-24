from pyboletox.Boleto.abstractBoleto import AbstractBoleto
from pyboletox.util import Util
from pyboletox.calculoDV import CalculoDV


class Itau(AbstractBoleto):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._localPagamento = 'Até o vencimento, preferencialmente no Itaú'

        self._codigoBanco = self.COD_BANCO_ITAU

        self._variaveis_adicionais = {
            'carteira_nome': ''
        }

        self._carteiras = ['112', '115', '188', '109', '121', '180', '110', '111']

        self.especiesCodigo = {
            'DM':  '01',
            'NP':  '02',
            'NS':  '03',
            'ME':  '04',
            'REC': '05',
            'CT':  '06',
            'CS':  '07',
            'DS':  '08',
            'LC':  '09',
            'ND':  '13',
            'CDA': '15',
            'EC':  '16',
            'CPS': '17',
        }

        self.init(**kwargs)

    # Seta dias para baixa automática
    def setDiasBaixaAutomatica(self, baixaAutomatica):
        if self.getDiasProtesto() > 0:
            raise Exception('Você deve usar dias de protesto ou dias de baixa, nunca os 2')
        baixaAutomatica = int(baixaAutomatica)
        self._diasBaixaAutomatica = baixaAutomatica if baixaAutomatica > 0 else 0

    # Gera o Nosso Número.
    def gerarNossoNumero(self):
        numero_boleto = Util.numberFormatGeral(self.getNumero(), 8)
        carteira = Util.numberFormatGeral(self.getCarteira(), 3)
        agencia = Util.numberFormatGeral(self.getAgencia(), 4)
        conta = Util.numberFormatGeral(self.getConta(), 5)
        dv = CalculoDV.itauNossoNumero(agencia, conta, carteira, numero_boleto)
        return numero_boleto + str(dv)

    def getNossoNumeroBoleto(self):
        nosso_numero = self.getNossoNumero()
        return self.getCarteira() + '/' + nosso_numero[:-1] + '-' + nosso_numero[-1]

    def getCampoLivre(self):
        if self._campoLivre:
            return self._campoLivre
        campoLivre = Util.numberFormatGeral(self.getCarteira(), 3)
        campoLivre += Util.numberFormatGeral(self.getNossoNumero(), 9)
        campoLivre += Util.numberFormatGeral(self.getAgencia(), 4)
        campoLivre += Util.numberFormatGeral(self.getConta(), 5)
        campoLivre += str(CalculoDV.itauContaCorrente(self.getAgencia(), self.getConta()))
        campoLivre += '000'
        self._campoLivre = campoLivre
        return self._campoLivre

    @staticmethod
    def parseCampoLivre(campoLivre):
        return {
            'convenio': None,
            'agenciaDv': None,
            'codigoCliente': None,
            'carteira': campoLivre[:3],
            'nossoNumero': campoLivre[3:3+8],
            'nossoNumeroDv': campoLivre[11],
            'nossoNumeroFull': campoLivre[3:3+9],
            'agencia': campoLivre[12:12+4],
            'contaCorrente': campoLivre[16:16+5],
            'contaCorrenteDv': campoLivre[21]
        }

    def getContaDv(self):
        if self._contaDv:
            return self.contaDv
        return CalculoDV.itauContaCorrente(self.getAgencia(), self.getConta())
