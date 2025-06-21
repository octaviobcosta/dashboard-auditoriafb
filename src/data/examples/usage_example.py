"""
Exemplo de uso do módulo de tratamento de dados.
"""

from data.mappers import ColumnMapper, TableSchema, ColumnDefinition, ColumnMapping, DataType
from data.validators import DataValidator, ValidationRule
from data.converters import TypeConverter
from data.processors import DataProcessor
from data.utils import DataImporter, DataExporter


def example_estornos_cancelamentos():
    """Exemplo de configuração para a tabela estornos_cancelamentos."""
    
    # 1. Criar mapeador de colunas
    mapper = ColumnMapper()
    
    # 2. Definir schema da tabela
    schema = TableSchema("estornos_cancelamento", "public")
    
    # Adicionar definições de colunas
    schema.add_column(ColumnDefinition(
        name="id",
        data_type=DataType.INTEGER,
        nullable=False,
        primary_key=True
    ))
    
    schema.add_column(ColumnDefinition(
        name="unidade",
        data_type=DataType.TEXT,
        nullable=False
    ))
    
    schema.add_column(ColumnDefinition(
        name="squad",
        data_type=DataType.TEXT,
        nullable=False
    ))
    
    schema.add_column(ColumnDefinition(
        name="ano",
        data_type=DataType.INTEGER,
        nullable=False
    ))
    
    schema.add_column(ColumnDefinition(
        name="data",
        data_type=DataType.DATE,
        nullable=False
    ))
    
    schema.add_column(ColumnDefinition(
        name="operacao",
        data_type=DataType.TEXT,
        nullable=False
    ))
    
    schema.add_column(ColumnDefinition(
        name="situacao",
        data_type=DataType.TEXT,
        nullable=True
    ))
    
    schema.add_column(ColumnDefinition(
        name="quantidade",
        data_type=DataType.INTEGER,
        nullable=False,
        default=0
    ))
    
    schema.add_column(ColumnDefinition(
        name="total_atendimentos",
        data_type=DataType.INTEGER,
        nullable=False,
        default=0
    ))
    
    schema.add_column(ColumnDefinition(
        name="percentual",
        data_type=DataType.DECIMAL,
        nullable=True
    ))
    
    # 3. Adicionar mapeamentos de colunas (Excel -> Banco)
    schema.add_mapping(ColumnMapping(
        source_name="UNIDADE",
        target_name="unidade",
        data_type=DataType.TEXT,
        transformations=[
            {"type": "trim"},
            {"type": "uppercase"}
        ]
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="SQUAD",
        target_name="squad",
        data_type=DataType.TEXT,
        transformations=[
            {"type": "trim"},
            {"type": "uppercase"}
        ]
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="ANO",
        target_name="ano",
        data_type=DataType.INTEGER
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="DIA = DATA (A)",
        target_name="data",
        data_type=DataType.DATE
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="OPERAÇÃO",
        target_name="operacao",
        data_type=DataType.TEXT,
        transformations=[
            {"type": "trim"}
        ]
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="SITUAÇÃO",
        target_name="situacao",
        data_type=DataType.TEXT,
        transformations=[
            {"type": "trim"}
        ]
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="QUANTIDADE",
        target_name="quantidade",
        data_type=DataType.INTEGER,
        default_value=0
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="TOTAL DE ATENDIMENTOS",
        target_name="total_atendimentos",
        data_type=DataType.INTEGER,
        default_value=0
    ))
    
    schema.add_mapping(ColumnMapping(
        source_name="PERCENTUAL",
        target_name="percentual",
        data_type=DataType.DECIMAL,
        transformations=[
            {"type": "custom", "function": lambda x: x * 100 if x and x < 1 else x}
        ]
    ))
    
    # 4. Adicionar índices
    schema.add_index(["unidade", "data"])
    schema.add_index(["ano", "data"])
    
    # 5. Registrar schema no mapeador
    mapper.register_schema(schema)
    
    return mapper


def example_import_process():
    """Exemplo completo de importação de dados."""
    
    # Configurar componentes
    mapper = example_estornos_cancelamentos()
    validator = DataValidator()
    converter = TypeConverter()
    processor = DataProcessor()
    
    # Criar importador
    importer = DataImporter(
        mapper=mapper,
        validator=validator,
        converter=converter,
        processor=processor
    )
    
    # Importar arquivo Excel
    result = importer.import_excel(
        filepath="Estornos e Cancelamentos.xlsx",
        sheet_name="Planilha1",
        table_name="estornos_cancelamento"
    )
    
    # Verificar resultado
    if result.status.value == "completed":
        print(f"✅ Importação concluída com sucesso!")
        print(f"   Total de registros: {result.total_rows}")
        print(f"   Registros processados: {result.processed_rows}")
        
        # Exportar para diferentes formatos
        exporter = DataExporter()
        
        # Exportar para CSV
        csv_result = exporter.export(
            data=result.output_data,
            filepath="output/estornos_cancelamentos.csv",
            format="csv",
            encoding="utf-8",
            sep=";"
        )
        
        # Exportar para SQL
        sql_result = exporter.export(
            data=result.output_data,
            filepath="output/estornos_cancelamentos.sql",
            format="sql",
            table_name="estornos_cancelamento",
            schema="public",
            batch_size=1000
        )
        
        print(f"\n📁 Arquivos exportados:")
        print(f"   CSV: {csv_result['filepath']} ({csv_result['rows_exported']} registros)")
        print(f"   SQL: {sql_result['filepath']} ({sql_result['total_batches']} batches)")
        
    else:
        print(f"❌ Erro na importação: {result.status.value}")
        print(f"   Total de erros: {len(result.errors)}")
        
        # Mostrar primeiros erros
        for error in result.errors[:5]:
            print(f"   - Linha {error.row_index}: {error.error_message}")
            
        # Exportar log de erros
        processor.export_errors("output/import_errors.json")


def example_custom_validation():
    """Exemplo de validação customizada."""
    
    validator = DataValidator()
    
    # Adicionar regra customizada para validar unidades
    unidades_validas = [
        "BB CENTRO", "ARCOS", "BRASILIA SHOPPING", "CASA PARK",
        "CONJUNTO NACIONAL", "IGUATEMI", "JK SHOPPING", "LIBERTY MALL",
        "PARK SHOPPING", "PIER 21", "TERRAÇO SHOPPING", "TAGUATINGA SHOPPING",
        "VENANCIO SHOPPING", "PATIO BRASIL"
    ]
    
    validator.add_rule("unidade", ValidationRule(
        name="unidade_valida",
        validator=lambda x: x.upper() in unidades_validas,
        error_message=f"Unidade inválida. Valores aceitos: {', '.join(unidades_validas)}",
        sanitizer=lambda x: x.upper().strip() if x else None
    ))
    
    # Validar percentual entre 0 e 100
    validator.add_rule("percentual", ValidationRule(
        name="percentual_range",
        validator=lambda x: 0 <= float(x) <= 100 if x is not None else True,
        error_message="Percentual deve estar entre 0 e 100"
    ))
    
    return validator


if __name__ == "__main__":
    # Executar exemplo
    print("🚀 Exemplo de uso do módulo de tratamento de dados\n")
    
    # Testar importação
    example_import_process()
    
    # Demonstrar SQL gerado
    mapper = example_estornos_cancelamentos()
    schema = mapper.schemas["estornos_cancelamento"]
    
    print("\n📋 SQL de criação da tabela:")
    print(schema.generate_create_table_sql())