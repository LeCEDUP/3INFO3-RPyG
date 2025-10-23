def mostrar_menu():
    print("Menu Principal")
    print("--------------")
    print("1. Modo História")
    print("2. Modo Infinito")
    print("3. Sair")    

print("Bem vindo ao RPyG")
print("-----------------")
print("finge que aqui tem uma intro")
print("-----------------")
nome_do_heroi = input("Insira um nome para o seu Herói: ")
print("-----------------")

mostrar_menu()
escolha = input('Insira uma Opção')
if escolha == '1':
    print("Exemplo história")
elif escolha == '2':
    print("Exemplo Infinito")