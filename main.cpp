#include <iostream>
#include <string>
#include "matrix.h"
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include "./approach_methods/least_squares_method.cpp"

using namespace cv;
using namespace std;

void test_box(Mat image, vector<vector<long double>> matrixImg, int kernelSize=5){
    Matrix matrix_img_box_blur(matrixImg);
    matrix_img_box_blur.box_bluring(kernelSize);
        
    Mat minha_img_box(image.rows,image.cols,CV_8UC1);

    for (int r=0; r< image.rows; r++) {
        for (int c=0; c < image.cols; c++) {
            minha_img_box.at<uchar>(r,c) = static_cast<uchar>(matrix_img_box_blur.matrix[r][c]);

        }
    }

    namedWindow("O GATO BOX", WINDOW_NORMAL);
    resizeWindow("O GATO BOX",400,400);
    imshow("O GATO BOX", minha_img_box);
    waitKey(0);



}

void test_gauss(Mat image, vector<vector<long double>> matrixImg, int kernelSize=5, long double sigma=0.1){
    Matrix matrix_img_box_blur(matrixImg);

    matrix_img_box_blur.gauss_blur(sigma, kernelSize);
        
    Mat minha_img_box(image.rows,image.cols,CV_8UC1);

    for (int r=0; r< image.rows; r++) {
        for (int c=0; c < image.cols; c++) {
            minha_img_box.at<uchar>(r,c) = static_cast<uchar>(matrix_img_box_blur.matrix[r][c]);

        }
    }

    namedWindow("O GATO GAUSS", WINDOW_NORMAL);
    resizeWindow("O GATO GAUSS",400,400);
    imshow("O GATO GAUSS", minha_img_box);
    waitKey(0);
}

void test_gauss_opencv(Mat image,  int kernelSize=5, long double sigma=0.1){
        Mat outputMatrixImg;
       GaussianBlur(image, outputMatrixImg, Size(25,25), 1.5,1.5,0);
        namedWindow("O GATO OPENCV", WINDOW_NORMAL);
        resizeWindow("O GATO OPENCV",400,400);
        imshow("O GATO OPENCV", outputMatrixImg);
        waitKey(0);
}

int main()
{
    cout << "Hello Geek\n";
    Mat image;

    // IMREAD_GRAYSCALE
    // IMREAD_COLOR
    
    image = imread("images/gato.jpg", IMREAD_GRAYSCALE);   // Read the file
    cout << "Width : " << image.cols << endl;
    cout << "Height: " << image.rows << endl;

    namedWindow("O GATO", WINDOW_NORMAL);
    resizeWindow("O GATO",400,400);
    imshow("O GATO", image);
    waitKey(0);


    vector<vector<long double>> matrixImg (
    image.rows,
    vector<long double>(image.cols, 0));

    for (int r=0; r< image.rows; r++){
        for (int c=0; c < image.cols; c++){
            matrixImg[r][c] = static_cast<long double>(image.at<uchar>(r,c));    
        }
    }


    test_box(image,matrixImg, 15);
    // Quando usado -1 o calculo do sigma é feito de maneira automática
    test_gauss(image,matrixImg, 15,  -1);

    return 0;
}

