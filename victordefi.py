from seleniumbase import SB
import time
from datetime import datetime, timedelta
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
       
       

        links.append(sb.get_attribute("//div[@class='media-story-card__body__3tRWy']/h3/a",'href',timeout=30))
        elementos = sb.find_elements("//div[@class='media-story-card__body__3tRWy']/time")
    
    
        for elemento in elementos:
            datetime_str = elemento.get_attribute("datetime")
            try:
                datetime_publicacion = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            except:
                datetime_publicacion = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

            now = datetime.now()
            last_24_hours = now - timedelta(hours=24)

            if last_24_hours <= datetime_publicacion <= now:
                href = sb.get_attribute(f"//div[@class='media-story-card__body__3tRWy']/time[contains(@datetime,'{datetime_str}')]/../a",'href')
                if 'graphics' not in href and href not in links:
                    links.append(href)

        
        datos_reuters = []
        datos_reuters_4 = []

        evento = False
        for link in links:
            
          
            try:
                

                sb.driver.default_get(link)
                time.sleep(1.6)
        
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
    
    chromium_arg = '--disable-search-engine-choice-screen'
    start_event.wait()
    with SB(undetectable=True,pls='none',chromium_arg=chromium_arg,ad_block=True) as sb:
        sb.maximize_window()
        #comienza ABC
        sb.driver.default_get("https://www.abc.net.au/news/business")
        
        for x in range(7):

            sb.click('//button[@data-component="PaginationLoadMoreButton"]')
            time.sleep(1.5)

        
        links = []
        elementos = sb.find_elements("//div[@class='DetailCard_hat__n8QSK']/time[1]")

        for elemento in elementos:
            datetime_str = elemento.get_attribute("datetime")
        
            try:
                datetime_publicacion = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            except:
                
                datetime_publicacion = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                
            now = datetime.utcnow()
            last_24_hours = now - timedelta(hours=24)

            if last_24_hours <= datetime_publicacion <= now:
                href = sb.get_attribute(f"//time[contains(@datetime,'{datetime_str}')]/ancestor::article/div/h3/a",'href')
                links.append(href)
        
        

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
                    fecha_a_comprobar = datetime.strptime(fecha, "%I:%M%p%B %d, %Y")
            
                    fecha_actual = datetime.now()

            
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


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    first_results = []  
    second_results = []

    futures.append(executor.submit(reuters))
    
    futures.append(executor.submit(abc))
    futures.append(executor.submit(australian))

    for future in concurrent.futures.as_completed(futures):
        result1,result2 =future.result()

        first_results.append(result1)
        second_results.append(result2)

exportar2 = []
for x in second_results:
    nueva_lista = x
    for y in nueva_lista:
        exportar2.append(y)

exportar1 = []

for x in first_results:
    nueva_lista = x
    for y in nueva_lista:
        exportar1.append(y)

with open('DATA_all_content.json', 'w', encoding='utf-8') as f:
    json.dump(exportar1, f, ensure_ascii=False, indent=4)


with open('4_paragraphs.json', 'w', encoding='utf-8') as f:
        json.dump(exportar2, f, ensure_ascii=False, indent=4)



