from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import os

app = Flask(__name__)

@app.route("/teste")
def index():
	return 'Olá Mundo!'

# ----------------- Imagem para Texto ------------------------
# Diretório temporário para uploads
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_and_predict():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado!"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado!"}), 400

    try:
        # Salvar o arquivo localmente
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        #Envio para o modelo IA
        client = Client("acsimoes/ai-image")

        result = client.predict(
            param_0=handle_file(filepath), 
            api_name="/predict"
        )

        # Tratando retorno 
        start = result.find("generated_text='") + len("generated_text='")
        end = result.find("'",start)

        generated_text = result[start:end]

        # Retorna o resultado
        #return jsonify({"result": result[start:end]}), 200 -- *Retorno Bruto*

        return jsonify({"generated_text": generated_text}), 200 #Trás somente o texto gerado

    except Exception as e:
        return jsonify({"error": f"Erro ao processar: {str(e)}"}), 500

    finally:
        # Limpa o arquivo salvo temporariamente
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
