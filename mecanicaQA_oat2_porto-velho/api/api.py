
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI()

leituras = Counter(
    "iot_readings_total",
    "Total de leituras IoT",
    ["status"]
)

duracao = Histogram(
    "iot_request_duration_seconds",
    "Tempo de processamento das leituras"
)

@app.post("/readings")
def receber_leitura(dados: dict):
    inicio = time.monotonic()

    try:
        if dados.get("simulate_error"):
            leituras.labels(status="erro").inc()
            return Response(status_code=500)

        leituras.labels(status="sucesso").inc()
        return {"status": "recebido"}

    finally:
        duracao.observe(time.monotonic() - inicio)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
