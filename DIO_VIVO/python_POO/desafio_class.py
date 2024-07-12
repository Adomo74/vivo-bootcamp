import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

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
        self._saldo = 0
        self._number = number
        self._client = client
        self._historico = historico()

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


class Deposito(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = pf(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "D":
            depositar(clientes)

        elif opcao == "S":
            sacar(clientes)

        elif opcao == "E":
            exibir_extrato(clientes)

        elif opcao == "CP":
            criar_cliente(clientes)

        elif opcao == "CC":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()