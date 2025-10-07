#!/usr/bin/env python3
"""
Exemplo prático do Padrão State em Python
Sistema de documentos com controle de estados
Baseado na transcrição do vídeo sobre padrão State

Este exemplo demonstra como implementar o padrão State
para controlar os estados de um documento (rascunho, moderação, publicado)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TipoUsuario(Enum):
    """Tipos de usuário do sistema"""
    ADMIN = "admin"
    USUARIO = "usuario"


class EstadoDocumento(ABC):
    """Interface que define o contrato para todos os estados de documento"""
    
    @abstractmethod
    def publicar(self, documento: 'Documento', usuario: TipoUsuario) -> None:
        """Publica o documento baseado no tipo de usuário"""
        pass
    
    @abstractmethod
    def aprovar(self, documento: 'Documento') -> None:
        """Aprova o documento (apenas para moderação)"""
        pass
    
    @abstractmethod
    def rejeitar(self, documento: 'Documento') -> None:
        """Rejeita o documento (apenas para moderação)"""
        pass


class Rascunho(EstadoDocumento):
    """Estado inicial - Documento em rascunho"""
    
    def publicar(self, documento: 'Documento', usuario: TipoUsuario) -> None:
        print(f"📝 Publicando documento como {usuario.value}...")
        
        if usuario == TipoUsuario.ADMIN:
            # Admin pode publicar diretamente
            documento.set_estado(Publicado())
            print("✅ Documento publicado diretamente pelo admin")
        else:
            # Usuário comum vai para moderação
            documento.set_estado(Moderacao())
            print("⏳ Documento enviado para moderação")
    
    def aprovar(self, documento: 'Documento') -> None:
        raise ValueError("❌ Documento em rascunho não pode ser aprovado")
    
    def rejeitar(self, documento: 'Documento') -> None:
        raise ValueError("❌ Documento em rascunho não pode ser rejeitado")


class Moderacao(EstadoDocumento):
    """Estado de moderação - Documento aguardando aprovação"""
    
    def publicar(self, documento: 'Documento', usuario: TipoUsuario) -> None:
        raise ValueError("❌ Documento já está em moderação")
    
    def aprovar(self, documento: 'Documento') -> None:
        print("✅ Documento aprovado na moderação")
        documento.set_estado(Publicado())
    
    def rejeitar(self, documento: 'Documento') -> None:
        print("❌ Documento rejeitado na moderação")
        documento.set_estado(Rascunho())


class Publicado(EstadoDocumento):
    """Estado final - Documento publicado"""
    
    def publicar(self, documento: 'Documento', usuario: TipoUsuario) -> None:
        raise ValueError("❌ Documento já foi publicado")
    
    def aprovar(self, documento: 'Documento') -> None:
        raise ValueError("❌ Documento já foi publicado")
    
    def rejeitar(self, documento: 'Documento') -> None:
        raise ValueError("❌ Documento já foi publicado")


class Documento:
    """Classe Documento - Contexto do padrão State"""
    
    def __init__(self, titulo: str, conteudo: str, autor: str):
        self.titulo = titulo
        self.conteudo = conteudo
        self.autor = autor
        self.criado_em = datetime.now()
        self.modificado_em = datetime.now()
        self.historico_estados: List[str] = []
        
        # Sempre inicia como rascunho
        self.estado = Rascunho()
        self.historico_estados.append("Rascunho")
        
        print(f"📄 Documento '{titulo}' criado por {autor}")
        print(f"⏰ Criado em: {self.criado_em.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📊 Estado atual: {self.get_estado_atual()}\n")
    
    def publicar(self, usuario: TipoUsuario) -> None:
        """Delega a operação para o estado atual"""
        try:
            self.estado.publicar(self, usuario)
            self.modificado_em = datetime.now()
            self.historico_estados.append(self.get_estado_atual())
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def aprovar(self) -> None:
        """Delega a operação para o estado atual"""
        try:
            self.estado.aprovar(self)
            self.modificado_em = datetime.now()
            self.historico_estados.append(self.get_estado_atual())
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def rejeitar(self) -> None:
        """Delega a operação para o estado atual"""
        try:
            self.estado.rejeitar(self)
            self.modificado_em = datetime.now()
            self.historico_estados.append(self.get_estado_atual())
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def set_estado(self, estado: EstadoDocumento) -> None:
        """Permite que os estados alterem o estado do documento"""
        self.estado = estado
        print(f"🔄 Estado alterado para: {self.get_estado_atual()}")
    
    def get_estado_atual(self) -> str:
        """Retorna o nome do estado atual"""
        return self.estado.__class__.__name__
    
    def pode_editar(self) -> bool:
        """Verifica se o documento pode ser editado"""
        return isinstance(self.estado, Rascunho)
    
    def pode_publicar(self) -> bool:
        """Verifica se o documento pode ser publicado"""
        return isinstance(self.estado, (Rascunho, Moderacao))
    
    def get_info(self) -> dict:
        """Retorna informações do documento"""
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'estado': self.get_estado_atual(),
            'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'modificado_em': self.modificado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'historico': self.historico_estados
        }


def demonstrar_fluxo_admin():
    """Demonstra o fluxo de publicação por um admin"""
    print("=== FLUXO DE PUBLICAÇÃO POR ADMIN ===")
    
    documento = Documento(
        "Guia de Python", 
        "Este é um guia completo sobre Python...", 
        "João Silva"
    )
    
    # Admin publica diretamente
    documento.publicar(TipoUsuario.ADMIN)
    
    # Tentativa de publicar novamente
    documento.publicar(TipoUsuario.ADMIN)
    
    print(f"📊 Informações finais: {documento.get_info()}\n")


def demonstrar_fluxo_usuario():
    """Demonstra o fluxo de publicação por um usuário comum"""
    print("=== FLUXO DE PUBLICAÇÃO POR USUÁRIO ===")
    
    documento = Documento(
        "Tutorial de Django", 
        "Aprenda Django do zero...", 
        "Maria Santos"
    )
    
    # Usuário publica (vai para moderação)
    documento.publicar(TipoUsuario.USUARIO)
    
    # Admin aprova na moderação
    documento.aprovar()
    
    # Tentativa de publicar novamente
    documento.publicar(TipoUsuario.USUARIO)
    
    print(f"📊 Informações finais: {documento.get_info()}\n")


def demonstrar_fluxo_rejeicao():
    """Demonstra o fluxo de rejeição na moderação"""
    print("=== FLUXO DE REJEIÇÃO NA MODERAÇÃO ===")
    
    documento = Documento(
        "Artigo Polêmico", 
        "Conteúdo controverso...", 
        "Pedro Costa"
    )
    
    # Usuário publica (vai para moderação)
    documento.publicar(TipoUsuario.USUARIO)
    
    # Admin rejeita na moderação
    documento.rejeitar()
    
    # Agora pode publicar novamente
    documento.publicar(TipoUsuario.USUARIO)
    
    print(f"📊 Informações finais: {documento.get_info()}\n")


def demonstrar_violacoes():
    """Demonstra tentativas de violar as regras"""
    print("=== TENTATIVAS DE VIOLAR REGRAS ===")
    
    documento = Documento(
        "Documento Teste", 
        "Conteúdo de teste...", 
        "Ana Lima"
    )
    
    # Tentativa de aprovar documento em rascunho
    documento.aprovar()
    
    # Tentativa de rejeitar documento em rascunho
    documento.rejeitar()
    
    # Publicar como admin (vai direto para publicado)
    documento.publicar(TipoUsuario.ADMIN)
    
    # Tentativa de aprovar documento já publicado
    documento.aprovar()
    
    print(f"📊 Informações finais: {documento.get_info()}\n")


def main():
    """Função principal que executa todas as demonstrações"""
    print("🎯 DEMONSTRAÇÃO DO PADRÃO STATE EM PYTHON")
    print("Sistema de Documentos com Controle de Estados\n")
    
    demonstrar_fluxo_admin()
    demonstrar_fluxo_usuario()
    demonstrar_fluxo_rejeicao()
    demonstrar_violacoes()
    
    print("=== DEMONSTRAÇÃO CONCLUÍDA ===")
    print("✅ O padrão State garante que as regras de negócio sejam respeitadas!")
    print("✅ Cada estado controla suas próprias transições!")
    print("✅ Impossível violar as regras de transição!")


if __name__ == "__main__":
    main()




