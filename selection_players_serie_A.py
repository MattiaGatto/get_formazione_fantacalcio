#!pip install --upgrade pandas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import dump, load 
from pathlib import Path
from sklearn.metrics import mean_squared_error
import requests
from bs4 import BeautifulSoup
plt.style.use('fivethirtyeight')

import warnings
warnings.filterwarnings("ignore")


URL = "https://www.fantacalcio.it/probabili-formazioni-serie-a"
resp = requests.get(URL)
#print(resp.status_code)
# print(resp.content)

# creazione di un oggetto "soup"
data = BeautifulSoup(resp.content)
# print(data)

paragrafo = data.find('ul', attrs = {'class': 'match-list'})
# print(paragrafo)

def scramping(paragrafo,start_index,end_match):
  p1=paragrafo.split("\n")
  p_new=[]
  for x in p1 :
    if x.strip()!='' and x.strip()!="," :
      p_new.append(x.strip())

  start=p_new[p_new.index("-")+1:].index("-")+(p_new.index("-")+1)+1
  dati_p=p_new[0+start_index:start+start_index]

  info_=p_new[start+22+start_index:] # 22 giocatori in campo, da 9+29 in poi abbiamo informazioni sulla partita e sulle rose

  info_partita=info_[0]
  stadio=info_[1]
  s1=info_[2:info_.index(dati_p[2].strip())]
  nome_squadra=s1[0]
  modulo=s1[1]
  giocatori=[]
  percentuale_di_giocare=[]
  is_titolare=[]
  squadra={"Nome squadra":nome_squadra,"Giocatori":giocatori,"Percentuale di gioco del giocatore":percentuale_di_giocare,"Titolare":is_titolare,"Match":dati_p[1].strip()+" VS "+dati_p[2].strip(),"Stadio Partita":stadio,"Info Partita":info_partita,"Modulo Partita":modulo,"Giornata N":dati_p[0].strip()}
  gg=s1[2:]

  titolari=gg[:gg.index("Panchina")]
  panchina=gg[gg.index("Panchina")+1:]

  in_campo=True
  for g in range (0,len(titolari),2):
    
    squadra["Giocatori"].append(titolari[g])
    squadra["Percentuale di gioco del giocatore"].append(titolari[g+1].strip())
    squadra["Titolare"].append(in_campo)

  in_campo=False
  for g in range (0,len(panchina),2):
    
    squadra["Giocatori"].append(panchina[g])
    squadra["Percentuale di gioco del giocatore"].append(panchina[g+1].strip())
    squadra["Titolare"].append(in_campo)

  df1=pd.DataFrame(squadra)


  s2=info_[info_.index(dati_p[2].strip()):info_.index("Presentazione squadre")]
  nome_squadra=s2[0]
  modulo=s2[1]
  giocatori=[]
  percentuale_di_giocare=[]
  is_titolare=[]
  squadra={"Nome squadra":nome_squadra,"Giocatori":giocatori,"Percentuale di gioco del giocatore":percentuale_di_giocare,"Titolare":is_titolare,"Match":dati_p[1].strip()+" VS "+dati_p[2].strip(),"Stadio Partita":stadio,"Info Partita":info_partita,"Modulo Partita":modulo,"Giornata N":dati_p[0].strip()}
  gg=s2[2:]
  # print(gg)
  titolari=gg[:gg.index("Panchina")]
  panchina=gg[gg.index("Panchina")+1:]

  # print(titolari,panchina)
  in_campo=True
  for g in range (0,len(titolari),2):
    
    squadra["Giocatori"].append(titolari[g])
    squadra["Percentuale di gioco del giocatore"].append(titolari[g+1].strip())
    squadra["Titolare"].append(in_campo)

  in_campo=False
  for g in range (0,len(panchina),2):
    
    squadra["Giocatori"].append(panchina[g])
    squadra["Percentuale di gioco del giocatore"].append(panchina[g+1].strip())
    squadra["Titolare"].append(in_campo)

  df2=pd.DataFrame(squadra)

  df=df1.append(df2)


  index_squalificati=info_.index("Squalificati")
  index_infortunati=info_.index("Infortunati")
  index_in_dubbio=info_.index("In dubbio")

  lista_infortunati=[]
  for x in info_[index_infortunati+1:index_in_dubbio]:
    if x!="Nessun calciatore":
      lista_infortunati.append(x)
  lista_squalificati=[]
  for x in info_[index_squalificati+1:index_infortunati]:
    if x!="Nessun calciatore":
      lista_squalificati.append(x)
  lista_indubbio=[]
  if end_match==True:
    limit_lista_indubbio=info_[index_in_dubbio+1:]
  else:
    limit_lista_indubbio=info_[index_in_dubbio+1:info_.index('6')]
  for x in limit_lista_indubbio:
    if x!="Nessun calciatore":
      lista_indubbio.append(x)
  # print(lista_indubbio,lista_infortunati,lista_squalificati)
  lista_infortunati_=[]
  lista_squalificati_=[]
  lista_indubbio_=[]


  for g in df["Giocatori"]:
    trovato_s=False
    for l in range (0,len(lista_squalificati),2):
      if g.strip()==lista_squalificati[l].strip():
        trovato_s=True
        lista_squalificati_.append(True.strip())
        break
    if trovato_s==False:
      lista_squalificati_.append(False)
    else:
      trovato_s=False

  for g in df["Giocatori"]:
    trovato_i=False
    for l in range (0,len(lista_infortunati),2):
      if g.strip()==lista_infortunati[l].strip():
        trovato_i=True
        lista_infortunati_.append(str(lista_infortunati[l+1]).strip())
        break
    if trovato_i==False:
      lista_infortunati_.append(str("No"))
    else:
      trovato_i=False

  for g in df["Giocatori"]:
    trovato_d=False
    for l in range (0,len(lista_indubbio),2):
      if g.strip()==lista_indubbio[l].strip():
        trovato_d=True
        lista_indubbio_.append(str(lista_indubbio[l+1]).strip())
        break
    if trovato_d==False:
      lista_indubbio_.append(str("No"))
    else:
      trovato_d=False

  df["Squalificato"]=lista_squalificati_
  df["Infortunato"]=lista_infortunati_
  df["In dubbio"]=lista_indubbio_


  squalificati_infortunati_indubbio={"Nome squadra":'',"Giocatori":[],"Percentuale di gioco del giocatore":[],"Titolare":False,"Match":dati_p[1].strip()+" VS "+dati_p[2].strip(),"Stadio Partita":stadio,"Info Partita":info_partita,"Modulo Partita":modulo,"Giornata N":dati_p[0].strip(),
                "Squalificato":[], "Infortunato":[], "In dubbio":[]}

  for l in range (0,len(lista_squalificati),2):
    trovato_s=False
    for g in df["Giocatori"]:
      if g.strip()==lista_squalificati[l].strip():
        trovato_s=True
        break
    if trovato_s==False:
      squalificati_infortunati_indubbio['Giocatori'].append(lista_squalificati[l])
      squalificati_infortunati_indubbio['Percentuale di gioco del giocatore'].append(0)
      squalificati_infortunati_indubbio['Squalificato'].append(True)
      squalificati_infortunati_indubbio['Infortunato'].append("No")
      squalificati_infortunati_indubbio['In dubbio'].append("No")
  
  for l in range (0,len(lista_infortunati),2):
    trovato_i=False
    for g in df["Giocatori"]:
      if g.strip()==lista_infortunati[l].strip():
        trovato_i=True
        break
    if trovato_i==False:
      squalificati_infortunati_indubbio['Giocatori'].append(lista_infortunati[l])
      squalificati_infortunati_indubbio['Percentuale di gioco del giocatore'].append("0%")
      squalificati_infortunati_indubbio['Squalificato'].append("No")
      squalificati_infortunati_indubbio['Infortunato'].append(lista_infortunati[l+1])
      squalificati_infortunati_indubbio['In dubbio'].append("No")
    
  for l in range (0,len(lista_indubbio),2):
    trovato_d=False
    for g in df["Giocatori"]:
      if g.strip()==lista_indubbio[l].strip():
        trovato_d=True
        break
    if trovato_d==False:
      squalificati_infortunati_indubbio['Giocatori'].append(lista_indubbio[l])
      squalificati_infortunati_indubbio['Percentuale di gioco del giocatore'].append("0%")
      squalificati_infortunati_indubbio['Squalificato'].append("No")
      squalificati_infortunati_indubbio['Infortunato'].append("No")
      squalificati_infortunati_indubbio['In dubbio'].append(lista_indubbio[l+1])

  squalificati_infortunati_indubbio=pd.DataFrame(squalificati_infortunati_indubbio)
  df=df.append(squalificati_infortunati_indubbio)

  if end_match==True:
    indice=len(info_)+start+22+start_index
  else:
    indice=info_.index('6')+start+22+start_index
  
  return df,indice


