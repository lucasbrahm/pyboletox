import os
import re
import math
import unicodedata
from datetime import datetime
from pyboletox.Contracts.Boleto.boleto import Boleto as BoletoContract


class Util:
    bancos = {
        '246': 'Banco ABC Brasil S.A.',
        '025': 'Banco Alfa S.A.',
        '641': 'Banco Alvorada S.A.',
        '029': 'Banco Banerj S.A.',
        '000': 'Banco Bankpar S.A.',
        '740': 'Banco Barclays S.A.',
        '107': 'Banco BBM S.A.',
        '031': 'Banco Beg S.A.',
        '739': 'Banco BGN S.A.',
        '096': 'Banco BM&F de Serviços de Liquidação e Custódia S.A',
        '318': 'Banco BMG S.A.',
        '752': 'Banco BNP Paribas Brasil S.A.',
        '248': 'Banco Boavista Interatlântico S.A.',
        '218': 'Banco Bonsucesso S.A.',
        '065': 'Banco Bracce S.A.',
        '036': 'Banco Bradesco BBI S.A.',
        '204': 'Banco Bradesco Cartões S.A.',
        '394': 'Banco Bradesco Financiamentos S.A.',
        '237': 'Banco Bradesco S.A.',
        '225': 'Banco Brascan S.A.',
        '208': 'Banco BTG Pactual S.A.',
        '044': 'Banco BVA S.A.',
        '263': 'Banco Cacique S.A.',
        '473': 'Banco Caixa Geral - Brasil S.A.',
        '040': 'Banco Cargill S.A.',
        '233': 'Banco Cifra S.A.',
        '745': 'Banco Citibank S.A.',
        'M08': 'Banco Citicard S.A.',
        'M19': 'Banco CNH Capital S.A.',
        '215': 'Banco Comercial e de Investimento Sudameris S.A.',
        '756': 'Banco Cooperativo do Brasil S.A. - BANCOOB',
        '748': 'Banco Cooperativo Sicredi S.A.',
        '222': 'Banco Credit Agricole Brasil S.A.',
        '505': 'Banco Credit Suisse (Brasil) S.A.',
        '229': 'Banco Cruzeiro do Sul S.A.',
        '003': 'Banco da Amazônia S.A.',
        '083': 'Banco da China Brasil S.A.',
        '707': 'Banco Daycoval S.A.',
        'M06': 'Banco de Lage Landen Brasil S.A.',
        '024': 'Banco de Pernambuco S.A. - BANDEPE',
        '456': 'Banco de Tokyo-Mitsubishi UFJ Brasil S.A.',
        '214': 'Banco Dibens S.A.',
        '001': 'Banco do Brasil S.A.',
        '047': 'Banco do Estado de Sergipe S.A.',
        '037': 'Banco do Estado do Pará S.A.',
        '041': 'Banco do Estado do Rio Grande do Sul S.A.',
        '004': 'Banco do Nordeste do Brasil S.A.',
        '265': 'Banco Fator S.A.',
        'M03': 'Banco Fiat S.A.',
        '224': 'Banco Fibra S.A.',
        '626': 'Banco Ficsa S.A.',
        'M18': 'Banco Ford S.A.',
        'M07': 'Banco GMAC S.A.',
        '612': 'Banco Guanabara S.A.',
        'M22': 'Banco Honda S.A.',
        '063': 'Banco Ibi S.A. Banco Múltiplo',
        'M11': 'Banco IBM S.A.',
        '604': 'Banco Industrial do Brasil S.A.',
        '320': 'Banco Industrial e Comercial S.A.',
        '653': 'Banco Indusval S.A.',
        '249': 'Banco Investcred Unibanco S.A.',
        '184': 'Banco Itaú BBA S.A.',
        '479': 'Banco ItaúBank S.A',
        'M09': 'Banco Itaucred Financiamentos S.A.',
        '376': 'Banco J. P. Morgan S.A.',
        '074': 'Banco J. 074 S.A.',
        '217': 'Banco John Deere S.A.',
        '600': 'Banco Luso Brasileiro S.A.',
        '389': 'Banco Mercantil do Brasil S.A.',
        '746': 'Banco Modal S.A.',
        '045': 'Banco Opportunity S.A.',
        '079': 'Banco Original do Agronegócio S.A.',
        '623': 'Banco Panamericano S.A.',
        '611': 'Banco Paulista S.A.',
        '643': 'Banco Pine S.A.',
        '638': 'Banco Prosper S.A.',
        '747': 'Banco Rabobank International Brasil S.A.',
        '356': 'Banco Real S.A.',
        '633': 'Banco Rendimento S.A.',
        'M16': 'Banco Rodobens S.A.',
        '072': 'Banco Rural Mais S.A.',
        '453': 'Banco Rural S.A.',
        '422': 'Banco 422 S.A.',
        '033': 'Banco Santander (Brasil) S.A.',
        '749': 'Banco Simples S.A.',
        '366': 'Banco Société Générale Brasil S.A.',
        '637': 'Banco Sofisa S.A.',
        '012': 'Banco Standard de Investimentos S.A.',
        '464': 'Banco Sumitomo Mitsui Brasileiro S.A.',
        '082': 'Banco Topázio S.A.',
        'M20': 'Banco Toyota do Brasil S.A.',
        '634': 'Banco Triângulo S.A.',
        'M14': 'Banco Volkswagen S.A.',
        'M23': 'Banco Volvo (Brasil) S.A.',
        '655': 'Banco Votorantim S.A.',
        '610': 'Banco VR S.A.',
        '119': 'Banco Western Union do Brasil S.A.',
        '370': 'Banco WestLB do Brasil S.A.',
        '021': 'BANESTES S.A. Banco do Estado do Espírito Santo',
        '719': 'Banif-Banco Internacional do Funchal (Brasil)S.A.',
        '755': 'Bank of America Merrill Lynch Banco Múltiplo S.A.',
        '073': 'BB Banco Popular do Brasil S.A.',
        '250': 'BCV - Banco de Crédito e Varejo S.A.',
        '078': 'BES Investimento do Brasil S.A.-Banco de Investimento',
        '069': 'BPN Brasil Banco Múltiplo S.A.',
        '070': 'BRB - Banco de Brasília S.A.',
        '104': 'Caixa Econômica Federal',
        '477': 'Citibank S.A.',
        '081': 'Concórdia Banco S.A.',
        '487': 'Deutsche Bank S.A. - Banco Alemão',
        '064': 'Goldman Sachs do Brasil Banco Múltiplo S.A.',
        '062': 'Hipercard Banco Múltiplo S.A.',
        '399': 'HSBC Bank Brasil S.A.',
        '492': 'ING Bank N.V.',
        '652': 'Itaú Unibanco Holding S.A.',
        '341': 'Itaú Unibanco S.A.',
        '488': 'JPMorgan Chase Bank',
        '751': 'Scotiabank Brasil S.A. Banco Múltiplo',
        '409': 'UNIBANCO - União de Bancos Brasileiros S.A.',
        '230': 'Unicard Banco Múltiplo S.A.',
        'XXX': 'Desconhecido',
    }

    # Retorna somente os digitos da string
    @staticmethod
    def numbersOnly(string):
        return re.sub(r"\D", '', string)

    # Função para limpar acentos de uma string
    @staticmethod
    def normalizeChars(string):
        if not string:
            return ""
        string = str(string)
        return unicodedata.normalize('NFKD', string).encode("ascii", "ignore").decode("utf-8")

    # Mostra o Valor no float Formatado
    @staticmethod
    def nFloat(number, decimals=2, showThousands=False):
        if number is None or len(Util.numbersOnly(str(number))) == 0:
            return "0"

        number = str(number)
        pontuacao = re.sub(r'\d', '', number)

        if decimals is None:
            decimals = 2
            ret = re.search(r'\d\D(\d+)', number)
            if ret is not None:
                decimals = len(ret.groups()[0])

        # Trocar o , por . para converter corretamente para float
        if pontuacao == ',':
            number = number.replace(',', '.')

        ret = "{:{t}.{decimals}f}".format(float(number), t=',' if showThousands else '', decimals=decimals)

        # Trocar de volta o . por , caso o número original tinha ,
        if pontuacao == ',':
            ret = ret.replace('.', ',')

        return ret

    @staticmethod
    def nReal(number, decimals=2, symbol=True, fixed=True):
        if number is None or len(Util.numbersOnly(str(number))) == 0:
            return "0"

        number = str(number)
        pontuacao = re.sub(r'\d', '', number)

        if decimals is None:
            decimals = 2
            ret = re.search(r'\d\D(\d+)', number)
            if ret is not None:
                decimals = len(ret.groups()[0])

        # Trocar o , por . para converter corretamente para float
        if pontuacao == ',':
            number = number.replace(',', '.')

        ret = "{:.{decimals}f}".format(float(number), decimals=decimals)

        # Trocar o . por ,
        ret = ret.replace('.', ',')

        # remove zero trailing. (14,300 -> 14,3)
        if not fixed:
            ret2 = re.search(r"\d+,\d*?(0+)$", ret)
            if ret2:
                pos = ret2.span(1)[0]  # start position of group '
                ret = ret[:pos]

        pos = ret.find(",")
        if pos >= 0:
            integral = ret[:pos]
            fractional = ret[pos + 1:]
        else:
            integral = ret
            fractional = ''

        integral = "{:,}".format(int(integral))
        integral = integral.replace(',', '.')

        return "R$ " + integral + ',' + fractional

    @staticmethod
    def modulo11(n, factor=2, base=9, x10=0, resto10=0):
        sum = 0
        i = len(n)
        while i > 0:
            sum += int(n[i - 1]) * factor
            if factor == base:
                factor = 1
            factor += 1
            i -= 1

        if x10 == 0:
            sum *= 10
            digito = sum % 11
            if digito == 10:
                digito = resto10
            return digito
        return sum % 11

    @staticmethod
    def modulo10(n):
        chars = list(n)[::-1]
        odd = list(map(lambda n: int(chars[n]), range(1, len(chars), 2)))
        even = list(map(lambda n: int(chars[n]), range(0, len(chars), 2)))
        even = list(map(lambda n: 2 * n - 9 if n >= 5 else 2 * n, even))
        total = sum(odd) + sum(even)
        return ((math.floor(total / 10) + 1) * 10 - total) % 10

    @staticmethod
    def percent(big, percent):
        if percent < 0.01:
            return 0
        return Util.nFloat(big * (percent / 100))

    @staticmethod
    def maskString(val, mask):
        if len(val) == 0:
            return val
        maskared = ''
        k = 0
        if val.isnumeric():
            val = val.rjust(len(re.sub(r"[^#]", '', mask)), '0')

        i = 0

        len_mask = len(mask)
        len_val = len(val)

        while i < len_mask:
            if mask[i] == '#':
                if k < len_val:
                    maskared += val[k]
                    k += 1
            else:
                if i < len_mask:
                    maskared += mask[i]

            i += 1

        return maskared

    @staticmethod
    def numberFormatGeral(n, loop, insert='0'):
        n = str(n)
        n = Util.numbersOnly(n)[0:loop]
        return n.rjust(loop, insert)

    @staticmethod
    def formatCnab(tipo, valor, tamanho, dec=0, sFill=''):
        tipo = tipo.upper()
        valor = Util.normalizeChars(valor).upper()

        if tipo in ['9', 9, 'N', '9L', 'NL']:

            if not valor:
                valor = "0"

            if tipo == '9L' or tipo == 'NL':
                valor = Util.numbersOnly(valor)
            left = '>'
            sFill = '0'
            format_type = 's'
            if dec > 0:
                valor = ("{:." + str(dec) + "f}").format(float(valor))

            valor = valor.replace(",", "").replace(".", "")
        elif tipo in ['A', 'X']:
            left = '<'
            format_type = 's'
        else:
            raise Exception('Tipo inválido')

        return "{0:{fill}{align}{tamanho}{type}}".format(valor[0:tamanho], fill=sFill, align=left, tamanho=tamanho,
                                                         type=format_type)

    @staticmethod
    def fatorVencimento(date, format='%Y-%m-%d'):
        if type(date) is str:
            date = datetime.strptime(date, format)
        ref = datetime(year=1997, month=10, day=7)

        return (date - ref).days

    # Remove trecho do array.
    @staticmethod
    def remove(i, f, array):
        if array is None:
            return None

        if type(array) is str:
            array = array.rstrip("\r\n")

        i -= 1

        if i > 398 or f > 400:
            raise Exception('$ini ou $fim ultrapassam o limite máximo de 400')

        if f < i:
            raise Exception(f'$ini é maior que o $fim')

        return array[i:f]

    # Função para add valor a linha nas posições informadas.
    @staticmethod
    def adiciona(line, i, f, value):
        i -= 1

        if i > 398 or f > 400:
            raise Exception('$ini ou $fim ultrapassam o limite máximo de 400')

        if f < i:
            raise Exception('$ini é maior que o $fim')

        t = f - i

        if len(value) > t:
            raise Exception(
                f'String $valor maior que o tamanho definido em $ini e $fim: $valor={len(value)} e tamanho é de: {t}')

        value = " " * (t - len(value)) + value
        return line[:i] + value + line[f:]

    # Validação para o tipo de cnab 240
    @staticmethod
    def isCnab240(content):
        content = content[0] if type(content) is list else content
        return True if len(content.rstrip("\r\n")) == 240 else False

    # Validação para o tipo de cnab 400
    @staticmethod
    def isCnab400(content):
        content = content[0] if type(content) is list else content
        return True if len(content.rstrip("\r\n")) == 400 else False

    @staticmethod
    def file2array(file):
        if type(file) is list:
            return file

        with open(file) as f:
            file_content = f.readlines()
        return file_content

    @staticmethod
    def isHeaderRetorno(header):
        if not Util.isCnab240(header) and not Util.isCnab400(header):
            return False
        if Util.isCnab400(header) and header[0:9] != '02RETORNO':
            return False
        if Util.isCnab240(header) and header[142] != '2':
            return False
        return True

    @staticmethod
    def getBancoClass(banco):

        dBancos = {
            BoletoContract.COD_BANCO_BB: 'Bb',
            BoletoContract.COD_BANCO_SANTANDER: 'Santander',
            BoletoContract.COD_BANCO_CEF: 'Caixa',
            BoletoContract.COD_BANCO_BRADESCO: 'Bradesco',
            BoletoContract.COD_BANCO_ITAU: 'Itau',
            BoletoContract.COD_BANCO_HSBC: 'Hsbc',
            BoletoContract.COD_BANCO_SICREDI: 'Sicredi',
            BoletoContract.COD_BANCO_BANRISUL: 'Banrisul',
            BoletoContract.COD_BANCO_BANCOOB: 'Bancoob',
            BoletoContract.COD_BANCO_BNB: 'Bnb',
        }

        if banco in dBancos:
            return dBancos[banco]

        raise Exception("Banco: $banco, inválido")

    @staticmethod
    def addPessoa(obj):
        from pyboletox.pessoa import Pessoa
        if issubclass(obj.__class__, Pessoa):
            return obj
        elif issubclass(obj.__class__, dict):
            obj = Pessoa(obj)
            return obj
        raise Exception('Objeto inválido, somente Pessoa e Array')

    @staticmethod
    def get_extension(url_or_file_path):
        ret = re.search(r"\.(\w+?)(&)?(?(2).*)$", "Sem+Logo")
        if ret is None:
            return ""
        else:
            return ret.groups()[0]

    @staticmethod
    def get_content(url_or_file_path):
        if os.path.exists(url_or_file_path):
            with open(url_or_file_path, 'rb') as f:
                content = f.read()
        else:
            import requests
            ret = requests.get(url_or_file_path)
            content = ret.content
        return content

    @staticmethod
    def appendStrings(*args):
        return " ".join(args)
