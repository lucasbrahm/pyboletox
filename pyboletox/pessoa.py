from pyboletox.Contracts.pessoa import IPessoa
from pyboletox.util import Util


class Pessoa(IPessoa):
    def __init__(self, d) -> None:
        super().__init__()
        self._nome = d.get('nome')
        self._endereco = d.get('endereco')
        self._bairro = d.get('bairro')
        self._cep = d.get('cep')
        self._uf = d.get('uf')
        self._cidade = d.get('cidade')
        self._documento = d.get('documento')
        self._dda = False

    @staticmethod
    def create(nome, documento, endereco=None, bairro=None, cep=None, cidade=None, uf=None):
        return Pessoa({
            'nome': nome,
            'documento': documento,
            'endereco': endereco,
            'bairro': bairro,
            'cep': cep,
            'cidade': cidade,
            'uf': uf
        })

    # Define o CEP
    def setCep(self, cep):
        self._cep = cep
        return self

    # Retorna o CEP
    def getCep(self):
        if self._cep is None:
            return None
        return Util.maskString(Util.numbersOnly(self._cep), '#####-###')

    # Define a cidade
    def setCidade(self, cidade):
        self._cidade = cidade
        return self

    # Retorna a cidade
    def getCidade(self):
        return self._cidade

    # Define o documento (CPF, CNPJ ou CEI)
    def setDocumento(self, documento):
        documento = Util.numbersOnly(documento)[:14]
        if len(documento) not in [10, 11, 14, 0]:
            raise Exception('Documento inválido')
        self._documento = documento
        return self

    # Retorna o documento (CPF ou CNPJ)
    def getDocumento(self):
        if self.getTipoDocumento() == 'CPF':
            return Util.maskString(Util.numbersOnly(self._documento), '###.###.###-##')
        elif self.getTipoDocumento() == 'CEI':
            return Util.maskString(Util.numbersOnly(self._documento), '##.#####.#-##')
        return Util.maskString(Util.numbersOnly(self._documento), '##.###.###/####-##')

    # Define o endereço
    def setEndereco(self, endereco):
        self._endereco = endereco
        return self

    # Retorna o endereço
    def getEndereco(self):
        return self._endereco

    # Define o bairro
    def setBairro(self, bairro):
        self._bairro = bairro
        return self

    # Retorna o bairro
    def getBairro(self):
        return self._bairro

    # Define o nome
    def setNome(self, nome):
        self._nome = nome
        return self

    # Retorna o nome
    def getNome(self):
        return self._nome

    # Define a UF
    def setUf(self, uf):
        self._uf = uf
        return self

    # Retorna a UF
    def getUf(self):
        return self._uf

    # Retorna o nome e o documento formatados
    def getNomeDocumento(self):
        if not self.getDocumento():
            return self.getNome()
        else:
            return self.getNome() + ' / ' + self.getTipoDocumento() + ': ' + self.getDocumento()

    # Retorna se o tipo do documento é CPF ou CNPJ ou Documento
    def getTipoDocumento(self):
        cpf_cnpj_cei = Util.numbersOnly(self._documento)

        if len(cpf_cnpj_cei) == 11:
            return 'CPF'
        elif len(cpf_cnpj_cei) == 10:
            return 'CEI'

        return 'CNPJ'

    # Retorna o endereço formatado para a linha 2 de endereço
    def getCepCidadeUf(self):
        dados = list(filter(None, [self.getCep(), self.getCidade(), self.getUf()]))
        return ' - '.join(dados)

    # Retorna o endereço completo em uma única string
    def getEnderecoCompleto(self):
        dados = list(
            filter(None, [self.getEndereco(), self.getBairro(), self.getCidade(), self.getUf(), self.getCep()]))
        return ' - '.join(dados)

    def isDda(self):
        return self._dda

    def setDda(self, dda):
        self._dda = dda

    def toDict(self):
        return {
            'nome': self.getNome(),
            'endereco': self.getEndereco(),
            'bairro': self.getBairro(),
            'cep': self.getCep(),
            'uf': self.getUf(),
            'cidade': self.getCidade(),
            'documento': self.getDocumento(),
            'nome_documento': self.getNomeDocumento(),
            'endereco2': self.getCepCidadeUf(),
            'endereco_completo': self.getEnderecoCompleto(),
            'dda': self.isDda(),
        }