p = paragrafo.text

match_1,end=scramping(p,0, False)
match_2,end2=scramping(p,end, False)
match_3,end3=scramping(p,end2, False)
match_4,end4=scramping(p,end3, False)
match_5,end5=scramping(p,end4, False)
match_6,end6=scramping(p,end5, False)
match_7,end7=scramping(p,end6, False)
match_8,end8=scramping(p,end7, False)
match_9,end9=scramping(p,end8, False)
match_10,end10=scramping(p,end9, True)
#print(len(match_1)+len(match_2)+len(match_3)+len(match_4)+len(match_5)+len(match_6)+len(match_7)+len(match_8)+len(match_9)+len(match_10))

df=match_1.append(match_2.append(match_3.append(match_4.append(match_5.append(match_6.append(match_7.append(match_8.append(match_9.append(match_10))))))))).rename_axis('Giocatore in rosa').reset_index()
#print(df)


Rosa_fantacalcio=[
    "Rui Patricio",
    "Szczesny",
    "Montipo'",
    "Milenkovic",
    "Di Lorenzo",
    "Danilo",
    "Kalulu",
    "Bremer",
    "Smalling",
    "Bastoni",
    "Bonucci",
    "Barella",
    "Luis Alberto",
    "Zaniolo",
    "Zielinski",
    "Kostic",
    "Tonali",
    "Miretti",
    "Pogba",
    "Vlahovic",
    "Dybala",
    "Giroud",
    "Jovic",
    "Pinamonti",
    "Caprari"
  ]
