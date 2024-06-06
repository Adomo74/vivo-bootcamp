

def banco():


    conta = 0
    esc = True
    while esc == True:
        print("\nBem vindo ao sistema bancário da empresa DIO")
        ope = input("""Selecione qual operação quer fazer:
         Depósito   (D)
         Saque      (S)
         Extrato    (E)
         Fechar     (F)
        
         """).strip().upper()


        if ope == "D":

            def deposito():
                global conta
                vdp = int(input("Qual o valor do depósito? "))
                if vdp >= 0:
                    conta += vdp
                    print(conta)
                else:
                    print("Operação inválida. O valor do depósito deve ser maior ou igual a zero.")

            deposito()




    if ope == "S":
        #tentativas = [1 + 0]
        saq = int(input("Qual o valor do saque?"))
        dsaq = saq - conta
        print(conta)
        #while tentativas == 3:
            #print("chegou o limite de operações")

    if ope == "E":
        print("DEU BOM")

    if ope == "F":
        esc = False


banco()