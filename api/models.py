from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

db = SQLAlchemy()

class Agent(db.Model):
    """Modelo de Agente"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    machines = db.relationship('Machine', backref='agent', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'machine_count': len(self.machines)
        }
    
    def __repr__(self):
        return f'<Agent {self.name}>'


class Machine(db.Model):
    """Modelo de Máquina"""
    __tablename__ = 'machines'
    
    SEVERITY_CHOICES = ['High', 'Medium', 'Critical', 'Low', 'Not Reported']
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)  # High, Medium, Critical, Low, Not Reported
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)  # 2024, 2025, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'severity': self.severity,
            'agent_id': self.agent_id,
            'agent_name': self.agent.name if self.agent else None,
            'month': self.month,
            'year': self.year,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Machine {self.name} - {self.severity}>'


class MachineCount(db.Model):
    """Modelo de Contagem de Máquinas (para relatórios otimizados)"""
    __tablename__ = 'machine_counts'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, default=0)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    agent = db.relationship('Agent', backref='machine_counts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'agent_name': self.agent.name if self.agent else None,
            'severity': self.severity,
            'count': self.count,
            'month': self.month,
            'year': self.year,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<MachineCount {self.severity}: {self.count}>'