from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date

def criar_conta(conta: Conta, engine):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco == conta.banco)
        results = session.exec(statement).all()
        
        if results:
            print("ja existe uma conta nesse banco")
            return
        
        session.add(conta)
        session.commit()
        return conta
    
def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
        
    return results

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first()
        
        if not conta:
            return
        
        if conta.valor > 0:
            raise ValueError("Essa conta ainda possui valor.")
        
        conta.status = Status.INATIVO
        
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_saida)
        conta_saida = session.exec(statement).first()
        
        if not conta_saida:
            return
        
        if conta_saida.valor < valor:
            raise ValueError("Saldo insuficiente")
        
        statement = select(Conta).where(Conta.id == id_conta_entrada)
        conta_entrada = session.exec(statement).first()
        
        if not conta_entrada:
            return
        
        conta_saida.valor -= valor
        conta_entrada.valor += valor
        
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == historico.conta_id)
        conta = session.exec(statement).first()
        #TODO: validar se a conta esta ativa
        
        if not conta:
            return
        
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
            
        else:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente")
            
            conta.valor -= historico.valor
        
        session.add(historico)
        session.commit()
        
        return historico

def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        
        total = 0
        for conta in contas:
            total += conta.valor
            
        return float(total)

conta = Conta(valor=10, banco=Bancos.INTER) # type:ignore
criar_conta(conta, engine)

print(listar_contas())

# transferir_saldo(1, 2, 2)

print(total_contas())