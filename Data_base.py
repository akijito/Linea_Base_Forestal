import numpy as np
import pandas as pd
import xlsxwriter


def data_base(path, ID_Parcela, ID_Arbol, Nombre_Comun, Nombre_Cientifico, 
              Familia, HT, HC, DAP = None, CAP1= None, CAP2= None, 
              CAP3= None, CAP4= None, CAP5= None, Densidad = None):
    db = pd.read_csv(path)
    ID_Parcela = db[ID_Parcela].astype('string')
    ID_Arbol = db[ID_Arbol].astype('string')
    def clean_names(name):
        names = name.strip()
        return(names[0].upper()+names[1:])
    Nombre_Comun = db[Nombre_Comun].apply(clean_names).astype('string')
    Nombre_Cientifico = db[Nombre_Cientifico].apply(clean_names).astype('string')
    Familia = db[Familia].astype('string')
    if DAP == None:
        db_dap = db[[CAP1, CAP2, CAP3, CAP4, CAP5]].fillna(0)
        def dap(x1, x2, x3, x4, x5):
            DAP = np.sqrt(x1**2+x2**2+x3**2+x4**2+x5**2)/np.pi
            return(DAP)
        DAP2 = dap(db_dap[CAP1], db_dap[CAP2], db_dap[CAP3], db_dap[CAP4], db_dap[CAP5])
    if not DAP == None:
        DAP2 = db[DAP].astype('float64')
    GA = (np.pi/40000)*(DAP2**2)
    HT = db[HT].astype('float64')
    # Volver opcional la altura comercial
    HC = db[HC].astype('float64')
    # Base de datos
    data_base = {'ID_Parcela': ID_Parcela, 'ID_Arbol':ID_Arbol, 'Nombre_Comun': Nombre_Comun,
                 'Nombre_Cientifico': Nombre_Cientifico, 'Familia': Familia, 'DAP': DAP2,
                 'GA': GA,'HT': HT, 'HC': HC}
    if Densidad != None:
        data_base['Densidad'] = db[Densidad]
    data_base = pd.DataFrame(data = data_base)
    return data_base
def volume(db, ff, vol):
    if vol == None:
        db['Vol_T'] = db['GA']*db['HT']*ff 
        db['Vol_C'] = db['GA']*db['HC']*ff
    if not vol == None:
        DAP = db['DAP']
        HT = db['HT']
        GA = db['GA']
        db['Vol'] = vol
    return(db)
