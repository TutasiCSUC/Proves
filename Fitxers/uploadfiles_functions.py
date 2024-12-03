#CREAT PER CSUC, si teniu dubtes contactar amb rdr-contacte@csuc.cat. Aquest arxiu no s'ha d'executar, només són funcions. Els scripts els trobareu a https://confluence.csuc.cat/display/RDM/Scripts
def pujar_arxius(base_url,token,doi,excel_path):
    from pyDataverse.api import NativeApi, DataAccessApi
    from pyDataverse.models import Dataverse
    from pyDataverse.models import Datafile
    from pathlib import Path
    import pandas as pd
    api = NativeApi(base_url,token)#funció per accedir a l'API
    data_api = DataAccessApi(base_url,token) #funció per accedir a dades mitjançant l'API
    try:
        arxius = pd.read_excel(excel_path).to_numpy().tolist()
        verificador=True
        for i in range(len(arxius)):
            file_name = arxius[i][0]
            path = Path(file_name)
            if path.is_file()==False:
                print('NO s\'ha trobat el fitxer: '+file_name)
                verificador=False
        if verificador==True:
            try:
                dataset = api.get_dataset(doi)
                for i in range(len(arxius)):
                    df = Datafile()
                    df.set({'pid': doi})
                    file_name = arxius[i][0]
                    df.set({'filename': file_name})
                    if type(arxius[i][1])!= float:
                        file_description = arxius[i][1]
                        df.set({'description': file_description})
                    if type(arxius[i][2])!= float:
                        file_path = arxius[i][2]
                        df.set({'directoryLabel': file_path})
                    if type(arxius[i][3])!= float:
                        file_categories = arxius[i][3].split(",")
                        df.set({'categories': file_categories})
                    df.get()
                    resp = api.upload_datafile(doi, file_name, df.json())
                    print('S\'ha penjat el fitxer: '+file_name)
            except:
                print('El token no és correcte o no s\'ha trobat el DOI: '+doi)
        else:
            print('No s\'ha penjat cap fitxer, modifiqueu els noms dels fitxers que estan malament.')
    except FileNotFoundError:
        print('No s\'ha trobat el fitxer de metadades amb el nom: '+excel_path)