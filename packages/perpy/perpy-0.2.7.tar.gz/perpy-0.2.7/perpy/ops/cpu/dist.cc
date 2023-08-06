#include "dist.h"




double _dist(double* x, double* y, int num){
    double res = 0.0;
    for(int i=0; i<num; i++){
        x[i] -= y[i];
        x[i] *= x[i];
    }
    
    for(int i=0; i<num; i++){
        res += x[i];
    }
    
    return sqrt(res);
}

