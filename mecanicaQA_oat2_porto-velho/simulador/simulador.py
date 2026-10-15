import argparse
import concurrent.futures
import json
import random
import time
import urllib.error
import urllib.request
 
def enviar(url, fim, erro):
    contagens = {}
    while time.monotonic() < fim:
        dados = {
            'sensor_id': f'oficina-{random.randint(1,200)}',
            'temperature_c': round(random.uniform(65, 110), 1),
            'electrical_fault': random.random() < .05,
            'simulate_error': random.random() < erro,
        }
        req = urllib.request.Request(url.rstrip('/') + '/readings',
                data=json.dumps(dados).encode(),
                headers={'Content-Type':'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                codigo = resp.status
        except urllib.error.HTTPError as ex:
            codigo = ex.code
        except Exception:
            codigo = 0
        contagens[codigo] = contagens.get(codigo, 0) + 1
    return contagens
 
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url', default='http://localhost:8000')
    p.add_argument('--seconds', type=int, default=30)
    p.add_argument('--workers', type=int, default=4)
    p.add_argument('--error-rate', type=float, default=0.0)
    a = p.parse_args()
    if not (1 <= a.seconds <= 600 and 1 <= a.workers <= 100 and 0 <= a.error_rate <= 1):
        p.error('seconds deve ser 1..600, workers 1..100 e error-rate 0..1')
    fim = time.monotonic() + a.seconds
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        resultados = list(pool.map(lambda _: enviar(a.url, fim, a.error_rate), range(a.workers)))
    totais = {}
    for r in resultados:
        for k,v in r.items():
            totais[k] = totais.get(k,0) + v
    print('HTTP status => quantidade:', totais)
 
if __name__ == '__main__':
    main()