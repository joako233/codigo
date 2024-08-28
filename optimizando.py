from seleniumbase import SB
import time
from datetime import datetime
import json
import sys
import os


now = datetime.now()
ruta_actual = os.getcwd() 

fecha = now.strftime("%Y-%m-%d")
dia = (int(now.strftime("%d")) -1)


def codigos(ruta_actual):
    #para reuters:

    dia_actual = now.strftime("%d")
    dia_anterior = dia
    datetime_actual = fecha

    with SB(undetectable=True,pls='none',headless=False,block_images=False) as sb:
        sb.maximize_window()
        

        try:
            sb.uc_open_with_reconnect("https://www.reuters.com/account/sign-in/",3)
            
            
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
            sb.get("https://www.reuters.com/business/")
        
            try:
                sb.click("//button[@id='onetrust-reject-all-handler']",timeout=2.3)
            except:
                pass
            #for x in range(13)

            while True:
                try:
                    for x in range(1):
                        sb.click("span:contains('Load more')",timeout=10)
                    break
                except:
                    sb.driver.disconnect()
                    time.sleep(12)
                    sb.driver.connect()
            

            time.sleep(1)
            elementos = sb.find_elements(f"//div[@class='media-story-card__body__3tRWy']//time[contains(text(),'{dia_actual}') or contains(text(),'{dia_anterior}') or contains(@datetime,'{datetime_actual}') or contains(@datetime,'{dia_anterior}')]/ancestor::div[@class='media-story-card__body__3tRWy']//a[@data-testid='Heading' or @class='text__text__1FZLe text__dark-grey__3Ml43 text__inherit-font__1Y8w3 text__inherit-size__1DZJi link__link__3Ji6W link__underline_on_hover__2zGL4 link__inherit-line-height__2qjXx media-story-card__heading__eqhp9']")
        except Exception as e:
            sb.save_screenshot('errore.png')
            print(e)
         
        datos_reuters = []
        links = []


        for ele in elementos:
        
            links.append(ele.get_attribute('href'))
       
      
        visitados = []
        contador = 0
        for link in links:
            try:
                if contador == 1:
                    break
                if link not in visitados:
                    visitados.append(link)
                    sb.get(link)
                 
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
      
        sb.get("https://www.abc.net.au/news/business")
 
        visitados = []
        #for x in range(8)
        for x in range(1):
            sb.click('//button[@data-component="PaginationLoadMoreButton"]',timeout=30)
        links = []
        time.sleep(1)
        elementos = sb.find_elements(f"//div[@data-component='PaginationList']//time[contains(@datetime,'{fecha}') or contains(@datetime,'{dia}')]/../..//a[@data-component='Link']")
        for e in elementos:
            links.append(e.get_attribute('href'))


        datos_abc = []
        contador = 0
    
        for link in links:
            if contador == 1:
                break
            if link not in visitados:
                contador = contador +1 
                try:
                    visitados.append(link)
                    contenido = ""
                    sb.driver.default_get(link)
                
        
                    titulo = sb.get_text("//h1[contains(@class,'ArticleHeadline')]",timeout=30)
                    url = link

                    parrafos = sb.find_elements("//p[@class='paragraph_paragraph__iYReA']",limit=3)
                    for p in parrafos:
                        parrafo = p.text.strip()
                        contenido = (contenido + " " + parrafo).strip()
                    
                
                    nueva_entrada = {
                    "Title": titulo,
                    "Url": url,
                    "Content": contenido.replace('"',"'")
                    }
                    datos_abc.append(nueva_entrada)
                except Exception as e:
                    print(e)
                
                    input()
       
       
        carpeta = 'saved_cookies'
        archivo = 'australian.txt'
        
        completa = os.path.join(ruta_actual,carpeta,archivo)

      
    
        if os.path.isfile(completa):
            sb.uc_open_with_reconnect("https://www.theaustralian.com.au/business",5)
            sb.load_cookies('australian.txt')
            sb.driver.default_get("https://www.theaustralian.com.au/business")
            time.sleep(8)
            sb.save_cookies('australian.txt')
        else:
            sb.get("https://www.theaustralian.com.au/business")
            while True:
                try:
                    sb.click("//a[@class='header_log-in']",timeout=30)
                    break
                except:
                    sb.refresh()
                    continue
            sb.send_keys("//input[@type='email']",'ben.wong@moelisaustralia.com',timeout=30)
            sb.send_keys("//input[@type='password']",'Moelis21!',timeout=30)
            sb.click("//button[@type='submit']",timeout=30)
            time.sleep(8)
         
            sb.save_cookies('australian.txt')

    
        links = []
    
        elementos = sb.find_elements('//a[contains(@class,"storyblock_title_link")  and (contains(@data-tgev-container,"business-tops")  or contains(@data-tgev-container,"dataroom")  or contains(@data-tgev-container,"spotlight")  or contains(@data-tgev-container,"margin-call")  or contains(@data-tgev-container,"media")  or contains(@data-tgev-container,"wealth")  or contains(@data-tgev-container,"technology")  or contains(@data-tgev-container,"stockhead"))]')
       
        for ele in elementos:
        
            links.append(ele.get_attribute('href'))
    
        
        visitados = []
       
        contador = 0
        datos_australian = []
        
        for link in links:
            try:

                if contador == 1:
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
     
    listas_unidas = datos_reuters + datos_australian + datos_abc

    return listas_unidas

term = codigos(ruta_actual)
with open('DATA.json', 'w', encoding='utf-8') as f:
    json.dump(term, f, ensure_ascii=False, indent=4)
