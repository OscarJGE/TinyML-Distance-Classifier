import numpy as np
import pandas as pd
from pathlib import Path

def Datos_entrenamiento(matriz,x1,xn):
    xin = matriz[:,x1:xn+1]
    return xin

def Datos_validacion(matriz,xji,xjn):
    xjn = matriz[:,xji:xjn+1]
    return xjn

def entrenamiento(pesos, bias, tasa_aprendizaje, epocas, xi, d):
    print("\nAprendiendo...")
    for ep in range(epocas):
        error_total = 0
        for i in range(len(xi)):
            prediccion = activacion(pesos, xi[i], bias)
            error = d[i] - prediccion
            error_total += error**2
            
            pesos[0] += tasa_aprendizaje * xi[i][0] * error
            pesos[1] += tasa_aprendizaje * xi[i][1] * error
            bias += tasa_aprendizaje * error
        print("Época: ", ep + 1, " --> Error: ",error_total, end="%\n")

    return pesos, bias

def clasificar(entradas, pesos, bias):
    print(entradas, "=", activacion(pesos, entradas, bias))

def activacion(pesos, x, bias):
    z = pesos * x
    if z.sum() + bias > 0:
        return 1
    else:
        return 0
    
if __name__=="__main__":
    pesos = np.random.uniform(0, 1, size = 2)
    bias = np.random.uniform(0, 1)
    tasa_aprendizaje = 0.0001
    epocas = 100

    # Ruta absoluta a la carpeta donde está este script (training/)
    BASE_DIR = Path(__file__).parent
    # Sube un nivel y entra a data/
    DATA_PATH = BASE_DIR.parent / "data" / "Values.csv"
    
    # Importamos los datos y los convertimos en un DataFrame
    datos = pd.read_csv(DATA_PATH)
    matrix_data = np.array(datos)

    # Datos de entrada
    x_inicio = 0
    x_n = 1
    # Datos de entrada validacion
    xj_inicio = 3
    xj_n = 4
    # Datos de entrada validacion
    xk_inicio = 6
    xk_n = 7
    # Crear vector de entradas xi
    xi = (Datos_entrenamiento(matrix_data,x_inicio,x_n))
    d1 = matrix_data[:,x_n+1]
    # Crear vector de entradas xj
    xj = (Datos_validacion(matrix_data,xj_inicio,xj_n))
    d2 = matrix_data[:,xj_n+1]
    # Crear vector de entradas xk
    xk = (Datos_validacion(matrix_data,xk_inicio,xk_n))
    d3 = matrix_data[:,xk_n+1]
    

    print("Visualización de los datos de entrenamiento:")
    print(f"{d1}\n{d2}\n{d3}\n")
    
    pesos, bias = entrenamiento(pesos, bias, tasa_aprendizaje, epocas, xi, d1)
    print("Valores de entrenamiento del Perceptrón 1:\n")
    print("n[0] =", "((",pesos[0],"* distancia ) + (", pesos[1], "* distancia)) +", bias)
    
    print("\nTest del Perceptrón 1:")
    for _ in range(41):
        clasificar([_, _], pesos, bias)
    

    pesos2 = np.random.uniform(0, 1, size = 2)
    bias2 = np.random.uniform(0, 1)
    
    pesos2, bias2 = entrenamiento(pesos2, bias2, tasa_aprendizaje, epocas, xj, d2)
    print("\n\nValores de entrenamiento del Perceptrón 2:\n")
    print("n[1] =", "((",pesos2[0],"* distancia ) + (", pesos2[1], "* distancia)) +", bias2)
    
    print("\nTest del Perceptrón 2:")
    for _ in range(41):
        clasificar([_, _], pesos2, bias2)
        
    pesos3 = np.random.uniform(0, 1, size = 2)
    bias3 = np.random.uniform(0, 1)
    
    pesos3, bias3 = entrenamiento(pesos3, bias3, tasa_aprendizaje, epocas, xk, d3)
    print("\n\nValores de entrenamiento del Perceptrón 3:\n")
    print("n[2] =", "((",pesos3[0],"* distancia ) + (", pesos3[1], "* distancia)) +", bias3)
    
    print("\nTest del Perceptrón 3:")
    for _ in range(41):
        clasificar([_, _], pesos3, bias3)

    print("\nReducción de los datos en C para Arduino IDE:")
    print("float pesos[] = {" + f"{pesos[0] + pesos[1]:.6f}, {pesos2[0] + pesos2[1]:.6f}, {pesos3[0] + pesos3[1]:.6f}" + "};")
    print("float bias[] = {" + f"{bias:.6f}, {bias2:.6f}, {bias3:.6f}" + "};")
    
    