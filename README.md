# Conversor de números romanos

Aplicação web em Django para converter numerais romanos e números inteiros positivos.

## Funcionalidades

- Converte numerais romanos canônicos (I a MMMCMXCIX) em números.
- Converte inteiros de 1 a 3999 em numerais romanos.
- Mantém a notação personalizada com ponto para converter cada parte separadamente, por exemplo, `25.25` ↔ `XXV.XXV`. **Isso não é uma representação padrão de frações em números romanos.**
- Valida entradas e devolve respostas JSON com status HTTP apropriados.

## Requisitos

- Python 3.10 ou superior
- pip

## Executar localmente

```bash
git clone https://github.com/GabrielV26/roman-numeral-converter.git
cd roman-numeral-converter
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

No Windows, ative o ambiente virtual com `.venv\\Scripts\\activate`.

Acesse http://127.0.0.1:8000/.

## Configuração

A aplicação aceita estas variáveis de ambiente:

- `DJANGO_SECRET_KEY`: chave secreta Django. Defina uma chave própria fora do controle de versão em qualquer implantação.
- `DJANGO_DEBUG`: use `true` apenas no desenvolvimento local; o padrão é `false`.
- `DJANGO_ALLOWED_HOSTS`: hosts separados por vírgula; o padrão permite localhost e loopback.
- `DJANGO_SESSION_COOKIE_SECURE` e `DJANGO_CSRF_COOKIE_SECURE`: cookies seguros em HTTPS, habilitados por padrão quando `DEBUG=false`.
- `DJANGO_SECURE_SSL_REDIRECT`: redirecionamento HTTPS; habilite somente quando o ambiente de implantação estiver configurado para HTTPS.
- `DJANGO_SECURE_HSTS_SECONDS`: HSTS em segundos. Configure apenas após confirmar que todo o domínio atende HTTPS.

A chave de desenvolvimento padrão não deve ser usada em produção.

## Testes

```bash
python manage.py test
python manage.py check
```

## Limites da conversão

Os numerais romanos padrão não representam zero, números negativos ou valores acima de 3999 nesta aplicação. A notação com ponto é uma convenção específica do projeto, não matemática romana histórica.
