import importlib
from posixpath import basename
from pyboletox.util import Util


class Factory:

    @staticmethod
    def make(file):
        file_content = Util.file2array(file)

        if not Util.isHeaderRetorno(file_content[0]):
            raise Exception(f"Arquivo: {file}, não é um arquivo de retorno")

        instancia = Factory.getBancoClass(file_content)
        return instancia.processar()

    @staticmethod
    def getBancoClass(file_content):
        banco = ''
        namespace = 'pyboletox.Cnab.Retorno'
        if Util.isCnab400(file_content):
            banco = file_content[0][76:79]
            namespace += '.Cnab400.'
        elif Util.isCnab240(file_content):
            banco = file_content[0][0:3]
            namespace += '.Cnab400.'

        bancoClassName = Util.getBancoClass(banco)
        mod = importlib.import_module(namespace + 'Banco.' + bancoClassName.lower())
        bancoClass = getattr(mod, bancoClassName)
        return bancoClass(file_content)
