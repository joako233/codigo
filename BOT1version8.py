from seleniumbase import SB
import time
from datetime import datetime, timedelta,timezone
import json
import requests.cookies
import os
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import threading
import sys
import re 
sys.argv.append("-n")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
}

print()
print("(+) Analyzing the pages...")
print("(+) Please wait for the terminal to close automatically...")
print()
def reuters():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.reuters.com/business/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    offset = 0
    contador = 0
    with requests.Session() as session:
        # Donde almaceno el contenido para ser exportado
        datos_reuters = []
        datos_reuters_4 = []

        session.headers = headers
        titulo_links = {}
        while True:
            
            params = {
            'query': json.dumps({"fetch_type":"section","orderby":"last_updated_date:desc","offset":offset,"section_id":"/business/","size":10,"website":"reuters"}),
            'd': '221',
            '_website': 'reuters',
            }
            session.params = params
            response = session.get(
                'https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1',
            )
        
            diccionario = response.json()
            articulos = diccionario['result']['articles']
            for articulo in articulos:
                titulo = articulo['title']
                url = articulo['canonical_url']
                fecha_publicacion = articulo['display_time']
            
                hoy = datetime.now()
                operacion = (hoy - timedelta(hours=24)).replace(second=0,microsecond=0).astimezone(timezone.utc)
                
                try:
                    convertida = datetime.strptime(fecha_publicacion,"%Y-%m-%dT%H:%M:%SZ").replace(second=0,microsecond=0).astimezone(timezone.utc)
                except:
                    convertida = datetime.strptime(fecha_publicacion,"%Y-%m-%dT%H:%M:%S.%fZ").replace(second=0,microsecond=0).astimezone(timezone.utc)

                if convertida >= operacion:
                    titulo = articulo['title']
    
                    url = "https://www.reuters.com"+articulo['canonical_url']
                    titulo_links[titulo] = url
        
                else:
                    contador = contador +1
                if contador >=3:
                    break

            if contador >=3:
                break
        
            offset = offset+10


        json_data = {
        'userName': 'yobev55195@daypey.com',
        'credentials': 'Sensei2002#',
        'grantType': 'password',
        'rememberMe': True,
        }

        response = session.post(
            'https://api-reuters-reuters-prod.cdn.arcpublishing.com/identity/public/v1/auth/login',
            json=json_data,
        )

        for titulo,link in titulo_links.items():
            while True:
                res = session.get(link)
    
                if res.status_code != 200:
        
                    time.sleep(1)
                    continue
                else:
                    # print(f"(+) BIEN EN {link}")
                    break
            
            soup = BeautifulSoup(res.text,'lxml')
            
            parrafos = soup.find_all("div",attrs={"data-testid":re.compile(r'^paragraph')})
            
            contenido = ""
            contenido4 = ""
            for p in parrafos:
                p = p.text.strip()
                contenido = (contenido + " " + p).strip()
            
            parrafos4 = soup.find_all("div",attrs={"data-testid":re.compile(r'^paragraph')},limit=4)
            for p in parrafos4:
                p = p.text.strip()
                contenido4 = (contenido4 + " " + p).strip()
            
            nueva_entrada = {
                "Title": titulo,
                "Url": link,
                "Content": contenido.replace('"',"'").replace('\n, opens new tab\n'," ").replace(", opens new tab"," ")
                }
            
            entrada4 = {
                "Title": titulo,
                "Url": link,
                "Content": contenido4.replace('"',"'").replace('\n, opens new tab\n'," ").replace(", opens new tab"," ")
                }
            
            datos_reuters.append(nueva_entrada)
            datos_reuters_4.append(entrada4)

            
    return datos_reuters,datos_reuters_4
                    

