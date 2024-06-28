conta = 0
tentativas = [0, 1, 2]
transacoes = []
contas = []
usuarios = []
T = True


def cadastro_pessoa():
    nome = input("Qual seu nome?").strip()
    dtn = input("Qual sua data de nascimento?").strip()
    cpf = input("Qual seu cpf?").strip()
    logradouro = input("Qual seu logradouro?").strip()
    nro = input("Qual seu número?").strip()
    bairro = input("Qual o seu bairro?").strip()
    cidade = input("Qual sua cidade?").strip()
    estado = input("Qual o Estado? Em sigla por favor").strip()
    endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}"
    pessoa = {"nome": nome, "data_nascimento": dtn, "cpf": cpf, "endereco": endereco}

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Usuário com este cpf já está cadastrado")
            return

    usuarios.append(pessoa)
    print(f"Usuário cadastro com sucesso \n {pessoa}")


def criar_conta(cpf):
    agencia = "0001"
    num_conta = len(contas) + 1

    usu_encontrado = None

    for pessoa in usuarios:
        if pessoa["cpf"] == cpf:
            usu_encontrado = pessoa
            break

    if usu_encontrado is None:
        print("Usuario não encontrado. Por favor, faça o registro novamente")
        return

    dados_conta = {"agencia": agencia, "numero_conta": num_conta, "usuario": usu_encontrado}
    contas.append(dados_conta)
    print("Conta criada com sucesso")
    print(conta)


def deposito():
    global conta
    vdp = int(input("Qual o valor do depósito? "))
    if vdp >= 0:
        conta += vdp
        print(f"Você depositou R${vdp}, e agora sua conta está com R${conta}")
        transacoes.append({"tipo": "Depósito", "valor": vdp})
    else:
        print("Operação inválida. O valor do depósito deve ser maior ou igual a zero.")

    return conta


def saque():
    global conta

    vds = int(input("Qual valor do saque?"))

    for vezes in tentativas:
        if vezes == 4:
            print("Você chegou ao número máximo de saques, por favor reinicie o programa")
            pass
    if vds >= conta:
        conta -= vds
        print(f"Você sacou R${vds} e agora sua conta está com R${conta}")

    else:
        print(
            "Você não pode retirar esse valor, pois ele não existe, logo estará devendo e será descontado no "
            "próximo depósito")
        transacoes.append({"tipo": "Saque", "valor": vds})

        return conta


def extrato():
    for t in transacoes:
        print(f"{t['tipo']}: R${t['valor']}")

    if ope == "F":
        pass


def fechar():
    global T
    T = False
    print(f"O programa encerra aqui. Saldo final: R${conta}. Tenha um bom dia!")


while False != T:
    print("\nBem-vindo ao sistema bancário da empresa DIO")
    ope = input("""
             Selecione qual operação quer fazer:
                Depósito           (D)
                Saque              (S)
                Extrato            (E)
                Fechar             (F)
                Cadastro pessoal   (CP)
                Criar conta        (CC)

             """).strip().upper()

    if ope == "D":
        deposito()

    if ope == "S":
        saque()

    if ope == "E":
        extrato()

    if ope == "F":
        fechar()

    if ope == "CP":
        cadastro_pessoa()

    if ope == "CC":
        cpf = input("Qual o cpf do usuário: ").strip()
        criar_conta(cpf)