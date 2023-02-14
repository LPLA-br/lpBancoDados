"""
    Autor: Luiz Paulo de Lima Araújo
    Licença: GPLv3
    Descrição:
        Funções utilitárias do UNIX_TIMESTAMP() para projeto
        final de banco de dados.
"""
import datetime
import time
import re


class UnixTimestampNotflux:

    def __init__(self):
        self.dia = 86400 #numero de segundos em um dia
        self.basico = self.dia*10
        self.master = self.dia*20
        self.premium = self.dia*30

    #comesso - timestamp inicial definido no momento da aquisição do plano.
    #plano - qual plano
    #retorna:
    #   false - fora de validade. Anule o plano!
    #   true  - dentro da validade.
    def estaValido(self, comesso, plano):
        agora = int( re.sub("\.[0-9]+", "", str(datetime.datetime.timestamp(datetime.datetime.now()))) )
        tempoDesdeAssinatura = agora - comesso
        
        match plano:
            case 1:
                if tempoDesdeAssinatura > self.basico:
                    return False
                else:
                    return True
            case 2:
                if tempoDesdeAssinatura > self.master:
                    return False
                else:
                    return True
            case 3:
                if tempoDesdeAssinatura > self.premium:
                    return False
                else:
                    return True
            case other:
                return None