def abc():
    headers = {
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.abc.net.au',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.abc.net.au/news/2024-11-13/choice-shonky-award-2024-meta-scams-nib-vacuum-juice-socks/104591152',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    datos_abc = []
    abc4 = []
    links = []
    offset = 0
    with requests.Session() as session:
        
        while True:
            respuesta = session.get(f'https://www.abc.net.au/news-web/api/loader/channelrefetch?name=PaginationArticlesFuture&documentId=12785638&prepareParams=%7B%22imagePosition%22%3A%7B%22mobile%22%3A%22right%22%2C%22tablet%22%3A%22right%22%2C%22desktop%22%3A%22right%22%7D%7D&loaderParams=%7B%22pagination%22%3A%7B%22size%22%3A5%7D%7D&future=true&offset={offset}&size=5&total=250')
          
            diccionario = respuesta.json()
            salir = False
            lista = diccionario['collection']
            for elemento in lista:
                dia = elemento['dates']['lastUpdated']
                link = elemento['link']
        
                id = link.split("/")[-1]
        
                convertida = datetime.fromisoformat(dia).replace(tzinfo=None,second=0,microsecond=0)
     
        
                hoy = datetime.now().replace(microsecond=0,second=0,tzinfo=None)
        
                operacion = hoy - timedelta(hours=24)
                if (hoy - convertida).days >= 8:    
                    salir = True
                    break

                if convertida >= operacion:
                    
                    links.append(id)
            
            if salir == True:
                break
            else:
    
                offset = offset + 5
      
    params = {
    'apikey': 'fdc2894edc424a80989df33c0e853f80',
    }
    with requests.Session() as session:
        session.params = params
        session.headers = headers

        
        for link in links:
            contador = 0
            respuesta = session.get(f"https://api.abc.net.au/terminus/api/v2/content/coremedia/article/{link}")
            diccionario = respuesta.json()
            lista = diccionario['text']['plain'].split("\n")
            url = diccionario['canonicalURL']
            titulo = diccionario['title']

            cuerpo = ""
            cuerpo4 = ""

            for x in lista:
                if '[' not in x and x != '' and '#' not in x:
                    cuerpo = cuerpo + " "+x
                    if contador <=3:
                        cuerpo4 = cuerpo4 + x
                        contador = contador + 1

    
            nueva_entrada = {
                    "Title": titulo,
                    "Url": url,
                    "Content": cuerpo.replace('"',"'").strip()
                    }
            entrada4 = {
                    "Title": titulo,
                    "Url": url,
                    "Content": cuerpo4.replace('"',"'").strip()
                    } 
            datos_abc.append(nueva_entrada)
            abc4.append(entrada4)

    return datos_abc,abc4

def australian():

    chromium_arg = '--disable-search-engine-choice-screen'
    with SB(undetectable=True,pls='none',chromium_arg=chromium_arg,ad_block=True,headless2=True) as sb:
        sb.maximize_window()
        ruta_actual = os.getcwd() 
        
        carpeta = 'saved_cookies'
        archivo = 'australian.txt'
        
        completa = os.path.join(ruta_actual,carpeta,archivo)


        if os.path.isfile(completa):
            sb.driver.default_get("https://www.theaustralian.com.au/business")
            sb.load_cookies('australian.txt')
            sb.driver.default_get("https://www.theaustralian.com.au/business")
            sb.assert_element_visible('//a[contains(@class,"storyblock_title_link")]',timeout=30)
            sb.save_cookies('australian.txt')
        else:
            sb.driver.default_get("https://www.theaustralian.com.au/business")
            while True:
                try:
                    sb.click("//a[@class='header_log-in']",timeout=5)
                    sb.send_keys("//input[@type='email']",'ben.wong@moelisaustralia.com',timeout=5)
                    
                    break
                except:
                    sb.refresh()
                    continue

            
            sb.send_keys("//input[@type='password']",'Moelis21!',timeout=30)
            sb.click("//button[@type='submit']",timeout=30)
            sb.assert_element_visible('//a[contains(@class,"storyblock_title_link")]',timeout=30)
        
            sb.save_cookies('australian.txt')

        links = []
        time.sleep(4)
      
        elementos = sb.find_elements('//a[contains(@class,"storyblock_title_link")  and (contains(@data-tgev-container,"business-tops")  or contains(@data-tgev-container,"dataroom")  or contains(@data-tgev-container,"spotlight")  or contains(@data-tgev-container,"margin-call")  or contains(@data-tgev-container,"media")  or contains(@data-tgev-container,"wealth")  or contains(@data-tgev-container,"technology")  or contains(@data-tgev-container,"stockhead"))]')
        # print(f"Longitud de austrlian: {len(elementos)}")
        for ele in elementos:
        
            links.append(ele.get_attribute('href'))
        
    
    jar = requests.cookies.RequestsCookieJar()

    with open('saved_cookies/australian.txt','r',encoding='utf-8') as archivo:
        lineas = json.load(archivo)

        for linea in lineas:
            jar.set(linea['name'],linea['value'])

    visitados = []


    datos_australian = []
    aus4 = []
    with requests.Session() as session:
        for link in links:
           
            
            if link not in visitados:
                visitados.append(link)
                re = session.get(link,cookies=jar)
                soup = BeautifulSoup(re.text,'lxml')
                try:
                    fecha = soup.find('div', id='publish-date', class_='byline_publish').text
                except:
                    continue
                    
                if 'hours' in fecha or 'minutes' in fecha:

                    pass
                else:
                    fecha = fecha.replace(".","").strip()
                    fecha_a_comprobar = datetime.strptime(fecha, "%I:%M%p%B %d, %Y").replace(second=0,microsecond=0)
            
                    fecha_actual = datetime.now().replace(second=0,microsecond=0)

            
                    rango_24_horas = fecha_actual - timedelta(hours=24)

            
                    dentro_ultimas_24_horas = rango_24_horas <= fecha_a_comprobar <= fecha_actual

            
                    if dentro_ultimas_24_horas:
                        pass
                    else:
                        
                        continue

            titulo = soup.find('h1',attrs={'id':'story-headline'}).text.strip()
            url = link
            parrafos = soup.select('div#story-primary > p') #selecciona solo los elementos <p> que son hijos directos del <div> con id='story-primary'.
            contenido = ""
            for p in parrafos:
                if not p.find('b') and not p.find('i'):
                    parrafo = p.text.strip()
                    contenido = (contenido + " " + parrafo).strip()

            contenido4 = ""
            salir_aus = 0
            for p in parrafos:
                if not p.find('b') and not p.find('i'):
                    if salir_aus == 4:
                        break
                    salir_aus = salir_aus +1
                    parrafo = p.text.strip()
                    contenido4 = (contenido4 + " " + parrafo).strip()

            nueva_entrada = {
                            "Title": titulo,
                            "Url": url,
                            "Content": contenido.replace('"',"'")
                            }
            
            entrada4 = {
                        "Title": titulo,
                        "Url": url,
                        "Content": contenido4.replace('"',"'") 
                        }
            
            datos_australian.append(nueva_entrada)
            aus4.append(entrada4)
                
    return datos_australian,aus4

def theguardian(headers):
    url = 'https://www.theguardian.com/au/business'
    with requests.Session() as session:

        session.headers.update(headers)
        response = session.get(url)

        #donde almaceno los links
        links = []
        soup = BeautifulSoup(response.text,'lxml')
        #distintos recuadros div con noticias
        ids = ['container-news','container-in-depth','container-world-news','container-global-view']
        #aqui itero colocando distintas ids para poder extraer los hrefs de los distintos recuadros
        for id in ids:
            
            guardian = soup.find('div',attrs={f'id':id})
            
            divs = guardian.find_all('div',class_=re.compile(r'^dcr-'))
           
            for div in divs:
                try:
                    href = div.find('a',class_='dcr-lv2v9o').get('href')
                except:
                   continue
                news = 'https://www.theguardian.com'+href
                if 'live' not in href and news not in links:
                   
    
                    links.append(news)
                else:
                    continue
    

        #los distintos datos para ser exportados
        datos_theguardian = []
        datos_4_theguardian = []

        # itero en la lista de links
        for link in links:
            
             
            respuesta = session.get(link)

            soup = BeautifulSoup(respuesta.text,'lxml')

            #porque cambia la forma de extraer la fecha en alguna página
            try:
                fecha = soup.find('summary',class_=re.compile(r'^dcr-')).find('span').get_text(strip=True)
            except:
                fecha = soup.find('div',class_='dcr-1pexjb9').get_text(strip=True)
          
            #comprobando si la publicación supera o no las 24 horas

            hoy = datetime.now().replace(second=0,microsecond=0)
            formatos = ['AEDT','AEST','CEST','CET']
            for f in formatos:
                try:
                    convertido = datetime.strptime(fecha,f'%a %d %b %Y %H.%M {f}').replace(second=0,microsecond=0)
                except:
                    continue
                
            objeto_time_delta = timedelta(hours=24)
            operacion = hoy- objeto_time_delta
            #parrafos 
            todos_parrafos = ""
            solo_4 = ""
            #filtro aquellas noticias de las últimas 24 horas
            if convertido >= operacion:
                try:
                    titulo = soup.find('div',class_='dcr-cohhs3').find('h1').get_text(strip=True)
                except:
                    titulo = soup.find('h1',class_='dcr-s88ov6').get_text(strip=True)
                url = respuesta.request.url
                
                cuerpo = soup.find('div',class_='article-body-commercial-selector')
                #porque cambia en alguna noticia la forma de extraer los párrafos
                parrafos = cuerpo.find_all('p',class_=re.compile(r'^dcr-'))
               
                #contador para los 4 párrafos
                contador = 0
                for p in parrafos:
                    #ya que la etiqueta strong es de un texto publicitario
                    if p.find('strong') is None and p.find('span') is None:
                        anterior = p.get_text(strip=True)

                        #esto es para poner bien aquellas palabras que sean hipervínculos porque se imprimen juntas
                        if p.find('a'):

                            añadir = p.find('a').get_text(strip=True)
                            if añadir + "." in anterior:
                                texto_final = anterior.replace(añadir," "+añadir)
                            else:
                                texto_final = anterior.replace(añadir," "+añadir+" ")

                            todos_parrafos = (todos_parrafos + " " + texto_final).strip()
                        
                            #para los 4 párrafos
                            if contador <= 3:
                                solo_4 = (solo_4 + " " + texto_final).strip()
                                contador = contador + 1   
                        else:
                            todos_parrafos = (todos_parrafos + " " + anterior).strip()
                            if contador <= 3:
                                solo_4 = (solo_4 + " " + anterior).strip()
                                contador = contador + 1

                        
                datos_completo = {'Title':titulo,
                                    'Url': url,
                                    'Content': todos_parrafos}
                
                parrafos_4 = {'Title':titulo,
                                'Url': url,
                                'Content': solo_4}
                
                datos_theguardian.append(datos_completo)          
                datos_4_theguardian.append(parrafos_4)     
            else:
                continue

    return datos_theguardian,datos_4_theguardian


def sydneymorning(headers):

    urls = ['https://www.smh.com.au/business/companies','https://www.smh.com.au/business/markets',
            'https://www.smh.com.au/business/the-economy','https://www.smh.com.au/business/banking-and-finance',
            'https://www.smh.com.au/business/small-business','https://www.smh.com.au/business/workplace',
            'https://www.smh.com.au/technology']
    
    chromium_arg = '--disable-search-engine-choice-screen'
    
    links = []
    with SB(undetectable=True,ad_block=True,pls='none',headless2=True,chromium_arg=chromium_arg) as sb:
    
        # sb.maximize_window()
        links = []
        for url in urls:
            sb.get(url)
            
            fechas_usadas = []
            salir = False
            while True:
                time.sleep(1)
                tiempos = sb.find_elements("//time[@class='_2_zR-']")
            
   
                for tiempo in tiempos:
                    fecha = tiempo.get_attribute('datetime')
       
                    if fecha not in fechas_usadas:
                        fechas_usadas.append(fecha)
                        hoy = datetime.now(timezone.utc).replace(microsecond=0,second=0,tzinfo=None)
                        convertida = datetime.fromisoformat(fecha).astimezone(timezone.utc).replace(microsecond=0,second=0,tzinfo=None)
                        operacion = (hoy - timedelta(hours=24))
                   
                        if (hoy - convertida).days > 2:
                            salir = True
                    
                            break
                        
                        if convertida >= operacion:
                            href = sb.find_element(f"//time[@datetime='{fecha}']/ancestor::div/h3/a").get_attribute('href')
                            url_completa = href
                            
                            if url_completa not in links:
                                
                                links.append(url_completa)
           
                if salir == True:
                    break
                else:
                    sb.click("//button[@class='_3we9i']")

    with requests.Session() as session:
        session.headers.update(headers)
    
        
        #donde almaceno todos los diccionarios para ser exportados
        datos_4 = []
        datos_totales = []
        
        #  Me meto ya en las publicaciones
        for link in links:
            respuesta = session.get(link)
            soup = BeautifulSoup(respuesta.text,'lxml')

            titulo = soup.find('h1',attrs={'data-testid':'headline'}).get_text(strip=True)
            #contador para los 4 párrafos
            contador = 0

            bloques = soup.find_all('div',attrs={'data-testid':'body-content'})

            cuerpo_completo = ""
            cuerpo_4 = ""
            # itero sobre los distintos bloques de información de la web
            for bloque in bloques:
                #despues busco todos los parrafos dentro de cada bloque de información
                pes = bloque.find_all('p')
                for p in pes:
      
                    # son condiciones que aplico para no seleccionar texto no deseado
                    if not p.find('strong') and not p.find('b') and not p.find('span') and not p.find('em'):
                        texto_parrafo = p.get_text(strip=True)
                        cuerpo_completo = (cuerpo_completo + " " + texto_parrafo).strip()
                        
                    
                        if contador < 4:
                            contador = contador + 1
                            cuerpo_4 = (cuerpo_4 + " " + texto_parrafo).strip()
               
        
            #construyo los diccionarios y posteriormente los añado a las listas de arriba
            datos_completo = {'Title':titulo,
                            'Url': link,
                            'Content': cuerpo_completo}
        
            parrafos_4 = {'Title':titulo,
                            'Url': link,
                            'Content': cuerpo_4}

            datos_4.append(parrafos_4)
            datos_totales.append(datos_completo)

    return datos_totales,datos_4

def capitalbrief(headers):

    urls = [
    "https://www.capitalbrief.com/finance/",
    "https://www.capitalbrief.com/technology/",
    "https://www.capitalbrief.com/law/",
    "https://www.capitalbrief.com/media/",
    "https://www.capitalbrief.com/climate/"]
   
    with requests.Session() as session:
        session.headers.update(headers)
        links = []
        contador_pagina = 1
        #donde almaceno todo el contenido para luego exportarlo
        solo_4 = []

        for url in urls:
          
            #creo esta variable para salir cuando las publicaciones sean ya muy antiguas
            salir = False
            #creo un contador para ir iterando entre las distintas paginas de cada url
            contador_pagina = 1
     
            # creo una nueva url para cada pagina según el contador
       
            
            while True:
                contador_pagina = str(contador_pagina)
               
                linki = url+contador_pagina+"/"
       
                contador_pagina = int(contador_pagina)
                response = session.get(linki)
                contador_pagina = contador_pagina + 1
            
                soup = BeautifulSoup(response.text,'lxml')

                tiempos = soup.find_all('time')
                hoy = datetime.now(timezone.utc).replace(microsecond=0,second=0,tzinfo=None)
            
                for tiempo in tiempos:
                    fecha = tiempo.get('datetime')
                    formateada = datetime.strptime(fecha,'%Y-%m-%dT%H:%M:%S.%fZ').replace(microsecond=0,second=0)

                    operacion = hoy - timedelta(hours=24)
                    # Si hay una diferencia de mas de 2 dias entre hoy y la fecha de publicacion de la noticia
                    if (hoy - formateada).days > 2:
                
                        salir = True
                        break

                    # si la fecha no supera las 24 horas creo el link 
                    if formateada >= operacion:
                        href = tiempo.find_parent('article').find('h2').find('a').get('href')
                        url_completa = 'https://www.capitalbrief.com'+href
                        links.append(url_completa)
                       

                if salir == True:
                 
                    break
    
                contador_pagina = contador_pagina + 1
        
        links = list(set(links))

      
        for link in links:
        
            respuesta = session.get(link)
            soup = BeautifulSoup(respuesta.text,'lxml')
            titulo = soup.find('h1',class_=re.compile(r'^sm:')).get_text(strip=True)

            cuerpo_4 = ""
            
            try:
                if soup.find('div',class_='briefing content content-open').find('ul'):
                    texto = soup.find('div',class_='briefing content content-open').get_text(strip=True)
                    cuerpo_4 = cuerpo_4 + texto
                    parrafos_4 = {'Title':titulo,
                        'Url': link,
                        'Content': cuerpo_4.replace('"',"'").strip()}
        
                    solo_4.append(parrafos_4)
              
                    continue
            except:
                pass
          
            parrafos = soup.find('div',class_=re.compile(r'^newsletter|^article|^briefing')).find_all('p')
            
  
            for p in parrafos:
                buscar = ['i','a','b']
                if not p.find('em'):
                    texto = p.get_text(strip=True)
                    for letra in buscar:
                        # tengo que buscar todas las ocurrencias en el párrafo
                        if p.find_all(f'{letra}'):
                            for r in p.find_all(f'{letra}'):
                                r = r.get_text(strip=True)
                                if r +"." in texto:
                                    texto = texto.replace(r," "+r)
                                else:
                                    texto = texto.replace(r," "+r+" ")
                else:
                    continue
                cuerpo_4 = (cuerpo_4 + " "+texto).strip()
            
         
            #solo extraigo 4 parrafos porque se necesita suscripción para ver la demás información
        
            parrafos_4 = {'Title':titulo,
                        'Url': link,
                        'Content': cuerpo_4.replace('"',"'").strip()}

        
            solo_4.append(parrafos_4)
    
    return solo_4


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    first_results = []  
    second_results = []

    futures.append(executor.submit(reuters))
    
    futures.append(executor.submit(abc))
    futures.append(executor.submit(australian))
    futures.append(executor.submit(theguardian,headers))
    futures.append(executor.submit(sydneymorning,headers))
    futures.append(executor.submit(capitalbrief,headers))


    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        # Result es asi: ([{},{},{}], [{},{},{}]) en este caso len sera 2
        # o asi: ([{},{},{}]) en este caso len será 3
        if len(result) == 2:
            result1,result2 = future.result()
            first_results.append(result1)
            second_results.append(result2)
        else:
            result2 = future.result()
            second_results.append(result2)

        
exportar2 = []
# Second results es una lista asi: [[{},{}...]]
for x in second_results:
    # x es una lista así: [{},{}..]
    nueva_lista = x
    for y in nueva_lista:
        #cuando itero entre cada y me queda en cada linea un diccionario: {}
        exportar2.append(y)

exportar1 = []
# firs results sera así: [[{},{},{}], [{},{},{}]]
for x in first_results:
    # [{},{},{}], [{},{},{}]
    nueva_lista = x
    for y in nueva_lista:
        #{},{},{}, {},{},{}
        exportar1.append(y)

with open('DATA_all_content.json', 'w', encoding='utf-8') as f:
    json.dump(exportar1, f, ensure_ascii=False, indent=4)


with open('4_paragraphs.json', 'w', encoding='utf-8') as f:
        json.dump(exportar2, f, ensure_ascii=False, indent=4)