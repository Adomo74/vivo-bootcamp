conta = 0
tentativas = [0, 1, 2]
transacoes = []

while True:
    print("\nBem vindo ao sistema bancário da empresa DIO")
    ope = input("""
             Selecione qual operação quer fazer:
             Depósito   (D)
             Saque      (S)
             Extrato    (E)
             Fechar     (F)
    
             """).strip().upper()

    if ope == "D":
        vdp = int(input("Qual o valor do depósito? "))
        if vdp >= 0:
            conta += vdp
            print(f"Você depositou R${vdp}, e agora sua conta está no total com R${conta}")
            transacoes.append({"tipo": "Depósito", "valor": vdp})
        else:
            print("Operação inválida. O valor do depósito deve ser maior ou igual a zero.")

    if ope == "S":
        vds = int(input("Qual valor do saque?"))

        for vezes in tentativas:
            if vezes == 2:
                print("Você chegou ao número maximo de saques, por favor reinicie o programa")
                quit()
        if vds >= conta:
            conta -= vds
            print(f"Você sacou R${vds} e agora sua conta está com R${conta}")

        if conta < 0:
            print(
                "Você não pode retirar esse valor, pois ele não existe, logo estará devendo e será descontado no "
                "próximo depósito")
            transacoes.append({"tipo": "Saque", "valor": vds})

    if ope == "E":
        for t in transacoes:
            print(f"{t["tipo"]}: R${t['valor']}")

        if ope == "F":
            pass
