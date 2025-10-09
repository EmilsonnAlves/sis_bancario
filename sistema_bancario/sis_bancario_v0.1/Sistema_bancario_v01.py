contas = {1:{"cliente": "João", "saldo": 800, "extrato": [], "saque_atual": 0},
          2:{"cliente": "Maria", "saldo": 500, "extrato": [], "saque_atual": 0}}
limite_saque = 300
saque_diario = 3

def saque(numero_conta):
    if contas[numero_conta]["saque_atual"] >= saque_diario:
        print("LIMITE DIÁRIO DE SAQUE ATINGIDO")
        return
    valor = int(input("VALOR DO SAQUE: R$ "))
    if valor > limite_saque:
        print("VALOR ACIMA DO LIMITE DE SAQUE")
    elif valor > contas[numero_conta]["saldo"]:
        print("SALDO INSUFICIENTE")
    else:
        contas[numero_conta]["saldo"] -= valor
        contas[numero_conta]["saque_atual"] += 1
        contas[numero_conta]["extrato"].append(f"SAQUE: {valor}")
        print(f"SAQUE EFETUADO. SALDO ATUAL R${contas[numero_conta]['saldo']:.2f}")

def deposito(numero_conta):
    valor = int(input("VALOR DO DEPÓSITO: R$ "))
    if valor > 0:
        contas[numero_conta]["saldo"] += valor
        contas[numero_conta]["extrato"].append(f"DEPÓSITO: {valor}")
        print(f"DEPÓSITO EFETUADO. SALDO ATUAL R${contas[numero_conta]['saldo']:.2f}")
    else:
        print("VALOR INVÁLIDO")

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

print("\t" * 5 + "BEM VINDO!" + "\t" * 10)
print("-" * 50)
while True:
    try:
        conta = int(input("NÚMERO DA CONTA: "))
        if conta in contas.keys():
            while True:
                try:
                    print("\n" + "\t"*2 + "SELECIONE A OPERAÇÃO" + "\t"*2)
                    print("\t"*4 + "[1] SAQUE")
                    print("\t"*4 + "[2] DEPÓSITO")
                    print("\t"*4 + "[3] EXTRATO")
                    print("\t"*4 + "[4] SAIR")
                    opcao = int(input("\t"*4 + ">>"))

                    match opcao:
                        case 1:
                            saque(conta)
                        case 2:
                            deposito(conta)
                        case 3:
                            extrato(conta)
                        case 4:
                            break
                        case _:
                            print("\n" + "\t"*4 + "OPERAÇÃO INVÁLIDA")
                            continue

                except ValueError:
                    print("\n" + "\t"*4 + "OPERAÇÃO INVÁLIDA")
                    continue
        else:
            print("CONTA NÃO ENCONTRADA")
            continue
    except ValueError:
        print("ERRO. TENTE NOVAMENTE")
        continue
