import Data_base

path = None
ID_Parcela = None
ID_Arbol = None
Nombre_Comun = None
Nombre_Cientifico = None
Familia = None
CAP1 = None
CAP2 = None
CAP3 = None
CAP4 = None
CAP5 = None
DAP1 = None
HT = None
HC = None
ff = None
vol = None
biomass = False
db = Data_base.data_base(path, ID_Parcela, ID_Arbol, Nombre_Comun, Nombre_Cientifico, Familia, HT, HC, 
                         DAP1, CAP1, CAP2, CAP3, CAP4, CAP5)

Data_base.volume(db, ff, vol, biomass)