def biomass(db, Choco= False, Bosque= 'bh-M', Modelo= 3):
    if Choco:
        if Bosque == 'Colina':
            if Modelo == 1:
                db['BA'] = np.exp(-2.71532)+np.exp(2.0071)*db['DAP']+np.exp(0.78445)*db['HT']+np.exp(0.3594)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-1.74094)+np.exp(2.3774)*(db['DAP']**2)*db['HT']*db['Densidad']
            if Modelo == 3:
                db['BA'] = np.exp(-3.22921)+np.exp(1.0056)*(db['DAP']**2)*db['HC']
            if Modelo == 4:
                db['BA'] = np.exp(-2.25974)+np.exp(2.2617)*db['DAP']+np.exp(0.3353)*db['HC']
        if Bosque == 'Guandal':
            if Modelo == 1:
                db['BA'] = np.exp(-2.28327)+np.exp(1.8261)*db['DAP']+np.exp(0.78445)*db['HT']+np.exp(0.3594)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-1.27086)+np.exp(2.1339)*(db['DAP']**2)*db['HT']*db['Densidad']
            if Modelo == 3:
                db['BA'] = np.exp(-2.42490)+np.exp(0.8919)*(db['DAP']**2)*db['HC']
            if Modelo == 4:
                db['BA'] = np.exp(-1.78705)+np.exp(2.0237)*db['DAP']+np.exp(0.3353)*db['HC']
        if Bosque == 'Mangle':
            if Modelo == 1:
                db['BA'] = np.exp(-3.09096)+np.exp(2.1558)*db['DAP']+np.exp(0.78445)*db['HT']+np.exp(0.3594)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-3.49060)+np.exp(2.5442)*(db['DAP']**2)*db['HT']*db['Densidad']
            if Modelo == 3:
                db['BA'] = np.exp(-3.39375)+np.exp(1.0627)*(db['DAP']**2)*db['HC']
            if Modelo == 4:
                db['BA'] = np.exp(-2.58130)+np.exp(2.0990)*db['DAP']+np.exp(0.3353)*db['HC']
    if not Choco:
        if Bosque == 'bh-M':
            if Modelo == 1:
                db['BA'] = np.exp(3.4415)+np.exp(-1.809)*db['DAP']+np.exp(1.237)*np.exp(np.log(db['DAP'])**2)+np.exp(-0.126)*np.exp(np.log(db['DAP'])**3)+np.exp(1.744)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-2.6164)+np.exp(2.37)*db['DAP']
            if  Modelo == 3:
                db['BA'] = np.exp(-2.450)+np.exp(0.932)*db['DAP']**2*db['HT']*db['Densidad']
        if Bosque == 'bh-MB':
            if Modelo == 1:
                db['BA'] = np.exp(2.2256)+np.exp(-1.552)*db['DAP']+np.exp(1.237)*np.exp(np.log(db['DAP'])**2)+np.exp(-0.126)*np.exp(np.log(db['DAP'])**3)+np.exp(-0.237)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-1.6630)+np.exp(2.37)*db['DAP']
            if  Modelo == 3:
                db['BA'] = np.exp(-1.993)+np.exp(0.932)*db['DAP']**2*db['HT']*db['Densidad']
        if Bosque == 'bh-PM':
            if Modelo == 1:
                db['BA'] = np.exp(2.4210)+np.exp(-1.415)*db['DAP']+np.exp(1.237)*np.exp(np.log(db['DAP'])**2)+np.exp(-0.126)*np.exp(np.log(db['DAP'])**3)+np.exp(1.068)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-1.86601)+np.exp(2.37)*db['DAP']
            if  Modelo == 3:
                db['BA'] = np.exp(-2.289)+np.exp(0.932)*db['DAP']**2*db['HT']*db['Densidad']
        if Bosque == 'bh-T':
            if Modelo == 1:
                db['BA'] = np.exp(2.8287)+np.exp(-1.596)*db['DAP']+np.exp(1.237)*np.exp(np.log(db['DAP'])**2)+np.exp(-0.126)*np.exp(np.log(db['DAP'])**3)+np.exp(0.441)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-1.5442)+np.exp(2.37)*db['DAP']
            if  Modelo == 3:
                db['BA'] = np.exp(-2.218)+np.exp(0.932)*db['DAP']**2*db['HT']*db['Densidad']
        if Bosque == 'bp-T':
            if Modelo == 1:
                db['BA'] = np.exp(1.5956)+np.exp(-1.225)*db['DAP']+np.exp(1.237)*np.exp(np.log(db['DAP'])**2)+np.exp(-0.126)*np.exp(np.log(db['DAP'])**3)+np.exp(0.691)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-1.9084)+np.exp(2.37)*db['DAP']
            if  Modelo == 3:
                db['BA'] = np.exp(-2.413)+np.exp(0.932)*db['DAP']**2*db['HT']*db['Densidad']
        if Bosque == 'bs-T':
            if Modelo == 1:
                db['BA'] = np.exp(4.0396)+np.exp(-1.991)*db['DAP']+np.exp(1.237)*np.exp(np.log(db['DAP'])**2)+np.exp(-0.126)*np.exp(np.log(db['DAP'])**3)+np.exp(1.283)*db['Densidad']
            if Modelo == 2:
                db['BA'] = np.exp(-2.2353)+np.exp(2.37)*db['DAP']
            if  Modelo == 3:
                db['BA'] = np.exp(-2.290)+np.exp(0.932)*db['DAP']**2*db['HT']*db['Densidad']
    return None
