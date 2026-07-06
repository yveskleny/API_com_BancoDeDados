from flask import Flask, jsonify, request
from models import db, Tarefas

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
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

    nova_tarefa = Tarefas(
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
    query = db.select(Tarefas).order_by(Tarefas.id)
    tarefas = db.session.execute(query).scalars().all()

    tarefas_dict = [tarefa.to_dict() for tarefa in tarefas]
    return jsonify(tarefas_dict), 200


@app.route('/tarefas/<int:id_tarefa>', methods=['GET'])
def listar_tarefa(id_tarefa):

    tarefa = db.session.get(Tarefas, id_tarefa)

    if tarefa is None:
        return jsonify({'erro': f'Tarefa não encontrada'}), 404
    
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

    tarefa = db.session.get(Tarefas, id_tarefa)

    if tarefa is None:
        return jsonify({'erro': f'Tarefa não encontrada'}), 404

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
    
    tarefa = db.session.get(Tarefas, id_tarefa)

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
    tarefa = db.session.get(Tarefas, id_tarefa)
    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({'mensagem': 'Tarefa deletada com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)