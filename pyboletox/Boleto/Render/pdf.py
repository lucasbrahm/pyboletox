import os

from reportlab.graphics.barcode.common import I2of5
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A4, landscape as pagesize_landscape
from reportlab.lib.units import mm, cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from pyboletox.util import Util

class BoletoPDF(object):

    def __init__(self, file_descr, landscape=False):
        self.width = 190 * mm
        self.width_canhoto = 70 * mm
        self.height_line = 6.5 * mm
        self.space = 1 * mm
        self.font_size_title = 9
        self.font_size_value = 9
        self.delta_title = self.height_line - (self.font_size_title + 1)
        self.delta_font = self.font_size_value + 1
        #self.font_title = 'Helvetica-Bold'
        self.font_title = 'Times-Bold'
        #self.font_value = 'Helvetica'
        self.font_value = 'Times-Roman'

        if landscape:
            pagesize = pagesize_landscape(A4)
        else:
            pagesize = A4

        self.pdf_canvas = canvas.Canvas(file_descr, pagesize=pagesize)
        self.pdf_canvas.setStrokeColor(black)


    def _drawHorizontalCorteLine(self, x, y, width):
        self.pdf_canvas.saveState()
        self.pdf_canvas.translate(x, y)

        self.pdf_canvas.setLineWidth(1)
        self.pdf_canvas.setDash(1, 2)
        self.__horizontalLine(0, 0, width)

        self.pdf_canvas.restoreState()

    def _drawVerticalCorteLine(self, x, y, height):
        self.pdf_canvas.saveState()
        self.pdf_canvas.translate(x, y)

        self.pdf_canvas.setLineWidth(1)
        self.pdf_canvas.setDash(1, 2)
        self.__verticalLine(0, 0, height)

        self.pdf_canvas.restoreState()

    def _drawRecibo(self, boleto, x, y):

        start_x = x
        start_y = y

        self.pdf_canvas.saveState()

        self.pdf_canvas.translate(x, y)

        # height to 3 lines (Nome do pagador, Endereço, Sacador/Avalista) and a margin between texts and box
        height_pagador_box = 3 * self.font_size_value + 4 * self.space

        #y = height_barcode + margin_barcode
        self.pdf_canvas.rect(0, 0, self.width, height_pagador_box, stroke=1, fill=0)

        y = 1 * self.space
        x = 1 * self.space
        text = "Sacador/Avalista:"
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x, y, text)
        text_size = self.pdf_canvas.stringWidth(text)
        x += text_size

        # Just to calculate 30 characters of offset
        offset_cnpjcpf = self.pdf_canvas.stringWidth('W' * 30)

        x += self.space
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        text = boleto.getSacadorAvalista().getNome() if boleto.getSacadorAvalista() else ''
        self.pdf_canvas.drawString(x, y, self._truncate_text_in_size(text, offset_cnpjcpf))

        x += offset_cnpjcpf
        x += self.space
        text = "CNPJ/CPF "
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x, y, text)
        text_size = self.pdf_canvas.stringWidth(text)
        x += text_size

        text = boleto.getSacadorAvalista().getDocumento() if boleto.getSacadorAvalista() else ''
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawString(x, y, text)

        y += self.space + self.font_size_value
        text = "Endereço:"
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(1 * self.space, y, text)
        text_size = self.pdf_canvas.stringWidth(text)

        text = boleto.getPagador().getEnderecoCompleto()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawString(2 * self.space + text_size, y, text)

        y += self.space + self.font_size_value
        x = self.space
        text = "Nome do Pagador: "
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x, y, text)
        x += self.pdf_canvas.stringWidth(text)

        text = boleto.getPagador().getNome()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawString(x, y, self._truncate_text_in_size(text, offset_cnpjcpf))

        x += offset_cnpjcpf
        x += self.space
        text = "CNPJ/CPF "
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x, y, text)
        x += self.pdf_canvas.stringWidth(text)

        text = boleto.getPagador().getDocumento()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawString(x, y, text)

        # Instruções
        width_left = 150 * mm
        # height of cells: (-) Desconto/Abatimento, (+) Juros/Multa, (=) Valor Pago
        height_cell = 3 * self.space + self.font_size_value + self.font_size_value
        start_y_instrucoes_box = height_pagador_box
        self.pdf_canvas.rect(0, start_y_instrucoes_box, width_left, 3 * height_cell)

        y = start_y_instrucoes_box + 3 * height_cell - (self.space + self.font_size_value)
        self.pdf_canvas.drawString(self.space, y, "Instruções de responsabilidade do BENEFICIÁRIO."
                                                  " Qualquer dúvida sobre este Boleto, contate o BENEFICIÁRIO.")
        y -= self.space  # Extra space

        instrucoes = boleto.getInstrucoes()
        for instrucao in instrucoes:
            if instrucao is None:
                continue
            y -= (self.space + self.font_size_value)
            self.pdf_canvas.drawString(self.space, y, self._truncate_text_in_size(instrucao, width_left - self.space))

        x_right_width = self.width - width_left

        # Valor Pago
        self.pdf_canvas.rect(width_left, start_y_instrucoes_box, x_right_width, height_cell)
        y = start_y_instrucoes_box + height_cell
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(width_left + self.space, y - self.font_size_title - self.space, '(=) Valor Pago')
        text = ''
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawRightString(self.width - 2*self.space, start_y_instrucoes_box + self.space, text)

        # Juros/Multa
        self.pdf_canvas.rect(width_left, start_y_instrucoes_box + height_cell, x_right_width, height_cell)
        y += height_cell
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(width_left + self.space, y - self.font_size_title - self.space, '(+) Juros/Multa')
        text = ''
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawRightString(self.width - 2 * self.space,
                                        start_y_instrucoes_box + height_cell + self.space, text)

        # Descontos/Abatimento
        self.pdf_canvas.rect(width_left, start_y_instrucoes_box + 2*height_cell, x_right_width, height_cell)
        y += height_cell
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(width_left + self.space, y - self.font_size_title - self.space,
                                   '(-) Descontos/Abatimento')
        text = ''
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawRightString(self.width - 2 * self.space,
                                        start_y_instrucoes_box + 2*height_cell + self.space, text)

        # Uso do banco
        text = boleto.getUsoBanco() if boleto.getUsoBanco() else ''
        width_left2 = width_left / 4
        x = 0
        y = start_y_instrucoes_box + 3 * height_cell
        self.pdf_canvas.rect(x, y, width_left2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Uso do Banco')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 2, y + self.space, text)

        text = boleto.getCarteiraNome()
        x += width_left2
        self.pdf_canvas.rect(x, y, width_left2 / 2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Carteira')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 4, y + self.space, text)

        text = 'R$'
        x += width_left2 / 2
        self.pdf_canvas.rect(x, y, width_left2 / 2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Espécie')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 4, y + self.space, text)

        # Quantidade
        text = ''
        x += width_left2 / 2
        self.pdf_canvas.rect(x, y, width_left2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Quantidade')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 2, y + self.space, text)

        text = Util.nReal(boleto.getValor()) if boleto.getCodigoBanco() == '001' else ''
        x += width_left2
        self.pdf_canvas.rect(x, y, width_left2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Valor')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 2, y + self.space, text)

        text = Util.nReal(boleto.getValor())
        text = text[3:]  # remove 'R$ '
        x += width_left2
        self.pdf_canvas.rect(x, y, x_right_width, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space,
                                   '(=) Valor do Documento')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawRightString(x + x_right_width - 2 * self.space, y + self.space, text)

        y += height_cell
        x = 0
        self.pdf_canvas.rect(x, y, width_left2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space,
                                   'Data do documento')
        text = boleto.getDataDocumento().strftime('%d/%m/%Y')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 2, y + self.space, text)

        x += width_left2
        self.pdf_canvas.rect(x, y, width_left2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space,
                                   'Núm. do documento')
        text = boleto.getNumeroDocumento()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 2, y + self.space, text)

        x += width_left2
        self.pdf_canvas.rect(x, y, width_left2 * 0.625, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Espécie doc.')
        text = boleto.getEspecieDoc()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 * 0.625 / 2, y + self.space, text)

        x += width_left2 * 0.625
        self.pdf_canvas.rect(x, y, width_left2 * 0.375, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space, 'Aceite')
        text = boleto.getAceite()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 * 0.375 / 2, y + self.space, 'N')

        x += width_left2 * 0.375
        self.pdf_canvas.rect(x, y, width_left2, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space,
                                   'Data Processamento')
        text = boleto.getDataProcessamento().strftime('%d/%m/%Y')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawCentredString(x + width_left2 / 2, y + self.space, text)

        x += width_left2
        self.pdf_canvas.rect(x, y, x_right_width, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space,
                                   'Nosso Número')
        text = boleto.getNossoNumeroBoleto()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawRightString(x + x_right_width - 2 * self.space, y + self.space, text)

        y += height_cell
        x = 0
        # size to 1 title + 2 value lines + space between things
        height_cell = 4 * self.space + self.font_size_title + 2*self.font_size_value
        self.pdf_canvas.rect(x, y, width_left, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.font_size_title - self.space,
                                   'Nome do beneficiário / CNPJ / CPF / Endereço:')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        text = boleto.getBeneficiario().getNome()
        self.pdf_canvas.drawString(x + self.space, y + 2 * self.space + self.font_size_value,
                                   self._truncate_text_in_size(text, offset_cnpjcpf))
        text = boleto.getBeneficiario().getTipoDocumento() + " " + boleto.getBeneficiario().getDocumento()
        self.pdf_canvas.drawString(x + 2 * self.space + offset_cnpjcpf, y + 2 * self.space + self.font_size_value,
                                   text)
        text = boleto.getBeneficiario().getEnderecoCompleto()
        self.pdf_canvas.drawString(x + self.space, y + self.space,
                                   text)

        x += width_left
        self.pdf_canvas.rect(x, y, x_right_width, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.space - self.font_size_title,
                                   'Agência/Código Beneficiário')

        text = boleto.getAgenciaCodigoBeneficiario()
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        self.pdf_canvas.drawRightString(x + x_right_width - 2 * self.space, y + self.space, text)

        y += height_cell
        x = 0
        height_cell = 4*self.space + self.font_size_title + 2*self.font_size_value
        y2 = y + height_cell - self.font_size_title - self.space
        self.pdf_canvas.rect(x, y, width_left, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y2,
                                   'Local de Pagamento')
        self.pdf_canvas.setFont(self.font_value, self.font_size_value)
        text = boleto.getLocalPagamento()
        texts = self._split_text_in_size(text, width_left - self.space)
        texts = texts[:2]  # max 2 lines
        for text in texts:
            y2 -= (self.space + self.font_size_value)
            self.pdf_canvas.drawString(x + self.space, y2, text)

        x += width_left
        self.pdf_canvas.rect(x, y, x_right_width, height_cell)
        self.pdf_canvas.setFont(self.font_title, self.font_size_title)
        self.pdf_canvas.drawString(x + self.space, y + height_cell - self.space - self.font_size_title,
                                   'Data de Vencimento')
        text = boleto.getDataVencimento().strftime('%d/%m/%Y')
        self.pdf_canvas.setFont(self.font_title, self.font_size_title * 1.3)
        self.pdf_canvas.drawRightString(x + x_right_width - 2 * self.space, y + self.space, text)

        y += height_cell
        height_cell = 3*self.space + self.font_size_title + self.font_size_value
        file_path = boleto.getLogoBanco()
        ret = utils.getImageData(file_path)
        aspect = float(ret[1]) / ret[0]
        image_new_height = aspect*width_left2
        image_size = self.pdf_canvas.drawImage(file_path,
                                               0, y+1,
                                               width=width_left2,
                                               height=image_new_height,
                                               preserveAspectRatio=False)
        self.pdf_canvas.line(width_left2, y, width_left2, y + height_cell)

        x = width_left2
        text = boleto.getCodigoBancoComDv()
        self.pdf_canvas.setFont(self.font_title, self.font_size_title * 1.8)
        self.pdf_canvas.drawCentredString(x + width_left2 / 4, y + 2*self.space, text)

        x += width_left2 / 2
        self.pdf_canvas.line(x, y, x, y + height_cell)

        text = boleto.getLinhaDigitavel()
        self.pdf_canvas.setFont(self.font_title, self.font_size_title * 1.5)
        self.pdf_canvas.drawCentredString(x + (self.width - x) / 2, y + 2*self.space, text)

        self.pdf_canvas.restoreState()
        return start_x, start_y + y + max(image_new_height, height_cell)

    def _drawFooterCompensacao(self, boleto, x, y):

        start_x = x
        start_y = y

        self.pdf_canvas.saveState()
        self.pdf_canvas.translate(x, y)
        self._codigoBarraI25(boleto.getCodigoBarras(), 0 + 2*self.space, 0)

        height_barcode = 13 * mm
        margin_barcode = 2 * self.space
        font_size = self.font_size_title * 1.5

        self.pdf_canvas.setFont(self.font_title, font_size)
        y = height_barcode + margin_barcode - font_size - self.space
        self.pdf_canvas.drawRightString(
            self.width - 2 * mm,  # margin 2 mm right
            y,
            'Ficha de Compensação'
        )

        font_size = self.font_size_title
        self.pdf_canvas.setFont(self.font_title, font_size)
        y = y - self.font_size_title - 1 * self.space
        self.pdf_canvas.drawRightString(
            self.width - 2 * self.space,
            y,
            'Autenticação Mecânica'
        )

        self.pdf_canvas.restoreState()
        return start_x, start_y + height_barcode + margin_barcode

    def _drawHeaderReciboPagador(self, x, y):
        start_x = x
        start_y = y

        self.pdf_canvas.saveState()
        self.pdf_canvas.translate(x, y)

        self.pdf_canvas.setFont(self.font_title, self.font_size_title*1.3)
        self.pdf_canvas.drawRightString(self.width - 2*self.space, -self.space, "Recibo do pagador")

        self.pdf_canvas.restoreState()

    def drawBoleto(self, boleto):
        x = 9 * mm  # margem esquerda
        y = 12 * mm  # margem inferior
        y += 30 * mm

        x, y = self._drawFooterCompensacao(boleto, x, y)

        #self._drawHorizontalCorteLine(x, y, self.width)
        #y += 4 * mm  # distancia entre linha de corte e barcode

        d = self._drawRecibo(boleto, x, y)
        y = d[1] + (12 * mm)  # distancia entre Recibo caixa e linha de corte
        #y = d[1]

        self._drawHorizontalCorteLine(d[0], y, self.width)

        y += 12 * mm

        d = self._drawRecibo(boleto, x, y)

        y = d[1]
        self._drawHeaderReciboPagador(x, y)

        title = "%s - %s" % (boleto.getPagador().getNome(),
                             boleto.getNumeroDocumento())
        self.pdf_canvas.setTitle(title)
        return self.width, y

    def _truncate_text_in_size(self, text, size):
        str_len = len(text)
        while self.pdf_canvas.stringWidth(text[:str_len]) > size:
            str_len -= 1
            if str_len == 0:
                return ""
        return text[:str_len]

    def _split_text_in_size(self, text, size):
        texts = []
        str_len = len(text)
        total = 0
        while total < str_len:
            i = len(text)
            while self.pdf_canvas.stringWidth(text[:i]) > size:
                i -= 1
                if i == 0:
                    return []
            texts.append(text[:i])
            total += i
            text = text[i:]
        return texts


    def nextPage(self):
        """Força início de nova página"""

        self.pdf_canvas.showPage()

    def save(self):
        """Fecha boleto e constroi o arquivo"""

        self.pdf_canvas.save()

    def __horizontalLine(self, x, y, width):
        self.pdf_canvas.line(x, y, x + width, y)

    def __verticalLine(self, x, y, width):
        self.pdf_canvas.line(x, y, x, y + width)

    def _formataValorParaExibir(self, nfloat):
        if nfloat:
            txt = nfloat
            txt = txt.replace('.', ',')
        else:
            txt = ""
        return txt

    def _codigoBarraI25(self, num, x, y):
        """Imprime Código de barras otimizado para boletos

        O código de barras é otmizado para que o comprimento seja sempre o
        estipulado pela Febraban de 103mm.

        """
        # http://en.wikipedia.org/wiki/Interleaved_2_of_5

        altura = 13 * mm
        comprimento = 103 * mm

        thin_bar = 0.254320987654 * mm  # Tamanho correto aproximado

        bc = I2of5(num,
                   barWidth=thin_bar,
                   ratio=3,
                   barHeight=altura,
                   bearers=0,
                   quiet=0,
                   checksum=0)

        # Recalcula o tamanho do thin_bar para que o cod de barras tenha o
        # comprimento correto
        thin_bar = (thin_bar * comprimento) / bc.width
        bc.__init__(num, barWidth=thin_bar)

        bc.drawOn(self.pdf_canvas, x, y)

