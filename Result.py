import pandas as pd
import os
import re
import codecs, json



from tkinter import filedialog
from tkinter import *
import warnings


#ocultando future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()





def run():
    
    
    itens = os.listdir(folder_selected)
    itens = [x for x in itens if ".py" not in x]

    
    
    
    arquivos = []
    # =============================================================================
    # LENDO TODOS OS ARQUIVOS DA PASTA DATASET SPLIT BY PARÁGRAFO
    # =============================================================================
    for i in itens:
        
        f = open(folder_selected + '/' + str(i), "r")
        f = f.read().upper() #.split('\n')

	##############################
	# FAZENDO LIMPEZA DOS NOMES
	##############################
        f = re.split(r"[\n |* |!  |\( | \) |.   \ |, | \* |: |\/ |\- |\? |\; |\']",f)#|\( | \) |.   \ |, |\n | \*  
        arquivos.append(f)
        
        
        
        
    words = [item for sublist in arquivos for item in sublist]
    word_cont = pd.DataFrame(words, columns =['tmp'])
    word_cont['tmp'] = word_cont['tmp'].str.replace('"','')
    
    word_cont = word_cont[word_cont.tmp != '']
    word_cont = word_cont.tmp.value_counts().reset_index()
    word_cont.columns = ['WordId','tmp']
    
    
    
    
    
    for i in range(len(itens)):
    
        
        word_cont.loc[word_cont.loc[:, 'WordId'].isin(arquivos[i]), itens[i]] = True
        word_cont.loc[~word_cont.loc[:, 'WordId'].isin(arquivos[i]), itens[i]] = False
    
    
    from tqdm import trange
    
    
    print(
          '''
# =============================================================================
#           Criando indexador reverso  
# =============================================================================
          '''
          )
    
    
    
    lista = []
    for i in trange(word_cont.shape[0]):#
        lista.append(str(word_cont.iloc[i,2:][word_cont.iloc[i,2:].fillna(False)].index))
        
        
    
    word_cont['ReverseId'] = lista
    
    
    word_cont.loc[:, 'ReverseId'] = word_cont['ReverseId'].str.replace('''[Index | typ= | objc]''', '')
    
    word_cont.loc[:, 'ReverseId'] = word_cont['ReverseId'].str.replace('''[\[ | \] |\' | \n]''','')
    
    
        
    dictionary = word_cont.loc[:,['WordId']].to_dict()
    dictionary_id = word_cont.loc[:,['ReverseId']].to_dict()
    
    
    
    file_path = r"./WordId.json" ## your path variable
    json.dump(dictionary, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    
    
    
    file_path = r"./ReverseId.json" ## your path variable
    json.dump(dictionary_id, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    
    msg = ''' 
# =============================================================================
# ARQUIVOS GERADOS COM SUCESSO: ReverseId.json | WordId.json
# =============================================================================
    '''
    
    
    return dictionary, dictionary_id, print(msg)
    
run()