#len(Rosa_fantacalcio)

def rosa_df(df,Rosa_fantacalcio):
  res=df.loc[df['Giocatori'] == Rosa_fantacalcio[0]]
  for g in range (1,len(Rosa_fantacalcio)):
    res=res.append(df.loc[df['Giocatori'] == Rosa_fantacalcio[g]])
  res.reset_index(drop=True)
  res.index = np.arange(1, len(res) + 1)
  return res
rosa=rosa_df(df,Rosa_fantacalcio)
#print(len(rosa))
#rosa


URL = "https://www.fantacalcio.it/quotazioni-fantacalcio"
resp1 = requests.get(URL)
#print(resp1.status_code)
# print(resp1.content)

# creazione di un oggetto "soup"
data2 = BeautifulSoup(resp1.content)
paragrafo2 = data2.find('header', attrs = {'class': 'mb-3 d-flex align-items-center'})

link=str(paragrafo2).split("href=")[1]
link="https://www.fantacalcio.it"+link.split("\" ")[0][1:]
#print(link)
dati = pd.read_excel('C:/Users/matti/Desktop/doc/FANTACALCIO 2022-2023/Fanatacalcio_project/Quotazioni_Fantacalcio_Stagione_2022_23_ds.xlsx',header=1)

ind=[]
ruolo=[]
ruolo_fanta=[]
squadra=[]
fvm=[]
for r in rosa['Giocatori']:
  for g in dati['Nome']:
    if r==g:
      player=dati.loc[dati['Nome']==g]      
      ruolo.append(player['RM'].values[0])#.values[0])
      ruolo_fanta.append(player['R'].values[0])
      squadra.append(player['Squadra'].values[0])
      fvm.append(player['FVM'].values[0])
  
rosa["Ruolo"]=ruolo
rosa["Ruolo Fanta"]=ruolo_fanta
rosa["Nome squadra"]=squadra
rosa["FVM"]=fvm
#rosa

def plt_bar_roles(ruolo,titl,col):
  g=rosa.loc[rosa['Ruolo Fanta']==ruolo ]
  g=g.loc[rosa['Titolare']==True ]
  
  val=g['Percentuale di gioco del giocatore'].values
  for v in range (len(val)):
    val[v]=int (val[v][:len(val[v])-1])

  ris={'Giocatori':g['Giocatori'],'Percentuale di gioco':val}

  plt.figure(figsize=(8, 4), dpi=80)
  plt.plot(g['Giocatori'],val,color = col)
  # plt.pie(val,labels=g['Giocatori'])
  plt.title("Probabilità di gioco "+titl)
  plt.show()

plt_bar_roles('P','Portieri','y')
plt_bar_roles('D','Difensori','g')
plt_bar_roles('C','Centrocampisti','b')
plt_bar_roles('A','Attaccanti','r')

