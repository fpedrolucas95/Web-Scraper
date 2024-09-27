import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def inicializar():
    options = Options()
    options.headless = False
    options.add_argument("start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def espera_elemento_presente(by, value, driver, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def converter_float(preco_texto):
    try:
        return float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
    except ValueError:
        return None

def atualizar_pagina_url(url_atual, nova_pagina):
    url_parsed = urlparse(url_atual)
    query_params = parse_qs(url_parsed.query)
    query_params['page'] = [str(nova_pagina)]
    nova_query_string = urlencode(query_params, doseq=True)
    
    if not url_parsed.query.startswith('&') and '&' not in url_parsed.query:
        nova_query_string = f"&{nova_query_string}"
    
    nova_url = urlunparse((url_parsed.scheme, url_parsed.netloc, url_parsed.path, url_parsed.params, nova_query_string, url_parsed.fragment))
    
    return nova_url

def produto_ja_existe(nome, link, preco, lista_resultados):
    return any(item['nome'] == nome and item['link'] == link and item['preco_pix'] == preco for item in lista_resultados)

def realizar_pesquisa(palavra_chave, quantidade):
    driver = inicializar()
    driver.get('https://www.casasbahia.com.br/')
    
    resultados = []
    produtos_contados = 0

    barra_de_pesquisa = espera_elemento_presente(By.ID, 'search-form-input', driver)
    barra_de_pesquisa.clear()

    tempo_base = 0.05
    fator_proporcional = len(palavra_chave) * 0.02

    for letra in palavra_chave.strip():
        barra_de_pesquisa.send_keys(letra)
        time.sleep(random.uniform(tempo_base, tempo_base + fator_proporcional))

    barra_de_pesquisa.send_keys(Keys.ENTER)
    time.sleep(random.uniform(3, 5))

    try:
        total_paginas = int(driver.find_element(By.CSS_SELECTOR, 'span[data-testid="paginação-component-total-paginas"]').text.split()[-1])
    except Exception:
        total_paginas = 1

    pagina_atual = 1

    while produtos_contados < quantidade and pagina_atual <= total_paginas:
        time.sleep(random.uniform(3, 6))
        ActionChains(driver).move_by_offset(random.randint(100, 300), random.randint(100, 300)).perform()
        produtos = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card-desktop"]')

        for produto_elemento in produtos:
            if produtos_contados >= quantidade:
                break

            try:
                nome_produto = produto_elemento.find_element(By.TAG_NAME, 'h3').text
                link_produto = produto_elemento.find_element(By.TAG_NAME, 'a').get_attribute('href')
                preco_pix = produto_elemento.find_element(By.CSS_SELECTOR, 'div.product-card__highlight-price').text
                preco_pix_float = converter_float(preco_pix)

                if not produto_ja_existe(nome_produto, link_produto, preco_pix_float, resultados):
                    resultados.append({'nome': nome_produto, 'link': link_produto, 'preco_pix': preco_pix_float})
                    produtos_contados += 1
            except Exception:
                continue

        if produtos_contados < quantidade and pagina_atual < total_paginas:
            try:
                driver.get(atualizar_pagina_url(driver.current_url, pagina_atual + 1))
                pagina_atual += 1
                time.sleep(random.uniform(5, 7))
            except Exception:
                break

    driver.quit()
    return resultados
