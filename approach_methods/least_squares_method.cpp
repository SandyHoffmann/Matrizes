/**
 * \author Sandy Hoffmann
 * \date November 11, 2023
 * \version November 11, 2023
 **/
#include <iostream>
#include <vector>
#include <string>
#include <cmath>

#include "../matrix.h"
using namespace std;



/**
* Least Square Aproach Method
* \param equacao (formato: a + b*x + c*x^2)
* \param grau (para facilitar, usuario informa grau e ja teremos as funções sigma listadas)
* \param pontos (formato: [[x1,x2,..,xn], [y1,y2,..,yn]])
*/

void least_square_method(string equacao="a + b*x + c*(x**2)", int grau=3,  Matrix matrix_test=Matrix({{1,2,3,4,5,6,7,8},{0.5,0.6,0.9,0.8,1.2,1.5,1.7,2}})){
    // grau para numero ser elevado.
    int graus[4] = {0, 1, 2, 3};
    vector<vector<double>> resultados;
    for (int grau_repeticao_i = 0; grau_repeticao_i < grau; grau_repeticao_i+=1){
        vector<double> resultados_linha;
        for (int grau_repeticao_j = 0; grau_repeticao_j < grau; grau_repeticao_j+=1){

            double soma = 0;
            // * Soma para as linhas do lado esquerdo da igualdade
            for (int linha = 0; linha < matrix_test.j; linha+=1){
                soma += pow(matrix_test.matrix[0][linha], grau_repeticao_j) * pow(matrix_test.matrix[0][linha], grau_repeticao_i);
            }
            cout << "soma: " << soma << "\n";
            resultados_linha.push_back(soma);
        }
        double soma_dir = 0;
        // * Soma para as linhas do lado direito da igualdade
        for (int linha = 0; linha < matrix_test.j; linha+=1){
            soma_dir += matrix_test.matrix[1][linha] * pow(matrix_test.matrix[0][linha], grau_repeticao_i);
        }
        cout << "= : " << soma_dir << "\n";

        resultados_linha.push_back(soma_dir);
        resultados.push_back(resultados_linha);
    }

}