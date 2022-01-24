import os
from datetime import datetime
from pyboletox.pessoa import Pessoa
from pyboletox.Cnab.Remessa.Cnab400.Banco.itau import Itau as RemessaItau
from pyboletox.Boleto.Banco.itau import Itau as BoletoItau

dir_path = os.path.dirname(os.path.realpath(__file__))
logo_path = os.path.join(dir_path, '..', 'logos', '341.png')
file_path = os.path.join(dir_path, '..', 'arquivos', 'itau.txt')

beneficiario = Pessoa({
    'nome':      'ACME',
    'endereco':  'Rua um, 123',
    'cep':       '99999-999',
    'uf':        'UF',
    'cidade':    'CIDADE',
    'documento': '99.999.999/9999-99',
})

pagador = Pessoa({
    'nome':      'Cliente',
    'endereco':  'Rua um, 123',
    'cep':       '99999-999',
    'uf':        'UF',
    'cidade':    'CIDADE',
    'documento': '99.999.999/9999-99',
})

boleto = BoletoItau(**{
    'logo': logo_path,
    'dataVencimento': datetime.now(),
    'valor': 100,
    'multa': False,
    'juros': False,
    'numero': 1,
    'numeroDocumento': 1,
    'pagador': pagador,
    'beneficiario': beneficiario,
    'diasBaixaAutomatica': 2,
    'carteira': 112,
    'agencia': 1111,
    'conta': 99999,
    'descricaoDemonstrativo': ['demonstrativo 1', 'demonstrativo 2', 'demonstrativo 3'],
    'instrucoes': ['instrucao 1', 'instrucao 2', 'instrucao 3'],
    'aceite': 'S',
    'especieDoc': 'DM',
})
# print(boleto.toDict())

remessa = RemessaItau(**{
    'agencia': 1111,
    'conta': 99999,
    'contaDv': 9,
    'carteira': 112,
    'beneficiario': beneficiario,
})

remessa.addBoleto(boleto)
remessa.save(file_path)
