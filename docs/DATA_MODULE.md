# Módulo de Tratamento de Dados 📊

## Índice
- [Visão Geral](#visão-geral)
- [Arquitetura do Módulo](#arquitetura-do-módulo)
- [Componentes](#componentes)
- [Como Usar](#como-usar)
- [Exemplos Práticos](#exemplos-práticos)
- [Referência da API](#referência-da-api)
- [Boas Práticas](#boas-práticas)

## Visão Geral

O módulo de tratamento de dados é responsável por todo o pipeline de processamento, desde a importação de arquivos até a gravação no banco de dados. Foi projetado para ser extensível, robusto e fácil de usar.

### Características Principais
- ✅ Suporte a múltiplos formatos (Excel, CSV, JSON)
- ✅ Validação customizável de dados
- ✅ Mapeamento flexível de colunas
- ✅ Conversão inteligente de tipos
- ✅ Tratamento de erros detalhado
- ✅ Logging completo do processamento

## Arquitetura do Módulo

```
src/data/
├── __init__.py           # Exports principais
├── mappers/              # Mapeamento de colunas
│   ├── __init__.py
│   └── base.py          # ColumnMapper, TableSchema
├── validators/           # Validação de dados
│   ├── __init__.py
│   └── base.py          # DataValidator, ValidationRule
├── converters/           # Conversão de tipos
│   ├── __init__.py
│   └── base.py          # TypeConverter
├── processors/           # Pipeline de processamento
│   ├── __init__.py
│   └── base.py          # DataProcessor, ProcessingResult
└── utils/               # Utilitários
    ├── __init__.py
    ├── importer.py      # DataImporter
    └── exporter.py      # DataExporter
```

## Componentes

### 1. ColumnMapper 🗺️

O `ColumnMapper` é responsável por mapear colunas de origem (Excel, CSV) para o formato do banco de dados.

#### Conceitos Principais

**TableSchema**: Define a estrutura de uma tabela
```python
schema = TableSchema("nome_tabela", "schema_name")
```

**ColumnDefinition**: Define uma coluna
```python
column = ColumnDefinition(
    name="id",
    data_type=DataType.INTEGER,
    nullable=False,
    primary_key=True
)
```

**ColumnMapping**: Mapeia origem → destino
```python
mapping = ColumnMapping(
    source_name="Nome Original",
    target_name="nome_limpo",
    data_type=DataType.TEXT,
    transformations=[{"type": "lowercase"}]
)
```

#### Tipos de Dados Suportados
- `TEXT`: Texto
- `INTEGER`: Número inteiro
- `FLOAT`: Número decimal
- `DECIMAL`: Decimal preciso (monetário)
- `BOOLEAN`: Verdadeiro/Falso
- `DATE`: Data
- `DATETIME`: Data e hora
- `JSON`: Objeto JSON
- `ARRAY`: Lista de valores

#### Transformações Disponíveis
- `uppercase`: Converte para maiúsculas
- `lowercase`: Converte para minúsculas
- `trim`: Remove espaços extras
- `replace`: Substitui texto
- `regex`: Substituição com regex
- `custom`: Função personalizada

### 2. DataValidator ✅

O `DataValidator` valida e sanitiza dados antes do processamento.

#### Validações Pré-definidas
- **Texto**: não vazio, tamanho máximo
- **Números**: inteiros, decimais, faixas
- **Datas**: formatos válidos, intervalos
- **Email**: formato correto
- **CPF/CNPJ**: validação completa
- **Monetário**: formato brasileiro

#### Criando Validações Customizadas
```python
validator = DataValidator()

# Adicionar regra customizada
validator.add_rule("meu_tipo", ValidationRule(
    name="regra_customizada",
    validator=lambda x: len(x) > 5,
    error_message="Deve ter mais de 5 caracteres",
    sanitizer=lambda x: x.strip().upper()
))
```

### 3. TypeConverter 🔄

O `TypeConverter` converte dados entre diferentes formatos.

#### Conversões Suportadas
- String → Número (suporta formato brasileiro)
- Excel Date → ISO Date
- Timestamp → DateTime
- Boolean em múltiplos formatos
- Arrays e JSON

#### Exemplo de Uso
```python
converter = TypeConverter()

# Converter valor monetário brasileiro
valor = converter.to_money("R$ 1.234,56")  # Decimal('1234.56')

# Converter data Excel
data = converter.to_date(44562)  # '2022-01-01'

# Converter booleano
ativo = converter.to_boolean("Sim")  # True
```

### 4. DataProcessor 🔧

O `DataProcessor` orquestra todo o pipeline de processamento.

#### Pipeline de Processamento
1. **Limpeza**: Remove dados inválidos
2. **Mapeamento**: Aplica mapeamentos
3. **Validação**: Valida regras
4. **Conversão**: Converte tipos
5. **Exportação**: Grava resultados

#### Recursos
- Logging detalhado
- Tratamento de erros por linha
- Exportação de relatórios
- Processamento em lotes

### 5. DataImporter/Exporter 📥📤

Utilitários para importar e exportar dados.

#### Formatos de Importação
- Excel (.xlsx, .xls)
- CSV (detecção automática de delimitador)
- JSON (objetos ou arrays)

#### Formatos de Exportação
- CSV
- Excel (com formatação)
- JSON
- SQL (com CREATE TABLE)
- Parquet

## Como Usar

### Exemplo Básico

```python
from data import *

# 1. Configurar mapeamento
mapper = ColumnMapper()
schema = TableSchema("vendas")

# Definir colunas
schema.add_column(ColumnDefinition(
    name="id",
    data_type=DataType.INTEGER,
    primary_key=True
))

schema.add_column(ColumnDefinition(
    name="produto",
    data_type=DataType.TEXT,
    nullable=False
))

schema.add_column(ColumnDefinition(
    name="valor",
    data_type=DataType.DECIMAL
))

# Mapear Excel → Banco
schema.add_mapping(ColumnMapping(
    source_name="Nome do Produto",
    target_name="produto",
    data_type=DataType.TEXT
))

schema.add_mapping(ColumnMapping(
    source_name="Preço",
    target_name="valor",
    data_type=DataType.DECIMAL
))

mapper.register_schema(schema)

# 2. Importar dados
importer = DataImporter(mapper=mapper)
result = importer.import_excel("vendas.xlsx", table_name="vendas")

# 3. Verificar resultado
if result.status == ProcessingStatus.COMPLETED:
    print(f"✅ Sucesso! {result.processed_rows} linhas processadas")
else:
    print(f"❌ Erro! {len(result.errors)} erros encontrados")
```

### Exemplo Avançado

```python
# Configuração completa com validações customizadas

# 1. Criar validador customizado
validator = DataValidator()

# Validar unidades específicas
unidades_validas = ["LOJA A", "LOJA B", "LOJA C"]
validator.add_rule("unidade", ValidationRule(
    name="unidade_valida",
    validator=lambda x: x.upper() in unidades_validas,
    error_message=f"Unidade deve ser uma de: {', '.join(unidades_validas)}"
))

# 2. Criar conversor customizado
converter = TypeConverter()

# Registrar conversão especial para SKU
def convert_sku(value):
    # SKU deve ter formato: ABC-12345
    if not value:
        return None
    parts = str(value).split('-')
    if len(parts) == 2:
        return f"{parts[0].upper()}-{parts[1].zfill(5)}"
    return value

converter.register_converter("sku", convert_sku)

# 3. Configurar processador com logging
import logging

logger = logging.getLogger("ImportacaoVendas")
processor = DataProcessor(logger=logger)

# 4. Pipeline completo
importer = DataImporter(
    mapper=mapper,
    validator=validator,
    converter=converter,
    processor=processor
)

# 5. Importar com tratamento de erros
try:
    result = importer.import_excel(
        filepath="vendas_janeiro.xlsx",
        sheet_name="Dados",
        table_name="vendas",
        skiprows=2  # Pular cabeçalho customizado
    )
    
    # Exportar erros se houver
    if result.errors:
        processor.export_errors("erros_importacao.json")
        
    # Exportar dados processados
    if result.output_data is not None:
        exporter = DataExporter()
        exporter.export(
            data=result.output_data,
            filepath="vendas_processadas.csv",
            format="csv"
        )
        
except Exception as e:
    logger.error(f"Erro crítico: {str(e)}")
```

## Exemplos Práticos

### 1. Importar Estornos e Cancelamentos

```python
def importar_estornos():
    # Configurar schema específico
    mapper = ColumnMapper()
    schema = TableSchema("estornos_cancelamento")
    
    # Colunas do banco
    colunas = [
        ("id", DataType.INTEGER, {"primary_key": True}),
        ("unidade", DataType.TEXT, {"nullable": False}),
        ("data", DataType.DATE, {"nullable": False}),
        ("quantidade", DataType.INTEGER, {"default": 0}),
        ("percentual", DataType.DECIMAL, {})
    ]
    
    for nome, tipo, opts in colunas:
        schema.add_column(ColumnDefinition(
            name=nome,
            data_type=tipo,
            **opts
        ))
    
    # Mapeamentos Excel → Banco
    mappings = [
        ("UNIDADE", "unidade", DataType.TEXT, [{"type": "uppercase"}]),
        ("DIA = DATA (A)", "data", DataType.DATE, []),
        ("QUANTIDADE", "quantidade", DataType.INTEGER, []),
        ("PERCENTUAL", "percentual", DataType.DECIMAL, [
            {"type": "custom", "function": lambda x: x * 100 if x < 1 else x}
        ])
    ]
    
    for source, target, dtype, transforms in mappings:
        schema.add_mapping(ColumnMapping(
            source_name=source,
            target_name=target,
            data_type=dtype,
            transformations=transforms
        ))
    
    mapper.register_schema(schema)
    
    # Importar
    importer = DataImporter(mapper=mapper)
    return importer.import_excel(
        "Estornos e Cancelamentos.xlsx",
        table_name="estornos_cancelamento"
    )
```

### 2. Validação de Dados Financeiros

```python
def validar_dados_financeiros():
    validator = DataValidator()
    
    # Validar formato de moeda
    validator.add_rule("valor", ValidationRule(
        name="formato_monetario",
        validator=lambda x: DataValidator()._is_valid_money(x),
        error_message="Formato monetário inválido",
        sanitizer=lambda x: DataValidator()._sanitize_money(x)
    ))
    
    # Validar intervalo de datas
    from datetime import datetime, timedelta
    data_minima = datetime.now() - timedelta(days=365)
    
    validator.add_rule("data_venda", ValidationRule(
        name="data_valida",
        validator=lambda x: datetime.fromisoformat(x) >= data_minima,
        error_message=f"Data deve ser posterior a {data_minima.date()}"
    ))
    
    return validator
```

### 3. Exportação Multi-formato

```python
def exportar_relatorio(dados):
    exporter = DataExporter()
    
    # Exportar para múltiplos formatos
    formatos = {
        "relatorio.xlsx": "excel",
        "relatorio.csv": "csv",
        "relatorio.json": "json",
        "relatorio.sql": "sql"
    }
    
    resultados = {}
    for arquivo, formato in formatos.items():
        if formato == "sql":
            # Configurações específicas para SQL
            resultado = exporter.export(
                data=dados,
                filepath=arquivo,
                format=formato,
                table_name="relatorio_vendas",
                schema="public",
                batch_size=1000
            )
        else:
            resultado = exporter.export(
                data=dados,
                filepath=arquivo,
                format=formato
            )
        resultados[formato] = resultado
    
    return resultados
```

## Referência da API

### ColumnMapper

```python
class ColumnMapper:
    def register_schema(schema: TableSchema) -> ColumnMapper
    def map_data(table_name: str, source_data: Dict) -> Dict
    def validate_mapping(table_name: str, source_columns: List[str]) -> Dict
```

### DataValidator

```python
class DataValidator:
    def add_rule(data_type: str, rule: ValidationRule) -> None
    def validate(value: Any, data_type: str) -> ValidationResult
    def validate_row(row: Dict, schema: Dict) -> Dict[str, ValidationResult]
```

### TypeConverter

```python
class TypeConverter:
    def register_converter(type_name: str, converter: Callable) -> None
    def convert(value: Any, target_type: str, **kwargs) -> Any
    def convert_dataframe(df: DataFrame, type_mapping: Dict) -> DataFrame
```

### DataProcessor

```python
class DataProcessor:
    def add_processing_step(step: Callable, name: str) -> None
    def process(data: Union[DataFrame, List, Dict]) -> ProcessingResult
    def export_errors(filepath: str, format: str = "json") -> None
    def get_summary() -> Dict
```

### DataImporter

```python
class DataImporter:
    def import_excel(filepath: str, sheet_name=0, table_name=None) -> ProcessingResult
    def import_csv(filepath: str, table_name=None, encoding='utf-8') -> ProcessingResult
    def import_json(filepath: str, table_name=None) -> ProcessingResult
    def preview_file(filepath: str, rows=10) -> DataFrame
```

### DataExporter

```python
class DataExporter:
    def export(data: DataFrame, filepath: str, format=None, **kwargs) -> Dict
    def export_multiple(datasets: Dict[str, DataFrame], base_path: str) -> Dict
    def to_buffer(df: DataFrame, format: str) -> BytesIO
```

## Boas Práticas

### 1. Sempre Validar Antes de Processar
```python
# Verificar mapeamento antes de importar
validation = mapper.validate_mapping("tabela", df.columns.tolist())
if not validation["valid"]:
    print(f"Colunas faltando: {validation['missing_required']}")
```

### 2. Use Transações para Importações Grandes
```python
# Processar em lotes
for chunk in pd.read_excel("arquivo.xlsx", chunksize=1000):
    result = importer.import_from_dataframe(chunk, "tabela")
    if result.status == ProcessingStatus.FAILED:
        break
```

### 3. Sempre Trate Erros
```python
try:
    result = importer.import_excel("dados.xlsx")
except Exception as e:
    logger.error(f"Erro na importação: {e}")
    # Notificar usuário ou tentar recuperação
```

### 4. Configure Logging Apropriado
```python
import logging

# Configurar logger específico
logger = logging.getLogger("DataImport")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("import.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

processor = DataProcessor(logger=logger)
```

### 5. Documente Seus Mapeamentos
```python
# SEMPRE documente a origem dos dados
schema.add_mapping(ColumnMapping(
    source_name="VLTOTAL",  # Campo no Excel de vendas
    target_name="valor_total",  # Campo no banco
    data_type=DataType.DECIMAL,
    transformations=[
        {"type": "custom", "function": lambda x: abs(x)}  # Sempre positivo
    ]
))
```

## Troubleshooting

### Problema: Importação lenta
**Solução**: Use processamento em chunks
```python
pd.read_excel("arquivo.xlsx", chunksize=5000)
```

### Problema: Memória insuficiente
**Solução**: Use tipos de dados eficientes
```python
dtypes = {
    'codigo': 'int32',
    'valor': 'float32',
    'ativo': 'bool'
}
df = pd.read_csv("arquivo.csv", dtype=dtypes)
```

### Problema: Codificação incorreta
**Solução**: Detecte encoding automaticamente
```python
import chardet

with open('arquivo.csv', 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']

df = pd.read_csv('arquivo.csv', encoding=encoding)
```

## Próximos Passos

1. Explore os exemplos em `/src/data/examples/`
2. Crie seus próprios mapeamentos
3. Implemente validações específicas do negócio
4. Configure logging detalhado
5. Otimize para seus volumes de dados