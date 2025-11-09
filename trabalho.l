%{
#include <stdio.h>
#include <stdlib.h> // Para atof()
#include <string.h> // Para sscanf()

int checkRange(char* val_str);

%}
%option noyywrap
VOGAL   [AEIOUaeiou]
LETRA   [A-Za-z]
DIGITO  [0-9]

/* Tarefa 2: <ID-N> */
ID_N    {VOGAL}{LETRA}{DIGITO}{DIGITO}{DIGITO}?

/* Tarefa 1: <Valor-V>*/
REAL    (-)?({DIGITO}+(\.{DIGITO}*)?|\.{DIGITO}+)

/* Tarefa 3: <Ponto-(X,Y)> */
PONTO   \({REAL},{REAL}\)


%%


"<Triangulo-"{ID_N}"-"{PONTO}"-"{PONTO}"-"{PONTO}">" {
    char id[10], x1[100], y1[100], x2[100], y2[100], x3[100], y3[100];
    sscanf(yytext, "<Triangulo-%[^-]-(%[^,],%[^)])-(%[^,],%[^)])-(%[^,],%[^)])>", 
           id, x1, y1, x2, y2, x3, y3);
    
    if (checkRange(x1) && checkRange(y1) && checkRange(x2) && checkRange(y2) && checkRange(x3) && checkRange(y3)) {
        printf("TOKEN: <Triangulo-ID-P1-P2-P3> (ID: %s, P1: (%s,%s), P2: (%s,%s), P3: (%s,%s)) -> VALIDO\n", id, x1, y1, x2, y2, x3, y3);
    } else {
        printf("TOKEN: <Triangulo-ID-P1-P2-P3> (ID: %s) -> INVALIDO (Valores fora do range [-1000, 1000])\n", id);
    }
}

"<Retangulo-"{ID_N}"-"{PONTO}"-"{PONTO}">" {
    char id[10], x1[100], y1[100], x2[100], y2[100];
    sscanf(yytext, "<Retangulo-%[^-]-(%[^,],%[^)])-(%[^,],%[^)])>", 
           id, x1, y1, x2, y2);
           
    if (checkRange(x1) && checkRange(y1) && checkRange(x2) && checkRange(y2)) {
        printf("TOKEN: <Retangulo-ID-P1-P2> (ID: %s, P1: (%s,%s), P2: (%s,%s)) -> VALIDO\n", id, x1, y1, x2, y2);
    } else {
        printf("TOKEN: <Retangulo-ID-P1-P2> (ID: %s) -> INVALIDO (Valores fora do range [-1000, 1000])\n", id);
    }
}

"<Circulo-"{ID_N}"-"{PONTO}"-"{REAL}">" {
    char id[10], x[100], y[100], r[100];
    sscanf(yytext, "<Circulo-%[^-]-(%[^,],%[^)])-%[^>]>", 
           id, x, y, r);

    if (checkRange(x) && checkRange(y) && checkRange(r)) {
        printf("TOKEN: <Circulo-ID-P-R> (ID: %s, P: (%s,%s), R: %s) -> VALIDO\n", id, x, y, r);
    } else {
        printf("TOKEN: <Circulo-ID-P-R> (ID: %s) -> INVALIDO (Valores fora do range [-1000, 1000])\n", id);
    }
}


"<Ponto-"{PONTO}">" {
    char x[100], y[100];
    sscanf(yytext, "<Ponto-(%[^,],%[^)])>", x, y);
    
    if (checkRange(x) && checkRange(y)) {
        printf("TOKEN: <Ponto-(X,Y)> (X: %s, Y: %s) -> VALIDO\n", x, y);
    } else {
        printf("TOKEN: <Ponto-(X,Y)> (X: %s, Y: %s) -> INVALIDO (Valores fora do range [-1000, 1000])\n", x, y);
    }
}

"<Raio-"{REAL}">" {
    char val[100];
    sscanf(yytext, "<Raio-%[^>]>", val);
    
    if (checkRange(val)) {
        printf("TOKEN: <Raio-V> (Raio: %s) -> VALIDO\n", val);
    } else {
        printf("TOKEN: <Raio-V> (Raio: %s) -> INVALIDO (Raio fora do range [-1000, 1000])\n", val);
    }
}

"<Valor-"{REAL}">" {
    char val[100];
    sscanf(yytext, "<Valor-%[^>]>", val);
    
    if (checkRange(val)) {
        printf("TOKEN: <Valor-V> (Valor: %s) -> VALIDO\n", val);
    } else {
        printf("TOKEN: <Valor-V> (Valor: %s) -> INVALIDO (Valor fora do range [-1000, 1000])\n", val);
    }
}

"<ID-"{ID_N}">" {
    char id[10];
    sscanf(yytext, "<ID-%[^>]>", id);
    printf("TOKEN: <ID-N> (ID: %s) -> VALIDO\n", id);
}

[ \t\n]+ {}

. { }

%%


int checkRange(char* val_str) {
    double val = atof(val_str);
    if (val >= -1000.0 && val <= 1000.0) {
        return 1; 
    }
    return 0;
}

int main(int argc, char** argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Erro ao abrir ficheiro");
            return 1;
        }
        yyin = file;
    } else {
        printf("A analisar input da consola (stdin). Pressione Ctrl+D para terminar.\n");
        yyin = stdin;
    }
    
    yylex(); 
    
    return 0;
}
