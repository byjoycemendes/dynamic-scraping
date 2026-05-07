import os

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


class BrowserManager:

    # Classe responsável por gerenciar a infraestrutura do navegador automatizado.
    def __init__(self, headless=True):

        self.headless = headless

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        print("[*] Iniciando navegador...")

        # Remove arquivos gerados em execuções anteriores
        files_to_remove = [
            "trace.zip",
            "resultado.png",
            "responses.json"
        ]

        for file in files_to_remove:

            if os.path.exists(file):
                os.remove(file)

        # Inicializa engine principal do Playwright
        self.playwright = sync_playwright().start()

        # Inicia navegador Chromium
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        # Cria contexto isolado de navegação simulando usuário real
        self.context = self.browser.new_context(
            viewport={
                "width": 1920,
                "height": 1080
            },
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            java_script_enabled=True,
            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        self.context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """)

        # Cria nova aba de navegação
        self.page = self.context.new_page()

        # Inicializa objeto Stealth
        stealth = Stealth()

        # Compatibilidade entre versões da biblioteca
        if hasattr(stealth, "use_sync"):
            stealth.use_sync(self.page)

        elif hasattr(stealth, "apply_stealth_sync"):
            stealth.apply_stealth_sync(self.page)

        # Inicia tracing do Playwright
        self.context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        # Retorna objeto Page principal
        return self.page

    def close(self):

        # Finaliza tracing e encerra todos os recursos utilizados pelo navegador.
        print("[*] Fechando navegador...")

        # Salva tracing completo da execução
        self.context.tracing.stop(
            path="trace.zip"
        )

        # Fecha navegador
        self.browser.close()

        # Finaliza Playwright
        self.playwright.stop()