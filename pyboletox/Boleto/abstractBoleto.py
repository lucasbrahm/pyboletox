import datetime
import io
import os
import base64
from datetime import timedelta
from pyboletox.Contracts.Boleto.boleto import Boleto as BoletoContract
from pyboletox.util import Util
from pyboletox.Boleto.Render.pdf import BoletoPDF


class AbstractBoleto(BoletoContract):

    def __init__(self) -> None:
        super().__init__()

        self.camposObrigatorios = [
            'numero',
            'agencia',
            'conta',
            'carteira',
        ]

        self.protectedFields = [
            'nossoNumero',
        ]

        self._codigoBanco = None

        self._moeda = 9

        self._valor = None

        self._desconto = None

        self._multa = 0

        self._juros = 0

        self._jurosApos = 0

        self._diasProtesto = 0

        self._diasBaixaAutomatica = None

        self._dataDocumento = None

        self._dataProcessamento = None

        self._dataVencimento = None

        self._dataDesconto = None

        self._aceite = 'N'

        self._especieDoc = 'DM'

        self.especiesCodigo = []

        self.especiesCodigo240 = []

        self.especiesCodigo400 = []

        self._numeroDocumento = None

        self._numero = None

        self._numeroControle = None

        self._usoBanco = None

        self._agencia = None

        self._agenciaDv = None

        self._conta = None

        self._contaDv = None

        self._carteira = None

        self._carteiras = []

        self.carteirasNomes = []

        self._beneficiario = None

        self._pagador = None

        self._sacadorAvalista = None

        self._descricaoDemonstrativo = []

        self._localPagamento = 'Pagável em qualquer agência bancária até o vencimento.'

        self._instrucoes = ['Pagar até a data do vencimento.']

        self._instrucoes_impressao = []

        self._logo = None

        self._variaveis_adicionais = {}

        self._campoLivre = None

        self.campoNossoNumero = None

        self._campoLinhaDigitavel = None

        self._campoCodigoBarras = None

        self._status = BoletoContract.STATUS_REGISTRO

        self._status_custom = None

        self._mostrarEnderecoFichaCompensacao = None

    # Inicializa object realizando os 'set' com os parametros no kwargs
    def init(self, **kwargs):
        for k, v in kwargs.items():
            f = getattr(self, 'set' + k[0].upper() + k[1:], None)
            if f is not None:
                f(v)

        # Marca a data de emissão para hoje, caso não especificada
        if not self.getDataDocumento():
            self.setDataDocumento(datetime.datetime.now())
            # Marca a data de processamento para hoje, caso não especificada
        if not self.getDataProcessamento():
            self.setDataProcessamento(datetime.datetime.now())
        # Marca a data de vencimento para daqui a 5 dias, caso não especificada
        if not self.getDataVencimento():
            self.setDataVencimento(datetime.datetime.now() + datetime.timedelta(days=5))
        # Marca a data de desconto
        if not self.getDataDesconto():
            self.setDataDesconto(self.getDataVencimento())

    def getProtectedFields(self):
        return self.protectedFields

    # Define a agência
    def setAgencia(self, agencia):
        self._agencia = str(agencia)

    # Retorna a agência
    def getAgencia(self):
        return self._agencia

    # Define o dígito da agência
    def setAgenciaDv(self, agenciaDv):
        self._agenciaDv = agenciaDv

    # Retorna o dígito da agência
    def getAgenciaDv(self):
        return self._agenciaDv

    # Define o código da carteira (Com ou sem registro)
    def setCarteira(self, carteira):
        carteira = str(carteira)
        if carteira not in self.getCarteiras():
            raise Exception("Carteira não disponível!")
        self._carteira = carteira

    # Retorna o código da carteira (Com ou sem registro)
    def getCarteira(self):
        return self._carteira

    # Retorna as carteiras disponíveis para este banco
    def getCarteiras(self):
        return self._carteiras

    # Define a entidade beneficiario
    def setBeneficiario(self, beneficiario):
        self._beneficiario = Util.addPessoa(beneficiario)

    # Retorna a entidade beneficiario
    def getBeneficiario(self):
        return self._beneficiario

    # Retorna o código do banco
    def getCodigoBanco(self):
        return self._codigoBanco

    # Define o número da conta
    def setConta(self, conta):
        self._conta = str(conta)

    # Retorna o número da conta
    def getConta(self):
        return self._conta

    # Define o dígito verificador da conta
    def setContaDv(self, contaDv):
        self._contaDv = contaDv

    # Retorna o dígito verificador da conta
    def getContaDv(self):
        return self._contaDv

    # Define a data de vencimento
    def setDataVencimento(self, dataVencimento):
        self._dataVencimento = dataVencimento

    # Retorna a data de vencimento
    def getDataVencimento(self):
        return self._dataVencimento

    # Define a data de limite de desconto
    def setDataDesconto(self, dataDesconto):
        self._dataDesconto = dataDesconto

    # Retorna a data de limite de desconto
    def getDataDesconto(self):
        return self._dataDesconto

    # Define a data do documento
    def setDataDocumento(self, dataDocumento):
        self._dataDocumento = dataDocumento

    # Retorna a data do documento
    def getDataDocumento(self):
        return self._dataDocumento

    # Retorna a data do juros após
    def getDataVencimentoApos(self):
        return self.getDataVencimento() + timedelta(days=self.getJurosApos())

    # Define o campo aceite
    def setAceite(self, aceite):
        self._aceite = aceite

    # Retorna o campo aceite
    def getAceite(self):
        if self._aceite.isnumeric():
            if int(self._aceite):
                return 'A'
            else:
                return 'N'

        return self._aceite

    # Define o campo Espécie Doc, geralmente DM (Duplicata Mercantil)
    def setEspecieDoc(self, especieDoc):
        self._especieDoc = especieDoc

    # Retorna o campo Espécie Doc, geralmente DM (Duplicata Mercantil)
    def getEspecieDoc(self):
        return self._especieDoc

    # Retorna o codigo da Espécie Doc
    def getEspecieDocCodigo(self, default=99, tipo=240):
        if len(self.especiesCodigo240) > 0 and tipo == 240:
            especie = self.especiesCodigo240
        elif len(self.especiesCodigo400) > 0 and tipo == 400:
            especie = self.especiesCodigo400
        else:
            especie = self.especiesCodigo

        if self._especieDoc.upper() in especie:
            return especie[self._especieDoc.upper()]
        else:
            return default

    # Define o campo Número do documento
    def setNumeroDocumento(self, numeroDocumento):
        self._numeroDocumento = str(numeroDocumento)

    # Retorna o campo Número do documento
    def getNumeroDocumento(self):
        return self._numeroDocumento

    # Define o número definido pelo cliente para compor o nosso número
    def setNumero(self, numero):
        self._numero = numero

    # Retorna o número definido pelo cliente para compor o nosso número
    def getNumero(self):
        return self._numero

    # Define o número  definido pelo cliente para controle da remessa
    def setNumeroControle(self, numeroControle):
        self._numeroControle = numeroControle

    # Retorna o número definido pelo cliente para controle da remessa
    def getNumeroControle(self):
        return self._numeroControle

    # Define o campo Uso do banco
    def setUsoBanco(self, usoBanco):
        self._usoBanco = usoBanco

    # Retorna o campo Uso do banco
    def getUsoBanco(self):
        return self._usoBanco

    # Define a data de geração do boleto
    def setDataProcessamento(self, dataProcessamento):
        self._dataProcessamento = dataProcessamento

    # Retorna a data de geração do boleto
    def getDataProcessamento(self):
        return self._dataProcessamento

    # Adiciona uma instrução (máximo 5)
    def addInstrucao(self, instrucao):
        if len(self.getInstrucoes()) > 8:
            raise Exception('Atingido o máximo de 5 instruções.')
        self._instrucoes.append(instrucao)

    # Define um array com instruções (máximo 8) para pagamento
    def setInstrucoes(self, instrucoes):
        if len(instrucoes) > 8:
            raise Exception('Máximo de 8 instruções.')
        self._instrucoes = instrucoes

    # Retorna um array com instruções (máximo 8) para pagamento
    def getInstrucoes(self):
        return [self._instrucoes[i] if (i < len(self._instrucoes)) else None for i in range(8)]

    # Define um array com instruções (máximo 5) para impressao
    def setInstrucoesImpressao(self, instrucoes_impressao):
        if len(instrucoes_impressao) > 5:
            raise Exception('Máximo de 5 instruções.')
        self._instrucoes_impressao = instrucoes_impressao

    # Retorna um array com instruções (máximo 5) para impressão
    def getInstrucoesImpressao(self):
        if len(self._instrucoes_impressao) == 0:
            return []
        else:
            return [self._instrucoes_impressao[i] if (i < len(self._instrucoes_impressao)) else None for i in range(5)]

    #  Adiciona um demonstrativo (máximo 5)
    def addDescricaoDemonstrativo(self, descricaoDemonstrativo):
        if len(self.getDescricaoDemonstrativo()) > 5:
            raise Exception('Atingido o máximo de 5 demonstrativos.')

        self._descricaoDemonstrativo.append(descricaoDemonstrativo)

    # Define um array com a descrição do demonstrativo (máximo 5)
    def setDescricaoDemonstrativo(self, descricaoDemonstrativo):
        if len(descricaoDemonstrativo) > 5:
            raise Exception('Máximo de 5 demonstrativos.')
        self._descricaoDemonstrativo = descricaoDemonstrativo

    # Retorna um array com a descrição do demonstrativo (máximo 5)
    def getDescricaoDemonstrativo(self):
        return [self._descricaoDemonstrativo[i] if (i < len(self._descricaoDemonstrativo)) else None for i in range(5)]

    # Define o local de pagamento do boleto
    def setLocalPagamento(self, localPagamento):
        self._localPagamento = localPagamento

    # Retorna o local de pagamento do boleto
    def getLocalPagamento(self):
        return self._localPagamento

    # Define a moeda utilizada pelo boleto
    def setMoeda(self, moeda):
        self._moeda = moeda

    # Retorna a moeda utilizada pelo boleto
    def getMoeda(self):
        return self._moeda

    # Define o objeto do pagador
    def setPagador(self, pagador):
        self._pagador = Util.addPessoa(pagador)

    # Retorna o objeto do pagador
    def getPagador(self):
        return self._pagador

    # Define o objeto sacador avalista do boleto
    def setSacadorAvalista(self, sacadorAvalista):
        if sacadorAvalista is None:
            self._sacadorAvalista = None
        else:
            self._sacadorAvalista = Util.addPessoa(sacadorAvalista)

    # Retorna o objeto sacador avalista do boleto
    def getSacadorAvalista(self):
        return self._sacadorAvalista

    # Define o valor total do boleto (incluindo taxas)
    def setValor(self, valor):
        self._valor = Util.nFloat(valor, 2, False)

    # Retorna o valor total do boleto (incluindo taxas)
    def getValor(self):
        return Util.nFloat(self._valor, 2, False)

    # Define o desconto total do boleto (incluindo taxas)
    def setDesconto(self, desconto):
        self._desconto = Util.nFloat(desconto, 2, False)

    # Retorna o desconto total do boleto (incluindo taxas)
    def getDesconto(self):
        return Util.nFloat(self._desconto, 2, False)

    # Seta a % de multa
    def setMulta(self, multa):
        if multa:
            self._multa = float(multa)
        else:
            self._multa = 0.00

    # Retorna % de multa
    def getMulta(self):
        return self._multa

    # Seta a % de juros
    def setJuros(self, juros):
        if juros:
            self._juros = float(juros)
        else:
            self._juros = 0.00

    # Retorna % juros
    def getJuros(self):
        return self._juros

    # Retorna valor mora diária
    def getMoraDia(self):
        if self.getJuros() <= 0:
            return 0
        return Util.percent(self.getValor(), self.getJuros()) / 30

    # Seta a quantidade de dias apos o vencimento que cobra o juros
    def setJurosApos(self, jurosApos):
        if not jurosApos:
            self._jurosApos = 0
        else:
            jurosApos = int(jurosApos)
            self._jurosApos = jurosApos if jurosApos > 0 else 0

    # Retorna a quantidade de dias apos o vencimento que cobrar a juros
    def getJurosApos(self):
        return self._jurosApos if self._jurosApos else None

    # Seta dias para protesto
    def setDiasProtesto(self, diasProtesto):
        if self.getDiasBaixaAutomatica() > 0:
            raise Exception('Você deve usar dias de protesto ou dias de baixa, nunca os 2')
        if not diasProtesto:
            self._diasProtesto = 0
        diasProtesto = int(diasProtesto)
        self._diasProtesto = diasProtesto if diasProtesto > 0 else 0

    # Retorna os diasProtesto
    def getDiasProtesto(self, default=0):
        if self._diasProtesto:
            return default
        else:
            return self._diasProtesto if self._diasProtesto > 0 else default

    # Seta dias para baixa automática
    def setDiasBaixaAutomatica(self, baixaAutomatica):
        exception = f'O banco {self.__class__.__name__} não suporta baixa automática, ' \
                    f'pode usar também: setDiasProtesto({baixaAutomatica}) '
        raise Exception(exception)

    # Retorna os diasProtesto
    def getDiasBaixaAutomatica(self, default=0):
        return self._diasBaixaAutomatica if self._diasBaixaAutomatica else default

    # Define a localização do logotipo
    def setLogo(self, logo):
        self._logo = logo

    # Retorna a localização do logotipo
    def getLogo(self):
        if self._logo:
            return self._logo
        else:
            return "http://dummyimage.com/300x70/f5/0.png&text=Sem+Logo"

    # Retorna o logotipo em Base64, pronto para ser inserido na página
    def getLogoBase64(self):
        return 'data:image/' + Util.get_extension(self.getLogo()) \
               + ';base64,' + base64.b64encode(Util.get_content(self.getLogo())).decode('utf-8')

    # Retorna a localização do logotipo do banco relativo à pasta de imagens
    def getLogoBanco(self):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, '..', 'logos', self.getCodigoBanco() + '.png')
        return path

    def getStatus(self):
        return self._status

    # Marca o boleto para ser alterado no banco
    def alterarBoleto(self):
        self._status = BoletoContract.STATUS_ALTERACAO

    # Marca o boleto para alterar data vecimento no banco
    def alterarDataDeVencimento(self):
        self._status = BoletoContract.STATUS_ALTERACAO_DATA

    # Comandar instrução custom
    def comandarInstrucao(self, instrucao):
        self._status = BoletoContract.STATUS_CUSTOM
        self._status_custom = instrucao

    def getComando(self):
        return self._status_custom if self._status == BoletoContract.STATUS_CUSTOM else None

    # Marca o boleto para ser baixado no banco
    def baixarBoleto(self):
        self._status = BoletoContract.STATUS_BAIXA

    # Retorna o logotipo do banco em Base64, pronto para ser inserido na página
    def getLogoBancoBase64(self):
        return 'data:image/' + Util.get_extension(self.getLogoBanco()) \
               + ';base64,' + base64.b64encode(Util.get_content(self.getLogoBanco())).decode('utf-8')

    # Mostra exception ao erroneamente tentar setar o nosso número
    def setNossoNumero(self):
        raise Exception('Não é possível definir o nosso número diretamente. Utilize o método setNumero.')

    # Retorna o Nosso Número calculado.
    def getNossoNumero(self):
        if not self.campoNossoNumero:
            self.campoNossoNumero = self.gerarNossoNumero()
        return self.campoNossoNumero

    # Método que retorna o nosso numero usado no boleto. alguns bancos possuem algumas diferenças.
    def getNossoNumeroBoleto(self):
        return self.getNossoNumero()

    # Método onde o Boleto deverá gerar o Nosso Número.
    def gerarNossoNumero(self):
        pass

    # Método onde qualquer boleto deve extender para gerar o código da posição de 20 a 44
    def getCampoLivre(self):
        pass

    # Método que valida se o banco tem todos os campos obrigadotorios preenchidos
    def isValid(self):
        messages = ''
        for campo in self.camposObrigatorios:
            user_func = getattr(self, 'get' + campo.title(), None)
            test = user_func()
            if test is None or test == '':
                messages += f"Campo {campo} está em branco"
                return False, messages

        return True, messages

    # Retorna o campo Agência/Beneficiário do boleto
    def getAgenciaCodigoBeneficiario(self):

        if self.getAgenciaDv() is not None:
            agencia = self.getAgencia() + '-' + str(self.getAgenciaDv())
        else:
            agencia = self.getAgencia()

        if self.getContaDv() is not None:
            conta = self.getConta() + '-' + str(self.getContaDv())
        else:
            conta = self.getConta()

        return agencia + ' / ' + conta

    """
    Retorna o nome da carteira para impressão no boleto

    Caso o nome da carteira a ser impresso no boleto seja diferente do número
    Então crie uma variável na classe do banco correspondente $carteirasNomes
    sendo uma array cujos índices sejam os números das carteiras e os valores
    seus respectivos nomes
    """

    def getCarteiraNome(self):
        try:
            ret = self.carteirasNomes[self.getCarteira()]
        except:
            ret = self.getCarteira()

        return ret

    # Retorna o codigo de barras
    def getCodigoBarras(self):
        if self._campoCodigoBarras:
            return self._campoCodigoBarras

        ret, messages = self.isValid()
        if not ret:
            raise Exception('Campos requeridos pelo banco, aparentam estar ausentes ' + messages)

        codigo = (Util.numberFormatGeral(self.getCodigoBanco(), 3)
                  + str(self.getMoeda())
                  + str(Util.fatorVencimento(self.getDataVencimento()))
                  + Util.numberFormatGeral(self.getValor(), 10)
                  + self.getCampoLivre())

        resto = Util.modulo11(codigo, 2, 9, 0)
        dv = 1 if resto in [0, 10, 11] else resto

        self._campoCodigoBarras = codigo[:4] + str(dv) + codigo[4:]
        return self._campoCodigoBarras

    # Retorna o código do banco com o dígito verificador
    def getCodigoBancoComDv(self):
        codigoBanco = self.getCodigoBanco()

        semX = [BoletoContract.COD_BANCO_CEF]
        x10 = 0 if codigoBanco in semX else 'X'

        return codigoBanco + '-' + str(Util.modulo11(codigoBanco, 2, 9, 0, x10))

    # Retorna a linha digitável do boleto
    def getLinhaDigitavel(self):
        if self._campoLinhaDigitavel:
            return self._campoLinhaDigitavel

        codigo = self.getCodigoBarras()

        s1 = codigo[:4] + codigo[19:19 + 5]
        s1 = s1 + str(Util.modulo10(s1))
        s1 = s1[:5] + '.' + s1[5:]

        s2 = codigo[24:24 + 10]
        s2 = s2 + str(Util.modulo10(s2))
        s2 = s2[:5] + '.' + s2[5:]

        s3 = codigo[34:34 + 10]
        s3 = s3 + str(Util.modulo10(s3))
        s3 = s3[:5] + '.' + s3[5:]

        s4 = codigo[4]

        s5 = codigo[5:5 + 14]

        self._campoLinhaDigitavel = f'{s1} {s2} {s3} {s4} {s5}'

        return self._campoLinhaDigitavel

    # Retorna se a segunda linha contendo o endereço do beneficiário deve ser exibida na ficha de compensação
    def getMostrarEnderecoFichaCompensacao(self):
        return self._mostrarEnderecoFichaCompensacao

    # Seta se a segunda linha contendo o endereço do beneficiário deve ser exibida na ficha de compensação
    def setMostrarEnderecoFichaCompensacao(self, mostrarEnderecoFichaCompensacao):
        self.mostrarEnderecoFichaCompensacao = mostrarEnderecoFichaCompensacao

    # Render PDF
    def renderPDF(self, file, print=False, instrucoes=True):
        pdf = BoletoPDF(file)
        pdf.drawBoleto(self)
        pdf.save()

    # Render HTML
    def renderHTML(self, print=False, instrucoes=True):
        raise NotImplementedError("TODO")

    # Return Boleto Dict.
    def toDict(self):
        sacadorAvalista = self.getSacadorAvalista()
        if sacadorAvalista:
            sacadorAvalistaDict = {
                'nome': sacadorAvalista.getNome(),
                'endereco': sacadorAvalista.getEndereco(),
                'bairro': sacadorAvalista.getBairro(),
                'cep': sacadorAvalista.getCep(),
                'uf': sacadorAvalista.getUf(),
                'cidade': sacadorAvalista.getCidade(),
                'documento': sacadorAvalista.getDocumento(),
                'nome_documento': sacadorAvalista.getNomeDocumento(),
                'endereco2': sacadorAvalista.getCepCidadeUf(),
                'endereco_completo': sacadorAvalista.getEnderecoCompleto(),
            }
        else:
            sacadorAvalistaDict = dict()

        return {
            **{
                'linha_digitavel': self.getLinhaDigitavel(),
                'codigo_barras': self.getCodigoBarras(),
                'beneficiario': {
                    'nome': self.getBeneficiario().getNome(),
                    'endereco': self.getBeneficiario().getEndereco(),
                    'bairro': self.getBeneficiario().getBairro(),
                    'cep': self.getBeneficiario().getCep(),
                    'uf': self.getBeneficiario().getUf(),
                    'cidade': self.getBeneficiario().getCidade(),
                    'documento': self.getBeneficiario().getDocumento(),
                    'nome_documento': self.getBeneficiario().getNomeDocumento(),
                    'endereco2': self.getBeneficiario().getCepCidadeUf(),
                    'endereco_completo': self.getBeneficiario().getEnderecoCompleto(),
                },
                'logo_base64': self.getLogoBase64(),
                'logo': self.getLogo(),
                'logo_banco_base64': self.getLogoBancoBase64(),
                'logo_banco': self.getLogoBanco(),
                'codigo_banco': self.getCodigoBanco(),
                'codigo_banco_com_dv': self.getCodigoBancoComDv(),
                'especie': 'R$',
                'data_vencimento': self.getDataVencimento(),
                'data_processamento': self.getDataProcessamento(),
                'data_documento': self.getDataDocumento(),
                'data_desconto': self.getDataDesconto(),
                'valor': Util.nReal(self.getValor(), 2, False),
                'desconto': Util.nReal(self.getDesconto(), 2, False),
                'multa': Util.nReal(self.getMulta(), 2, False),
                'juros': Util.nReal(self.getJuros(), 2, False),
                'juros_apos': self.getJurosApos(),
                'dias_protesto': self.getDiasProtesto(),
                'sacador_avalista': sacadorAvalistaDict,
                'pagador': {
                    'nome': self.getPagador().getNome(),
                    'endereco': self.getPagador().getEndereco(),
                    'bairro': self.getPagador().getBairro(),
                    'cep': self.getPagador().getCep(),
                    'uf': self.getPagador().getUf(),
                    'cidade': self.getPagador().getCidade(),
                    'documento': self.getPagador().getDocumento(),
                    'nome_documento': self.getPagador().getNomeDocumento(),
                    'endereco2': self.getPagador().getCepCidadeUf(),
                    'endereco_completo': self.getPagador().getEnderecoCompleto(),
                },
                'demonstrativo': self.getDescricaoDemonstrativo(),
                'instrucoes': self.getInstrucoes(),
                'instrucoes_impressao': self.getInstrucoesImpressao(),
                'local_pagamento': self.getLocalPagamento(),
                'numero': self.getNumero(),
                'numero_documento': self.getNumeroDocumento(),
                'numero_controle': self.getNumeroControle(),
                'agencia_codigo_beneficiario': self.getAgenciaCodigoBeneficiario(),
                'nosso_numero': self.getNossoNumero(),
                'nosso_numero_boleto': self.getNossoNumeroBoleto(),
                'especie_doc': self.getEspecieDoc(),
                'especie_doc_cod': self.getEspecieDocCodigo(),
                'aceite': self.getAceite(),
                'carteira': self.getCarteira(),
                'carteira_nome': self.getCarteiraNome(),
                'uso_banco': self.getUsoBanco(),
                'status': self.getStatus(),
                'mostrar_endereco_ficha_compensacao': self.getMostrarEnderecoFichaCompensacao()
            },
            **self._variaveis_adicionais
        }
