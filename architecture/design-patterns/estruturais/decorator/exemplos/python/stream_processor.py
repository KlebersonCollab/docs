"""
Exemplo prático do padrão Decorator em Python
Sistema de processamento de streams de dados com diferentes transformações
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import json
import gzip
import base64
from datetime import datetime


# Interface base para processamento de streams
class StreamProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass


# Implementação concreta - Processamento básico
class BasicStreamProcessor(StreamProcessor):
    def process(self, data: Any) -> Any:
        print(f"🔄 Processando dados básicos: {type(data).__name__}")
        
        # Simulação de validação básica
        if data is None:
            raise ValueError("Dados não podem ser nulos")
        
        # Simulação de formatação básica
        if isinstance(data, dict):
            data['processed_at'] = datetime.now().isoformat()
            data['version'] = '1.0'
        
        print(f"✅ Dados processados: {len(str(data))} caracteres")
        return data


# Decorator abstrato
class StreamProcessorDecorator(StreamProcessor):
    def __init__(self, processor: StreamProcessor):
        self.processor = processor
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass


# Decorador concreto - Compressão
class CompressionDecorator(StreamProcessorDecorator):
    def __init__(self, processor: StreamProcessor, compression_level: int = 6):
        super().__init__(processor)
        self.compression_level = max(1, min(9, compression_level))  # Clamp entre 1 e 9
    
    def process(self, data: Any) -> Any:
        print(f"🗜️ Comprimindo dados (nível: {self.compression_level})")
        
        # Primeiro processa os dados base
        processed_data = self.processor.process(data)
        
        # Depois comprime
        compressed_data = self._compress(processed_data)
        
        print(f"✅ Dados comprimidos: {len(compressed_data)} bytes")
        return compressed_data
    
    def _compress(self, data: Any) -> bytes:
        # Converte para JSON se necessário
        if not isinstance(data, (str, bytes)):
            data = json.dumps(data, ensure_ascii=False)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Comprime os dados
        compressed = gzip.compress(data, compresslevel=self.compression_level)
        return compressed


# Decorador concreto - Criptografia
class EncryptionDecorator(StreamProcessorDecorator):
    def __init__(self, processor: StreamProcessor, key: str = "default_key"):
        super().__init__(processor)
        self.key = key
    
    def process(self, data: Any) -> Any:
        print(f"🔐 Criptografando dados")
        
        # Primeiro processa os dados base
        processed_data = self.processor.process(data)
        
        # Depois criptografa
        encrypted_data = self._encrypt(processed_data)
        
        print(f"✅ Dados criptografados: {len(encrypted_data)} bytes")
        return encrypted_data
    
    def _encrypt(self, data: Any) -> str:
        # Simulação simples de criptografia (Base64 + chave)
        if isinstance(data, bytes):
            data_str = data.decode('utf-8')
        else:
            data_str = str(data)
        
        # Adiciona a chave aos dados
        encrypted_str = data_str + "|" + self.key
        
        # Codifica em Base64
        encrypted_bytes = base64.b64encode(encrypted_str.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')


# Decorador concreto - Logging
class LoggingDecorator(StreamProcessorDecorator):
    def __init__(self, processor: StreamProcessor, log_level: str = "INFO"):
        super().__init__(processor)
        self.log_level = log_level
    
    def process(self, data: Any) -> Any:
        print(f"📝 Logging dados (nível: {self.log_level})")
        
        # Log de entrada
        self._log_entry(data)
        
        # Processa os dados
        processed_data = self.processor.process(data)
        
        # Log de saída
        self._log_exit(processed_data)
        
        return processed_data
    
    def _log_entry(self, data: Any):
        print(f"   📥 Entrada: {type(data).__name__} - {len(str(data))} caracteres")
    
    def _log_exit(self, data: Any):
        print(f"   📤 Saída: {type(data).__name__} - {len(str(data))} caracteres")


# Decorador concreto - Validação
class ValidationDecorator(StreamProcessorDecorator):
    def __init__(self, processor: StreamProcessor, schema: Dict = None):
        super().__init__(processor)
        self.schema = schema or {}
    
    def process(self, data: Any) -> Any:
        print(f"✅ Validando dados")
        
        # Valida os dados de entrada
        self._validate_input(data)
        
        # Processa os dados
        processed_data = self.processor.process(data)
        
        # Valida os dados de saída
        self._validate_output(processed_data)
        
        return processed_data
    
    def _validate_input(self, data: Any):
        if data is None:
            raise ValueError("Dados de entrada não podem ser nulos")
        
        if isinstance(data, dict) and self.schema:
            for field in self.schema.get('required_fields', []):
                if field not in data:
                    raise ValueError(f"Campo obrigatório ausente: {field}")
        
        print(f"   ✅ Validação de entrada: OK")
    
    def _validate_output(self, data: Any):
        if data is None:
            raise ValueError("Dados de saída não podem ser nulos")
        
        print(f"   ✅ Validação de saída: OK")


# Decorador concreto - Cache
class CacheDecorator(StreamProcessorDecorator):
    def __init__(self, processor: StreamProcessor, cache_size: int = 100):
        super().__init__(processor)
        self.cache_size = cache_size
        self.cache = {}
        self.access_count = {}
    
    def process(self, data: Any) -> Any:
        # Cria uma chave de cache baseada nos dados
        cache_key = self._generate_cache_key(data)
        
        # Verifica se está no cache
        if cache_key in self.cache:
            print(f"💾 Cache hit para chave: {cache_key[:10]}...")
            self.access_count[cache_key] = self.access_count.get(cache_key, 0) + 1
            return self.cache[cache_key]
        
        print(f"🔄 Cache miss - processando dados")
        
        # Processa os dados
        processed_data = self.processor.process(data)
        
        # Adiciona ao cache
        self._add_to_cache(cache_key, processed_data)
        
        return processed_data
    
    def _generate_cache_key(self, data: Any) -> str:
        # Gera uma chave simples baseada no hash dos dados
        return str(hash(str(data)))
    
    def _add_to_cache(self, key: str, data: Any):
        # Remove itens antigos se o cache estiver cheio
        if len(self.cache) >= self.cache_size:
            # Remove o item menos acessado
            least_used_key = min(self.access_count.keys(), 
                               key=lambda k: self.access_count[k])
            del self.cache[least_used_key]
            del self.access_count[least_used_key]
        
        self.cache[key] = data
        self.access_count[key] = 1
        print(f"   💾 Adicionado ao cache: {key[:10]}...")


# Decorador concreto - Rate Limiting
class RateLimitDecorator(StreamProcessorDecorator):
    def __init__(self, processor: StreamProcessor, max_requests: int = 10, time_window: int = 60):
        super().__init__(processor)
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def process(self, data: Any) -> Any:
        current_time = datetime.now()
        
        # Remove requisições antigas
        self.requests = [req_time for req_time in self.requests 
                        if (current_time - req_time).seconds < self.time_window]
        
        # Verifica se excedeu o limite
        if len(self.requests) >= self.max_requests:
            print(f"⏰ Rate limit excedido: {len(self.requests)}/{self.max_requests} requisições")
            raise Exception("Rate limit excedido")
        
        # Adiciona a requisição atual
        self.requests.append(current_time)
        
        print(f"🚦 Rate limit: {len(self.requests)}/{self.max_requests} requisições")
        
        # Processa os dados
        return self.processor.process(data)


def demonstrate_decorator_pattern():
    """Demonstra o padrão Decorator com diferentes cenários"""
    print("🚀 Demonstração do Padrão Decorator - Processamento de Streams\n")
    
    # Dados de exemplo
    sample_data = {
        "user_id": 12345,
        "name": "João Silva",
        "email": "joao@exemplo.com",
        "preferences": ["notifications", "newsletter"]
    }
    
    # Cenário 1: Processamento básico
    print("📊 Cenário 1: Processamento básico")
    processor1 = BasicStreamProcessor()
    result1 = processor1.process(sample_data.copy())
    print(f"Resultado: {type(result1).__name__}\n")
    
    # Cenário 2: Com validação e logging
    print("📊 Cenário 2: Com validação e logging")
    processor2 = LoggingDecorator(
        ValidationDecorator(
            BasicStreamProcessor(),
            {"required_fields": ["user_id", "name", "email"]}
        )
    )
    result2 = processor2.process(sample_data.copy())
    print(f"Resultado: {type(result2).__name__}\n")
    
    # Cenário 3: Com cache e rate limiting
    print("📊 Cenário 3: Com cache e rate limiting")
    processor3 = RateLimitDecorator(
        CacheDecorator(
            BasicStreamProcessor(),
            cache_size=5
        ),
        max_requests=3,
        time_window=60
    )
    
    # Processa o mesmo dado múltiplas vezes para testar o cache
    for i in range(3):
        try:
            result3 = processor3.process(sample_data.copy())
            print(f"Tentativa {i+1}: {type(result3).__name__}")
        except Exception as e:
            print(f"Tentativa {i+1}: Erro - {e}")
    print()
    
    # Cenário 4: Com compressão e criptografia
    print("📊 Cenário 4: Com compressão e criptografia")
    processor4 = EncryptionDecorator(
        CompressionDecorator(
            BasicStreamProcessor(),
            compression_level=9
        ),
        key="minha_chave_secreta"
    )
    result4 = processor4.process(sample_data.copy())
    print(f"Resultado: {type(result4).__name__} - {len(result4)} caracteres\n")
    
    # Cenário 5: Pipeline completo
    print("📊 Cenário 5: Pipeline completo")
    processor5 = RateLimitDecorator(
        CacheDecorator(
            LoggingDecorator(
                ValidationDecorator(
                    EncryptionDecorator(
                        CompressionDecorator(
                            BasicStreamProcessor(),
                            compression_level=6
                        ),
                        key="chave_producao"
                    ),
                    {"required_fields": ["user_id", "name"]}
                )
            ),
            cache_size=10
        ),
        max_requests=5,
        time_window=60
    )
    
    result5 = processor5.process(sample_data.copy())
    print(f"Resultado: {type(result5).__name__} - {len(result5)} caracteres\n")


if __name__ == "__main__":
    demonstrate_decorator_pattern()

