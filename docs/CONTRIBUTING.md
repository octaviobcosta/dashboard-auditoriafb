# Guia de Contribuição 🤝

Obrigado por considerar contribuir para o Dashboard Auditoria FB! Este documento fornece diretrizes para contribuir com o projeto.

## Índice
- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Estrutura de Commits](#estrutura-de-commits)
- [Testes](#testes)
- [Documentação](#documentação)

## Código de Conduta

### Nossos Princípios
- Seja respeitoso e inclusivo
- Aceite feedback construtivo
- Foque no que é melhor para a comunidade
- Demonstre empatia com outros contribuidores

### Comportamentos Inaceitáveis
- Uso de linguagem ou imagens sexualizadas
- Comentários insultuosos/depreciativos
- Ataques pessoais ou políticos
- Assédio público ou privado

## Como Contribuir

### 1. Reportando Bugs 🐛

Antes de criar um bug report:
- Verifique se já não existe uma issue similar
- Teste na versão mais recente
- Colete informações detalhadas

**Template de Bug Report:**
```markdown
## Descrição
Breve descrição do bug.

## Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que está acontecendo.

## Screenshots
Se aplicável, adicione screenshots.

## Ambiente
- OS: [e.g. Windows 11]
- Browser: [e.g. Chrome 120]
- Versão: [e.g. 1.0.0]

## Logs
```
Adicione logs relevantes aqui
```
```

### 2. Sugerindo Melhorias ✨

**Template de Feature Request:**
```markdown
## Problema
Descreva o problema que esta feature resolve.

## Solução Proposta
Descreva como você imagina a solução.

## Alternativas Consideradas
Outras formas de resolver o problema.

## Contexto Adicional
Qualquer contexto extra, mockups, etc.
```

### 3. Submetendo Código 💻

1. **Fork o repositório**
2. **Clone seu fork**
   ```bash
   git clone https://github.com/seu-usuario/dashboard-auditoriafb.git
   cd dashboard-auditoriafb
   ```

3. **Crie uma branch**
   ```bash
   git checkout -b feature/minha-feature
   # ou
   git checkout -b fix/correcao-bug
   ```

4. **Faça suas alterações**
5. **Commit suas mudanças**
6. **Push para seu fork**
7. **Abra um Pull Request**

## Configuração do Ambiente

### Ambiente de Desenvolvimento

```bash
# 1. Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 2. Configurar pre-commit hooks
pre-commit install

# 3. Executar testes
pytest

# 4. Executar linting
flake8 src/
black src/ --check
```

### Ferramentas Recomendadas

- **IDE**: VSCode ou PyCharm
- **Extensões VSCode**:
  - Python
  - Pylance
  - Black Formatter
  - GitLens
- **Ferramentas CLI**:
  - black (formatação)
  - flake8 (linting)
  - pytest (testes)
  - mypy (type checking)

## Padrões de Código

### Python Style Guide

Seguimos PEP 8 com algumas extensões:

```python
# Imports
import os
import sys
from typing import Dict, List, Optional

import pandas as pd
from flask import Flask, request

from src.models import User
from src.utils import process_data


# Classes
class DataProcessor:
    """
    Processa dados para o dashboard.
    
    Attributes:
        config: Configurações do processador
        logger: Logger para registro
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Processa um DataFrame.
        
        Args:
            data: DataFrame de entrada
            
        Returns:
            DataFrame processado
            
        Raises:
            ValueError: Se dados inválidos
        """
        if data.empty:
            raise ValueError("DataFrame vazio")
            
        # Processamento...
        return data


# Funções
def calculate_metrics(
    values: List[float],
    metric_type: str = "mean"
) -> float:
    """Calcula métricas dos valores."""
    if metric_type == "mean":
        return sum(values) / len(values)
    elif metric_type == "sum":
        return sum(values)
    else:
        raise ValueError(f"Tipo inválido: {metric_type}")


# Constantes
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {"xlsx", "xls", "csv", "json"}
DEFAULT_TIMEOUT = 30  # segundos
```

### JavaScript Style Guide

```javascript
// Use const/let, nunca var
const API_URL = '/api/v1';
let userData = null;

// Arrow functions para callbacks
const processData = (data) => {
    return data.map(item => ({
        ...item,
        processed: true
    }));
};

// Async/await ao invés de promises
async function fetchDashboardData() {
    try {
        const response = await fetch(`${API_URL}/dashboard`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        throw error;
    }
}

// Classes ES6
class ChartManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.charts = new Map();
    }
    
    addChart(name, config) {
        const chart = new Chart(config);
        this.charts.set(name, chart);
        return chart;
    }
}
```

### CSS/SCSS Style Guide

```scss
// Variáveis no topo
:root {
    --primary-color: #F1C232;
    --secondary-color: #f9d71c;
    --bg-dark: #0f0f0f;
    --text-primary: #FFFFFF;
}

// BEM naming convention
.dashboard {
    &__header {
        padding: var(--space-lg);
        background: var(--bg-dark);
    }
    
    &__content {
        display: grid;
        gap: var(--space-md);
        
        &--full-width {
            grid-column: 1 / -1;
        }
    }
    
    &__card {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        
        &:hover {
            transform: translateY(-2px);
        }
    }
}

// Utility classes
.u-text-center { text-align: center; }
.u-mt-lg { margin-top: var(--space-lg); }
.u-hidden { display: none; }
```

## Processo de Pull Request

### Antes de Abrir um PR

- [ ] Código segue os padrões do projeto
- [ ] Testes passam localmente
- [ ] Documentação atualizada
- [ ] Commits organizados e com mensagens claras
- [ ] Branch atualizada com main

### Template de PR

```markdown
## Descrição
Breve descrição das mudanças.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Como Testar
1. Passo 1
2. Passo 2
3. Verificar resultado

## Checklist
- [ ] Código segue style guide
- [ ] Self-review realizado
- [ ] Comentários adicionados em código complexo
- [ ] Documentação atualizada
- [ ] Testes adicionados/atualizados
- [ ] Testes passam localmente

## Screenshots (se aplicável)
Adicione screenshots das mudanças visuais.

## Issues Relacionadas
Closes #123
```

### Review Process

1. **Auto-review**: Revise seu próprio código
2. **CI/CD**: Aguarde testes automáticos
3. **Code Review**: Pelo menos 1 aprovação necessária
4. **Merge**: Apenas maintainers podem fazer merge

## Estrutura de Commits

### Formato

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

### Tipos

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Documentação
- **style**: Formatação, sem mudança de código
- **refactor**: Refatoração de código
- **perf**: Melhoria de performance
- **test**: Adição/correção de testes
- **chore**: Tarefas de manutenção

### Exemplos

```bash
feat(auth): adicionar autenticação dois fatores

Implementa autenticação dois fatores usando TOTP.
Usuários podem agora habilitar 2FA nas configurações.

Closes #45

---

fix(upload): corrigir limite de tamanho de arquivo

O limite estava sendo verificado em bytes mas o valor
estava em megabytes, causando rejeição de arquivos válidos.

---

docs(api): atualizar documentação de endpoints

Adiciona exemplos de requisição e resposta para todos
os endpoints da API v2.
```

## Testes

### Estrutura de Testes

```
tests/
├── unit/           # Testes unitários
├── integration/    # Testes de integração
├── e2e/           # Testes end-to-end
├── fixtures/      # Dados de teste
└── conftest.py    # Configurações pytest
```

### Escrevendo Testes

```python
# tests/unit/test_data_processor.py
import pytest
from src.data.processors import DataProcessor

class TestDataProcessor:
    """Testes para DataProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Cria instância do processor."""
        return DataProcessor()
        
    def test_process_empty_data(self, processor):
        """Testa processamento de dados vazios."""
        with pytest.raises(ValueError, match="dados vazios"):
            processor.process([])
            
    def test_process_valid_data(self, processor):
        """Testa processamento de dados válidos."""
        data = [{"id": 1, "value": 100}]
        result = processor.process(data)
        
        assert len(result) == 1
        assert result[0]["processed"] is True
        
    @pytest.mark.parametrize("input_data,expected", [
        ([{"value": "100"}], 100),
        ([{"value": "100.50"}], 100.5),
        ([{"value": "R$ 100,50"}], 100.5),
    ])
    def test_value_conversion(self, processor, input_data, expected):
        """Testa conversão de valores."""
        result = processor.process(input_data)
        assert result[0]["value"] == expected
```

### Executando Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/test_data_processor.py

# Testes com markers
pytest -m "not slow"
```

## Documentação

### Docstrings

```python
def process_file(
    filepath: str,
    encoding: str = "utf-8",
    chunk_size: int = 1000
) -> ProcessingResult:
    """
    Processa um arquivo de dados.
    
    Lê o arquivo especificado, valida os dados e processa
    em chunks para otimizar uso de memória.
    
    Args:
        filepath: Caminho para o arquivo
        encoding: Codificação do arquivo (padrão: utf-8)
        chunk_size: Tamanho do chunk para processamento
        
    Returns:
        ProcessingResult com estatísticas e dados processados
        
    Raises:
        FileNotFoundError: Se arquivo não existe
        ValueError: Se formato inválido
        ProcessingError: Se erro durante processamento
        
    Examples:
        >>> result = process_file("data.csv")
        >>> print(f"Processados: {result.processed_count}")
        Processados: 1000
        
    Note:
        Arquivos grandes são processados em chunks para
        evitar uso excessivo de memória.
    """
```

### Documentação de API

```python
@app.route('/api/v1/indicators/<int:indicator_id>', methods=['GET'])
@login_required
def get_indicator(indicator_id: int):
    """
    Retorna dados de um indicador específico.
    
    ---
    tags:
      - Indicators
    parameters:
      - name: indicator_id
        in: path
        type: integer
        required: true
        description: ID do indicador
      - name: start_date
        in: query
        type: string
        format: date
        description: Data inicial (YYYY-MM-DD)
      - name: end_date
        in: query
        type: string
        format: date
        description: Data final (YYYY-MM-DD)
    responses:
      200:
        description: Dados do indicador
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            data:
              type: array
              items:
                type: object
      404:
        description: Indicador não encontrado
      401:
        description: Não autorizado
    """
```

## Recursos Úteis

### Links
- [PEP 8](https://pep8.org/) - Python Style Guide
- [Flask Best Practices](https://flask.palletsprojects.com/patterns/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

### Ferramentas
- [Black](https://black.readthedocs.io/) - Formatador Python
- [Flake8](https://flake8.pycqa.org/) - Linter Python
- [Pre-commit](https://pre-commit.com/) - Git hooks
- [Pytest](https://pytest.org/) - Framework de testes

### Contato
- Email: octavio@eshows.com.br
- Issues: [GitHub Issues](https://github.com/seu-usuario/dashboard-auditoriafb/issues)

---

Obrigado por contribuir! 🎉