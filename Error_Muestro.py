import pandasql as pds
import pandas as pd
import numpy as np
import scipy.stats as scp
def error(db, Parcela, Vol, confianza = 0.95):
    db2 = db.rename(columns = {Parcela:'Parcela', Vol:'Volume'})
    query = '''
                SELECT Parcela, SUM(Volume) AS Volume, COUNT(*) AS N
                FROM db2
                GROUP BY Parcela
            '''
    db_error = pds.sqldf(query)
    t_value = scp.t.ppf(confianza, db_error['Volume'].count()-1)
    cv = (db_error['Volume'].std()/db_error['Volume'].mean())*100
    error = np.sqrt((t_value**2*cv**2)/db_error['Volume'].count())
    db_error2 = {'t_value':t_value, 'CV%':cv, 'Error%':error}
    db_er = pd.DataFrame(data=db_error2)
    print('El error es de: {:.2f} %'.format(error*100))
    return(db_er)