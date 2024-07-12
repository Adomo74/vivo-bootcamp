from abc import ABC, abstractproperty, abstractmethod

conta = 0


contas = []
usuarios = []


class client:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def r_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def add_conta(self, conta):
        self.contas.append(conta)


class pf(client):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf

    pass


class conta:
    def __init__(self, number, client):
        self.saldo = 0
        self.number = number
        self.client = client
        self.historico = historico()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    # colocar underline depois para privar o atributo
    @property
    def saldo(self):
        return self.saldo

    @property
    def number(self):
        return self.number

    @property
    def agencia(self):
        return self.agencia

    @property
    def cliente(self):
        return self.client

    @property
    def historico(self):
        return self.historico

    # vds == valor do saque
    def sacar(self, vds):

        saldo = self.saldo
        limit_saldo = vds > saldo

        if limit_saldo:
            saldo -= vds
            print(f"Você sacou R${vds} e agora sua conta está com R${conta}")

        elif vds > 0:
            print(
                "Você não pode retirar esse valor, pois ele não existe, logo estará devendo e será descontado no "
                "próximo depósito")
            transacoes.append({"tipo": "Saque", "valor": vds})

        else:
            print("Operação falhou!")

        return False

    def deposito(self,vdp):
        saldo = self.saldo
        if vdp > 0:
            saldo += vdp
            print(f"Você depositou R${vdp}, e agora sua conta está com R${conta}")
            transacoes.append({"tipo": "Depósito", "valor": vdp})
        else:
            print("Operação inválida. O valor do depósito deve ser maior ou igual a zero.")

        return True

    @historico.setter
    def historico(self, value):
        self._historico = value


class corrente(conta):
    def __init__(self, number, client, limit = 500, tentativas = 3):
        super().__init__(number, client)
        self.limit = limit
        self.tentativas = tentativas

    def sacar(self, vds):
        n_saques =  len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == saque.__name__])

        exe_limit = vds > self.limit
        exe_limit_saques = n_saques >= self.tentativas

        if exe_limit:
            print("Operação falha!\n Excedeu o limite")

        elif exe_limit_saques:
            print("Operação falha! Número máximo de saques alcançado")

        else:
            return super().sacar(vds)
        return False
    pass


class historico():
    def __init__(self):
        self.transacoes = []

    def add_transacao(self, transacao):

    pass


class transacao(ABC):
    pass


class saque(transacao):
    pass
