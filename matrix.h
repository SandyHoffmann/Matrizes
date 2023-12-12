/**
 * \author Sandy Hoffmann
 * \date November 11, 2023
 * \version November 11, 2023
 **/

#ifndef IFMOVE_MATRIX_H
#define IFMOVE_MATRIX_H
#include <vector>
#include <math.h>       /* pow */
#include <string.h>

using namespace std;
/**
* Matrix basic class
* \param i = linha
* \param j = coluna
* \param array = matrix ixj
*/

class Matrix {
    public:
        int i;
        int j;
        vector<vector<long double>> matrix;
        Matrix(vector<vector<long double>> matrix_atr){
            cout << "Inicializating matrix...";
            // definine i and j
            i = matrix_atr.size();
            j = (i > 0) ? matrix_atr[0].size() : 0;
            cout << "i: " << i << ", j: " << j << "\n";
            // matrix is matriz_atr (params)
            matrix = matrix_atr;
        }


        void printar_matriz(){
            cout << "[ ";
            for (int linha = 0; linha < i; ++linha){
                cout << "[";
                for (int coluna = 0; coluna < j; ++coluna){
                    cout << matrix[linha][coluna]; 
                    if (coluna != j-1){
                        cout<< ", ";
                    }

                }
                cout << "] ";
            }
            cout << "] ";
        }

        void printar_kernel(vector<vector<long double>> kernel, int kernelSize){
            cout << "\n[\n";
            for (int linha = 0; linha < kernelSize; ++linha){
                cout << "[";
                for (int coluna = 0; coluna < kernelSize; ++coluna){
                    cout << kernel[linha][coluna]; 
                    if (coluna != kernelSize-1){
                        cout<< ", ";
                    }

                }
                cout << "] \n";
            }
            cout << "]\n ";
        }

        void mudar_valor(int linha, int coluna, long double valor){
            matrix[linha][coluna] = valor;
        }

        void box_bluring(int kernelSize=5){
            // ? EDGES ESTÃO SENDO CONSIDERADAS = 0
            // ? MULTIPLICAR A MATRIZ
            int metade_kernel = kernelSize/2;
            for (int linha = 0; linha < i; ++linha){
                for (int coluna = 0; coluna < j; ++coluna){
                    long int total = 0;
                    #pragma omp parallel for reduction(+:total)
                    for (int linha_r = -metade_kernel; linha_r <= metade_kernel; linha_r++){
                        if (!(linha + linha_r < 0 || linha + linha_r > i-1)){
                            for (int coluna_r = -metade_kernel; coluna_r <= metade_kernel; coluna_r++){
                                if (!(coluna + coluna_r < 0 || coluna + coluna_r > j-1)){
                                // ? linha = linha - 1; linha - 0; linha + 1
                                // ? coluna = coluna - 1; coluna - 0; coluna + 1

                                    total += matrix[linha + linha_r][coluna + coluna_r];
                                }
                            }
                        }
                    }
                    double finalCor = total/(pow(kernelSize,2));
                    mudar_valor(linha, coluna, finalCor);
                }
            }
        }
        void flip_image(){
            for (int linha = 0; linha < i; ++linha){
                for (int coluna = 0; coluna < j/2; ++coluna){

                    int valor_coluna_selecionada_fim = matrix[i-linha-1][j-coluna-1];
                    mudar_valor( i-linha-1, j-coluna-1, matrix[linha][coluna]);
                    mudar_valor(linha, coluna, valor_coluna_selecionada_fim);
                }
            }
        }


        void gauss_blur(double sigma=1, int kernelSize=15){
            printf("GAUSS\n");
            // * Calcular matriz kernel com Gauss de acordo com o sigma estabelecido
            // Para o calculo é estabelecido que no centro do kernel estará o ponto 0,0
            // Vai se estabelecendo as coordenadas de acordo com o plano cartesiano
            vector<vector<long double>> kernel (
            kernelSize,
            vector<long double>(kernelSize, 0));
            int metade_kernel = kernelSize/2;
            if (kernelSize % 2 == 0) {
                metade_kernel-=1;
            }
            
            double total = 0;

            // Automatizando conta do sigma
            if (sigma == -1){
                sigma = kernelSize/4 + 1;
            }

            printf("Sigma: %f\n", sigma);

            // Calculando kernel preliminar
            #pragma omp parallel for reduction(+:total)
            for (int k = 0; k < kernelSize; k++){
                for (int l = 0; l < kernelSize; l++){
                    double gauss_part1 = 1/(2*M_PI*pow(sigma,2));
                    double gauss_part2 = (pow(-metade_kernel+k, 2) + pow(-metade_kernel+l, 2))/(2*pow(sigma,2));

                    double gauss = gauss_part1 * pow(exp(1), -1 * gauss_part2);
                    kernel[k][l] = gauss;
                    total+=gauss;

                }   
            }

            // Equilibrando kernel para que sua soma dê 1
            double total_soma = 0;
            #pragma omp parallel for reduction(+:total_soma)
            for (int k = 0; k < kernelSize; k++){
                for (int l = 0; l < kernelSize; l++){
                    kernel[k][l] = (kernel[k][l])/total;
                    total_soma+=kernel[k][l];
                }   
            }
            printf("soma total: %f\n", total_soma);

            for (int linha = 0; linha < i; ++linha){
                for (int coluna = 0; coluna < j; ++coluna){
                
                    long double total = 0;
                    #pragma omp parallel for reduction(+:total)
                    for (int linha_r = -metade_kernel; linha_r <= metade_kernel; linha_r++){
                        if ((linha + linha_r >= 0 && linha + linha_r < i)){
                            for (int coluna_r = -metade_kernel; coluna_r <= metade_kernel; coluna_r++){
                                if ((coluna + coluna_r >= 0 && coluna + coluna_r < j)){
                                    total += ((matrix[linha + linha_r][coluna + coluna_r]) * (kernel[linha_r+metade_kernel][coluna_r+metade_kernel]));
                                }
                            }
                        }
                    }
                     mudar_valor(linha, coluna, total);

                }
            }

        }

        vector<double> to_single_vector(){
            vector<double> my_vector;
            for (int linha = 0; linha < i; ++linha){
                for (int coluna = 0; coluna < j; ++coluna){
                    my_vector.push_back(matrix[linha][coluna]); 
                }
            }
            return my_vector;
        }
        
};


#endif