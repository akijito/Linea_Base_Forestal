import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandasql as pds
def estructurav(db, HT, HC, Nombre_Cientifico):
    db.rename(columns = {HT:'HT', HC:'HC', Nombre_Cientifico:'Nombre_Cientifico'})
    def dist_alt(x):
        if x > 0 and x < 5:
            return('Arbustivo')
        if x > 5 and x < 12:
            return('Sub arboreo')
        if x > 12 and x < 25:
            return('Arboreo inferior')
        else:
            return('Arboreo Superior')
    db['Dist_Alt'] = db[HT].apply(dist_alt)
    query_altimetricas = '''
                            SELECT*, CASE WHEN Dist_Alt = 'Arbustivo' THEN 1
                                          WHEN Dist_Alt = 'Sub arboreo' THEN 2
                                          WHEN Dist_Alt = 'Arboreo inferior' THEN 3
                                          ELSE 4 END AS Clase
                            FROM(
                                 SELECT Dist_Alt, COUNT(*) Cantidad
                                 FROM db
                                 GROUP BY Dist_Alt
                                 ) T1
                            ORDER BY Clase
                         '''
    graf_altimetrica = pds.sqldf(query_altimetricas)
    if 'Arbustivo' not in graf_altimetrica['Dist_Alt']:
        graf_altimetrica.loc[-1] = ['Abustivo', 0, 1]
    if 'Sub arboreo'not in graf_altimetrica['Dis_Alt']:
        graf_altimetrica.loc[-1] = ['Sub arboreo', 0, 2]
    if 'Arboreo inferior' not in graf_altimetrica['Dist_Alt']:
        graf_altimetrica.loc[-1] = ['Arboreo inferior', 0, 3]
    if 'Arboreo superior' not in graf_altimetrica['Dist_Alt']:
        graf_altimetrica.loc[-1] = ['Arboreo superior', 0, 4]
    graf_altimetrica.sort_values(by='Clase')
    palette=sns.color_palette('Greys')
    plt.figure(figsize=[15,10])
    sns.barplot(data = graf_altimetrica, y='Cantidad', x='Dist_Alt', palette = palette[-4:-3])
    plt.xlabel('Clase altimétrica', font = 'Times new roman', size = 20)
    plt.ylabel('Cantidad', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Clase_altimetricas.jpg', dpi=500)
    plt.show()
    #Clases altimetricas
    filas = db[HT].count()
    rango = db[HT].max()-db[HT].min()
    sturges = np.log10(filas)*3.32+1
    sturges = round(sturges,0)
    amplitud = rango/sturges
    altura_min = []
    altura_max = []
    for i in range(int(sturges)):
        altura_max.append(round((db[HT].min()+count),2))
        count += amplitud
    count = 0
    for i in range(int(sturges)):
        altura_min.append(round((db[HT].min()+count),2))
        count += amplitud
    clases_altimetricas = {'Altura_Min':altura_min, 'Altura_Max':altura_max}
    indices = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI',
               'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII',
               'XXIX', 'XXX']
    db_clases_alt = pd.DataFrame(data=clases_altimetricas, index=indices[:int(sturges)])
    upper_class = []
    lower_class = []
    indices_tabla = []
    alturas = []
    for i in range(len(db[HT])):
        alturas.append(round(db[HT][i]))
    for i in range(len(db[HT])):
        for j in range(len(db_clases_alt['Altura_Min'])):
            if alturas[i] >= db_clases_alt['Altura_Min'][j] and alturas[i] < db_clases_alt['Altura_Max'][j]:
                upper_class.append(db_clases_alt['Altura_Max'][j])
                lower_class.append(db_clases_alt['Altura_Min'][j])
                indices_tabla.append(db_clases_alt['Altura_Min'].index[j])
                break
            else:
                if alturas[i] == db_clases_alt['Altura_Max'].max():
                    upper_class.append(db_clases_alt['Altura_Max'].max())
                    lower_class.append(db_clases_alt['Altura_Min'].max())
                    indices_tabla.append(db_clases_alt['Altura_Min'].index[-1])
                    break
    db['Class_Alt_Min'] = lower_class 
    db['Class_Alt_Max'] = upper_class
    db['Indice_Alt'] = indices_tabla
    query_clases_alt = '''
                         SELECT Indice_Alt, Class_Alt_Min, Class_Alt_Max, COUNT(*) AS Conteo
                         FROM db
                         GROUP BY Indice_Alt
                         ORDER BY Class_Alt_Min
                      '''
    graf_class_alt = pds.sqldf(query_clases_alt)
    plt.figure(figsize=[15,10])
    sns.barplot(data = graf_class_alt, y='Conteo', x='Indice_Alt', palette = palette[-4:-3])
    plt.xlabel('Clase altimétrica', font = 'Times new roman', size = 20)
    plt.ylabel('Cantidad', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Clases_altimetricas2.jpg', dpi=500)
    plt.show()    
    # ogawa
    plt.figure(figsize=[15,15])
    sns.regplot(data=db, x='HC', y='HT', x_jitter=0.04, 
                scatter_kws={'alpha':1/4, 'color':'Black'}, line_kws={'lw':2,'color':'Black'}, fit_reg = False)
    plt.xlabel('Altura comercial (m)', font = 'Times new roman', size = 20)
    plt.ylabel('Altura total', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Clases_altimetricas2.jpg', dpi=500)
    plt.show()
    def pos_sc(x):
        if x <= 7:
            return('Dominado')
        if x > 7 and x <=15:
            return('Codominante')
        else:
            return('Dominante')
    db['pos_sc'] = db[HT].apply(pos_sc)
    query_psc = '''
                   WITH
                   table1 AS(
                   SELECT Nombre_Cientifico, SUM(Dominado) AS Dominado, SUM(Codominante) AS Codominante,
                          SUM(Dominante) AS Dominante
                   FROM(
                        SELECT Nombre_Cientifico, pos_sc,
                               CASE WHEN pos_sc = 'Dominado' THEN 1
                                    ELSE 0 END AS Dominado
                               CASE WHEN pos_sc = 'Codominante' THEN 1
                                    ELSE 0 END AS Codominante
                               CASE WHEN pos_sc = 'Dominante' THEN 1
                                    ELSE 0 END AS Dominante
                        FROM db
                        ) T1
                   GROUP BY Nombre_Cientifico
                   ),
                   table2 AS(
                   SELECT *, (Dominado*(SELECT SUM(Dominado) FROM table1)+
                              Codominante*(SELECT SUM(Codominante) FROM table1)+
                              Dominante*(SELECT SUM(Dominante) FROM table1)) AS PS
                   FROM table1
                   )
                   SELECT *, (CAST(PS AS REAL)/CAST((SELECT SUM(PS) FROM table2) AS REAL))*100 AS PS2
                   FROM table2
                   ORDER BY PS2 DESC
                ''' 
    db_psc = pds.sqldf(query_psc)
    query_psc2 = '''
                    SELECT Nombre_Cientifico, SUM(PS2) AS PS
                    FROM(
                        SELECT CASE WHEN Rank <= 10 THEN Rank
                                    ELSE 11 END AS Categoria,
                            CASE WHEN Rank <= 10 THEN Nombre_Cientifico
                                    ELSE 'Otras especies' END AS Nombre_Cientifico, PS2
                        FROM(
                            SELECT *, ROW_NUMBER() OVER (ORDER BY PS2 DESC) AS Rank
                            FROM db_psc
                            ) t1
                        )
                    GROUP BY Nombre_Cientifico
                 '''
    graf_ps = pds.sqldf(query_psc2)
    plt.figure(figsize=[20,10])
    sns.barplot(data = graf_ps, y='Nombre_Cientifico', x='PS', palette = palette[-4:-3])
    plt.xlabel('Peso sociológico (%)', font = 'Times new roman', size = 20)
    plt.ylabel('Especies', font = 'Times new roman', size = 20)
    plt.yticks(font = 'Times new roman', size = 12, style = 'italic')
    plt.xticks(font = 'Times new roman', size = 12)
    plt.tight_layout()
    plt.savefig('Peso_sociologico.jpg', dpi=500)
    plt.show()
    return(db)