def aggiungi(ruolo,g,rosa,qnt):
  indexNames=[]
  for n in g['Giocatori'].values:
    i=rosa[rosa['Giocatori'] ==n].index
    indexNames.append(i[0])
  rosa=rosa.drop(index=indexNames)
  
  val=rosa['Percentuale di gioco del giocatore'].values
  fvm_top=rosa['FVM'].values

  for v in range (len(val)):
    val[v]=int (val[v][:len(val[v])-1])

  ris={'Giocatori':rosa['Giocatori'],'Ruolo':rosa['Ruolo Fanta'],'Percentuale di gioco':val,"FVM":fvm_top}
  r=pd.DataFrame(ris)
  r['Sort']=(r['FVM']+r['Percentuale di gioco'])/2
  r = r.sort_values(['Sort'], ascending=False)
  r=r.loc[r['Ruolo']==ruolo]
  g=g.append(r.head(qnt))
  return g


def controlla(formazione,rosa):
  if len(formazione.loc[formazione['Ruolo']=='A' ])<5:
    # print("A")
    formazione=aggiungi('A',formazione,rosa,5-len(formazione.loc[formazione['Ruolo']=='A' ]))
  if len(formazione.loc[formazione['Ruolo']=='C' ])<6:
    # print("C")
    formazione=aggiungi('C',formazione,rosa,6-len(formazione.loc[formazione['Ruolo']=='C' ]))
  if len(formazione.loc[formazione['Ruolo']=='D' ])<5:
    # print("D")
    formazione=aggiungi('D',formazione,rosa,5-len(formazione.loc[formazione['Ruolo']=='D' ]))
  if len(formazione.loc[formazione['Ruolo']=='P' ])<2:
    # print("P")
    formazione=aggiungi('P',formazione,rosa,2-len(formazione.loc[formazione['Ruolo']=='P' ]))
  # print(len(formazione.loc[formazione['Ruolo']=='C' ]))
  return formazione


# g=rosa
g=rosa.loc[rosa['Titolare']==True ]
val=g['Percentuale di gioco del giocatore'].values
fvm_top=g['FVM'].values

for v in range (len(val)):
  val[v]=int (val[v][:len(val[v])-1])

ris={'Giocatori':g['Giocatori'],'Ruolo':g['Ruolo Fanta'],'Percentuale di gioco':val,"FVM":fvm_top}

formazione=pd.DataFrame(ris)

formazione=controlla(formazione,rosa).reset_index(drop=True)
formazione['Sort']=(formazione['FVM']+formazione['Percentuale di gioco'])/2

# formazione = formazione.sort_values(['FVM','Percentuale di gioco'], ascending=False)
formazione = formazione.sort_values(['Sort'], ascending=False)
#formazione

def titolari_panchina(formazione,Ruolo,n_tit,n_panc):
  titolari_top=formazione.loc[formazione['Ruolo']==Ruolo ]
  titolari=titolari_top.head(n_tit)
  titolari_top=titolari_top.drop(index=titolari.index)
  panchina=titolari_top.head(n_panc)
  return titolari,panchina

attaccanti_titolari,attaccanti_panchinari= titolari_panchina(formazione,'A',3,2)
centrocampisti_titolari,centrocampisti_panchinari= titolari_panchina(formazione,'C',4,2)
difensori_titolari,difensori_panchinari= titolari_panchina(formazione,'D',3,2)
portieri_titolari,portieri_panchinari= titolari_panchina(formazione,'P',1,1)

formazione_titolare=portieri_titolari.append(difensori_titolari.append(centrocampisti_titolari.append(attaccanti_titolari))).reset_index(drop=True)
formazione_titolare.index = np.arange(1, len(formazione_titolare) + 1)
formazione_titolare['Giocatore in']='campo'
#formazione_titolare

formazione_panchina=portieri_panchinari.append(difensori_panchinari.append(centrocampisti_panchinari.append(attaccanti_panchinari))).reset_index(drop=True)
formazione_panchina.index = np.arange(1, len(formazione_panchina) + 1)
formazione_panchina['Giocatore in']='panchina'
#formazione_panchina

formazione_finale=formazione_titolare.append(formazione_panchina)
formazione_finale.index = np.arange(1, len(formazione_finale) + 1)
#formazione_finale

formazione_finale.to_excel("C:/Users/matti/Desktop/doc/FANTACALCIO 2022-2023/Fanatacalcio_project/formazione_finale_da schierare.xlsx")

fig, ax = plt.subplots()
fig.set_size_inches(10, 10)
# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
ax.table(cellText=formazione_finale.values, colLabels=formazione_finale.columns, loc='center')

fig.tight_layout()
plt.savefig('C:/Users/matti/Desktop/doc/FANTACALCIO 2022-2023/Fanatacalcio_project/formazione_finale_da schierare.png', dpi=300)
plt.show()
