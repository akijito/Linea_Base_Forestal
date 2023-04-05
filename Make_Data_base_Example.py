import Data_base
import Horizontal_Structure as he
import Vertical_Structure as ve
# El path hace referencia a un archivo prueba 
path = "./Datos/Bosque_denso.csv"

ID_Parcela = 'Parcela'
ID_Arbol = 'ID'
Nombre_Comun = 'Nombre_común'
Nombre_Cientifico = 'Nombre_científico'
Familia = 'Familia'
CAP1 = 'CAP1'
CAP2 = 'CAP2_(cm)'
CAP3 = 'CAP3_(cm)'
CAP4 = 'CAP4_(cm)'
CAP5 = 'CAP5_(cm)'
DAP1 = None
HT = 'Ht1_(m)'
HC = 'Hc1_(m)'
Densidad = None
vol = None
ff = 0.65


db = Data_base.data_base(path, ID_Parcela, ID_Arbol, Nombre_Comun, Nombre_Cientifico, Familia, HT, HC, 
                         DAP1, CAP1, CAP2, CAP3, CAP4, CAP5)
volumen = Data_base.volume(db, ff, vol)

db_estructurah = he.estructurah(db,'Familia','Nombre_cientifico','Nombre_Comun', 'ID_Parcela', 'GA')
db_clase_diam = he.clase_diametrica(db,'DAP')
db_estructurav = ve.estructurav(db, 'HT', 'HC', 'Nombre_Cientifico')
with pd.ExcelWriter('Linea_Base.xlsx') as writer:
    volumen.to_excel(writer, sheet_name='Datos')
    db_estructurah.to_excel(writer, sheet_name='EstructuraH')
    db_clase_diam.to_excel(writer,sheet_name='Clases_Diam')
    db_estructurav.to_excel(writer, sheet_name='EstructuraV')

