class MagicTrait:
    def toDict(self):
        obj_vars = vars(self.__class__)
        dRet = {}
        for var in obj_vars:
            attr = getattr(self, var, None)
            if var.startswith('get') and callable(attr):
                ret = attr()
                attr2 = getattr(ret, 'toDict', None)
                if attr2:
                    dRet[var[3:]] = attr2()
                else:
                    dRet[var[3:]] = ret

        return dRet
