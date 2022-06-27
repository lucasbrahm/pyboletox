from pyboletox.Cnab.Retorno.factory import Factory
import os
from pprint import pprint

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, '..', 'arquivos', 'cef.ret')

retorno = Factory.make(file_path)
print(retorno.getBancoNome())

for detalhe in retorno.getDetalhes().values():
    pprint(detalhe.toDict())
