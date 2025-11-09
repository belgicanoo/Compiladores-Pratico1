import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys 

RE_ID = r"([AEIOUaeiou][A-Za-z]\d{2,3})"

RE_REAL = r"(-?\d*\.?\d+)"

RE_CIRCULO = re.compile(
    r"<Circulo-" + RE_ID + r"-" +  
    r"\(" + RE_REAL + r"\s*,\s*" + RE_REAL + r"\)" + 
    r"-" + RE_REAL + r">"
)

RE_RETANGULO = re.compile(
    r"<Retangulo-" + RE_ID + r"-" + 
    r"\(" + RE_REAL + r"\s*,\s*" + RE_REAL + r"\)" + 
    r"-\(" + RE_REAL + r"\s*,\s*" + RE_REAL + r"\)>"
)

RE_TRIANGULO = re.compile(
    r"<Triangulo-" + RE_ID + r"-" + 
    r"\(" + RE_REAL + r"\s*,\s*" + RE_REAL + r"\)" + 
    r"-\(" + RE_REAL + r"\s*,\s*" + RE_REAL + r"\)" + 
    r"-\(" + RE_REAL + r"\s*,\s*" + RE_REAL + r"\)>"
)


def desenhar_figuras(nome_ficheiro):
    """
    Lê um ficheiro de texto e desenha as figuras geométricas
    encontradas usando matplotlib.
    """
    fig, ax = plt.subplots()
    
    ax.set_xlim(-1000, 1000)
    ax.set_ylim(-1000, 1000)
    ax.set_aspect('equal') 
    ax.grid(True)

    print(f"A processar o ficheiro: {nome_ficheiro}\n")
    figuras_desenhadas = 0

    try:
        with open(nome_ficheiro, 'r') as f:
            for i, linha in enumerate(f):
                linha = linha.strip()
                if not linha or linha.startswith('#'):
                    continue

                if match := RE_CIRCULO.match(linha):
                    try:
                        grupos = match.groups()
                        id_fig = grupos[0]
                        centro_x = float(grupos[1]) 
                        centro_y = float(grupos[2]) 
                        raio = float(grupos[3])   
                        
                        print(f"Desenhando Círculo: {id_fig} @ ({centro_x},{centro_y}), R={raio}")
                        circulo = patches.Circle((centro_x, centro_y), raio, fill=False, color='blue')
                        ax.add_patch(circulo)
                        ax.text(centro_x, centro_y, id_fig, ha='center', va='center', fontsize=8, color='blue')
                        figuras_desenhadas += 1
                        
                    except Exception as e:
                        print(f"Erro ao processar Círculo (linha {i+1}: {linha}): {e}")

                elif match := RE_RETANGULO.match(linha):
                    try:
                        grupos = match.groups()
                        id_fig = grupos[0]
                        p1_x = float(grupos[1])
                        p1_y = float(grupos[2]) 
                        p2_x = float(grupos[3]) 
                        p2_y = float(grupos[4]) 
                        
                        largura = abs(p2_x - p1_x)
                        altura = abs(p2_y - p1_y)
                        
                        print(f"Desenhando Retângulo: {id_fig} [({p1_x},{p1_y}) a ({p2_x},{p2_y})]")
                        ponto_ancora = (p1_x, p2_y)
                        
                        retangulo = patches.Rectangle(ponto_ancora, largura, altura, fill=False, color='green')
                        ax.add_patch(retangulo)
                        ax.text(p1_x, p1_y, id_fig, ha='left', va='top', fontsize=8, color='green')
                        figuras_desenhadas += 1

                    except Exception as e:
                        print(f"Erro ao processar Retângulo (linha {i+1}: {linha}): {e}")
                        
                elif match := RE_TRIANGULO.match(linha):
                    try:
                        grupos = match.groups()
                        id_fig = grupos[0]
                        p1_x = float(grupos[1]) 
                        p1_y = float(grupos[2]) 
                        p2_x = float(grupos[3]) 
                        p2_y = float(grupos[4]) 
                        p3_x = float(grupos[5]) 
                        p3_y = float(grupos[6]) 
                        
                        pontos = [[p1_x, p1_y], [p2_x, p2_y], [p3_x, p3_y]]
                        print(f"Desenhando Triângulo: {id_fig} com vértices {pontos}")
                        
                        triangulo = patches.Polygon(pontos, closed=True, fill=False, color='red')
                        ax.add_patch(triangulo)
                        figuras_desenhadas += 1
                        
                        centro_x = (p1_x + p2_x + p3_x) / 3
                        centro_y = (p1_y + p2_y + p3_y) / 3
                        ax.text(centro_x, centro_y, id_fig, ha='center', va='center', fontsize=8, color='red')

                    except Exception as e:
                        print(f"Erro ao processar Triângulo (linha {i+1}: {linha}): {e}")

                else:
                    print(f"Linha ignorada (formato inválido): {linha}")

    except FileNotFoundError:
        print(f"Erro: O ficheiro '{nome_ficheiro}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return

    if figuras_desenhadas > 0:
        plt.title("Desenho de Figuras Geométricas")
        plt.xlabel("Eixo XX")
        plt.ylabel("Eixo YY")
        plt.show()
    else:
        print("\nNenhuma figura válida foi encontrada ou desenhada.")
        plt.close(fig)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        nome_ficheiro = sys.argv[1]
    else:
        nome_ficheiro = "fich.txt" 
        
    desenhar_figuras(nome_ficheiro)
