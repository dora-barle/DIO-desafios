from datetime import datetime


def menu():
    return  """\n
    ========= Sistema Bancário ==========
    [u]\tNovo usuário   
    [n]\tNova conta
    [l]\tListar clientes
    [d]\tDeposito
    [s]\tSaque
    [e]\tExtrato
    [q]\tSair
    => """

####Classe Cliente e a função que cadastrado novo cliente
class ClienteNovo:
    clientes_cadastrados = []

    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

        ###Tratando o erro de ter mais de um CPF cadastrado, tratando diretamente o erro
        if cpf in ClienteNovo.clientes_cadastrados:
            raise ValueError(f"Erro: CPF {cpf} já cadastrado.")
        else:
            ClienteNovo.clientes_cadastrados.append(cpf)

####Classe Conta e a função para cadastrar uma nova conta
class ContaNova:
    numero_conta_sequencial = 1
    AGENCIA = "0001"

    def __init__(self, cliente, saldo_inicial=0):
        self.cliente = cliente
        self.numero_conta = ContaNova.numero_conta_sequencial  
        ContaNova.numero_conta_sequencial += 1  
        self.saldo = saldo_inicial
        self.extrato = []
        self.numero_transacoes = 0
        self.data_transacoes = []  
        
        self.cliente.contas.append(self)

    ###Deve receber os argumentos saldo e valor por posição e extrato por nome.
    def deposito(self, saldo, valor, /, *, extrato):
        data_atual = datetime.now().date()
        if self.data_transacoes and self.data_transacoes[-1] != data_atual:
            self.numero_transacoes = 0
            self.data_transacoes = []

        if self.numero_transacoes >= 10:
            print("Limite diário de 10 transações atingido!")
            return saldo, extrato

        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f} efectuado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.numero_transacoes += 1
            self.data_transacoes.append(data_atual)
            print("O depósito foi efetuado com sucesso!")
            return saldo, extrato
        else:
            print("Valor inválido! O depósito deve ser maior que zero.")
            return saldo, extrato
    
        
    ####Deve receber o argumento valor como um argumento nomeado (keyword only)
    def saque(self, *, valor):
        
        data_atual = datetime.now().date()

        # Resetar o número de transações se for um novo dia
        if self.data_transacoes and self.data_transacoes[-1] != data_atual:
            self.numero_transacoes = 0
            self.data_transacoes = []

        if self.numero_transacoes >= 10:
            print("Limite diário de 10 transações atingido!")
            return self.saldo, self.extrato

        if 0 < valor and valor <= 500 <= self.saldo:
            self.saldo -= valor
            self.extrato.append(f"Saque: R$ {valor:.2f} em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.numero_transacoes += 1
            self.data_transacoes.append(data_atual)
            print("\nO saque foi realizado com sucesso!")
            return self.saldo, self.extrato
        else:
            print("\nValor inválido! Verifique se você tem saldo suficiente. Ou se o valor está dentro do limite permitido (máximo R$ 500).") 
            return self.saldo, self.extrato
        

    ###Recebe saldo por posição e o extrato como argumento nomeado    
    def mostrar_extrato(self, saldo, /, *, extrato):
        
        print(f"\n=====  Extrato da Conta de {self.cliente.nome} ====")
        for transacao in extrato:
            print(transacao)
        data_saldo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Saldo: R$ {saldo:.2f} na data {data_saldo}")
        return saldo, extrato


def main():
    clientes = []  

    while True:

        print(menu()) 

        opcao = input("Escolha uma opção: ")

        if opcao == 'u': 
            nome = input("Nome: ")
            data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço: ")
            try:
                cliente = ClienteNovo(nome, data_nascimento, cpf, endereco)
                clientes.append(cliente)
                print("Cliente cadastrado com sucesso!")
            except ValueError as e:
                print(e)

        elif opcao == 'n':
            cpf_cliente = input("Digite o CPF do cliente para criar uma conta: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            
            if not cliente_encontrado:
                print("Cliente não encontrado!")
                continue
            
            conta = ContaNova(cliente_encontrado)  
            print(f"Conta criada com sucesso! Número da conta: {conta.numero_conta}")

        elif opcao == 'l':
            print("\nClientes cadastrados:")
            for cliente in clientes:
                print(f"Nome: {cliente.nome}") 
                print(f"CPF: {cliente.cpf}")
                if cliente.contas:  
                    for conta in cliente.contas:
                        print(f"Número da Conta: {conta.numero_conta}")
                else:
                    print("Não possui contas associadas.")  
 
        
        elif opcao == 'd':  
            cpf_cliente = input("Digite o CPF do cliente: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if not cliente_encontrado or not cliente_encontrado.contas:
                print("Cliente não encontrado ou não possui contas.")
                continue
            
            conta = next((c for c in cliente_encontrado.contas), None)
            valor = float(input("Digite o valor do depósito: "))
            conta.saldo, conta.extrato = conta.deposito(conta.saldo, valor, extrato=conta.extrato)

        elif opcao == 's':  
            cpf_cliente = input("Digite o CPF do cliente: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if not cliente_encontrado or not cliente_encontrado.contas:
                print("Cliente não encontrado ou não possui contas.")
                continue
            
            conta = next((c for c in cliente_encontrado.contas), None)
            valor = float(input("Digite o valor do saque: "))
            conta.saldo, conta.extrato = conta.saque(valor=valor)

        elif opcao == 'e':  
            cpf_cliente = input("Digite o CPF do cliente: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if not cliente_encontrado or not cliente_encontrado.contas:
                print("Cliente não encontrado ou não possui contas.")
                continue
            
            conta = next((c for c in cliente_encontrado.contas), None)
            conta.mostrar_extrato(conta.saldo, extrato=conta.extrato)

        elif opcao == 'q':  
            print("\nObrigada por ultilizar nosso sistema bancário!")
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()