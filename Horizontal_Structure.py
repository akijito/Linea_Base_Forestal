import pandasql as pds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def estructurah(db, Familia, Nombre_Cientifico, Nombre_Comun, Parcela, GA):
    db2 = db.rename(columns={Familia: 'Familia', Nombre_Cientifico: 'Nombre_Cientifico', Nombre_Comun: 'Nombre_Comun',
                             Parcela: 'Parcela', GA: 'GA'})
    query_especies = '''
                        SELECT Familia, Nombre_Cientifico, Nombre_Comun, COUNT(*) AS Cantidad
                        FROM db2
                        GROUP BY Nombre_Cientifico
                     '''
    db_especies = pds.sqldf(query_especies)
    query_familias = '''
                        SELECT Familia, COUNT(*) N_Especies, SUM(Cantidad) N_individuos
                        FROM db_especies
                        GROUP BY Familia
                        ORDER BY N_Especies DESC
                     '''
    db_familia = pds.sqldf(query_familias)
    query_grafica1 = '''
                        SELECT CASE WHEN Clase <= 10 THEN Familia
                                    ELSE 'Otras Familias' END AS Familia, N_Especies, Clase
                        FROM(
                            SELECT Familia, SUM(N_Especies) N_Especies, Clase
                            FROM(
                                SELECT *, CASE WHEN Rank <= 10 THEN Rank
                                            ELSE 11 END AS Clase
                                FROM(
                                    SELECT *, ROW_NUMBER() OVER (ORDER BY N_Especies DESC) AS Rank
                                    FROM db_familia
                                    ) T1
                                ) T2
                            GROUP BY Clase
                            ) T3
                        ORDER BY Clase
                    '''
    db_grafica1 = pds.sqldf(query_grafica1)
    palette=sns.color_palette('Greys')
    plt.figure(figsize=[20,10])
    sns.barplot(data = db_grafica1, y='Familia', x='N_Especies', palette = palette[-4:-3])
    plt.xlabel('Número de especies', font = 'Times new roman', size = 20)
    plt.ylabel('Familia', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Numero_Especies.jpg', dpi=500)
    plt.show()
    query_grafica2 = '''
                        SELECT CASE WHEN Clase <= 10 THEN Familia
                                    ELSE 'Otras Familias' END AS Familia, N_individuos, Clase
                        FROM(
                            SELECT Familia, SUM(N_individuos) AS N_individuos, Clase 
                            FROM(
                                SELECT *, CASE WHEN Rank <= 10 THEN Rank
                                            ELSE 11 END AS Clase
                                FROM(
                                    SELECT *, ROW_NUMBER() OVER (ORDER BY N_individuos DESC) AS Rank
                                    FROM db_familia
                                    ) T1
                                ) T2
                            GROUP BY Clase
                            ) T3
                        ORDER BY Clase
                     '''
    db_grafica2 = pds.sqldf(query_grafica2)
    plt.figure(figsize=[20,10])
    sns.barplot(data = db_grafica2, y='Familia', x='N_individuos', palette = palette[-4:-3])
    plt.xlabel('Número de individuos', font = 'Times new roman', size = 20)
    plt.ylabel('Familia', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Numero_individuos.jpg', dpi=500)
    plt.show()
    # Abundancia
    query_ab = '''
                  SELECT Familia, Nombre_Comun, Nombre_Cientifico, Cantidad2/Sumatoria AS Ab_abs,
                         (Cantidad2/Sumatoria)*100 AS Ab_rl
                  FROM(
                        SELECT*, CAST((SELECT SUM(Cantidad) FROM db_especies) AS REAL) AS Sumatoria, 
                                CAST(Cantidad AS REAL) AS Cantidad2
                        FROM db_especies
                       ) T1
               '''
    db_abun = pds.sqldf(query_ab)
    #Frecuencia
    query_fr1 = '''
                    SELECT Familia, Nombre_Comun, Nombre_Cientifico, SUM(Fr) AS Fr_Abs,
                           (SELECT COUNT(*) Parcelas FROM(SELECT Parcela FROM db2 GROUP BY Parcela)T2) AS Parcelas
                    FROM(
                        SELECT Parcela, Familia, Nombre_Comun, Nombre_Cientifico, COUNT(*)/COUNT(*) AS Fr
                        FROM db2
                        GROUP BY Parcela, Nombre_Cientifico
                        ) T1
                    GROUP BY Nombre_Cientifico
                    ORDER BY Fr_Abs DESC
                '''
    db_fr1 = pds.sqldf(query_fr1)
    query_fr2 = '''
                    SELECT Familia, Nombre_Cientifico, Nombre_Comun, Fr_Abs, (Fr_Abs/CAST(Fr AS REAL))*100 AS Fr_Rl,
                           CASE WHEN Fr_Abs <= (Parcelas/5)*1 THEN 'Muy poco frecuente'
                                WHEN Fr_Abs <= (Parcelas/5)*2 THEN 'Poco frecuente'
                                WHEN Fr_Abs <= (Parcelas/5)*3 THEN 'Frecuente'
                                WHEN Fr_Abs <= (Parcelas/5)*4 THEN 'Bastante frecuente'
                                ELSE 'Muy frecuente' END AS Frecuencia, Parcelas     
                    FROM(
                        SELECT *, (SELECT SUM(Fr_Abs) FROM db_fr1) AS Fr
                        FROM db_fr1
                        ) T1
                '''
    db_fr2 = pds.sqldf(query_fr2)
    # Dominancia
    query_dom = '''
                   SELECT Nombre_Cientifico, Dom_Abs, (Dom_Abs/(SELECT SUM(GA) FROM db2))*100 AS Dom_Rl, NI
                   FROM(
                        SELECT Familia, Nombre_Cientifico, Nombre_Comun, SUM(GA) AS Dom_Abs, COUNT(*) AS NI
                        FROM db2
                        GROUP BY Nombre_Cientifico
                        ) T1
                '''
    db_dom = pds.sqldf(query_dom)
    # Estructura horizontal
    query_EH = '''
                  SELECT a.Familia, a.Nombre_Comun, a.Nombre_Cientifico, c.NI, b.Parcelas, a.Ab_abs Abundancia_Abs, 
                         a.Ab_rl Abundancia_Rel, b.Fr_Abs Frecuencia_Abs, b.Fr_Rl Frecuencia_Rel, b.Frecuencia C_Frecuencia,
                         c.Dom_Abs Dominancia_Abs, c.Dom_Rl Dominancia_Rel
                  FROM db_abun AS a
                  JOIN db_fr2 AS b
                  ON a.Nombre_Cientifico = b.Nombre_Cientifico
                  JOIN db_dom AS c
                  ON a.Nombre_Cientifico = c.Nombre_Cientifico
               '''
    db_estructurah = pds.sqldf(query_EH)
    db_estructurah['IVI'] = db_estructurah['Abundancia_Rel']+db_estructurah['Frecuencia_Rel']+db_estructurah['Dominancia_Rel']
    db_estructurah['CV'] = (db_estructurah['Abundancia_Rel']+db_estructurah['Dominancia_Rel'])/2
    db_estructurah = db_estructurah.sort_values(by=['IVI'], ascending=False)
    # Gráficas
    query_graf_abun = '''
                         SELECT CASE WHEN Rank <= 10 THEN Nombre_Cientifico
                                     ELSE 'Otras Especies' END AS Nom_Cientifico,
                                CASE WHEN Rank <= 10 THEN Rank
                                     ELSE 11 END AS Class, SUM(Abundancia_Rel) AS Abundancia_Rel
                         FROM(
                              SELECT *, ROW_NUMBER() OVER (ORDER BY Abundancia_Rel DESC) AS Rank
                              FROM db_estructurah
                              ) T1
                         GROUP BY Class
                         ORDER BY Class
                      '''
    graf_abundancia = pds.sqldf(query_graf_abun)
    plt.figure(figsize=[20,10])
    sns.barplot(data = graf_abundancia, y='Nom_Cientifico', x='Abundancia_Rel', palette = palette[-4:-3])
    plt.xlabel('Abundancia Relativa (%)', font = 'Times new roman', size = 20)
    plt.ylabel('Especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Abundancia_Rel.jpg', dpi=500)
    plt.show()
    query_graf_frec = '''
                         SELECT CASE WHEN Rank <= 10 THEN Nombre_Cientifico
                                     ELSE 'Otras Especies' END AS Nom_Cientifico,
                                CASE WHEN Rank <= 10 THEN Rank
                                     ELSE 11 END AS Class, SUM(Frecuencia_Rel) AS Frecuencia_Rel
                         FROM(
                              SELECT *, ROW_NUMBER() OVER (ORDER BY Frecuencia_Rel DESC) AS Rank
                              FROM db_estructurah
                              )
                         GROUP BY Class
                         ORDER BY Class
                      '''
    graf_frecuencia = pds.sqldf(query_graf_frec)
    plt.figure(figsize=[20,10])
    sns.barplot(data = graf_frecuencia, y='Nom_Cientifico', x='Frecuencia_Rel', palette = palette[-4:-3])
    plt.xlabel('Frecuencia Relativa (%)', font = 'Times new roman', size = 20)
    plt.ylabel('Especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Frecuencia_Rel.jpg', dpi=500)
    plt.show()
    # Gráfica categorias
    query_categorias = '''
                          SELECT *, 
                                 CASE WHEN C_Frecuencia = 'Muy poco frecuente' THEN 1
                                      WHEN C_Frecuencia = 'Poco frecuente' THEN 2
                                      WHEN C_Frecuencia = 'Frecuente' THEN 3
                                      WHEN C_Frecuencia = 'Bastante frecuente' THEN 4
                                      ELSE 5 END AS Categoria
                          FROM(
                               SELECT C_Frecuencia, COUNT(*) AS Conteo
                               FROM db_estructurah
                               GROUP BY C_Frecuencia
                               ) T1
                          ORDER BY Categoria
                       '''
    graf_categoria = pds.sqldf(query_categorias)
    plt.figure(figsize=[15,10])
    sns.barplot(data = graf_categoria, y='Conteo', x='C_Frecuencia', palette = palette[-4:-3])
    plt.xlabel('Nivel de frecuencia', font = 'Times new roman', size = 20)
    plt.ylabel('Número de especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Frecuencia_Categorias.jpg', dpi=500)
    plt.show()
    # IVI
    query_IVI = '''
                   SELECT CASE WHEN Class <= 10 THEN Nombre_Cientifico
                               ELSE 'Otras especies' END AS Nom_Cientifico, SUM(IVI) AS IVI, Class
                   FROM(
                        SELECT Nombre_Cientifico, IVI, CASE WHEN Rank <= 10 THEN Rank
                                                        ELSE 11 END AS Class
                        FROM(
                            SELECT *, ROW_NUMBER() OVER (ORDER BY IVI DESC) AS Rank
                            FROM db_estructurah
                            ) T1
                        ) T2
                   GROUP BY Class
                '''
    graf_IVI = pds.sqldf(query_IVI)
    plt.figure(figsize=[20,10])
    sns.barplot(data = graf_IVI, y='Nom_Cientifico', x='IVI', palette = palette[-4:-3])
    plt.xlabel('Índice de valor de importancia', font = 'Times new roman', size = 20)
    plt.ylabel('Especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('IVI.jpg', dpi=500)
    plt.show()
    # CV
    query_CV = '''
                   SELECT CASE WHEN Class <= 10 THEN Nombre_Cientifico
                               ELSE 'Otras especies' END AS Nom_Cientifico, SUM(CV) AS CV, Class
                   FROM(
                        SELECT Nombre_Cientifico, CV, CASE WHEN Rank <= 10 THEN Rank
                                                        ELSE 11 END AS Class
                        FROM(
                            SELECT *, ROW_NUMBER() OVER (ORDER BY CV DESC) AS Rank
                            FROM db_estructurah
                            ) T1
                        ) T2
                   GROUP BY Class
                '''
    graf_CV = pds.sqldf(query_CV)
    plt.figure(figsize=[20,10])
    sns.barplot(data = graf_CV, y='Nom_Cientifico', x='CV', palette = palette[-4:-3])
    plt.xlabel('Valor de Cobertura', font = 'Times new roman', size = 20)
    plt.ylabel('Especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('CV.jpg', dpi=500)
    plt.show()
    # Agregación
    query_agregacion = '''
                          SELECT Nombre_Comun, Nombre_Cientifico, NI, 
                                 (CAST(Frecuencia_Abs AS REAL)/Parcelas)*100 AS FA,
                                 NI/Parcelas AS DO
                          FROM db_estructurah
                       '''
    db_agregacion = pds.sqldf(query_agregacion)
    db_agregacion['DE'] = -np.log((1-(db_agregacion['FA']/100.000001)))
    db_agregacion['GA'] = db_agregacion['DO'].astype('float64')/db_agregacion['DE']
    def agrega(x):
        if x < 1:
            return('Dispersa')
        if x >= 1 and x < 2:
            return('Tendencia al agrupamiento')
        else:
            return('Agrupada')
    db_agregacion['Agregacion'] = db_agregacion['GA'].apply(agrega)
    query_agregacion2 = '''
                         SELECT *, CASE WHEN Agregacion = 'Dispersa' THEN 1
                                        WHEN Agregacion = 'Tendencia al agrupamiento' THEN 2
                                        ELSE 3 END AS Rank
                         FROM(
                              SELECT Agregacion, COUNT(*) AS Conteo
                              FROM db_agregacion
                              GROUP BY Agregacion
                              ) t1
                         ORDER BY Rank
                      '''
    graf_agregacion = pds.sqldf(query_agregacion2)
    plt.figure(figsize=[15,10])
    sns.barplot(data = graf_agregacion, y='Conteo', x='Aregacion', palette = palette[-4:-3])
    plt.xlabel('Nivel de agregacion', font = 'Times new roman', size = 20)
    plt.ylabel('Cantidad de especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Agregacion.jpg', dpi=500)
    plt.show()
    return (db_estructurah)

def clase_diametrica(db, DAP):
    db2 = db
    filas = db2[DAP].count()
    rango = db2[DAP].max()-db2[DAP].min()
    sturges = np.log10(filas)*3.32+1
    sturges = round(sturges,0)
    amplitud = rango/sturges
    diametro_min = []
    diametro_max = []
    count = amplitud
    for i in range(int(sturges)):
        diametro_max.append(round((db2[DAP].min()+count),2))
        count += amplitud
    count=0
    for i in range(int(sturges)):
        diametro_min.append(round((db2[DAP].min()+count),2))
        count += amplitud
    clases_diametricas = {'Diametro_Min':diametro_min, 'Diametro_Max':diametro_max}
    indices = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI',
               'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII',
               'XXIX', 'XXX']
    db_diametro = pd.DataFrame(data=clases_diametricas, index=indices[:int(sturges)])
    upper_class = []
    lower_class = []
    indices_tabla = []
    Diametro = []
    for i in range(len(db2[DAP])):
        Diametro.append(round(db2[DAP][i],2))
    for i in range(len(Diametro)):
        for j in range(len(db_diametro['Diametro_Min'])):
            if Diametro[i] >= db_diametro['Diametro_Min'][j] and Diametro[i] < db_diametro['Diametro_Max'][j]:
                upper_class.append(db_diametro['Diametro_Max'][j])
                lower_class.append(db_diametro['Diametro_Min'][j])
                indices_tabla.append(db_diametro['Diametro_Min'].index[j])
                break
            else:
                if Diametro[i] == db_diametro['Diametro_Max'].max():
                    upper_class.append(db_diametro['Diametro_Max'].max())
                    lower_class.append(db_diametro['Diametro_Min'].max())
                    indices_tabla.append(db_diametro['Diametro_Min'].index[-1])
                    break
    db2['Indice_DAP'] = indices_tabla
    db2['Class_DAP_Min'] = lower_class
    db2['Class_DAP_Max'] = upper_class
    #Clases diametricas
    query_clases_DAP = '''
                          SELECT Indice_dAP, Class_DAP_Min, Class_DAP_Max, COUNT(*) AS Conteo
                          FROM db
                          GROUP BY Indice_DAP
                          ORDER BY Class_DAP_Min
                       '''
    graf_class_diam = pds.sqldf(query_clases_DAP)
    palette=sns.color_palette('Greys')
    plt.figure(figsize=[15,10])
    sns.barplot(data = graf_class_diam, y='Conteo', x='Indice_DAP', palette = palette[-4:-3])
    plt.xlabel('Clase diamétrica', font = 'Times new roman', size = 20)
    plt.ylabel('Cantidad', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Clases_diametricas.jpg', dpi=500)
    plt.show()
    return(db2)

    






