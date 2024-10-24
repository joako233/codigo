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
start_event = threading.Event()
sys.argv.append("-n")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
}

def reuters():
    
    chromium_arg = '--disable-search-engine-choice-screen'
    #para reuters:
    
    with SB(undetectable=True,pls='none',chromium_arg=chromium_arg,ad_block=True) as sb:
        
        print()
        print("(+) Analyzing the pages...")
        print("(+) Please wait for the terminal to close automatically...")
        print()
        sb.maximize_window()
        
        
        sb.get("https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2Fbusiness%2F")
       
        # sb.uc_open_with_reconnect('https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2Fbusiness%2F',7)
       
        # try:
        #     sb.switch_to_frame("iframe[sandbox='allow-scripts allow-same-origin allow-forms']",timeout=2)
        #     sb.uc_open_with_reconnect('https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2Fbusiness%2F',7)
        # except:
        #     pass



        sb.send_keys("//input[@id='email']",'yobev55195@daypey.com',timeout=35)
        sb.send_keys("//input[@id='password']",'Sensei2002#',timeout=35)
        sb.click("span:contains('Sign in')",timeout=35)
        time.sleep(1)
        
        # try:
        #     sb.switch_to_frame("//iframe[@sandbox='allow-scripts allow-same-origin allow-forms']")
        #     try:
        #         sb.uc_open_with_reconnect('https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2Fbusiness%2F',7)
        #     except Exception as e:
        #         print(e)
        # except Exception as e:
        #     print(e)
        #     input()
        #     pass
        # input()
        try:
            sb.click("//button[@id='onetrust-reject-all-handler']",timeout=1)
        except:
            pass
        
        while True:
            try:
                for x in range(18):
                    sb.click("span:contains('Load more')")
                    time.sleep(0.5)
                break
            except:
                sb.uc_open_with_reconnect('https://www.reuters.com/business/',7)



        sb.assert_element_visible("span:contains('Load more')",timeout=10)
        links = []
       
        fechas_usadas = []

        links.append(sb.get_attribute("//div[@class='media-story-card__body__3tRWy']/h3/a",'href',timeout=30))
        while True:
            time.sleep(1)
            elementos = sb.find_elements("//div[@class='media-story-card__body__3tRWy']/time")
            salir = False
        
            for elemento in elementos:
                datetime_str = elemento.get_attribute("datetime")
                if datetime_str not in fechas_usadas:
                    fechas_usadas.append(datetime_str)
                    try:
                        datetime_publicacion = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
                    except:
                        datetime_publicacion = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

                    now = datetime.now(timezone.utc).replace(second=0,microsecond=0,tzinfo=None)
                    last_24_hours = now - timedelta(hours=24)
                    if (now - datetime_publicacion).days >= 2:
                      
                        salir = True
                        break


                    if last_24_hours <= datetime_publicacion <= now:
                        href = sb.get_attribute(f"//div[@class='media-story-card__body__3tRWy']/time[contains(@datetime,'{datetime_str}')]/../a",'href')
                        if 'graphics' not in href and href not in links:
                            links.append(href)

            if salir == True:
         
                break
            else:
                sb.click("span:contains('Load more')")

        
        datos_reuters = []
        datos_reuters_4 = []

        evento = False
        for link in links:
            
          
            try:
                

                sb.driver.default_get(link)
                time.sleep(1.6)
                # porque no habia otra forma de eliminar esta url
                if 'graphics' in sb.get_current_url():
                    continue
                while True:
                    try:
                        titulo = sb.get_text("//h1[@data-testid='Heading']",timeout=7)
                        if evento == False:
                            start_event.set()
                            evento = True
                        else:
                            pass
                        break
                    except:
                
                        sb.uc_open_with_reconnect(link,9)
        

                url = link
                parrafos = sb.find_elements("//div[contains(@data-testid,'paragraph')]")
                contenido = ""

                for p in parrafos:
                    p = p.text.strip()
                    contenido = (contenido + " " + p).strip()
                    
                
                contenido4 = ""
                salir_reuters = 0

                for p in parrafos:
                    if salir_reuters == 4:
                        break
                    salir_reuters = salir_reuters +1
                    p = p.text.strip()
                    contenido4 = (contenido4 + " " + p).strip()

                nueva_entrada = {
                    "Title": titulo,
                    "Url": url,
                    "Content": contenido.replace('"',"'").replace('\n, opens new tab\n'," ")
                    }
                
                entrada4 = {
                    "Title": titulo,
                    "Url": url,
                    "Content": contenido4.replace('"',"'").replace('\n, opens new tab\n'," ")
                    }
                
                datos_reuters.append(nueva_entrada)
                datos_reuters_4.append(entrada4)
                
            except Exception as e:
                print(e)
    
    return datos_reuters, datos_reuters_4

