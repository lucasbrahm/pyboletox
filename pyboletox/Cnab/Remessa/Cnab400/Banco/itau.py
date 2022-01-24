from pyboletox.Cnab.Remessa.Cnab400.abstractRemessaCnab400 import AbstractRemessaCnab400
from pyboletox.Contracts.Cnab.remessa import Remessa
from pyboletox.Contracts.Boleto.boleto import Boleto as BoletoContract
from pyboletox.util import Util
from pyboletox.calculoDV import CalculoDV
from datetime import datetime, timedelta


class Itau(AbstractRemessaCnab400, Remessa):
    ESPECIE_DUPLICATA = '01'
    ESPECIE_NOTA_PROMISSORIA = '02'
    ESPECIE_NOTA_SEGURO = '03'
    ESPECIE_MENSALIDADE_ESCOLAR = '04'
    ESPECIE_RECIBO = '05'
    ESPECIE_CONTRATO = '06'
    ESPECIE_COSSEGUROS = '07'
    ESPECIE_DUPLICATA_SERVICO = '08'
    ESPECIE_LETRA_CAMBIO = '09'
    ESPECIE_NOTA_DEBITOS = '13'
    ESPECIE_DOCUMENTO_DIVIDA = '15'
    ESPECIE_ENCARGOS_CONDOMINIAIS = '16'
    ESPECIE_NOTA_SERVICOS = '17'
    ESPECIE_DIVERSOS = '99'

    OCORRENCIA_REMESSA = '01'
    OCORRENCIA_PEDIDO_BAIXA = '02'
    OCORRENCIA_CONCESSAO_ABATIMENTO = '04'
    OCORRENCIA_CANC_ABATIMENTO = '05'
    OCORRENCIA_ALT_VENCIMENTO = '06'
    OCORRENCIA_ALT_CONTROLE_PARTICIPANTE = '07'
    OCORRENCIA_ALT_SEUNUMERO = '08'
    OCORRENCIA_PROTESTAR = '09'
    OCORRENCIA_NAO_PROTESTAR = '10'
    OCORRENCIA_PROTESTO_FALIMENTARES = '11'
    OCORRENCIA_SUSTAR_PROTESTO = '18'
    OCORRENCIA_EXCL_AVALISTA = '30'
    OCORRENCIA_ALT_OUTROS_DADOS = '31'
    OCORRENCIA_BAIXA_PAGO_DIRETAMENTE = '34'
    OCORRENCIA_CANC_INSTRUCAO = '35'
    OCORRENCIA_ALT_VENC_SUSTAR_PROTESTO = '37'
    OCORRENCIA_NAO_CONCORDA_SACADO = '38'
    OCORRENCIA_DISPENSA_JUROS = '47'

    INSTRUCAO_SEM = '00'
    INSTRUCAO_DEVOL_VENC_5 = '02'
    INSTRUCAO_DEVOL_VENC_30 = '03'
    INSTRUCAO_RECEBER_CONFORME_TITULO = '05'
    INSTRUCAO_DEVOL_VENC_10 = '06'
    INSTRUCAO_DEVOL_VENC_15 = '07'
    INSTRUCAO_DEVOL_VENC_20 = '08'
    INSTRUCAO_PROTESTAR_VENC_XX = '09'
    INSTRUCAO_NAO_PROTESTAR = '10'
    INSTRUCAO_DEVOL_VENC_25 = '11'
    INSTRUCAO_DEVOL_VENC_35 = '12'
    INSTRUCAO_DEVOL_VENC_40 = '13'
    INSTRUCAO_DEVOL_VENC_45 = '14'
    INSTRUCAO_DEVOL_VENC_50 = '15'
    INSTRUCAO_DEVOL_VENC_55 = '16'
    INSTRUCAO_DEVOL_VENC_60 = '17'
    INSTRUCAO_DEVOL_VENC_90 = '18'
    INSTRUCAO_NAO_RECEBER_VENC_05 = '19'
    INSTRUCAO_NAO_RECEBER_VENC_10 = '20'
    INSTRUCAO_NAO_RECEBER_VENC_15 = '21'
    INSTRUCAO_NAO_RECEBER_VENC_20 = '22'
    INSTRUCAO_NAO_RECEBER_VENC_25 = '23'
    INSTRUCAO_NAO_RECEBER_VENC_30 = '24'
    INSTRUCAO_NAO_RECEBER_VENC_35 = '25'
    INSTRUCAO_NAO_RECEBER_VENC_40 = '26'
    INSTRUCAO_NAO_RECEBER_VENC_45 = '27'
    INSTRUCAO_NAO_RECEBER_VENC_50 = '28'
    INSTRUCAO_NAO_RECEBER_VENC_55 = '29'
    INSTRUCAO_DESCONTO_DIA = '30'
    INSTRUCAO_NAO_RECEBER_VENC_60 = '31'
    INSTRUCAO_NAO_RECEBER_VENC_90 = '32'
    INSTRUCAO_CONCEDER_ABATIMENTO_VENCIDO = '33'
    INSTRUCAO_PROTESTAR_VENC_XX_S_AVISO = '34'
    INSTRUCAO_PROTESTAR_VENC_XX_UTEIS_S_AVISO = '35'
    INSTRUCAO_RECEBER_ULT_DIA_MES_VENC = '37'
    INSTRUCAO_CONCEDER_DESC_VENC = '38'
    INSTRUCAO_NAO_RECEBER_VENC = '39'
    INSTRUCAO_CONCEDER_DESC_NOTA_CRED = '40'
    INSTRUCAO_PROTESTO_FALIMENTARES = '42'
    INSTRUCAO_SUJEITO_PROTESTO_NAO_VENC = '43'
    INSTRUCAO_PAGTO_ATRASO_APOS_DDMMAA = '44'
    INSTRUCAO_DIA_GRACAO = '45'
    INSTRUCAO_DISPENSAR_JUROS = '47'
    INSTRUCAO_RECEBER_ANT_QUITADA = '51'
    INSTRUCAO_PAGTO_SOMENTE_BOLETO_BANCO = '52'
    INSTRUCAO_VENC_PAGTO_EMPRESA = '54'
    INSTRUCAO_VALOR_SOMA_MORA = '57'
    INSTRUCAO_DEVOL_VENC_365 = '58'
    INSTRUCAO_PAGTO_BANCO = '59'
    INSTRUCAO_ENTREGUE_PENHOR = '61'
    INSTRUCAO_TRANSFERIDO = '62'
    INSTRUCAO_VALOR_PRORATA_10 = '78'
    INSTRUCAO_JUROS_VENC_15 = '79'
    INSTRUCAO_PAGTO_CHEQUE = '80'
    INSTRUCAO_OPERACAO_VENDOR = '83'
    INSTRUCAO_AG_CEDENTE_APOS_VENC = '84'
    INSTRUCAO_ANTES_VENC_APOS_15_SEDE = '86'
    INSTRUCAO_NAO_RECEBER_ANTES_VENC = '88'
    INSTRUCAO_VENC_QLQ_AG = '90'
    INSTRUCAO_NAO_RECEBER_VENC_XX = '91'
    INSTRUCAO_DEVOL_VENC_XX = '92'
    INSTRUCAO_MSG_30_POS = '93'
    INSTRUCAO_MSG_40_POS = '94'

    def __init__(self, **kwargs) -> None:
        super().__init__()
        # Código do banco
        self._codigoBanco = BoletoContract.COD_BANCO_ITAU
        # Define as carteiras disponíveis para cada banco
        self._carteiras = ['112', '115', '188', '109', '121', '175']
        # Caracter de fim de linha
        self.fimLinha = "\r\n"
        # Caracter de fim de arquivo
        self.fimArquivo = "\r\n"

        self.init(**kwargs)

    def header(self):
        self.iniciaHeader()

        self.add(1, 1, '0')
        self.add(2, 2, '1')
        self.add(3, 9, 'REMESSA')
        self.add(10, 11, '01')
        self.add(12, 26, Util.formatCnab('X', 'COBRANCA', 15))
        self.add(27, 30, Util.formatCnab('9', self.getAgencia(), 4))
        self.add(31, 32, '00')
        self.add(33, 37, Util.formatCnab('9', self.getConta(), 5))
        contaDv = self.getContaDv()
        if contaDv:
            self.add(38, 38, contaDv)
        else:
            self.add(38, 38, CalculoDV.itauContaCorrente(self.getAgencia(), self.getConta())) 
        self.add(39, 46, '')
        self.add(47, 76, Util.formatCnab('X', self.getBeneficiario().getNome(), 30))
        self.add(77, 79, self.getCodigoBanco())
        self.add(80, 94, Util.formatCnab('X', 'BANCO ITAU SA', 15))
        self.add(95, 100, self.getDataRemessa('%d%m%y'))
        self.add(101, 394, '')
        self.add(395, 400, Util.formatCnab('9', 1, 6))

    def addBoleto(self, boleto):
        self.boletos.append(boleto)
        self.iniciaDetalhe()

        self.add(1, 1, '1')
        self.add(2, 3, '02' if len(Util.numbersOnly(self.getBeneficiario().getDocumento())) == 14 else '01')
        self.add(4, 17, Util.formatCnab('9', Util.numbersOnly(self.getBeneficiario().getDocumento()), 14))
        self.add(18, 21, Util.formatCnab('9', self.getAgencia(), 4))
        self.add(22, 23, '00')
        self.add(24, 28, Util.formatCnab('9', self.getConta(), 5))
        contaDv = self.getContaDv()
        if not contaDv:
            contaDv = CalculoDV.itauContaCorrente(self.getAgencia(), self.getConta())
        self.add(29, 29, contaDv)
        self.add(30, 33, '')
        self.add(34, 37, '0000')
        self.add(38, 62, Util.formatCnab('X', boleto.getNumeroControle(), 25))  # numero de controle
        self.add(63, 70, Util.formatCnab('9', boleto.getNossoNumero()[:-1], 8))
        self.add(71, 83, Util.formatCnab('9', '0', 13, 2))
        self.add(84, 86, Util.formatCnab('9', self.getCarteiraNumero(), 3))
        self.add(87, 107, '')
        self.add(108, 108, 'I')
        self.add(109, 110, self.OCORRENCIA_REMESSA)  # REGISTRO
        if boleto.getStatus() == BoletoContract.STATUS_BAIXA:
            self.add(109, 110, self.OCORRENCIA_PEDIDO_BAIXA)  # BAIXA
        if boleto.getStatus() == BoletoContract.STATUS_ALTERACAO:
            self.add(109, 110, self.OCORRENCIA_ALT_VENCIMENTO)  # ALTERAR VENCIMENTO
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
        self.add(159, 160, self.INSTRUCAO_VALOR_SOMA_MORA)
        if boleto.getDiasProtesto() > 0:
            self.add(157, 158, self.INSTRUCAO_PROTESTAR_VENC_XX)
        elif boleto.getDiasBaixaAutomatica() > 0:
            self.add(157, 158, self.INSTRUCAO_DEVOL_VENC_XX)
        self.add(161, 173, Util.formatCnab('9', boleto.getMoraDia(), 13, 2))
        self.add(174, 179, boleto.getDataDesconto().strftime('%d%m%y') if int(boleto.getDesconto()) > 0 else '000000')
        self.add(180, 192, Util.formatCnab('9', boleto.getDesconto(), 13, 2))
        self.add(193, 205, Util.formatCnab('9', 0, 13, 2))
        self.add(206, 218, Util.formatCnab('9', 0, 13, 2))
        self.add(219, 220, '02' if len(Util.numbersOnly(boleto.getPagador().getDocumento())) == 14 else '01')
        self.add(221, 234, Util.formatCnab('9', Util.numbersOnly(boleto.getPagador().getDocumento()), 14))
        self.add(235, 264, Util.formatCnab('X', boleto.getPagador().getNome(), 30))
        self.add(265, 274, '')
        self.add(275, 314, Util.formatCnab('X', boleto.getPagador().getEndereco(), 40))
        self.add(315, 326, Util.formatCnab('X', boleto.getPagador().getBairro(), 12))
        self.add(327, 334, Util.formatCnab('9', Util.numbersOnly(boleto.getPagador().getCep()), 8))
        self.add(335, 349, Util.formatCnab('X', boleto.getPagador().getCidade(), 15))
        self.add(350, 351, Util.formatCnab('X', boleto.getPagador().getUf(), 2))
        self.add(352, 381, Util.formatCnab('X', boleto.getSacadorAvalista().getNome() if boleto.getSacadorAvalista() else '', 30))
        self.add(382, 385, '')
        self.add(386, 391, '000000' if not boleto.getJurosApos() else (boleto.getDataVencimento() + timedelta(days=boleto.getJurosApos()).strftime('%d%m%y')))
        self.add(392, 393, Util.formatCnab('9', boleto.getDiasProtesto(boleto.getDiasBaixaAutomatica()), 2))
        self.add(394, 394, '')
        self.add(395, 400, Util.formatCnab('9', self.iRegistros + 1, 6))

        # Verifica multa
        if boleto.getMulta() > 0:
            # Inicia uma nova linha de detalhe e marca com a atual de edição
            self.iniciaDetalhe()
            # Campo adicional para a multa
            self.add(1, 1, 2)  # Adicional Multa
            self.add(2, 2, 2)  # Cód 2 = Informa Valor em percentual
            self.add(3, 10, boleto.getDataVencimento().strftime('%d%m%y'))  # Data da multa
            self.add(11, 23, Util.formatCnab('9', Util.nFloat(boleto.getMulta(), 2), 13))
            self.add(24, 394, '')
            self.add(395, 400, Util.formatCnab('9', self.iRegistros + 1, 6))

    def trailer(self):
        self.iniciaTrailer()

        self.add(1, 1, '9')
        self.add(2, 394, '')
        self.add(395, 400, Util.formatCnab('9', self.getCount(), 6))
