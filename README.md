# Matrizes

# openCV

## Instalação e configuração (linux)
Instalei a biblioteca libopencv-dev:
>sudo apt install libopencv-dev

Segui esse tutorial para setar os pacotes: 
>http://www.codebind.com/cpp-tutorial/install-opencv-ubuntu-cpp/

Se der o erro que a flag de desenvolvimento não estiver configurada basta:
>pkg-config --list-all

>*Vai dar o nome do pacote (o meu por exemplo estava como opencv4)

E então compilar o código da seguinte maneira:
>g++ main.cpp -o a.out `pkg-config --cflags --libs opencv4`
