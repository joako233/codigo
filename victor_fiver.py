from seleniumbase import SB
import time
import os
import concurrent.futures
from datetime import datetime
import json
import sys
from threading import Lock
sys.argv.append("-n")

lock = Lock()
now = datetime.now()
chrommium_arg = '--lang=en'

fecha = now.strftime("%Y-%m-%d")
dia = (int(now.strftime("%d")) -1)



def reuters():
    dia_actual = now.strftime("%d")
    dia_anterior = dia
    datetime_actual = fecha

    # print(dia_actual)
    # print(dia_anterior)
    # print(datetime_actual)
    # input()
    lock.acquire()
    with SB(undetectable=True,chromium_arg=chrommium_arg,pls='eager',headless=True,block_images=True,save_screenshot=True) as sb:
        sb.maximize_window()

        # ruta_actual = os.getcwd()
        # carpeta = 'saved_cookies'

        # ruta_completa = os.path.join(ruta_actual, carpeta)
        try:
            sb.uc_open_with_reconnect("https://www.reuters.com/account/sign-in/",3)
            lock.release()
            sb.send_keys("//input[@id='email']",'yobev55195@daypey.com',timeout=35)
            sb.send_keys("//input[@id='password']",'Sensei2002#',timeout=35)
            sb.uc_click("span:contains('Sign in')",timeout=35)
                
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
                
            sb.open("https://www.reuters.com/business/")
            for x in range(15):
                sb.click("span:contains('Load more')",timeout=35)

            time.sleep(4)
            elementos = sb.find_elements(f"//div[@class='media-story-card__body__3tRWy']//time[contains(text(),'{dia_actual}') or contains(text(),'{dia_anterior}') or contains(@datetime,'{datetime_actual}') or contains(@datetime,'{dia_anterior}')]/ancestor::div[@class='media-story-card__body__3tRWy']//a[@data-testid='Heading' or @class='text__text__1FZLe text__dark-grey__3Ml43 text__inherit-font__1Y8w3 text__inherit-size__1DZJi link__link__3Ji6W link__underline_on_hover__2zGL4 link__inherit-line-height__2qjXx media-story-card__heading__eqhp9']")
        except Exception as e:
            sb.save_screenshot('errore.png')
            print(e)
         
        datos_reuters = []
        links = []

        for ele in elementos:
            # time.sleep(0.5)
            links.append(ele.get_attribute('href'))
       
  
        visitados = []
        contador = 0
        for link in links:
            try:
                if contador == 5:
                    break
                if link not in visitados:
                    visitados.append(link)
                    sb.driver.default_get(link)
                    # sb.get(link)
                    contador = contador +1
                    titulo = sb.get_text("//h1[@data-testid='Heading']",timeout=30)
                    url = link
                    parrafos = sb.find_elements("//div[contains(@data-testid,'paragraph')]",limit=4)
                    contenido = ""

                    for p in parrafos:
                        p = p.text.strip()
                        contenido = (contenido + " " + p).strip()
                       
                        

                    nueva_entrada = {
                        "Title": titulo,
                        "Url": url,
                        "Content": contenido.replace('"',"'") 
                        }
                    
                    datos_reuters.append(nueva_entrada)
                    
                else:
                    pass
            except Exception as e:
                print(e)
        
    return datos_reuters
# abc ------------------

def abc():
    lock.acquire()
    with SB(undetectable=True,chromium_arg=chrommium_arg,pls='eager',headless=True,block_images=True) as sb:
        sb.maximize_window()

        sb.get("https://www.abc.net.au/news/business")
        lock.release()
        visitados = []
        for x in range(8):
            sb.click('//button[@data-component="PaginationLoadMoreButton"]',timeout=30)
        links = []

        elementos = sb.find_elements(f"//div[@data-component='PaginationList']//time[contains(@datetime,'{fecha}') or contains(@datetime,'{dia}')]/../..//a[@data-component='Link']")
        for e in elementos:
            links.append(e.get_attribute('href'))


        datos_abc = []
        contador = 0
    
        for link in links:
            if contador == 5:
                break
            if link not in visitados:
                contador = contador +1 
                try:
                    visitados.append(link)
                    contenido = ""
                    sb.driver.default_get(link)
                
        
                    time.sleep(1)
                    parrafos = sb.find_elements("//p[@class='paragraph_paragraph__iYReA']",limit=3)
                    for p in parrafos:
                        parrafo = p.text.strip()
                        contenido = (contenido + " " + parrafo).strip()
                    
                        

                    titulo = sb.get_text("//h1[contains(@class,'ArticleHeadline')]",timeout=30)
                    url = link
                
                    nueva_entrada = {
                    "Title": titulo,
                    "Url": url,
                    "Content": contenido.replace('"',"'")
                    }
                    datos_abc.append(nueva_entrada)
                except Exception as e:
                    print(e)
                    sb.save_screenshot('errorfiver_abc.png')
                    input()
    
    return datos_abc

