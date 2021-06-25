from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

def Funcion_extrae_valores():
    """
    esta funcion extrae los resultados de cada jugador por ronda
    
    input: nombre de arqchivoo etiquetas de los jugadores ( nombre archivo )  y nombre de archivo  csv data
    output: tabla de comprobacion valores scarping,  valores data csv, comparacion
    """
    print("\nIngrese nombre del archivo de las etiquetas [SIN EXTENSION  .TXT]...\n")  
    txt_label = input()+".txt"
    
    print("\nIngrese nombre del archivo .csv [SIN EXTENSION  .CSV]...\n")  
    dataframe_csv_otree_data = pd.read_csv(input()+".csv") 


    P = []
    participante = []               #lista que almacenara id  participantes
    label = []            #lista que almacenara  label
    contribucion = []            #lista que almacenara  contribucion x ronda
    ganancia = []            #lista que almacenara ganancia + monto no enviado final de ronda

    
    

    f = open (str(txt_label),'r')
    etiquetas = f.read()
    print('\n',etiquetas)
    f.close()
    etiquetas_individuales = etiquetas.split(",")
    print(etiquetas_individuales)


    for i in range(len(etiquetas_individuales)) :        #itero a traves de ...
        participante.append(i+1)
        x = etiquetas_individuales[i]        #  x almacena valor de la etiqueta
        P.append(x)
        
          
        urlP = "https://otree-demo.herokuapp.com/p/" +str(x) + "/public_goods/Results/4"
                #https://otree-demo.herokuapp.com/p/0vs6y7q5/public_goods/Results/4
            
        #print(urlP)
        htmlP = requests.get(urlP).content           
        soupP = BeautifulSoup(htmlP,'lxml')            #  parser    lxml
        textoP = soupP.find_all('td')              # buscar tag "td" 
        Valores_txt_html = []
        
        # #
        for i in textoP:
            #L.append(i)   
            Valores_txt_html.append(i.text)                # extraer texto (numero esta en str)
            #print(i.text)
            
        print(urlP)        
        print(Valores_txt_html[1], " contribucion")
        print(Valores_txt_html[14], " ganancia colectiva") 
        print(Valores_txt_html[17], "resultado")

        label.append(x)  # x = valor string de etiqueta
        contribucion.append(int(Valores_txt_html[14].replace(" points", "")))
        ganancia.append(int(Valores_txt_html[17].replace(" points", "")))
        
    dataframe_sraping = pd.DataFrame(list(zip(label,contribucion,ganancia)),
                                     columns = ['label', 'contribucion', 'ganancia'])
    
    
        
    #    se  conviernten los valores a  INTERGER    
    dataframe_csv_otree_data = pd.DataFrame(list(zip(
                                                dataframe_csv_otree_data["participant.code"],
                                                pd.to_numeric(dataframe_csv_otree_data["public_goods.1.group.individual_share"], downcast='integer'),
                                                pd.to_numeric(dataframe_csv_otree_data["public_goods.1.player.payoff"], downcast='integer') )),
                                                columns = ['label', 'contribucion_scraping', 'ganancia_scraping'])
    
    
    #print(list(dataframe_csv_otree_data["public_goods.1.group.individual_share"]))
    #list(dataframe_csv_otree_data["public_goods.1.player.payoff"]) 
     
    
        
    x = dataframe_sraping
    y = dataframe_csv_otree_data
            
    w = list(x['contribucion'] - y['contribucion_scraping'] == 0)          #si la diferencia es cero -->  bool TRUE
    z = list(x['ganancia'] - y['ganancia_scraping'] == 0)                #si la diferencia es cero -->  bool TRUE
    
    dataframe_prueba = pd.DataFrame(list(zip(label,w,z)), columns = ['label','contribucion_OK','ganancia_OK'])
    
    t = pd.merge(x,y, on = 'label')     # unir dataframe por atributos
    

    return pd.merge(t,dataframe_prueba, on = 'label')        # salida la union del data frame de valores con el comparacion
    
    
    
    
    
    
