# Importando os módulos necessários
# Flask para criar a API
# Response para criar as respostas HTTP
# request para acessar os dados da requisição
# SQLAlchemy para conectar com o banco de dados
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

# Inicializa a aplicação Flask      
app = Flask('carros')

# Configurações do SQLAlchemy
# Desativa o rastreamento de modificações para economizar recursos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# String de conexão com o banco de dados MySQL
# IMPORTANTE: Adicionado '+pymysql' para especificar o driver de conexão
# Isso resolve o erro 'ModuleNotFoundError: No module named 'MySQLdb''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_carro'

# Inicializa a extensão SQLAlchemy com a aplicação Flask
mydb = SQLAlchemy(app)

# Criando a classe/modelo que representa a tabela no banco de dados
class Carros(mydb.Model):
    __tablename__ = 'tb_carro'
    id_carro = mydb.Column(mydb.Integer, primary_key=True)
    marca = mydb.Column(mydb.String(255))
    modelo = mydb.Column(mydb.String(255))
    # Alterado para Integer para melhor consistência dos dados
    ano = mydb.Column(mydb.Integer)
    cor = mydb.Column(mydb.String(255))
    # Alterado para Float para representar valores monetários
    valor = mydb.Column(mydb.Float)
    # Alterado para Integer para representar uma contagem
    numero_vendas = mydb.Column(mydb.Integer)

    # Método para converter o objeto Carro em um dicionário (formato JSON)
    def to_json(self):
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "cor": self.cor,
            "valor": self.valor,
            "numero_vendas": self.numero_vendas
        }

# --- ROTAS DA API ---

# Rota para selecionar todos os carros (Método GET)
# CORREÇÃO: Adicionada a barra '/' no início da rota
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    # Executa uma consulta no banco de dados (SELECT * FROM tb_carro)
    carros_selecionados = Carros.query.all()
    # Converte a lista de objetos Carro para uma lista de dicionários JSON
    carros_json = [carro.to_json() for carro in carros_selecionados]
    # CORREÇÃO: Retornando a lista de carros em JSON que foi consultada
    return gera_resposta(200, carros_json)  

# metodo 2 - Get (por ID)
@app.route('/carros/<id_carro_pam>', methods=['GET'])
def seleciona_carro_id(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro = id_carro_pam).first()
    #SELECT * FROM tb_carro where id_carro = 5
    carro_json = carro_selecionado.to_json()
    # return gera_resposta(200, carro_json, 'Carro encontrado!')
    return gera_resposta(200, carro_json, 'Carro encontrado!')

# metodo 3 - POST
@app.route('/carros', methods=['POST'])
def criar_carro():
    requisicao = request.get_json()
    
    try: 
        carro = Carros(
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            ano = requisicao['ano'],
            valor = requisicao['valor'],
            cor = requisicao['cor'],
            numero_vendas = requisicao['numero_vendas']
        )
        
        mydb.session.add(carro)
        #adiciona ao banco
        mydb.session.commit()
        #salva
        
        return gera_resposta(201, carro.to_json(), 'criado com sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao Cadastrar!")

# metodo 3 deletar (delete)
@app.route('/carros/<id_carro_pam>', methods=['DELETE'])
def deleta_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()
    
    try:
        mydb.session.delete(carro)      
        mydb.session.commit()
        return gera_resposta(200, carro.to_json(), "deleteado com sucesso")
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao deletar")

# metodo 4 atualizacao
@app.route('/carros/<id_carro_pam>', methods=['PUT'])
def atualiza_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()
    
    requisicao = request.get_json()
    
    try:
        if('marca' in requisicao):
            carro.marca = requisicao['marca']
        if('modelo' in requisicao):
            carro.modelo = requisicao['modelo']
        if('ano' in requisicao):
            carro.ano = requisicao['ano']
        if('valor' in requisicao):
            carro.valor = requisicao['valor']
        if('cor' in requisicao):
            carro.cor = requisicao['cor']
        if('numero_vendas' in requisicao):
            carro.numero_vendas = requisicao['numero_vendas']
            
        mydb.session.add(carro)
        mydb.session.commit()
        
        return gera_resposta(200, carro.to_json(), "carro cadastrado com sucesso")
    
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, {}, "Erro ao atualizar")










# --- FUNÇÕES AUXILIARES ---

# Função para criar a resposta HTTP no formato JSON
def gera_resposta(status, conteudo, mensagem=False):
    # - status: Código HTTP (ex: 200 para OK, 404 para Não Encontrado)
    # - nome_do_conteudo: A chave principal do JSON (ex: "carros")
    # - conteudo: Os dados a serem enviados (ex: a lista de carros)
    # - mensagem: Uma mensagem opcional
    body = {}
    body["Lista de Carro"] = conteudo
    if(mensagem):
        body['mensagem'] = mensagem
    # json.dumps converte o dicionário Python para uma string no formato JSON
    return Response(json.dumps(body), status=status, mimetype='application/json')

# Inicia o servidor da aplicação Flask
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
    


