import json


class NetworkMonitor:

    # Classe responsável por monitorar e registrar requests e responses da página automatizada.

    def __init__(self):

        # Inicializa estrutura de armazenamento das responses capturadas.

        self.responses = []

    def handle_request(self, request):

        print(
            f"[REQUEST] "
            f"{request.method} "
            f"{request.url}"
        )

        try:

            # Captura payloads enviados em requisições POST
            if request.method == "POST":

                print("[POST DATA]")
                print(request.post_data)

        except Exception as e:

            print(f"[ERRO REQUEST] {e}")

    def handle_response(self, response):

        print(
            f"[RESPONSE] "
            f"{response.status} "
            f"{response.url}"
        )

        try:

            print("[HEADERS]")
            print(response.headers)

            # Obtém content-type da response
            content_type = response.headers.get(
                "content-type",
                ""
            )

            # Estrutura base da response armazenada
            response_data = {
                "url": response.url,
                "status": response.status,
                "headers": response.headers
            }

            # Captura responses JSON
            if "application/json" in content_type:

                try:
                    response_data["body"] = response.json()

                except Exception:
                    response_data["body"] = response.text()

            # Captura payloads relacionados ao hCaptcha
            elif "hcaptcha" in response.url:

                try:
                    response_data["body"] = response.text()

                except Exception:
                    response_data["body"] = "binary/octet-stream"

            # Adiciona response capturada à lista
            self.responses.append(response_data)

        except Exception as e:

            print(f"[ERRO RESPONSE] {e}")

    def save(self):

        # Persiste todas as responses capturada sem arquivo JSON
        with open(
            "responses.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.responses,
                f,
                indent=4,
                ensure_ascii=False
            )