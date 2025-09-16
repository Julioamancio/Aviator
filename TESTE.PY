# ================================
# Soluções dos 3 desafios (Python)
# ================================

# ----------------------------------------------------
# 🧩 Desafio 1 – saudacao(nome)
# Objetivo: retornar uma saudação personalizada (string)
# sem imprimir dentro da função.
# ----------------------------------------------------

def saudacao(nome):  # Define a função com o parâmetro 'nome'.
    mensagem = f"Olá, {nome}!"  # Monta a mensagem usando f-string.
    return mensagem  # Retorna a string; não há print dentro da função.

# Exemplo de uso do Desafio 1 (fora da função):
resultado_saudacao = saudacao("Maria")  # Chama a função passando "Maria".
print(resultado_saudacao)  # Exibe no console a saudação retornada.


# ----------------------------------------------------
# 🧩 Desafio 2 – eh_par(n)
# Objetivo: retornar True se o número for par e False
# se for ímpar, usando o operador módulo (%).
# Observação: a função não imprime nada; a entrada e o
# print ficam fora da função.
# ----------------------------------------------------

def eh_par(n):  # Define a função com um parâmetro numérico 'n'.
    return n % 2 == 0  # Retorna True se o resto por 2 for 0; caso contrário, False.

# Entrada do usuário (fora da função):
entrada = input("Digite um número inteiro: ")  # Solicita um número inteiro ao usuário.
n = int(entrada)  # Converte a string digitada para inteiro (pode lançar erro se não for número).
resultado_par = eh_par(n)  # Chama a função e guarda o valor booleano retornado.
print(resultado_par)  # Exibe True (par) ou False (ímpar) no console.


# ----------------------------------------------------
# 🧩 Desafio 3 – calcular_media(a, b, c)
# Objetivo: receber 3 notas e retornar a média com
# duas casas decimais usando round(media, 2).
# A função não deve imprimir nada.
# ----------------------------------------------------

def calcular_media(a, b, c):  # Define a função que recebe três números (notas).
    media = (a + b + c) / 3  # Calcula a média aritmética das três notas.
    return round(media, 2)  # Arredonda a média para 2 casas decimais e retorna.

# Testes do Desafio 3 (fora da função):
print(calcular_media(7, 8, 9))        # Exemplo 1: deve exibir 8.0
print(calcular_media(5.5, 6.3, 7.2))  # Exemplo 2: deve exibir 6.33