def abc():

    links = []
    offset = 0
    with requests.Session() as session:
        

        while True:
            respuesta = session.get(f'https://www.abc.net.au/news-web/api/loader/channelrefetch?name=PaginationArticlesFuture&documentId=12785638&prepareParams=%7B%22imagePosition%22%3A%7B%22mobile%22%3A%22right%22%2C%22tablet%22%3A%22right%22%2C%22desktop%22%3A%22right%22%7D%7D&loaderParams=%7B%22pagination%22%3A%7B%22size%22%3A5%7D%7D&future=true&offset={offset}&size=5&total=250')
            diccionario = respuesta.json()
            salir = False
            lista = diccionario['collection']
            for elemento in lista:
                dia = elemento['dates']['firstPublished']
                link = "https://www.abc.net.au"+ elemento['link']

                convertida = datetime.fromisoformat(dia).replace(tzinfo=None,second=0,microsecond=0)
                hoy = datetime.now(timezone.utc).replace(microsecond=0,second=0,tzinfo=None)
                operacion = hoy - timedelta(hours=24)
                if (hoy - convertida).days >= 3:    
                    salir = True
                    break

                if convertida >= operacion:
                    
                    links.append(link)
            
            if salir == True:
                break
            else:
    
                offset = offset + 5
      

    datos_abc = []
    abc4 = []
    visitados = []
    
    for link in links:
        
        if link not in visitados:
            contenido4 = ""
            contenido = ""
            
            
            re = requests.get(link)

            soup = BeautifulSoup(re.text,'lxml')
            encontrando = soup.find('div',class_='ArticleHeadlineTitle_container__f00HU')
            titulo = encontrando.find('h1').text
            url = link

            parrafos = soup.select('div.ArticleRender_article__7i2EW > p.paragraph_paragraph__iYReA')
            for p in parrafos:
                if not p.find('em') and not p.find('strong'):
                    parrafo = p.text.strip()
                    contenido = (contenido + " " + parrafo).strip()

            salir_abc = 0

            for p in parrafos:
                if salir_abc == 4:
                    break
                salir_abc = salir_abc +1
                if not p.find('a'):
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
                
            datos_abc.append(nueva_entrada)
            abc4.append(entrada4)
    return datos_abc,abc4

