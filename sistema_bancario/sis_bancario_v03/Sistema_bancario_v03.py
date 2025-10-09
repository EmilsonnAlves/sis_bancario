from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def recuperar_conta(self):
        if not self.contas:
            print("\n@@@ CLIENTE NÃO POSSUI CONTA! @@@")
            return None
        return self.contas[0]


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()

    def sacar(self, valor):
        if valor <= 0:
            print("\nVALOR INVÁLIDO")
            return False
        if valor > self.saldo:
            print("\nSALDO INSUFICIENTE")
            return False

        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\nVALOR INVÁLIDO")
            return False

        self.saldo += valor
        return True


class ContaCorrente(Conta):
    limite_saque = 300
    limite_saques = 3

    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("\nLIMITE DIÁRIO DE SAQUE ATINGIDO")
            return False
        if valor > self.limite_saque:
            print("\nVALOR ACIMA DO LIMITE DE SAQUE")
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def exibir(self):
        if not self.transacoes:
            print("NÃO FORAM REALIZADAS OPERAÇÕES")
            return
        for t in self.transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f} - {t['data']}")


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            print(f"\nSAQUE DE R${self.valor:.2f} EFETUADO COM SUCESSO")
        else:
            print("\nSAQUE NÃO REALIZADO")


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            print(f"\nDEPÓSITO DE R${self.valor:.2f} EFETUADO COM SUCESSO")
        else:
            print("\nDEPÓSITO NÃO REALIZADO")


class Banco:
    def __init__(self):
        self.clientes = {}   # cpf -> Cliente
        self.contas = {}     # numero_conta -> Conta
        self.numero_conta_seq = 1

    def criar_cliente(self):
        nome = input("NOME COMPLETO: ")
        cpf = input("CPF: ")
        data_nasc = input("DATA DE NASCIMENTO (dd/mm/aaaa): ")
        endereco = input("ENDEREÇO: ")

        if cpf.isdigit():
            cpf = int(cpf)
        else:
            print("CPF INVÁLIDO")
            return

        if cpf in self.clientes:
            print("CLIENTE JÁ CADASTRADO")
            return

        cliente = PessoaFisica(nome, cpf, data_nasc, endereco)
        self.clientes[cpf] = cliente
        print("CLIENTE CADASTRADO COM SUCESSO")

        opcao = input("DESEJA CRIAR CONTA CORRENTE? [1] SIM / [2] NÃO: ")
        if opcao == "1":
            self.criar_conta(cpf)

    def criar_conta(self, cpf=None):
        if cpf is None:
            cpf = input("CPF: ")
            if cpf.isdigit():
                cpf = int(cpf)
            else:
                print("CPF INVÁLIDO")
                return

        if cpf not in self.clientes:
            print("CLIENTE NÃO ENCONTRADO")
            return

        cliente = self.clientes[cpf]

        if cliente.contas:
            print("CLIENTE JÁ POSSUI CONTA")
            return

        numero_conta = self.numero_conta_seq
        conta = ContaCorrente(numero_conta, cliente)
        cliente.adicionar_conta(conta)
        self.contas[numero_conta] = conta
        self.numero_conta_seq += 1
        print(f"CONTA {numero_conta} CRIADA COM SUCESSO PARA {cliente.nome}")

    def acessar_conta(self):
        try:
            numero = int(input("NÚMERO DA CONTA: "))
        except ValueError:
            print("Número de conta inválido")
            return
        if numero not in self.contas:
            print("CONTA NÃO ENCONTRADA")
            return

        conta = self.contas[numero]
        while True:
            print("\n[1] SAQUE | [2] DEPÓSITO | [3] EXTRATO | [4] MENU PRINCIPAL")
            opcao = input(">> ")
            match opcao:
                case "1":
                    try:
                        valor = float(input("VALOR DO SAQUE: R$ "))
                        Saque(valor).registrar(conta)
                    except ValueError:
                        print("VALOR INVÁLIDO")
                case "2":
                    try:
                        valor = float(input("VALOR DO DEPÓSITO: R$ "))
                        Deposito(valor).registrar(conta)
                    except ValueError:
                        print("VALOR INVÁLIDO")
                case "3":
                    conta.historico.exibir()
                    print(f"SALDO ATUAL: R$ {conta.saldo:.2f}")
                case "4":
                    break
                case _:
                    print("OPÇÃO INVÁLIDA")

    def exibir_contas(self):
        if not self.contas:
            print("NÃO HÁ CONTAS CADASTRADAS")
            return
        for num, conta in self.contas.items():
            print(f"CONTA {num} | CLIENTE: {conta.cliente.nome} | SALDO: R${conta.saldo:.2f}")

def main():
    banco = Banco()
    print("\nBEM VINDO!\n")

    while True:
        print("\n[1] ACESSAR CONTA")
        print("[2] CADASTRO CLIENTE")
        print("[3] ABERTURA DE CONTA")
        print("[4] EXIBIR CONTAS")
        print("[5] SAIR")
        opcao = input(">> ")

        match opcao:
            case "1":
                banco.acessar_conta()
            case "2":
                banco.criar_cliente()
            case "3":
                banco.criar_conta()
            case "4":
                banco.exibir_contas()
            case "5":
                print("SAINDO...")
                break
            case _:
                print("OPÇÃO INVÁLIDA")


if __name__ == "__main__":
    main()
