from browser import BrowserManager
from monitor import NetworkMonitor


# URL utilizada no desafio
URL = "https://frenqulabi.com/ig/atlas"


def main():

    #Função principal responsável por executar o scraping dinâmico
    browser = BrowserManager(
        headless=True
    )

    # Inicia navegador e retorna objeto Page do Playwright
    page = browser.start()

    # Inicia monitor responsável pela interceptação de requests e responses HTTP

    monitor = NetworkMonitor()

    # Listener responsável por capturar todas as requests da página na navegação
    page.on(
        "request",
        monitor.handle_request
    )

    # Listener responsavel por capturar todas as responses recebidas pela página na navegação
    page.on(
        "response",
        monitor.handle_response
    )

    try:

        print("[*] Criando sessão inicial...")

        # Primeira navegação para criação de sessão, cookies e contexto inicial do domínio
        page.goto(
            "https://frenqulabi.com",
            wait_until="domcontentloaded"
        )

        # Aguarda estabilização inicial da página
        page.wait_for_timeout(3000)

        print("[*] Acessando rota protegida...")

        # Acessa a rota protegida pelo hCaptcha
        page.goto(
            URL,
            wait_until="load"
        )

        # Aguarda carregamento do challenge e assets do captcha
        page.wait_for_timeout(5000)

        print("[*] Título:")
        print(page.title())

        print("[*] Cookies:")

        # Captura cookies da sessão atual
        cookies = page.context.cookies()

        print(cookies)

        # Gera screenshot final da página renderizada
        page.screenshot(
            path="resultado.png",
            full_page=True
        )

        # Salva responses em JSON
        monitor.save()

        print("[*] Finalizado.")

    finally:

        # Finaliza navegador e salva tracing
        browser.close()


# Entrada do programa
if __name__ == "__main__":
    main()