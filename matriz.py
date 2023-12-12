from random import randint
import copy
from functools import reduce
import unittest
# Repositório com operações com matrizes feita na disciplina de métodos númericos
class Matriz:
    def __init__(self, linha:int, coluna:int):
        self.l = linha 
        self.c = coluna 
        self.iniciar()

    @classmethod
    def from_list(self, lista):
        objeto = self.__new__(self)
        objeto.m = lista
        objeto.l = len(lista)
        objeto.c = len(lista[0])
        return objeto

    def iniciar(self, zeros=True):
        self.m = [] 
        for i in range(self.l):
            self.m.append([]) # cria linha 
            for j in range(self.c):
                
                num = 0 if zeros else randint(1,10)

                # num = randint(1, 10)
                self.m[i].append(num) # preenche coluna

    def alocar(self, valor, numLinha, numColuna):
        self.m[numLinha-1][numColuna-1] = valor

    # * Função para printar matriz em forma de string
    def __str__(self):
        matriz_string = ''

        for i in range(self.l):
            for j in range(self.c):
                matriz_string += f'{self.m[i][j]} '

            matriz_string += '\n'

        return matriz_string         

    # * Função para multiplicação de matrizes
    def __mul__(self, m2):

        if isinstance(m2, int):
            n = Matriz(self.l, self.c) # nova matriz 
            for i in range(self.l):
                for j in range(self.c):
                    n.m[i][j] = self.m[i][j] * m2
            return n

        if self.c != m2.l:
            print('Operação inválida: a quantidade de colunas da matriz a' +
                'esquerda deve ser igual a quantidade de linhas da matriz a direita' +
                f'mas {self.c} != {m2.l}')
            return
        

        n = Matriz(self.l, m2.c) # nova matriz 


        for i in range(self.l):
            for j in range(m2.c):
                soma = 0
                for k in range(self.c): # índice auxiliar
                    soma += self.m[i][k] * m2.m[k][j]

                n.m[i][j] = soma 

        return n


    # * Função para soma de matrizes
    def __add__(self, m2):
        if self.l != m2.l or self.c != m2.c:
            print('Operação inválida: as matrizes devem ter a mesma dimensão')
            return

        n = Matriz(self.l, self.c)

        for i in range(self.l):
            for j in range(self.c):
                n.m[i][j] = self.m[i][j] + m2.m[i][j]
        
        return n

    # * Função de subtração de linhas
    def subtrair_linha(self, indiceLinha1, indiceLinha2, multLinha1=1, multLinha2=1):
        linha2 = [ x * multLinha2 for x in self.m[indiceLinha2] ]
        for i in range(self.l):
            for j in range(self.c):
                if i == indiceLinha1:
                    self.m[i][j] = self.m[i][j] * multLinha1 - linha2[j]

    # * Função de escalona na forma de Gauss ou Jordan, dependendo do input do usuário
    def escalonarGaussOuJordan(self, jordan=False):
        # * Declarações Comuns

        lista_operadores = []
        lista_matrizes = []

        parametrosIFor = []
        parametrosKFor = []

        # * Mudando sentido de range, dependendo do parametro jordan booleano da função

        if jordan:
            parametrosIFor = range(self.l-1,-1,-1)
            parametrosKFor = [-1,-1,-1]
        else:
            parametrosIFor = range(0, self.l, 1)
            parametrosKFor = [1,self.l,1]

        # * Loop principal
        indice = 0
        lista_trocas_pivo = []
        for i in parametrosIFor:
            pivo = self.m[i][i]
            indice_pivo = i
            lista_operadores.append(self.gerarIdentidade(self.c))
            # * Pivoteamento simples
            maiorPivoEmModulo = pivo
            lista_trocas = [l for l in range(self.l)]
            for p in range(i+parametrosKFor[0], parametrosKFor[1], parametrosKFor[2]):
                if abs(self.m[p][i]) > pivo:
                    # * Trocando na lista de save temporário de pivos
                    save_temp = lista_trocas[indice_pivo]
                    lista_trocas[indice_pivo] = p
                    lista_trocas[p] = save_temp
                    # * Fazendo a troca na matriz em si
                    # save_temp_m = self.m[indice_pivo]
                    # self.m[indice_pivo] = self.m[p]
                    # self.m[p] = save_temp_m
                    indice_pivo = p

            print(self.m)
            lista_trocas_pivo.append(lista_trocas)
            for k in range(i+parametrosKFor[0], parametrosKFor[1], parametrosKFor[2]):
                primeiro = self.m[k][i] 
                lista_operadores[indice][k][i] = primeiro
                self.subtrair_linha(k, i, pivo, primeiro)
            lista_matrizes.append(Matriz.from_list(copy.deepcopy(self.m)))
            lista_operadores[indice] = Matriz.from_list(lista_operadores[indice])
            indice += 1
            for matriz in lista_matrizes:
                print(matriz.m)

        print(lista_trocas_pivo)

        return lista_operadores, lista_matrizes
    
    # * Gauss + Jordan
    def gaussJordan(self):
        xs = []
        linha = {}
        for i in range(self.l):
            linha = [l for l in self.m[i] if l != 0]
            xs.append(linha[1]/linha[0])
        print(xs)

    # * Matriz transposta
    def transposta(self, matriz=False):
        if (not matriz):
            matriz = self.m
        matriz_transposta = [[0 for j in range(len(matriz))] for l in range(len(matriz))]
        matriz_copia = copy.deepcopy(matriz)
        for i in range(0,len(matriz)):
            for j in range(0,len(matriz)):
                matriz_transposta[i][j] = matriz_copia[j][i]

        return matriz_transposta

    # * Matriz LU
    # -> https://www.geeksforgeeks.org/l-u-decomposition-system-linear-equations/

    def decompondo_matriz_L_U(self):
        lista_operadores_gauss, lista_matrizes_gauss = self.escalonarGaussOuJordan(jordan=False)

        print(lista_operadores_gauss)
        begin = True
        matriz_original = Matriz(3,3)

        # ! FAZENDO PARA GAUSS

        lista_ls = lista_operadores_gauss
        lista_us = lista_matrizes_gauss

        resultados_c = Matriz.from_list([[1, 2, 3]])

        lista_l = Matriz.from_list(self.gerarIdentidade(self.l))
        for i in range(len(lista_ls)):
            print("----------------------")
            print(f'T{i+1}')
            print(lista_ls[i])
            print(f'M{i+1}')
            print(lista_us[i])
            print("T*M = ")
            print(lista_ls[i] * lista_us[i])
            print("----------------------")
            
            lista_l = lista_ls[i] + lista_l

            lista_l.alocar(1,0,0)
            lista_l.alocar(1,1,1)
            lista_l.alocar(1,2,2)

        lista_u = lista_us[-1]


        print("L")
        print(lista_l)
        print("U")
        print(lista_u)


        LC_merged = copy.deepcopy(lista_l.m).append(copy.deepcopy(resultados_c.m))
        print(LC_merged)

    # * Substituição de variaveis de forma direta ou indireta
    def substituicaoDiretaOuIndireta(self, matriz_triangular, Indireta=False):
        if not matriz_triangular:
            matriz_triangular = self.m
        reverse = False
        parametrosIFor = range(self.l)
        parametrosJFor = range(self.c-1)
        if Indireta:
            parametrosIFor = range(self.l-1,-1,-1)
            parametrosJFor = range(0, self.c-1)
            reverse = True

        lista_xs = [1 for i in range(self.c)]
        lista_resultado = []

        for i in parametrosIFor:
            divisor = matriz_triangular[i][i]
            matriz_triangular[i][i] = 0
            soma = 0

            for j in parametrosJFor:
                soma += matriz_triangular[i][j] * lista_xs[j]
            resultado = (matriz_triangular[i][self.l] - soma) / divisor
            lista_xs[i] = resultado
            lista_resultado.append(resultado)
        
        if reverse:
            lista_resultado.reverse()
        for resultado in lista_resultado:
            print(resultado)
        return lista_resultado

    # * Gerador da matriz identidade
    def gerarIdentidade(self, tamanho):
        print(tamanho)
        lista_identidade = []
        for i in range(tamanho):
            lista_identidade.append([])
            for j in range(tamanho):
                if i == j:
                    print(i)
                    print(j)
                    lista_identidade[i].append(1)
                else:
                    lista_identidade[i].append(0)

        return lista_identidade
    
    # * Método de Cholesky
    def cholesky(self, matriz=False):
        if (not matriz):
            matriz = self.m
        nova_matriz = self.gerarIdentidade(self.c)
        for i in range(0, self.l):

            for j in range(i, self.l):
                if i == j:
                    quadrados_m = 0
                    for k in range(0, i):
                        quadrados_m += nova_matriz[i][k] ** 2
                    numeroii = ((matriz[j][i])-quadrados_m)**(1/2)
                    nova_matriz[j][i] = numeroii
                else:
                    multiplicacao = 0
                    for k in range(0,i):
                        multiplicacao += nova_matriz[i][k] * nova_matriz[j][k]
                    numeroji = ((matriz[j][i]) - multiplicacao)/nova_matriz[i][i]
                    nova_matriz[j][i] = numeroji
        return nova_matriz

    def formata_equacao(self):
        coeficientes = []
        for linha in self.m:
            linha_sem_zero = list(filter(lambda l: l != 0,linha))
            coeficientes.append(linha_sem_zero[1] * (1/(linha_sem_zero[0])))
        print("coeficientes")
        print(coeficientes)

