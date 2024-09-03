from seleniumbase import SB
import time
from datetime import datetime, timedelta
import json
import os
from bs4 import BeautifulSoup
import requests


now = datetime.now()
ruta_actual = os.getcwd() 

ayer = now - timedelta(days=1)
ayer = ayer.strftime("%Y-%m-%d")
hoy = now.strftime("%Y-%m-%d")

def codigos(ruta_actual):
    chromium_arg = '--disable-search-engine-choice-screen'
    #para reuters:

    with SB(undetectable=True,pls='none',headless=False,block_images=True,chromium_arg=chromium_arg) as sb:
        sb.maximize_window()
         
        sb.driver.default_get("https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2Fbusiness%2F")
        
        sb.send_keys("//input[@id='email']",'yobev55195@daypey.com',timeout=35)
        sb.send_keys("//input[@id='password']",'Sensei2002#',timeout=35)
        sb.click("span:contains('Sign in')",timeout=35)
        time.sleep(1)
        # if os.path.isdir(ruta_completa):
        #     sb.open("https://www.reuters.com/business/")
        #     sb.load_cookies('reuters.txt')
        #     sb.open("https://www.reuters.com/business/")
        # else:
        
        #     sb.uc_open_with_reconnect("https://www.reuters.com/account/sign-in/",5)
        #     sb.send_keys("//input[@id='email']",'yobev55195@daypey.com')
        #     sb.send_keys("//input[@id='password']",'Sensei2002#')
        #     sb.uc_click("span:contains('Sign in')")
            
        #     sb.uc_open_with_reconnect('https://www.reuters.com/business/',4)
        #     time.sleep(4)
        #     sb.save_cookies('reuters.txt')
        # sb.driver.default_get("https://www.reuters.com/business/")
    
        try:
            sb.click("//button[@id='onetrust-reject-all-handler']",timeout=1)
        except:
            pass
        #for x in range(13)

        while True:
            try:
                for x in range(2):
                    sb.click("span:contains('Load more')",timeout=5)
                break
            except:
                sb.driver.disconnect()
                time.sleep(12)
                sb.driver.connect()
        

       
        links = []
        links.append(sb.get_attribute("//div[@class='media-story-card__body__3tRWy']/h3/a",'href',timeout=30))
        elementos = sb.find_elements(f"//div[@class='media-story-card__body__3tRWy']/time[contains(@datetime, '{hoy}') or contains(@datetime, '{ayer}')]/../a ")
       

        datos_reuters = []
        datos_reuters_4 = []
      
        for ele in elementos:
        
            links.append(ele.get_attribute('href'))
       
        visitados = []
        contador = 0
        for link in links:
            try:
                if contador == 2:
                    break
                if link not in visitados:
                    visitados.append(link)
                    # sb.get(link)
                    sb.driver.default_get(link)
                 
                    contador = contador +1
                    while True:
                        try:
                            titulo = sb.get_text("//h1[@data-testid='Heading']",timeout=10)
                            break
                        except:
                           
                            sb.driver.disconnect()
                            time.sleep(15)
                            sb.driver.connect()


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
                        "Content": contenido.replace('"',"'") 
                        }
                    
                    entrada4 = {
                        "Title": titulo,
                        "Url": url,
                        "Content": contenido4.replace('"',"'") 
                        }
                    
                    datos_reuters.append(nueva_entrada)
                    datos_reuters_4.append(entrada4)
                    
                else:
                    pass
            except Exception as e:
                print(e)
    
      
        #comienza ABC
        sb.driver.default_get("https://www.abc.net.au/news/business")
 

        #for x in range(8)
        for x in range(1):
            sb.click('//button[@data-component="PaginationLoadMoreButton"]',timeout=30)
        links = []
        time.sleep(1)
        elementos = sb.find_elements(f"//time[contains(@datetime,'{hoy}') or contains(@datetime,'{ayer}')]/ancestor::article/div/h3/a")

        for e in elementos:
            links.append(e.get_attribute('href'))


        datos_abc = []
        abc4 = []
        visitados = []
        contador = 0
        
        for link in links:
            if contador ==3:
                break
            if link not in visitados:
                contenido4 = ""
                contenido = ""
                contador = contador + 1
                
                re = requests.get(link)

                soup = BeautifulSoup(re.text,'lxml')
                encontrando = soup.find('div',class_='ArticleHeadlineTitle_container__f00HU')
                titulo = encontrando.find('h1').text
                url = link

                parrafos = soup.find_all('p',class_='paragraph_paragraph__iYReA')
                for p in parrafos:
                    if not p.find('a'):
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
            

        
        carpeta = 'saved_cookies'
        archivo = 'australian.txt'
        
        completa = os.path.join(ruta_actual,carpeta,archivo)

    
        if os.path.isfile(completa):
            sb.driver.default_get("https://www.theaustralian.com.au/business")
            sb.load_cookies('australian.txt')
   
            # sb.driver.default_get("https://www.theaustralian.com.au/business")
            time.sleep(3)
            sb.save_cookies('australian.txt')
        else:
            sb.driver.default_get("https://www.theaustralian.com.au/business")
            while True:
                try:
                    sb.click("//a[@class='header_log-in']",timeout=3)
                    sb.send_keys("//input[@type='email']",'ben.wong@moelisaustralia.com',timeout=30)
                    break
                except:
                    sb.refresh()
                    continue
            
            sb.send_keys("//input[@type='password']",'Moelis21!',timeout=30)
            sb.click("//button[@type='submit']",timeout=30)
            time.sleep(5)
        
            sb.save_cookies('australian.txt')

    
        links = []
    
        elementos = sb.find_elements('//a[contains(@class,"storyblock_title_link")  and (contains(@data-tgev-container,"business-tops")  or contains(@data-tgev-container,"dataroom")  or contains(@data-tgev-container,"spotlight")  or contains(@data-tgev-container,"margin-call")  or contains(@data-tgev-container,"media")  or contains(@data-tgev-container,"wealth")  or contains(@data-tgev-container,"technology")  or contains(@data-tgev-container,"stockhead"))]')

        for ele in elementos:
        
            links.append(ele.get_attribute('href'))
        
        time.sleep(1)

    with open('saved_cookies/australian.txt','r',encoding='utf-8') as archivo:
        lineas = json.load(archivo)

    cookies = {}
    for linea in lineas:
        cookies[linea['name']] = linea['value']

    
    visitados = []
    
    contador = 0
    datos_australian = []
    aus4 = []

    for link in links:
        if contador == 3:
            break
        contador = contador + 1
        if link not in visitados:
            visitados.append(link)
            re = requests.get(link,cookies=cookies)
            soup = BeautifulSoup(re.text,'lxml')

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
            
    
    parrafos_4 = datos_reuters_4 + abc4 + aus4

    with open('4_paragraphs.json', 'w', encoding='utf-8') as f:
        json.dump(parrafos_4, f, ensure_ascii=False, indent=4)
    
    listas_unidas = datos_reuters + datos_australian + datos_abc

    return listas_unidas

term = codigos(ruta_actual)
with open('DATA_all_content.json', 'w', encoding='utf-8') as f:
    json.dump(term, f, ensure_ascii=False, indent=4)
