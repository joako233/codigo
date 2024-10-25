import requests
from bs4 import BeautifulSoup
from datetime import datetime,timezone,timedelta
import json
import praw
from datetime import date,timedelta,datetime
from seleniumbase import SB
import concurrent.futures

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
}


def allthat():
    with SB(uc=True,headless2=True) as sb:
        sb.maximize_window()
        # Este es el numero que se asignara a las paginas que iremos visitando
        n_pagina = 1
        # Tengo que poner uc with reconnect porque tiene mucha seguridad y sino el contenido html de la página no carga
        # Donde almaceno todos los diccionarios para ser exportados
        todo = []
        while True:
            sb.uc_open_with_reconnect(f'https://allthatsinteresting.com/category/weird-news/page/{n_pagina}',12)
  
            # Itero por los distintos hrefs 
            hrefs = sb.find_elements("//a[contains(@href,'allthatsinteresting.com') and @role='link' and contains(@class,'css-175oi2r')]")
            # saco cada atributo href y lo meto en la lista de links
            links = []
            for href in hrefs:
            
                href = href.get_attribute('href')
                links.append(href)

            # Este contador lo establezco para salir cuando encuentre 5 o mas publicaciones fuera de los ultimos 2 días
            contador = 0
            for link in links:

                sb.uc_open_with_reconnect(link,15)


                try:
                    titulo = sb.get_text("//h1[@class='post-title']")
                    fecha = sb.get_text("//div[@class='date']").split("Published")[1].strip()
                except:
                    print("ERROR")
                    input()

                # Convierto las fechas a UTC
                hoy = datetime.now(timezone.utc).replace(hour=0,second=0,microsecond=0)
                convertida = datetime.strptime(fecha,'%B %d, %Y').astimezone(timezone.utc).replace(hour=0,second=0,microsecond=0)
                operacion = hoy -timedelta(hours=24)

                if convertida >= operacion:
                
            
                    parrafos = sb.find_elements("//article[@class='post-content']/p",limit=4)
                    contenido = ""
                    for p in parrafos:

                        contenido = (contenido + " " + p.text).strip()
                    
                    diccionario ={'Title':titulo,
                                    'Url': link,
                                    'Content': contenido}
                    
                    todo.append(diccionario)
                else:
                    contador = contador + 1
                
            if contador >= 5:
                break
            else:
                n_pagina = n_pagina + 1
    return todo


def thepoke(headers):
    with requests.Session() as session:
        session.headers.update(headers)
        # Pongo este contador para salir si hay 7 o mas publicaciones pasadas de fecha
        contador_salir = 0
        # Donde almaceno todos los datos
        datos_completos = []
        # Donde almaceno los links visitados para evitar repeticiones
        visitados = []
        numero_pag = 1
        while True:
            response = session.get(f'https://www.thepoke.com/page/{numero_pag}/')
   
        
            soup = BeautifulSoup(response.text,'lxml')
            # Porque la estructura cambia en las demás paginas
            if numero_pag == 1:
                links = soup.find('div',attrs={'id':'maincontent'}).find_all('a')
            else:
                links = soup.find('div',class_='boxframe').find_all('a')
            
            salir = False
            for link in links:
              
                if 'thepoke.com' in link.get('href'):
                    # si hay 7 o mas publicaciones pasadas de fecha salgo
                    if contador_salir >= 7:
                        salir = True
                        break
                    url = link.get('href')
                    # Para no duplicar los links
                    if url not in visitados:
                        res = session.get(url)
                        visitados.append(url)
                    else:
                        continue

                    soup = BeautifulSoup(res.text,'lxml')
                    fecha = soup.find('p',class_='byline').get_text(strip=True).split('Updated')[1].strip()
                    # Ya que hay distintos sufijos en las fechas 
                    posibles = ["nd",'st','th']
                    for sufijo in posibles:
                        try:
                            convertida = datetime.strptime(fecha,f'%B %d{sufijo}, %Y')
                            break
                        except:
                            continue
                    
                    hoy = datetime.now().replace(second=0,microsecond=0,hour=0,minute=0)
                    operacion = hoy - timedelta(hours=24)
                    contenido = ""
                    if convertida >= operacion:
                    
                        titulo = soup.find('div',class_='post').find('h1').get_text(strip=True)

                        parrafos = soup.find('div',class_='entry normal js-article-body').find_all('p')
                    
                        # Pongo el contador para no pasarme en los parrafos
                        contador = 0
                    
                        for p in parrafos:
                            # Porque no quiero imprimir el texto de los post de reddit
                            try:
                                href = p.find('a').get('href')
                
                                if 'reddit' not in href:
                                    pass
                                else:
                                    continue
                            except:
                                pass
                            # Ya que no quiero imprimir el texto de los tweets
                            if not p.find_parent('blockquote',class_='twitter-tweet'):
                                pass
                            else:
                                continue
                            # en esta web pongo el contador para los 4 párrafos ya que es lo más óptimo
                            if contador == 5:
                                break
                            texto = p.get_text(strip=True)
                            # busco todas estas ocurrencias porque tengo que aplicar espacios 
                            if 'strong' not in texto and (p.get_text(strip=True).split('.')[0].isdigit()) is False:

                                buscar = ['a','em']
                                for b in buscar:
                                    if p.find_all(f'{b}'):
                                        for pes in p.find_all(f'{b}'):
                                            texto_a = pes.get_text(strip=True)
                                            # Porque hay palabras que originalmente tienen espacios y otras NO

                                            if texto_a + " " in texto  or texto_a + "." in texto:
                                                texto = texto.replace(texto_a," "+texto_a)
                                            elif " " + texto_a in texto:
                                                texto = texto.replace(texto_a,texto_a+ " ")
                                            else:
                                                texto = texto.replace(texto_a, " "+texto_a+ " ")
                                            


                                contenido = (contenido + " "+texto.strip()).strip()
                                contador = contador + 1

                        diccionario ={'Title':titulo,
                                'Url': url,
                                'Content': contenido}
                        datos_completos.append(diccionario)
                    else:
                        contador_salir = contador_salir +1

            if salir == True:
                break
            else:
                numero_pag = numero_pag + 1
    return datos_completos
    # with open('ThePoke.json','w',encoding='utf-8') as archivo:
    #     json.dump(datos_completos,archivo,ensure_ascii=False,indent=4)
            
