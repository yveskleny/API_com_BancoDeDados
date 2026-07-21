from flask import Flask, jsonify, request
from models import db, Tarefa, Aluno
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'mensagem': 'API com Banco de Dados funcionando!'
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok'
    }), 200


@app.route('/tarefas', methods=['POST'])
def criar_tarefas():
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Nenhum dado fornecido'}), 400

    campos_obrigatorios = ['titulo', 'descricao']
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({'erro': f'Campo obrigatório ausente: {campo}'}), 400

    nova_tarefa = Tarefa(
        titulo=data['titulo'],
        descricao=data['descricao'],
        concluida=data.get('concluida', False)
    )

    db.session.add(nova_tarefa)
    db.session.commit()
    db.session.refresh(nova_tarefa)

    return jsonify(nova_tarefa.to_dict()), 201


@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    query = db.select(Tarefa).order_by(Tarefa.id)
    tarefas = db.session.execute(query).scalars().all()

    tarefas_dict = [tarefa.to_dict() for tarefa in tarefas]
    return jsonify(tarefas_dict), 200


@app.route('/tarefas/<int:id_tarefa>', methods=['GET'])
def listar_tarefa(id_tarefa):

    tarefa = db.session.get(Tarefa, id_tarefa)

    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    return jsonify(tarefa.to_dict()), 200


@app.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
def atualizar_tarefa(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado foi enviado'}), 400
    
    campos_obrigatorios = ['titulo', 'descricao', 'concluida']

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro': f'Campo {campo} é obrigatório!'}), 400

    tarefa = db.session.get(Tarefa, id_tarefa)

    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    tarefa.titulo = dados['titulo']
    tarefa.descricao = dados['descricao']
    tarefa.concluida = dados['concluida']

    db.session.commit()

    return jsonify(tarefa.to_dict()), 201



@app.route('/tarefas/<int:id_tarefa>', methods=['PATCH'])
def alterar_tarefa(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado foi enviado'}), 400
    
    tarefa = db.session.get(Tarefa, id_tarefa)

    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    if 'titulo' in dados:
        tarefa.titulo = dados['titulo']
    if 'descricao' in dados:
        tarefa.descricao = dados['descricao']
    if 'concluida' in dados:
        tarefa.concluida = dados['concluida']


    db.session.commit()

    return jsonify(tarefa.to_dict()), 200


@app.route('/tarefas/<int:id_tarefa>', methods=["DELETE"])
def deletar_tarefa(id_tarefa):
    tarefa = db.session.get(Tarefa, id_tarefa)
    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({'mensagem': 'Tarefa deletada com sucesso'}), 200


@app.route('/alunos', methods=['GET'])
def listar_alunos():
    query = db.select(Aluno).order_by(Aluno.nome)
    alunos = db.session.execute(query).scalars().all()

    alunos_dict = [aluno.to_dict() for aluno in alunos]
    return jsonify(alunos_dict), 200


@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Nenhum dado fornecido'}), 400
    
    campos_obrigatorios = ['nome', 'curso']

    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
    novo_aluno = Aluno(
        nome = data['nome'],
        curso = data['curso']
    )
    
    db.session.add(novo_aluno)
    db.session.commit()
    db.session.refresh(novo_aluno)

    return jsonify(novo_aluno.to_dict()), 201


@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def listar_aluno(id_aluno):
    
    aluno = db.session.get(Aluno, id_aluno)

    if aluno is None:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

    return jsonify(aluno.to_dict()), 200


@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhuma dado foi enviado'}), 400
    
    campos_obrigatorios = ['nome', 'curso']

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro': 'Campo {campo} obrigatório!'}), 400
        
    aluno = db.session.get(Aluno, id_aluno)

    if aluno is None:
        return jsonify({'erro': 'Aluno não encontrado!'}), 400
    
    aluno.nome = dados['nome']
    aluno.curso = dados['curso']

    db.session.commit()

    return jsonify(aluno.to_dict()), 201


@app.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def alterar_aluno(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado foi enviado'}), 400
    
    aluno = db.session.get(Aluno, id_aluno)

    if aluno is None:
        return jsonify({'erro': 'Aluno não encontrado!'}), 404
    
    if 'nome' in dados:
        aluno.nome = dados['nome']
    if 'curso' in dados:
        aluno.curso = dados['curso']

    db.session.commit()

    return jsonify(aluno.to_dict()), 200


@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def apagar_aluno(id_aluno):

    aluno = db.session.get(Aluno, id_aluno)

    if aluno is None:
        return jsonify({'erro': 'Aluno não encontrado!'}), 404
    
    db.session.delete(aluno)
    db.session.commit()

    return jsonify({'mensagem': 'Aluno deletado com sucesso'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)