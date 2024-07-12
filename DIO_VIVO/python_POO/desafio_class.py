import datetime
from abc import ABC, abstractproperty, abstractmethod

conta = 0

transacoes = []
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

        limit_saldo = vds > self.limit
        exe_limit_saques = n_saques >= self.tentativas

        if limit_saldo:
            print("Operação falha!\n Excedeu o limite")

        elif exe_limit_saques:
            print("Operação falha! Número máximo de saques alcançado")

        else:
            return super().sacar(vds)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.number}
            Titular:\t{self.client.nome}
            """
    pass


class historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def add_transacao(self, transacao):
        self._transacoes.append(
            {

                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data":datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractproperty
    def registrar(self, conta):
        pass


class saque(transacao):
    def __init__(self,vds):
        self._vds = vds

    @property
    def valor(self):
        return self._vds

    def registrar(self, conta):
        true_transacao = conta.sacar(self.valor)

        if true_transacao:
            conta.historico.add_transacao(self)
    pass


class deposito(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
