from pyboletox.Cnab.Retorno.Cnab400.abstractRetorno import AbstractRetorno
from pyboletox.Contracts.Cnab.retornoCnab400 import RetornoCnab400
from pyboletox.util import Util
from pyboletox.Contracts.Boleto.boleto import Boleto as BoletoContract


class Caixa(AbstractRetorno, RetornoCnab400):
    def __init__(self, file) -> None:
        super().__init__(file)

        self._codigoBanco = BoletoContract.COD_BANCO_CEF

        self._ocorrencias = {
            '01': 'Entrada Confirmada',
            '02': 'Baixa Confirmada',
            '03': 'Abatimento Concedido',
            '04': 'Abatimento Cancelado',
            '05': 'Vencimento Alterado',
            '06': 'Uso da Empresa Alterado',
            '07': 'Prazo de Protesto Alterado',
            '08': 'Prazo de Devolução Alterado',
            '09': 'Alteração Confirmada',
            '10': 'Alteração com Reemissão de Bloqueto Confirmada',
            '11': 'Alteração da Opção de Protesto para Devolução',
            '12': 'Alteração da Opção de Devolução para protesto',
            '20': 'Em Ser',
            '21': 'Liquidação',
            '22': 'Liquidação em Cartório',
            '23': 'Baixa por Devolução',
            '24': 'Baixa por Franco Pagamento',
            '25': 'Baixa por Protesto',
            '26': 'Título enviado para Cartório',
            '27': 'Sustação de Protesto',
            '28': 'Estorno de Protesto',
            '29': 'Estorno de Sustação de Protesto',
            '30': 'Alteração de Título',
            '31': 'Tarifa sobre Título Vencido',
            '32': 'Outras Tarifas de Alteração',
            '33': 'Estorno de Baixa/Liquidação',
            '34': 'Transferência de Carteira/Entrada',
            '35': 'Transferência de Carteira/Baixa',
            '99': 'Rejeição do Título – Cód. Rejeição informado nas POS 80 a 82'
        }

        self._rejeicoes = {
            '01': 'Movimento sem Cedente Correspondente ',
            '02': 'Movimento sem Título Correspondente',
            '08': 'Movimento para Título já com Movimentação no dia ',
            '09': 'Nosso Número não Pertence ao Cedente',
            '10': 'Inclusão de Título já Existente',
            '12': 'Movimento Duplicado',
            '13': 'Entrada Inválida para Cobrança Caucionada (Cedente não possui conta Caução)',
            '20': 'CEP do Sacado não Encontrado (Não foi possível a Determinação da Agência Cobradora para o Título) ',
            '21': 'Agência Cobradora não Encontrada (Agência Designada para Cobradora não Cadastrada no Sistema) ',
            '22': 'Agência Cedente não Encontrada (Agência do Cedente não Cadastrada no Sistema)',
            '45': 'Data de Vencimento com prazo mais de 1 ano',
            '49': 'Movimento Inválido para Título Baixado/Liquidado',
            '50': 'Movimento Inválido para Título enviado ao Cartório',
            '54': 'Faixa de CEP da Agência Cobradora não Abrange CEP do Sacado',
            '55': 'Título já com Opção de Devolução',
            '56': 'Processo de Protesto em Andamento',
            '57': 'Título já com Opção de Protesto',
            '58': 'Processo de Devolução em Andamento',
            '59': 'Novo Prazo p/ Protesto/Devolução Inválido',
            '76': 'Alteração de Prazo de Protesto Inválida',
            '77': 'Alteração de Prazo de Devolução Inválida',
            '81': 'CEP do Sacado Inválido',
            '82': 'CGC/CPF do Sacado Inválido (Dígito não Confere)',
            '83': 'Número do Documento (Seu Número) inválido',
            '84': 'Protesto inválido para título sem Número do Documento (Seu Número)',
        }
        
    def init(self):
        self._totais = {
            'valor_recebido': 0,
            'liquidados': 0,
            'entradas': 0,
            'baixados': 0,
            'protestados': 0,
            'erros': 0,
            'alterados': 0,
        }

    def processarHeader(self, header):
        self.getHeader()\
            .setOperacaoCodigo(self.rem(2, 2, header))\
            .setOperacao(self.rem(3, 9, header))\
            .setServicoCodigo(self.rem(10, 11, header))\
            .setServico(self.rem(12, 26, header))\
            .setAgencia(self.rem(27, 30, header))\
            .setConta(self.rem(33, 37, header))\
            .setContaDv(self.rem(38, 38, header))\
            .setData(self.rem(95, 100, header))

        return True

    def processarDetalhe(self, detalhe):
        d = self.detalheAtual()

        d.setCarteira(self.rem(83, 85, detalhe))\
            .setNossoNumero(self.rem(86, 94, detalhe))\
            .setNumeroDocumento(self.rem(117, 126, detalhe))\
            .setNumeroControle(self.rem(38, 62, detalhe))\
            .setOcorrencia(self.rem(109, 110, detalhe))\
            .setOcorrenciaDescricao(self.ocorrencias.get(d.getOcorrencia(), 'Desconhecida'))\
            .setDataOcorrencia(self.rem(111, 116, detalhe))\
            .setDataVencimento(self.rem(147, 152, detalhe))\
            .setDataCredito(self.rem(296, 301, detalhe))\
            .setCodigoLiquidacao(self.rem(393, 394, detalhe))\
            .setValor(Util.nFloat(self.rem(153, 165, detalhe) / 100, 2, False))\
            .setValorTarifa(Util.nFloat(self.rem(176, 188, detalhe) / 100, 2, False))\
            .setValorIOF(Util.nFloat(self.rem(215, 227, detalhe) / 100, 2, False))\
            .setValorAbatimento(Util.nFloat(self.rem(228, 240, detalhe) / 100, 2, False))\
            .setValorDesconto(Util.nFloat(self.rem(241, 253, detalhe) / 100, 2, False))\
            .setValorRecebido(Util.nFloat(self.rem(254, 266, detalhe) / 100, 2, False))\
            .setValorMora(Util.nFloat(self.rem(267, 279, detalhe) / 100, 2, False))\
            .setValorMulta(Util.nFloat(self.rem(280, 292, detalhe) / 100, 2, False))

        msg = self.rem(378, 385, detalhe)
        msg = "{0:0>8s}".format(msg)
        msgAdicional = [msg[i:i + 2] if msg[i:i + 2] else '' for i in range(0, len(msg), 2)]

        if d.hasOcorrencia('06', '07', '08', '10', '59'):
            self._totais['liquidados'] += 1
            d.setOcorrenciaTipo(d.OCORRENCIA_LIQUIDADA)
        elif d.hasOcorrencia('02', '64', '71', '73'):
            self._totais['entradas'] += 1
            d.setOcorrenciaTipo(d.OCORRENCIA_ENTRADA)
        elif d.hasOcorrencia('05', '09', '47', '72'):
            self._totais['baixados'] += 1
            d.setOcorrenciaTipo(d.OCORRENCIA_BAIXADA)
        elif d.hasOcorrencia('32'):
            self._totais['protestados'] += 1
            d.setOcorrenciaTipo(d.OCORRENCIA_PROTESTADA)
        elif d.hasOcorrencia('14'):
            self._totais['alterados'] += 1
            d.setOcorrenciaTipo(d.OCORRENCIA_ALTERACAO)
        elif d.hasOcorrencia('03', '15', '16', '17', '18', '60'):
            self._totais['erros'] += 1
            error = Util.appendStrings(
                self._rejeicoes.get(msgAdicional[0], ''),
                self._rejeicoes.get(msgAdicional[1], ''),
                self._rejeicoes.get(msgAdicional[2], ''),
                self._rejeicoes.get(msgAdicional[3], '')
            )
            d.setError(error)
        else:
            d.setOcorrenciaTipo(d.OCORRENCIA_OUTROS)

        return True
    
    def processarTrailer(self, trailer):
        self.getTrailer()\
            .setQuantidadeTitulos(
            int(self.rem(18, 25, trailer)) +
            int(self.rem(58, 65, trailer)) +
            int(self.rem(178, 185, trailer)))\
            .setValorTitulos(float(Util.nFloat(self.rem(221, 234, trailer) / 100, 2, False)))\
            .setQuantidadeErros(int(self._totais['erros']))\
            .setQuantidadeEntradas(int(self._totais['entradas']))\
            .setQuantidadeLiquidados(int(self._totais['liquidados']))\
            .setQuantidadeBaixados(int(self._totais['baixados']))\
            .setQuantidadeAlterados(int(self._totais['alterados']))

        return True
