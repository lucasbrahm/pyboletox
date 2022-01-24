from ..abstractRemessa import AbstractRemessa


class AbstractRemessaCnab400(AbstractRemessa):
    def __init__(self) -> None:
        super().__init__()
        self.tamanho_linha = 400

    # Inicia a edição do header
    def iniciaHeader(self):
        self.aRegistros[self.HEADER] = ' ' * self.tamanho_linha
        self.atual = self.HEADER

    def iniciaTrailer(self):
        self.aRegistros[self.TRAILER] = ' ' * self.tamanho_linha
        self.atual = self.TRAILER

    def getCountDetalhes(self):
        return len(self.aRegistros[self.DETALHE])

    def getCount(self):
        return self.getCountDetalhes() + 2

    def iniciaDetalhe(self):
        self.iRegistros += 1
        self.aRegistros[self.DETALHE][self.iRegistros] = ' ' * self.tamanho_linha
        self.atual = self.DETALHE

    def gerar(self):
        ret, messages = self.isValid()
        if not ret:
            raise Exception('Campos requeridos pelo banco, aparentam estar ausentes ' + messages)

        stringRemessa = ''
        if self.iRegistros < 1:
            raise Exception('Nenhuma linha detalhe foi adicionada')

        self.header()
        stringRemessa += self.valida(self.getHeader()) + self.fimLinha

        for i, detalhe in self.getDetalhes().items():
            stringRemessa += self.valida(detalhe) + self.fimLinha

        self.trailer()
        stringRemessa += self.valida(self.getTrailer()) + self.fimArquivo

        return stringRemessa.encode(encoding='utf-8')

