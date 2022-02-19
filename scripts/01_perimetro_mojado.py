# Obtener valores de perímetro mojado a partir de datos de secciones en un archivo .csv

import os
#os.chdir(r'E:\Desktop\prueba_nicolas')
print(os.getcwd())

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Perimetro_mojado.csv', na_values='NAN', usecols=(0,3,4,6))

# Nombres de secciones
nombres_secciones = df.iloc[:,0].unique()
print(f'nombres_secciones:\n {nombres_secciones}')

# Cantidad de secciones
cantidad_secciones = len(nombres_secciones)
print(f'cantidad_secciones: {cantidad_secciones}')

# Agrupar por secciones
s_agrupadas = df.groupby('prof_label')

# Crear una carpeta: 'imagenes'
os.mkdir('imagenes')

lista_perimetros = []

for i in nombres_secciones:

  # Secciones
  seccion = i
  s = s_agrupadas.get_group(seccion) # Seccion agrupada (con NaN)
  s_copy = s.copy().dropna() # Seccion agrupada (sin NaN)

  # Estimar perímetro mojado
  eje_x = s_copy.iloc[:,1].tolist() # Columna 'cds2d'
  eje_y = s_copy.iloc[:,2].tolist() # Columna 'Topografia (msnm)'

  distancias = []

  for j in range(len(eje_x)-1):
    distancia = ( (eje_x[j+1] - eje_x[j])**2 + (eje_y[j+1] - eje_y[j])**2 )**0.5
    distancias.append(distancia)

  import numpy as np
  sumatoria = np.array(distancias).sum()
  #print(f'{seccion} - Perímetro mojado: {sumatoria} m')

  # Plotear secciones (matplotlib)
  plt.figure(figsize=(7,4))
  plt.title(f'Sección {seccion}'), plt.ylabel('Eje Y'), plt.xlabel('Eje X')
  plt.plot(s.iloc[:,1], s.iloc[:,3], 'd-') # Topografía
  plt.plot(s.iloc[:,1], s.iloc[:,2], 'd-') # Nivel del agua
  plt.tight_layout()

  plt.savefig(f'imagenes/Sección-{seccion}.jpg') # Guardar la seccion en imagen
  
  plt.close() # No mostrar la imagen
  
  lista_perimetros.append([i, sumatoria])

#print(lista_perimetros)

# Armar el dataframe
titulos = ['Seccion', 'Perimetro mojado']
df_final = pd.DataFrame(lista_perimetros, columns=titulos)

# Exportar dataframe
df_final.to_csv('df_final.csv')

print('Script terminado')