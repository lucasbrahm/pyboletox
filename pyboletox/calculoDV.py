from pyboletox.util import Util


class CalculoDV:
    """
    |--------------------------------------------------------------------------
    | 001 - Banco do Brasil
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def bbAgencia(agencia):
        return Util.modulo11(agencia, 2, 9, 0, 'X')

    @staticmethod
    def bbContaCorrente(contaCorrente):
        return Util.modulo11(contaCorrente, 2, 9, 0, 'X')

    @staticmethod
    def bbNossoNumero(nossoNumero):
        if len(nossoNumero) >= 17:
            return None
        else:
            Util.modulo11(nossoNumero)

    """
    |--------------------------------------------------------------------------
    | 004 - Banco do Nordeste
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def bnbAgencia(agencia):
        dv = Util.modulo11(agencia, 2, 9, 0)
        if dv == 1:
            return 'X'
        else:
            return dv

    @staticmethod
    def bnbContaCorrente(agencia, conta):
        conta = format(Util.__bnbAgenciaReal(agencia), '0>3s') + format(conta, '0>9s')
        dv = Util.modulo11(conta, 2, 9, 1)
        if dv > 1:
            return 11 - dv
        return 0

    @staticmethod
    def bnbNossoNumero(nossoNumero):
        return Util.modulo11(Util.numberFormatGeral(nossoNumero, 7))

    @staticmethod
    def __bnbAgenciaReal(agencia):
        agenciaAntiga = {
            '1': '99', '2': '44', '3': '74', '4': '73', '5': '81', '6': '1',
            '7': '2', '8': '53', '9': '46', '10': '20', '11': '82', '12': '47',
            '13': '9', '14': '10', '15': '54', '16': '0', '17': '55', '18': '83',
            '19': '11', '20': '48', '21': '25', '22': '12', '23': '49', '24': '26',
            '25': '40', '26': '75', '27': '16', '28': '50', '29': '27', '30': '29',
            '31': '3', '32': '4', '33': '76', '34': '41', '35': '77', '36': '30',
            '37': '67', '38': '68', '39': '78', '40': '58', '41': '59', '42': '42',
            '43': '31', '44': '60', '45': '62', '46': '17', '47': '79', '48': '32',
            '49': '70', '50': '63', '51': '86', '52': '33', '53': '52', '54': '64',
            '55': '34', '56': '71', '57': '72', '58': '14', '59': '38', '60': '43',
            '61': '80', '62': '21', '63': '57', '64': '91', '66': '6', '67': '51',
            '68': '66', '69': '85', '70': '39', '71': '92', '72': '28', '73': '19',
            '74': '87', '75': '18', '76': '61', '77': '88', '78': '89', '80': '5',
            '81': '90', '82': '15', '83': '7', '84': '13', '85': '93', '86': '69',
            '87': '94', '88': '101', '89': '107', '90': '95', '91': '45', '92': '8',
            '93': '35', '95': '106', '96': '103', '97': '117', '98': '118', '99': '104',
            '100': '108', '101': '102', '102': '112', '103': '113', '104': '115', '105': '105',
            '106': '96', '107': '97', '108': '24', '109': '111', '110': '119', '111': '84',
            '112': '36', '113': '37', '114': '114', '115': '100', '116': '116', '117': '56',
            '118': '65', '119': '109',
        }

        if agencia in agenciaAntiga:
            return agenciaAntiga[agencia]

        return agencia

    """
    |--------------------------------------------------------------------------
    | 033 - Santander
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def santanderContaCorrente(agencia, contaCorrente):
        n = Util.numberFormatGeral(agencia, 4) \
            + '00' \
            + Util.numberFormatGeral(contaCorrente, 8)
        chars = list(n)[::-1]
        sums = list('97310097131973')[::-1]
        sum = 0
        for i in range(len(chars)):
            sum += int(str(int(chars[i]) * int(sums[i]))[-1])
        unidade = str(sum)[-1]
        unidade = int(unidade)
        if unidade == 0:
            return unidade
        else:
            return 10 - unidade

    @staticmethod
    def santanderNossoNumero(nossoNumero):
        return Util.modulo11(nossoNumero)

    """
    |--------------------------------------------------------------------------
    | 041 - Banrisul
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def banrisulAgencia(agencia):
        newDv1 = dv1 = Util.modulo10(agencia)
        dv2 = Util.modulo11(agencia + dv1, 2, 7)

        if dv2 == 1 and dv1 != 9:
            newDv1 = 1
        if dv2 == 1 and dv1 == 9:
            newDv1 = 0

        if dv1 != newDv1:
            dv1 = newDv1
            dv2 = Util.modulo11(agencia + dv1, 2, 7)

        return dv1 + dv2

    @staticmethod
    def banrisulContaCorrente(contaCorrente):
        chars = list(contaCorrente)[::-1]
        sums = list('234567423')

        sum = 0

        for i in range(len(chars)):
            sum += int(chars[i]) * int(sums[i])

        resto = sum % 11

        if resto == 0:
            return resto

        if resto == 1:
            return 6

        return 11 - resto

    @staticmethod
    def banrisulNossoNumero(nossoNumero):
        return CalculoDV.banrisulDuploDigito(nossoNumero)

    @staticmethod
    def banrisulDuploDigito(campo):
        dv1 = Util.modulo10(campo)
        dv2 = Util.modulo11(campo + dv1, 2, 7, 1, 10)

        if dv2 == 1:
            if dv1 == 9:
                dv1 = 0
            else:
                dv1 += 1

            dv2 = Util.modulo11(campo + dv1, 2, 7, 0, 10)
        elif dv2 != 0:
            dv2 = 11 - dv2

        return dv1 + dv2

    """
    |--------------------------------------------------------------------------
    | 104 - Caixa Econômica Federal
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def cefAgencia(agencia):
        return Util.modulo11(Util.numberFormatGeral(agencia, 5))

    @staticmethod
    def cefContaCorrente(agencia, contaCorrente):
        n = Util.numberFormatGeral(agencia, 5) \
            + Util.numberFormatGeral(contaCorrente, 11)
        return Util.modulo11(n)

    @staticmethod
    def cefNossoNumero(nossoNumero):
        return Util.modulo11(nossoNumero)

    """
    |--------------------------------------------------------------------------
    | 237 - Bradesco
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def bradescoAgencia(agencia):
        dv = Util.modulo11(agencia, 2, 9, 0, 'P')
        if dv == 11:
            return 0
        else:
            return dv

    @staticmethod
    def bradescoContaCorrente(contaCorrente):
        return Util.modulo11(contaCorrente, 2, 9, 0, 'P')

    @staticmethod
    def bradescoNossoNumero(carteira, nossoNumero):
        return Util.modulo11(carteira + Util.numberFormatGeral(nossoNumero, 11), 2, 7, 0, 'P')

    """
    |--------------------------------------------------------------------------
    | 341 - Itau
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def itauContaCorrente(agencia, contaCorrente):
        n = Util.numberFormatGeral(agencia, 4) \
            + Util.numberFormatGeral(contaCorrente, 5)
        return Util.modulo10(n)

    @staticmethod
    def itauNossoNumero(agencia, conta, carteira, numero_boleto):
        n = Util.numberFormatGeral(agencia, 4) \
            + Util.numberFormatGeral(conta, 5) \
            + Util.numberFormatGeral(carteira, 3) \
            + Util.numberFormatGeral(numero_boleto, 8)
        return Util.modulo10(n)

    """
    |--------------------------------------------------------------------------
    | 748 - Sicredi - Falta o calculo agencia e conta
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def sicrediNossoNumero(agencia, posto, codigoCliente, ano, byte, numero_boleto):
        n = Util.numberFormatGeral(agencia, 4) \
            + Util.numberFormatGeral(posto, 2) \
            + Util.numberFormatGeral(codigoCliente, 5) \
            + Util.numberFormatGeral(ano, 2) \
            + Util.numberFormatGeral(byte, 1) \
            + Util.numberFormatGeral(numero_boleto, 5)
        return Util.modulo11(n)

    """
    |--------------------------------------------------------------------------
    | 756 - Bancoob - Falta o calculo conta e confirmar agencia
    |--------------------------------------------------------------------------
    """

    @staticmethod
    def bancoobAgencia(agencia):
        return Util.modulo11(agencia)

    @staticmethod
    def bancoobContaCorrente(contaCorrente):
        return Util.modulo11(contaCorrente)

    @staticmethod
    def bancoobNossoNumero(agencia, convenio, numero_boleto):
        n = Util.numberFormatGeral(agencia, 4) \
            + Util.numberFormatGeral(convenio, 10) \
            + Util.numberFormatGeral(numero_boleto, 7)

        chars = list(n)
        sums = list('3197319731973197319731973197')
        sum = 0
        for i in range(len(chars)):
            sum += int(chars[i]) * int(sums[i])
        resto = sum % 11
        dv = 0

        if (resto != 0) and (resto != 1):
            dv = 11 - resto
        return dv