def australian():
    start_event.wait()
    chromium_arg = '--disable-search-engine-choice-screen'
    with SB(undetectable=True,pls='none',chromium_arg=chromium_arg,ad_block=True) as sb:
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
        try:
            elementos = sb.find_elements('//a[contains(@class,"storyblock_title_link")  and (contains(@data-tgev-container,"business-tops")  or contains(@data-tgev-container,"dataroom")  or contains(@data-tgev-container,"spotlight")  or contains(@data-tgev-container,"margin-call")  or contains(@data-tgev-container,"media")  or contains(@data-tgev-container,"wealth")  or contains(@data-tgev-container,"technology")  or contains(@data-tgev-container,"stockhead"))]')
            # print(f"Longitud de austrlian: {len(elementos)}")
            for ele in elementos:
            
                links.append(ele.get_attribute('href'))
        except Exception as e:
            print(e)
            input()
    
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
        visitadas = []
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
            divs = guardian.find_all('div',class_='dcr-rni59y')
            for div in divs:
                href = div.find('a').get('href')
                if 'live' not in href:
                    news = 'https://www.theguardian.com/'+href
    
                    links.append(news)
                else:
                    continue

        #los distintos datos para ser exportados
        datos_theguardian = []
        datos_4_theguardian = []

        # itero en la lista de links
        for link in links:
            if link not in visitadas:
                visitadas.append(link)
                respuesta = session.get(link)

                soup = BeautifulSoup(respuesta.text,'lxml')

                #porque cambia la forma de extraer la fecha en alguna página
                try:
                    fecha = soup.find('span',class_='dcr-u0h1qy').get_text(strip=True)
                except:
                    fecha = soup.find('div',class_='dcr-1pexjb9').get_text(strip=True)
                  
                #comprobando si la publicación supera o no las 24 horas
 
                hoy = datetime.now().replace(second=0,microsecond=0)
                formatos = ['AEDT','AEST','CEST']
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
                    parrafos = cuerpo.find_all('p',class_='dcr-1eu361v')
                    #porque cambia en alguna noticia la forma de extraer los párrafos
                    if len(parrafos) == 0:
                       
                        parrafos = cuerpo.find_all('p',class_='dcr-an2vbh')
                    if len(parrafos) == 0:
                     
                        parrafos = cuerpo.find_all('p',class_='dcr-1n1orvu')

                    #contador para los 4 párrafos
                    contador = 0
                    for p in parrafos:
                        #ya que la etiqueta strong es de un texto publicitario
                        if p.find('strong') is None:
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
    start_event.wait()
    links = []
    with SB(undetectable=True,ad_block=True,pls='none',headless2=False,chromium_arg=chromium_arg) as sb:
    
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
            while True:
                # creo una nueva url para cada pagina según el contador
                url = url+str(contador_pagina)+'/'
      
         
                response = session.get(url)
                
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
                        if url_completa not in links:
                            links.append(url_completa)

                if salir == True:
         
                    break

                contador_pagina = contador_pagina + 1
        
            

        for link in links:
        
            respuesta = session.get(link)
            soup = BeautifulSoup(respuesta.text,'lxml')
            titulo = soup.find('h1',class_='sm:text-5xl')
            cuerpo_4 = ""
            # cuando tenga el tipo de noticias cuyo titulo sea distinto, cambia la estructura, y aplico distintas cosas
            if titulo is None:
         
                titulo = soup.find('h1',class_='sm:mb-4').get_text(strip=True)
             
                #porque hay 2 tipos de párrafos que se pueden dar en la web:
                try:
                    parrafos = soup.find('div',class_='article content content-open').find_all('p')
                except:
                    parrafos = soup.find('div',class_='newsletter').find_all('p')
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

                        cuerpo_4 = (cuerpo_4 + " "+texto).strip()

           
              
                #solo extraigo 4 parrafos porque se necesita suscripción para ver la demás información
    
                
            # para el tipo de noticias normales aplico esto ya que puedo sacar toda la informacion sin necesidad de suscibirme a la web
            else:
                titulo = titulo.get_text(strip=True)
                parrafos = soup.find('div',class_='briefing content content-open').find_all('p')

                if soup.find('div',class_='briefing content content-open').find('ul'):
                    continue
                for p in parrafos:
                    buscar = ['i','a','b']
                    if not p.find('em'):
                        texto = p.get_text(strip=True)
                        for letra in buscar:
                            # tengo que buscar todas las ocurrencias en el párrafo
                            if p.find_all(f'{letra}'):
                                
                                for pe in p.find_all(f'{letra}'):
                                    pe = pe.get_text(strip=True)
                                    if pe +"." in texto:
                                        texto = texto.replace(pe," "+pe).strip()
                                    else:
                                        texto = texto.replace(pe," "+pe+" ").strip()

                        cuerpo_4 = (cuerpo_4 + " "+texto).strip()
    
            
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