def theaustralian():
    lock.acquire()
    with SB(undetectable=True,pls='eager',block_images=True,headless=True) as sb:
        sb.maximize_window()
        
        # nombre_archivo = 'australian.txt'
        # ruta_completa = os.path.join(ruta_actual, carpeta,nombre_archivo)
        try:
            sb.get("https://www.theaustralian.com.au/business")
            lock.release()
            sb.click("//a[@class='header_log-in']",timeout=25)
            sb.send_keys("//input[@type='email']",'ben.wong@moelisaustralia.com',timeout=25)
            sb.send_keys("//input[@type='password']",'Moelis21!',timeout=25)
            sb.click("//button[@type='submit']",timeout=25)
        
    
            # if os.path.isfile(ruta_completa):
            #     sb.get("https://www.theaustralian.com.au/")
                
            #     sb.load_cookies('australian.txt')
            #     sb.get("https://www.theaustralian.com.au/business")
            # else:
            #     sb.get("https://www.theaustralian.com.au/business")
            #     sb.click("//a[@class='header_log-in']")
            #     sb.send_keys("//input[@type='email']",'ben.wong@moelisaustralia.com')
            #     sb.send_keys("//input[@type='password']",'Moelis21!')
            #     sb.click("//button[@type='submit']")

            
            #     time.sleep(2)
            #     sb.save_cookies("australian.txt")
            time.sleep(6)
            links = []
            elementos = sb.find_elements('//a[contains(@class,"storyblock_title_link")  and (contains(@data-tgev-container,"business-tops")  or contains(@data-tgev-container,"dataroom")  or contains(@data-tgev-container,"spotlight")  or contains(@data-tgev-container,"margin-call")  or contains(@data-tgev-container,"media")  or contains(@data-tgev-container,"wealth")  or contains(@data-tgev-container,"technology")  or contains(@data-tgev-container,"stockhead"))]')
            
            for ele in elementos:
            
                links.append(ele.get_attribute('href'))
        except Exception as e:
            sb.save_screenshot('errorheader.png')
            print(e)

        visitados = []
       
        contador = 0
        datos_australian = []
        for link in links:
            try:

                if contador == 5:
                    break
                contador = contador + 1

                if link not in visitados:
                    visitados.append(link)
                    sb.driver.default_get(link)
                    titulo = sb.get_text("//h1[@id='story-headline']",timeout=30)
                    url = link
                    parrafos = sb.find_elements("//div[@id='story-primary']//p",limit=4)
                    contenido = ""

                    for p in parrafos:
                        parrafo = p.text.strip()
                        contenido = (contenido + " " + parrafo).strip()

                    nueva_entrada = {
                        "Title": titulo,
                        "Url": url,
                        "Content": contenido.replace('"',"'")
                        }
                    
                    datos_australian.append(nueva_entrada)

                
            except Exception as e:
                print(e)
                input()

    return datos_australian

            
with concurrent.futures.ThreadPoolExecutor() as executor:

    futures = []
    results = []

    futures.append(executor.submit(reuters))
    # time.sleep(2)
    futures.append(executor.submit(abc))
    # time.sleep(2)
    futures.append(executor.submit(theaustralian))
    

    print()
    print("(+) Analyzing data...")
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

    datos_combinados = [item for sublist in results for item in sublist]
    
    with open('results_combined.json', 'w', encoding='utf-8') as f:
        json.dump(datos_combinados, f, ensure_ascii=False, indent=4)

    
