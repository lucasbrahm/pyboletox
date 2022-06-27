from pyboletox.Cnab.Remessa.Cnab400.abstractRemessaCnab400 import AbstractRemessaCnab400
from pyboletox.Contracts.Cnab.remessa import Remessa
from pyboletox.Contracts.Boleto.boleto import Boleto as BoletoContract
from pyboletox.util import Util
from pyboletox.calculoDV import CalculoDV
from datetime import datetime, timedelta


class Caixa(AbstractRemessaCnab400, Remessa):
    ESPECIE_DUPLICATA = '01'
    ESPECIE_NOTA_PROMISSORIA = '02'
    ESPECIE_DUPLICATA_SERVICO = '03'
    SPECIE_NOTA_SEGURO = '05'
    ESPECIE_LETRAS_CAMBIO = '06'
    ESPECIE_OUTROS = '09'

    OCORRENCIA_REMESSA = '01'
    OCORRENCIA_PEDIDO_BAIXA = '02'
    OCORRENCIA_CONCESSAO_ABATIMENTO = '03'
    OCORRENCIA_CANC_ABATIMENTO = '04'
    OCORRENCIA_ALT_VENCIMENTO = '05'
    OCORRENCIA_ALT_USO_EMPRESA = '06'
    OCORRENCIA_ALT_PRAZO_PROTESTO = '07'
    OCORRENCIA_ALT_PRAZO_DEVOLUCAO = '08'
    OCORRENCIA_ALT_OUTROS_DADOS = '09'
    OCORRENCIA_ALT_OUTROS_DADOS_EMISSAO_BOLETO = '10'
    OCORRENCIA_ALT_PROTESTO_DEVOLUCAO = '11'
    OCORRENCIA_ALT_DEVOLUCAO_PROTESTO = '12'

    INSTRUCAO_SEM = '00'
    INSTRUCAO_PROTESTAR_VENC_XX = '01'
    INSTRUCAO_DEVOLVER_VENC_XX = '02'

    def __init__(self, **kwargs):
        super().__init__()

        # Código do banco
        self._codigoBanco = BoletoContract.COD_BANCO_CEF

        # Define as carteiras disponíveis para cada banco
        self._carteiras = ['RG', 'SR']

        # Caracter de fim de linha
        self.fimLinha = "\r\n"
        # Caracter de fim de arquivo
        self.fimArquivo = "\r\n"

        # Codigo do cliente junto ao banco.
        self._codigoCliente = None

        self.init(**kwargs)
        self.addCampoObrigatorio('codigoCliente', 'idRemessa')

    # Retorna o codigo do cliente.
    def getCodigoCliente(self):
        return self._codigoCliente

    # Retorna o numero da carteira, deve ser override em casos de carteira de letras
    def getCarteiraNumero(self):
        if self.getCarteira() == 'SR':
            return '02'
        return '01'

    #  Seta o codigo do cliente.
    def setCodigoCliente(self, codigoCliente):
        self._codigoCliente = codigoCliente
        return self

    def header(self):
        self.iniciaHeader()

        self.add(1, 1, '0')
        self.add(2, 2, '1')
        self.add(3, 9, 'REMESSA')
        self.add(10, 11, '01')
        self.add(12, 26, Util.formatCnab('X', 'COBRANCA', 15))
        self.add(27, 30, Util.formatCnab('9', self.getAgencia(), 4))
        if self.getCodigoCliente() > 1100000:
            self.add(31, 37, Util.formatCnab('9', self.getCodigoCliente(), 7))
        else:
            self.add(31, 36, Util.formatCnab('9', self.getCodigoCliente(), 6))
            self.add(37, 37, '')
        self.add(38, 46, '')
        self.add(47, 76, Util.formatCnab('X', self.getBeneficiario().getNome(), 30))
        self.add(77, 79, self.getCodigoBanco())
        self.add(80, 94, Util.formatCnab('X', 'C ECON FEDERAL', 15))
        self.add(95, 100, self.getDataRemessa('%d%m%y'))
        self.add(101, 103, '007')
        self.add(104, 389, '')
        self.add(390, 394, Util.formatCnab('9', self.getIdRemessa(), 5))
        self.add(395, 400, Util.formatCnab('9', 1, 6))

        return self

    def addBoleto(self, boleto):
        self.boletos.append(boleto)
        self.iniciaDetalhe()

        self.add(1, 1, '1')
        self.add(2, 3, '02' if len(Util.numbersOnly(self.getBeneficiario().getDocumento())) == 14 else '01')
        self.add(4, 17, Util.formatCnab('9', Util.numbersOnly(self.getBeneficiario().getDocumento()), 14))
        if self.isLayout007():
            self.add(18, 20, '')
            self.add(21, 27, Util.formatCnab('9', self.getCodigoCliente(), 7))
        else:
            self.add(18, 21, Util.formatCnab('9', self.getAgencia(), 4))
            self.add(22, 27, Util.formatCnab('9', self.getCodigoCliente(), 6))
        self.add(28, 28, '2')  # ‘1’ = Banco Emite ‘2’ = Cliente Emite
        self.add(29, 29, '0')  # ‘0’ = Postagem pelo Beneficiário ‘1’ = Pagador via Correio ‘2’ = Beneficiário via Agência CAIXA ‘3’ = Pagador via e-mail
        self.add(30, 31, '00')
        self.add(32, 56, Util.formatCnab('X', boleto.getNumeroControle(), 25))  # numero de controle
        self.add(57, 73, Util.formatCnab('9', boleto.getNossoNumero(), 17))
        self.add(74, 76, '')
        self.add(77, 106, '')
        self.add(107, 108, Util.formatCnab('9', self.getCarteiraNumero(), 2))
        self.add(109, 110, self.OCORRENCIA_REMESSA)  # REGISTRO
        if boleto.getStatus() == BoletoContract.STATUS_BAIXA:
            self.add(109, 110, self.OCORRENCIA_PEDIDO_BAIXA)  # BAIXA
        if boleto.getStatus() == BoletoContract.STATUS_ALTERACAO:
            self.add(109, 110, self.OCORRENCIA_ALT_OUTROS_DADOS)  # ALTERAR VENCIMENTO
        if boleto.getStatus() == BoletoContract.STATUS_ALTERACAO_DATA:
            self.add(109, 110, self.OCORRENCIA_ALT_VENCIMENTO)
        if boleto.getStatus() == BoletoContract.STATUS_CUSTOM:
            self.add(109, 110, format(boleto.getComando(), " >2.02s"))
        self.add(111, 120, Util.formatCnab('X', boleto.getNumeroDocumento(), 10))
        self.add(121, 126, boleto.getDataVencimento().strftime('%d%m%y'))
        self.add(127, 139, Util.formatCnab('9', boleto.getValor(), 13, 2))
        self.add(140, 142, self.getCodigoBanco())
        self.add(143, 147, '00000')
        self.add(148, 149, boleto.getEspecieDocCodigo())
        self.add(150, 150, boleto.getAceite())
        self.add(151, 156, boleto.getDataDocumento().strftime('%d%m%y'))
        self.add(157, 158, self.INSTRUCAO_SEM)
        self.add(159, 160, self.INSTRUCAO_SEM)
        if boleto.getDiasProtesto() > 0:
            self.add(157, 158, self.INSTRUCAO_PROTESTAR_VENC_XX)
        elif boleto.getDiasBaixaAutomatica() > 0:
            self.add(157, 158, self.INSTRUCAO_DEVOLVER_VENC_XX)
        self.add(161, 173, Util.formatCnab('9', boleto.getMoraDia(), 13, 2))
        self.add(174, 179, boleto.getDataDesconto().strftime('%d%m%y') if float(boleto.getDesconto()) > 0 else '000000')
        self.add(180, 192, Util.formatCnab('9', boleto.getDesconto(), 13, 2))
        self.add(193, 205, Util.formatCnab('9', 0, 13, 2))
        self.add(206, 218, Util.formatCnab('9', 0, 13, 2))
        self.add(219, 220, '02' if len(Util.numbersOnly(boleto.getPagador().getDocumento())) == 14 else '01')
        self.add(221, 234, Util.formatCnab('9', Util.numbersOnly(boleto.getPagador().getDocumento()), 14))
        self.add(235, 274, Util.formatCnab('X', boleto.getPagador().getNome(), 40))
        self.add(275, 314, Util.formatCnab('X', boleto.getPagador().getEndereco(), 40))
        self.add(315, 326, Util.formatCnab('X', boleto.getPagador().getBairro(), 12))
        self.add(327, 334, Util.formatCnab('9', Util.numbersOnly(boleto.getPagador().getCep()), 8))
        self.add(335, 349, Util.formatCnab('X', boleto.getPagador().getCidade(), 15))
        self.add(350, 351, Util.formatCnab('X', boleto.getPagador().getUf(), 2))
        self.add(352, 357, '000000' if not boleto.getJurosApos() else (boleto.getDataVencimento() + timedelta(days=boleto.getJurosApos()).strftime('%d%m%y')))
        self.add(358, 367, Util.formatCnab('9', Util.percent(boleto.getValor(), boleto.getMulta()), 10, 2))
        self.add(368, 389, Util.formatCnab('X', boleto.getSacadorAvalista().getNome() if boleto.getSacadorAvalista() else '', 22))
        self.add(390, 391, '00')
        self.add(392, 393, Util.formatCnab('9', boleto.getDiasProtesto(boleto.getDiasBaixaAutomatica()), 2))
        # Código da Moeda - Código adotado para identificar a moeda referenciada no Título. Informar fixo: ‘1’ = REAL
        self.add(394, 394, Util.formatCnab('9', 1, 1))
        self.add(395, 400, Util.formatCnab('9', self.iRegistros + 1, 6))

        return self

    def trailer(self):
        self.iniciaTrailer()

        self.add(1, 1, '9')
        self.add(2, 394, '')
        self.add(395, 400, Util.formatCnab('9', self.getCount(), 6))

        return self

    def isLayout007(self):
        return self.getCodigoCliente() > 1100000