def main():
    m1=Matriz(4,4)
    m1 = Matriz.from_list([
        [204, 1296, 8772, 319.1],
        [36, 204, 1296, 50.5],
        [8, 36, 204, 9.2]
        ])
    m1.escalonarGaussOuJordan()
    m1.escalonarGaussOuJordan(True)
    print(m1.m)
    m1.formata_equacao()

class TestingMatriz(unittest.TestCase):
    def test_creation(self):
        m1 = Matriz.from_list([
        [4, -2, 2], 
        [-2, 10, -7],
        [2, -7, 6]])
        self.assertEqual(m1.m, [ [4, -2, 2], 
        [-2, 10, -7],
        [2, -7, 6]])

    def test_sum(self):
        m1 = Matriz.from_list([
        [1, 2, 3], 
        [4, 5, 6],
        [7, 8, 9]])
        m2 = Matriz.from_list([
        [4, -2, 2], 
        [-2, 10, -7],
        [2, -7, 6]])
        self.assertEqual((m1 + m2).m, [[5, 0, 5], 
        [2, 15, -1],
        [9, 1, 15]])

    def test_gauss(self):
        m1 = Matriz.from_list([
        [2, 1, -1, 8], 
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]])
        m1.escalonarGaussOuJordan()
        self.assertEqual(m1.m, [[2, 1, -1, 8], 
        [0, 1, 1, 2],
        [0, 0, -2, 2]])
        resultados = m1.substituicaoDiretaOuIndireta(False,True)
        self.assertEqual(resultados, [2,3,-1])

    def test_gauss_jordan(self):
                
        m1 = Matriz.from_list([
        [2, 1, -1, 8], 
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]])
        m1.escalonarGaussOuJordan()
        m1.escalonarGaussOuJordan(True)
        self.assertEqual(m1.m, [[8, 0, 0, 16], 
        [0, -2, 0, -6],
        [0, 0, -2 , 2]])
    
    def test_cholesky(self):
        m1 = Matriz.from_list([
        [4, 2, -4], 
        [2, 10, 4],
        [-4, 4, 9]])
        
        self.assertEqual(m1.cholesky(False), [[2,0,0],[1,3,0],[-2,2,1]])

    def test_transposta(self):
        m1 = Matriz.from_list([
        [2,0,0],[1,3,0],[-2,2,1]])

        self.assertEqual(m1.transposta(), [[2,1,-2],[0,3,2],[0,0,1]])

    # ! TESTAR L.U TBM


if __name__ == "__main__":
    main()
    # unittest.main()

