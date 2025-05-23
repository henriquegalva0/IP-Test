from flask import Flask, request, render_template_string
import requests

# Definir web app em flask
app = Flask(__name__)

# HTML importado direto no arquivo python para evitar criar outro arquivo pra enviar no sigaa
PAGINA_EM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Previsão do Tempo</title>
</head>
<body>
    <h1>Digite o nome da cidade:</h1>
    <form method="post">
        <input type="text" name="cidadeinputada" required>
        <input type="submit" value="Buscar">
    </form>

    {% if dados %}
        <h3>Resultado:</h3>
        <ul>
            <li><strong>Cidade:</strong> {{ dados.cida }}</li>
            <li><strong>Temperatura:</strong> {{ dados.temp }}°C</li>
            <li><strong>Descrição:</strong> {{ dados.desc }}</li>
            <li><strong>Condição:</strong> {{ dados.cond }}</li>
            <li><strong>Data e hora:</strong> {{ dados.datahora }}</li>
        </ul>
    {% endif %}
</body>
</html>
"""

# Definindo rota em flask com métodos get e post para inputar os valores dentro do site
@app.route('/', methods=["GET", "POST"])
def main():

    # Definir variável que vai pro site
    dados = None

    # Se eu clicar no botão buscar, ele começa essa função
    if request.method == 'POST':
        cidade = request.form.get('cidadeinputada')

        # Pega a chave API e a cidade e pesquisa
        API_KEY = 'e784e2b5'
        url = f'https://api.hgbrasil.com/weather?key={API_KEY}&city_name={cidade}'
        response = requests.get(url)
        resultado = response.json().get('results', {})

        # Imprime o resultado organizado em uma listinha organizada
        if resultado:
            dados = type('obj', (object,), {
                'cida': resultado.get('city_name'),
                'temp': resultado.get('temp'),
                'desc': resultado.get('description'),
                'cond': resultado.get('condition_slug'),
                'datahora': f"{resultado.get('date')} {resultado.get('time')}"
            })()

    # Imprime o html com os valores em python (dados)
    return render_template_string(PAGINA_EM_HTML, dados=dados)

if __name__ == "__main__":
    app.run()
