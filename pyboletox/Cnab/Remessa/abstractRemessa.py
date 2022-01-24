import os
from abc import ABCMeta, abstractmethod
from datetime import datetime
from pyboletox.util import Util


class AbstractRemessa(metaclass=ABCMeta):    

    HEADER = 'header'
    HEADER_LOTE = 'header_lote'
    DETALHE = 'detalhe'
    TRAILER_LOTE = 'trailer_lote'
    TRAILER = 'trailer'

    def __init__(self) -> None:

        # Campos que são necessários para a remessa
        self.camposObrigatorios = [
            'carteira',
            'agencia',
            'conta',
            'beneficiario',
        ]

        self.boletos = []

        # Código do banco
        self._codigoBanco = ''

        # Contagem dos registros Detalhes
        self.iRegistros = 0

        # Array contendo o cnab.
        self.aRegistros = {
            self.HEADER: '',
            self.DETALHE: {},
            self.TRAILER: ''
        }

        # Variavel com ponteiro para linha que esta sendo editada.
        self.atual = None

        # Caracter de fim de linha
        self.fimLinha = "\n"

        # Caracter de fim de arquivo
        self.fimArquivo = None

        # ID do arquivo remessa, sequencial.
        self._idremessa = None

        # A data que será informada no header da remessa
        self._dataRemessa = None

        # Agência
        self._agencia = None

        # Conta
        self._conta = None

        # Dígito da conta
        self._contaDv = None

        # Carteira de cobrança.
        self._carteira = None

        # Define as carteiras disponíveis para cada banco
        self._carteiras = []

        # Entidade beneficiario (quem esta gerando a remessa)
        self._beneficiario = None

    # Inicializa object realizando os 'set' com os parametros no kwargs
    def init(self, **kwargs):
        for k, v in kwargs.items():
            f = getattr(self, 'set' + k[0].upper() + k[1:], None)
            if f is not None:
                f(v)

    # Informa a data da remessa a ser gerada
    def setDataRemessa(self, data):
        self._dataRemessa = data

    # Retorna a data da remessa a ser gerada
    def getDataRemessa(self, format):
        if self._dataRemessa is None:
            return datetime.now().strftime(format)
        return self._dataRemessa.strftime(format)

    # Retorna o código do banco
    def getCodigoBanco(self):
        return self._codigoBanco

    def getIdremessa(self):
        return self._idremessa

    def setIdremessa(self, idremessa):
        self._idremessa = idremessa

    def getBeneficiario(self):
        return self._beneficiario

    def setBeneficiario(self, beneficiario):
        self._beneficiario = Util.addPessoa(beneficiario)

    # Define a agência
    def setAgencia(self, agencia):
        self._agencia = str(agencia)

    # Retorna a agência
    def getAgencia(self):
        return self._agencia

    # Define o número da conta
    def setConta(self, conta):
        self._conta = str(conta)

    # Retorna o número da conta
    def getConta(self):
        return self._conta

    # Define o dígito verificador da conta
    def setContaDv(self, contaDv):
        self._contaDv = str(contaDv)[-1]

    # Retorna o dígito verificador da conta
    def getContaDv(self):
        return self._contaDv

    # Define o código da carteira (Com ou sem registro)
    def setCarteira(self, carteira):
        carteira = str(carteira)
        if carteira not in self.getCarteiras():
            raise Exception("Carteira não disponível!")
        self._carteira = carteira

    # Retorna o código da carteira (Com ou sem registro)
    def getCarteira(self):
        return self._carteira

    # Retorna o código da carteira (Com ou sem registro)
    def getCarteiraNumero(self):
        return self._carteira

    # Retorna as carteiras disponíveis para este banco
    def getCarteiras(self):
        return self._carteiras

    # Método que valida se o banco tem todos os campos obrigatórios preenchidos
    def isValid(self):
        messages = ''
        for campo in self.camposObrigatorios:
            user_func = getattr(self, 'get' + campo.title(), None)
            test = user_func()
            if test is None or test == '':
                messages += f"Campo {campo} está em branco"
                return False, messages

        return True, messages

    def add(self, i, f, value):
        if self.atual == self.DETALHE:
            self.aRegistros[self.atual][self.iRegistros] = Util.adiciona(self.aRegistros[self.atual][self.iRegistros], i, f, value)
            return self.aRegistros[self.atual][self.iRegistros]
        else:
            self.aRegistros[self.atual] = Util.adiciona(self.aRegistros[self.atual], i, f, value)
            return self.aRegistros[self.atual]

    # Retorna o header do arquivo.
    def getHeader(self):
        return self.aRegistros[self.HEADER]

    # Retorna os detalhes do arquivo
    def getDetalhes(self):
        return self.aRegistros[self.DETALHE]

    # Retorna o trailer do arquivo.
    def getTrailer(self):
        return self.aRegistros[self.TRAILER]

    #  Valida se a linha esta correta.
    def valida(self, a):
        if self.tamanho_linha is None:
            raise Exception('Classe remessa deve informar o tamanho da linha')
        
        if len(a) != self.tamanho_linha:
            raise Exception(f'array não possui {self.tamanho_linha} posições, possui: {len(a)}')
        return a

    # Gera o arquivo, retorna a string.
    @abstractmethod
    def gerar(self):
        pass

    #  Salva o arquivo no path informado
    def save(self, path):
        folder = os.path.dirname(path)
        if folder and not os.path.isdir(folder):
            os.makedirs(folder, mode=0o777, exist_ok=True)

        string = self.gerar()
        with open(path, 'wb') as f:
            f.write(string)
