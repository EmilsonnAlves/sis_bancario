from datetime import datetime

clientes = {}
contas = {}
limite_saque = 300
saque_diario = 3

def adicionar_cliente():
    tentativas = 0
    while tentativas < 3:
        entrada=input("CPF: ")
        if not entrada.isdigit():
            print("DIGITE APENAS NUMEROS")
            tentativas += 1
            continue
        else:
            cpf = int(entrada)
            if cpf in clientes.keys():
                print("CLIENTE JÁ CADASTRADO")
                return
            nome = input("NOME COMPLETO: ")
            if not nome.replace(" ","").isalpha():
                print("NOME INVÁLIDO.")
                tentativas += 1
                continue
            clientes[cpf]= {"nome": nome}
            print("CADASTRO EFETUADO COM SUCESSO")
            print("DESEJA CRIAR CONTA CORRENTE?\n[1] SIM\n[2] NÃO")
            opcao=int(input(">>"))
            if opcao == 1:
                abertura_conta()
                return
            else:
                print("SAINDO")
                return

def abertura_conta():
    tentativas = 0
    while tentativas < 3:
        entrada = input("CPF: ")
        if not entrada.isdigit():
            print("DIGITE APENAS NUMEROS")
            tentativas += 1
            continue
        cpf = int(entrada)
        if cpf in contas.values():
            print("CLIENTE JÁ POSSUI CONTA NO BANCO")
            return
        if cpf in clientes.keys():
            numero_conta = len(contas) + 1
            contas[numero_conta]={"cpf": cpf, "saldo": 0, "extrato": [], "saque_atual": 0}
            print("ABERTURA DE CONTA CONCLUÍDA")
            return
        else:
            print("USUÁRIO NÃO ENCONTRADO, DESEJA REALIZAR CADASTRO?\n[1] SIM\n[2] NÃO")
            opcao = int(input(">>"))
            if opcao == 1:
                adicionar_cliente()
                return
            else:
                print("SAINDO")
                return
def saque(numero_conta):
    if contas[numero_conta]["saque_atual"] >= saque_diario:
        print("\nLIMITE DIÁRIO DE SAQUE ATINGIDO")
        return
    if contas[numero_conta]["saldo"] <= 0:
        print("\nNÃO POSSUI SALDO PARA SAQUE")
        return
    tentativas = 0
    while tentativas <3:
        try:
            valor = float(input("VALOR DO SAQUE: R$ :"))
        except ValueError:
            print("VALOR INVÁLIDO, DIGITE APENAS NÚMEROS.")
            tentativas+=1
            continue
        if valor > limite_saque:
            print("VALOR ACIMA DO LIMITE DE SAQUE")
            tentativas += 1
            continue
        elif valor > contas[numero_conta]["saldo"]:
            print("SALDO INSUFICIENTE")
            tentativas += 1
            continue
        else:
            contas[numero_conta]["saldo"] -= valor
            contas[numero_conta]["saque_atual"] += 1
            contas[numero_conta]["extrato"].append(f"SAQUE: {valor} /{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"SAQUE EFETUADO. SALDO ATUAL R${contas[numero_conta]['saldo']:.2f}")
            return

def deposito(numero_conta):
    tentativas = 0
    while tentativas <3:
        try:
            valor = float(input("VALOR DO DEPÓSITO: R$ "))
        except ValueError:
            print("VALOR INVÁLIDO, DIGITE APENAS NÚMEROS.")
            tentativas += 1
            continue
        if valor < 0:
            print("DIGITE UM VALOR MAIOR QUE ZERO")
            tentativas += 1
            continue
        contas[numero_conta]["saldo"] += valor
        contas[numero_conta]["extrato"].append(f"DEPÓSITO: {valor} /{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"DEPÓSITO EFETUADO. SALDO ATUAL R${contas[numero_conta]['saldo']:.2f}")
        return

def extrato(numero_conta):
    print("\n" + "=" * 10 + "EXTRATO" + "=" * 10)
    if contas[numero_conta]["extrato"]:
        for operacao in contas[numero_conta]["extrato"]:
            print(operacao)
        print(f"\nSALDO ATUAL: R$ {contas[numero_conta]['saldo']:.2f}")
    else:
        print("\nNÃO FORAM REALIZADAS OPERAÇÕES.")
        print(f"\nSALDO ATUAL: R$ {contas[numero_conta]['saldo']:.2f}")
        print("\n" + "=" * 27)

def exibir_contas():
    if contas:
        for item in contas.items():
            print(item)
        return
    print("NÃO HÁ CONTAS CADASTRADAS")

print("\t" * 5 + "BEM VINDO!" + "\t" * 10)
print("-" * 50)
while True:
    print("\n" + "\t" * 3 + "SELECIONE A OPERAÇÃO\n")
    print("\t" * 3 + "[1] ACESSAR CONTA")
    print("\t" * 3 + "[2] CADASTRO CLIENTE")
    print("\t" * 3 + "[3] ABERTURA DE CONTA")
    print("\t" * 3 + "[4] EXIBIR CONTAS")  # Aqui será implementado um sistema de autorização
    print("\t" * 3 + "[5] SAIR")
    opcao = input("\t"*4 + ">>")

    match opcao:
        case "1":
            tentativas = 0
            retornar_menu = 0
            while tentativas < 3 and retornar_menu == 0:
                try:
                    conta = int(input("\t" * 3 + "NÚMERO DA CONTA: "))
                    if conta in contas.keys():
                        tentativas = 0
                        while True:
                            try:
                                print("\n" + "\t"*2 + "SELECIONE A OPERAÇÃO\n")
                                print("\t"*3 + "[1] SAQUE")
                                print("\t"*3 + "[2] DEPÓSITO")
                                print("\t"*3 + "[3] EXTRATO")
                                print("\t"*3 + "[4] MENU PRINCIPAL")
                                opcao = input("\t"*4 + ">>")

                                match opcao:
                                    case "1":
                                        saque(conta)
                                    case "2":
                                        deposito(conta)
                                    case "3":
                                        extrato(conta)
                                    case "4":
                                        retornar_menu = 1
                                        break
                                    case _:
                                        print("\n" + "\t"*3 + "OPERAÇÃO INVÁLIDA")
                                        tentativas+=1
                                        continue
                            except ValueError:
                                print("\n" + "\t"*3 + "OPERAÇÃO INVÁLIDA")
                                tentativas+=1
                                continue
                    else:
                        print("\n" + "\t"*3 + "CONTA NÃO ENCONTRADA")
                        break
                except ValueError:
                    print("\n" + "\t"*3 + "ERRO. TENTE NOVAMENTE")
                    tentativas+=1
                    continue
        case "2":
            adicionar_cliente()
        case "3":
            abertura_conta()
        case "4":
            exibir_contas()
        case "5":
            exit()
        case _:
            print("\n" + "\t" * 4 + "OPERAÇÃO INVÁLIDA")
            continue

