
menu = """ 
++++++++++++++++
Sistema Bancário
++++++++++++++++

[d] Depósito
[s] Saque
[e] Extrato
[q] Sair
=> """

saldo = 0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    
    if opcao == "d":
        valor = float(input("\nDigite o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n" 
            print("Seu depósito foi efetuado com sucesso!")
        else:
            print("Valor inválido! O depósito deve ser maior que zero.")

    elif opcao == "s":
        valor = float(input("\nDigite o valor do saque: "))
        if 0 < valor <= saldo and numero_saques < LIMITE_SAQUES and valor <=500:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("Seu saque foi efetuado com sucesso! Retire o dinheiro!")
        else:
            print("Valor inválido! Verifique se você tem saldo suficiente ou se não excedeu o limite de saques.")

    elif opcao == "e":
        print("\n++++  Extrato ++++")
        print(extrato)
        print(f"Saldo: R$ {saldo:.2f}") 

    elif opcao == "q":
        print("\nObrigada por ultilizar nosso sistema bancário!")
        print("Saindo...")
        break

    else:
        print("\nOperação inválida, por favor selecione uma opção válida.")