def reddit():
    reddit = praw.Reddit(
        client_id='rH7xuqysFtxVEazNodBUXg',
        client_secret='9qmUSTk28t46qvrzWBGVmrTqAl-i7A',
        user_agent='script:victor:v1.0 (by u/Serious_Magazine_552)',
    )

    #donde voy a guardar el contenido
    contenido_total = []

    # Se realiza una solicitud get a la API
    for post in reddit.subreddit('politics').new(limit=1000):
        
        fecha = post.created_utc

        # Transformo las fechas a UTC
        hoy = datetime.now(timezone.utc)
        objeto_datetime = datetime.fromtimestamp(fecha,tz=timezone.utc)
        operacion = hoy -timedelta(hours=24)
   

        if objeto_datetime >= operacion:
            # Para limpiar correctamente el título
            titulo = post.title.replace('"',"'").replace("\n","")
            url = post.url

            diccionario = {'Title': titulo,
                        'Url': url,
                        'Content': 'REDDIT'}
            
            contenido_total.append(diccionario)
        else:
          
            break
    return contenido_total

def nypost(headers):
    pag = 1
    
    
    with requests.Session() as session:
        session.headers.update(headers)
        #donde voy a almacenar todo el contenido para ser exportado:
        todo = []
   
        while True:
            url = f'https://nypost.com/weird-but-true/page/{pag}/'
            response = session.get(url)
            salir = False
            soup = BeautifulSoup(response.text,'lxml')
            fechas = soup.find_all('span',class_='meta meta--byline')

            for fecha in fechas:
                texto_fecha = fecha.get_text(strip=True)
                # Convierto ambas a UTC para evitar malentendidos
                convertida = datetime.strptime(texto_fecha,'%B %d, %Y | %I:%M%p').astimezone(timezone.utc).replace(tzinfo=None)
                hoy = datetime.now(timezone.utc).replace(second=0,microsecond=0,tzinfo=None)
                # el valor de operacion es el día anterior (ayer)
                operacion = hoy - timedelta(hours=24)
                
                # Salgo directamente al encontrar una noticia que supere los 2 días de publicación
                if (hoy - convertida).days > 2:
                    salir = True
                    break


                if convertida >= operacion:
                    link = fecha.find_parent('div',class_='story__text').find('h3').find('a').get('href')
                    respuesta = session.get(link)

                    soup = BeautifulSoup(respuesta.text,'lxml')
                    
                    titulo = soup.find('h1',class_='headline headline--single-fallback').get_text(strip=True)

                    # cojo todos los parrafos p y los almaceno en una lista
                    parrafos = soup.find('div',class_='single__content entry-content m-bottom').find_all('p',limit=5)
                    contenido = ""
        
                    for p in parrafos:
                        texto_parrafo = p.get_text(strip=True)

                        if p.find('a'):
                            texto_a = p.find('a').get_text(strip=True)
                            if texto_a + "." in texto_parrafo:
                                texto_parrafo = texto_parrafo.replace(texto_a," "+texto_a).strip()
                            else:
                                texto_parrafo = texto_parrafo.replace(texto_a," "+texto_a+" ").strip()

                        contenido = (contenido + " "+texto_parrafo).strip()
                    
                    diccionario ={'Title':titulo,
                            'Url': link,
                            'Content': contenido}
                    
                    todo.append(diccionario)
         
        
            if salir == True:
                break
            pag = pag + 1
    return todo

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    only_results = []  

    futures.append(executor.submit(allthat))
    
    futures.append(executor.submit(nypost,headers))
    futures.append(executor.submit(reddit))
    futures.append(executor.submit(thepoke,headers))
 

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        # Result es asi: ([{},{},{}], [{},{},{}]) en este caso len sera 2
        # o asi: ([{},{},{}]) en este caso len será 3
        only_results.append(result)
    
exportar = []
# only results es una lista asi: [[{},{}...]]
for x in only_results:
    # x es una lista así: [{},{}..]
    nueva_lista = x
    for y in nueva_lista:
        #cuando itero entre cada y me queda en cada linea un diccionario: {}
        exportar.append(y)

with open('SecondBot.json','w',encoding='utf-8') as archivo:
        json.dump(exportar,archivo,ensure_ascii=False,indent=4)