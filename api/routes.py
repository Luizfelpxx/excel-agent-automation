from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Agent, Machine, MachineCount
from sqlalchemy import func

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ==================== AGENTS ====================

@api_bp.route('/agents', methods=['GET'])
def get_agents():
    """Listar todos os agentes"""
    try:
        agents = Agent.query.all()
        return jsonify([agent.to_dict() for agent in agents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/agents', methods=['POST'])
def create_agent():
    """Criar novo agente"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Nome do agente é obrigatório'}), 400
        
        # Verificar se agente já existe
        existing_agent = Agent.query.filter_by(name=data['name']).first()
        if existing_agent:
            return jsonify({'error': 'Agente com este nome já existe'}), 409
        
        agent = Agent(
            name=data['name'],
            email=data.get('email'),
            status=data.get('status', 'active')
        )
        
        db.session.add(agent)
        db.session.commit()
        
        return jsonify(agent.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Obter agente específico"""
    try:
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agente não encontrado'}), 404
        return jsonify(agent.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/agents/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Atualizar agente"""
    try:
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agente não encontrado'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            agent.name = data['name']
        if 'email' in data:
            agent.email = data['email']
        if 'status' in data:
            agent.status = data['status']
        
        db.session.commit()
        return jsonify(agent.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Deletar agente"""
    try:
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agente não encontrado'}), 404
        
        db.session.delete(agent)
        db.session.commit()
        
        return jsonify({'message': 'Agente deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== MACHINES ====================

@api_bp.route('/machines', methods=['GET'])
def get_machines():
    """Listar todas as máquinas"""
    try:
        machines = Machine.query.all()
        return jsonify([machine.to_dict() for machine in machines]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/machines', methods=['POST'])
def create_machine():
    """Criar nova máquina"""
    try:
        data = request.get_json()
        
        # Validações
        required_fields = ['name', 'severity', 'agent_id', 'month', 'year']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Campos obrigatórios: name, severity, agent_id, month, year'}), 400
        
        # Validar severidade
        if data['severity'] not in Machine.SEVERITY_CHOICES:
            return jsonify({'error': f'Severidade deve ser uma de: {", ".join(Machine.SEVERITY_CHOICES)}'}), 400
        
        # Validar agente existe
        agent = Agent.query.get(data['agent_id'])
        if not agent:
            return jsonify({'error': 'Agente não encontrado'}), 404
        
        machine = Machine(
            name=data['name'],
            severity=data['severity'],
            agent_id=data['agent_id'],
            month=data['month'],
            year=data['year']
        )
        
        db.session.add(machine)
        db.session.commit()
        
        return jsonify(machine.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/machines/<int:machine_id>', methods=['GET'])
def get_machine(machine_id):
    """Obter máquina específica"""
    try:
        machine = Machine.query.get(machine_id)
        if not machine:
            return jsonify({'error': 'Máquina não encontrada'}), 404
        return jsonify(machine.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/machines/<int:machine_id>', methods=['PUT'])
def update_machine(machine_id):
    """Atualizar máquina"""
    try:
        machine = Machine.query.get(machine_id)
        if not machine:
            return jsonify({'error': 'Máquina não encontrada'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            machine.name = data['name']
        if 'severity' in data:
            if data['severity'] not in Machine.SEVERITY_CHOICES:
                return jsonify({'error': f'Severidade deve ser uma de: {", ".join(Machine.SEVERITY_CHOICES)}'}), 400
            machine.severity = data['severity']
        if 'agent_id' in data:
            agent = Agent.query.get(data['agent_id'])
            if not agent:
                return jsonify({'error': 'Agente não encontrado'}), 404
            machine.agent_id = data['agent_id']
        if 'month' in data:
            machine.month = data['month']
        if 'year' in data:
            machine.year = data['year']
        
        db.session.commit()
        return jsonify(machine.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/machines/<int:machine_id>', methods=['DELETE'])
def delete_machine(machine_id):
    """Deletar máquina"""
    try:
        machine = Machine.query.get(machine_id)
        if not machine:
            return jsonify({'error': 'Máquina não encontrada'}), 404
        
        db.session.delete(machine)
        db.session.commit()
        
        return jsonify({'message': 'Máquina deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== RELATÓRIOS ====================

@api_bp.route('/machines/count-by-severity', methods=['GET'])
def get_count_by_severity():
    """Obter contagem de máquinas por severidade"""
    try:
        agent_id = request.args.get('agent_id', type=int)
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        
        query = Machine.query
        
        if agent_id:
            query = query.filter_by(agent_id=agent_id)
        if month:
            query = query.filter_by(month=month)
        if year:
            query = query.filter_by(year=year)
        
        # Contar por severidade
        counts = {}
        for severity in Machine.SEVERITY_CHOICES:
            counts[severity] = query.filter_by(severity=severity).count()
        
        return jsonify({
            'agent_id': agent_id,
            'month': month,
            'year': year,
            'counts': counts,
            'total': sum(counts.values())
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/machines/monthly-report/<int:agent_id>/<int:month>/<int:year>', methods=['GET'])
def get_monthly_report(agent_id, month, year):
    """Obter relatório mensal de máquinas por agente"""
    try:
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agente não encontrado'}), 404
        
        machines = Machine.query.filter_by(
            agent_id=agent_id,
            month=month,
            year=year
        ).all()
        
        # Contar por severidade
        counts = {severity: 0 for severity in Machine.SEVERITY_CHOICES}
        for machine in machines:
            counts[machine.severity] += 1
        
        return jsonify({
            'agent_id': agent_id,
            'agent_name': agent.name,
            'month': month,
            'year': year,
            'machines': [machine.to_dict() for machine in machines],
            'summary': {
                'counts': counts,
                'total': len(machines)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/machines/all-agents-report/<int:month>/<int:year>', methods=['GET'])
def get_all_agents_report(month, year):
    """Obter relatório consolidado de todos os agentes"""
    try:
        agents = Agent.query.all()
        report = []
        
        for agent in agents:
            machines = Machine.query.filter_by(
                agent_id=agent.id,
                month=month,
                year=year
            ).all()
            
            counts = {severity: 0 for severity in Machine.SEVERITY_CHOICES}
            for machine in machines:
                counts[machine.severity] += 1
            
            report.append({
                'agent_id': agent.id,
                'agent_name': agent.name,
                'counts': counts,
                'total': len(machines)
            })
        
        return jsonify({
            'month': month,
            'year': year,
            'report': report,
            'grand_total': sum(item['total'] for item in report)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== HEALTH CHECK ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar saúde da API"""
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200