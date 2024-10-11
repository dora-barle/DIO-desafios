from abc import ABC, abstractmethod
from datetime import date
from datetime import datetime

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas_registradas = []

    def adicionar_conta(self, conta):
        self.contas_registradas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, endereco: str, data_nascimento: date):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento        


###Interface Transacao Transacao->classe abstrata
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        """Registra as transações na conta"""
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

class Historico_Transacao:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente: Cliente, numero_conta: int, agencia: str):
        self.cliente = cliente
        self.numero_conta = numero_conta
        self.agencia = agencia
        self.saldo = 0.0
        self.historico = Historico_Transacao()

    def get_saldo(self):
        return self.saldo
    
    def nova_conta(self):
        self.cliente.adicionar_conta(self)

    def sacar(self, valor: float) -> bool:
        """Realiza o saque e retorna True se foi bem-sucedido"""
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        return False
    
    def depositar(self, valor: float) -> bool:
        """Realiza o depósito e retorna True se foi bem-sucedido"""
        self.saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero_conta: int, agencia:str, limite:float, limite_saques: int):
        super().__init__(cliente, numero_conta, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

from datetime import date

def menu():
    return """
    Menu:
    [u] - Cadastrar Cliente
    [n] - Criar Conta
    [l] - Listar Clientes
    [d] - Depositar
    [s] - Sacar
    [e] - Exibir Extrato
    [q] - Sair
    """

def main():
    clientes = []
    numero_conta = 1  
    limite_saques = 3  

    while True:
        print(menu())
        opcao = input("Escolha uma opção: ")

        if opcao == 'u':
            nome = input("Nome: ")
            data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")  
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(cpf, nome, endereco, data_nascimento)  
            clientes.append(cliente)
            print("Cliente cadastrado com sucesso!")

        elif opcao == 'n':
            cpf_cliente = input("Digite o CPF do cliente para criar uma conta: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if cliente_encontrado:
                agencia = input("Digite o número da agência: ")
                limite = float(input("Digite o limite da conta: "))
                conta = ContaCorrente(cliente_encontrado, numero_conta, agencia, limite, limite_saques)
                conta.nova_conta()
                numero_conta += 1  
                print(f"Conta criada com sucesso! Número da conta: {conta.numero_conta}")
            else:
                print("Cliente não encontrado!")

        elif opcao == 'l':
            print("\nClientes cadastrados:")
            for cliente in clientes:
                print(f"Nome: {cliente.nome}")
                print(f"CPF: {cliente.cpf}")
                for conta in cliente.contas_registradas:
                    print(f"Número da Conta: {conta.numero_conta} - Saldo: {conta.get_saldo():.2f}")

        elif opcao == 'd':
            cpf_cliente = input("Digite o CPF do cliente: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if cliente_encontrado and cliente_encontrado.contas_registradas:
                conta = cliente_encontrado.contas_registradas[0]  
                valor = float(input("Digite o valor do depósito: "))
                conta.depositar(valor)
                deposito = Deposito(valor)
                cliente_encontrado.realizar_transacao(conta, deposito)
                print(f"Depósito de {valor:.2f} realizado com sucesso.")
            else:
                print("Cliente não encontrado ou não possui contas.")

        elif opcao == 's':
            cpf_cliente = input("Digite o CPF do cliente: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if cliente_encontrado and cliente_encontrado.contas_registradas:
                conta = cliente_encontrado.contas_registradas[0]  
                if conta.limite_saques > 0:  
                    valor = float(input("Digite o valor do saque: "))
                    if conta.sacar(valor):
                        saque = Saque(valor)
                        cliente_encontrado.realizar_transacao(conta, saque)
                        conta.limite_saques -= 1  
                        print(f"Saque de {valor:.2f} realizado com sucesso.")
                    else:
                        print("Saldo insuficiente para o saque.")
                else:
                    print("Limite de saques atingido. Não é possível realizar mais saques.")
            else:
                print("Cliente não encontrado ou não possui contas.")

        elif opcao == 'e':
            cpf_cliente = input("Digite o CPF do cliente: ")
            cliente_encontrado = next((c for c in clientes if c.cpf == cpf_cliente), None)
            if cliente_encontrado and cliente_encontrado.contas_registradas:
                conta = cliente_encontrado.contas_registradas[0]  
                print("Extrato da Conta:")
                for transacao in conta.historico.transacoes:
                    print(f"{transacao.__class__.__name__}: {transacao.valor:.2f}")
                print(f"Saldo atual: {conta.get_saldo():.2f}")
            else:
                print("Cliente não encontrado ou não possui contas.")

        elif opcao == 'q':
            print("\nObrigada por utilizar nosso sistema bancário!")
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()



# # Registrando Cliente
# cliente1 = PessoaFisica("Maria", "123.456.789-00", "Rua A, 123", date(1990, 1, 1))
# conta1 = Conta(cliente1, 12345, "Agência 001")
# conta1.nova_conta()  
# print(cliente1.nome)  
# print(conta1.agencia) 

# # Depositando dinheiro
# deposito = Deposito(100.0)
# cliente1.realizar_transacao(conta1, deposito)

# # Sacando dinheiro
# saque = Saque(50.0)
# cliente1.realizar_transacao(conta1, saque)

# # Verificando o saldo
# print("Saldo atual:", conta1.get_saldo())


          

        


