"""
Classes base para mapeamento de colunas entre diferentes fontes de dados e Supabase.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import re


class DataType(Enum):
    """Tipos de dados suportados."""
    TEXT = "text"
    INTEGER = "integer"
    FLOAT = "float"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    JSON = "json"
    ARRAY = "array"
    UUID = "uuid"


@dataclass
class ColumnDefinition:
    """Define uma coluna com suas propriedades."""
    name: str
    data_type: DataType
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[Any] = None
    description: Optional[str] = None
    constraints: List[str] = field(default_factory=list)
    transformations: List[str] = field(default_factory=list)
    
    def to_sql_type(self) -> str:
        """Converte o tipo de dados para SQL."""
        type_mapping = {
            DataType.TEXT: "TEXT",
            DataType.INTEGER: "INTEGER",
            DataType.FLOAT: "REAL",
            DataType.DECIMAL: "DECIMAL(15,2)",
            DataType.BOOLEAN: "BOOLEAN",
            DataType.DATE: "DATE",
            DataType.DATETIME: "TIMESTAMP",
            DataType.TIME: "TIME",
            DataType.JSON: "JSONB",
            DataType.ARRAY: "ARRAY",
            DataType.UUID: "UUID"
        }
        return type_mapping.get(self.data_type, "TEXT")


@dataclass
class ColumnMapping:
    """Mapeia uma coluna de origem para destino."""
    source_name: str
    target_name: str
    data_type: DataType
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    validation_rules: List[Dict[str, Any]] = field(default_factory=list)
    default_value: Optional[Any] = None
    skip_if_empty: bool = False
    
    def clean_name(self) -> str:
        """Limpa e normaliza o nome da coluna."""
        # Remove caracteres especiais e espaços
        cleaned = re.sub(r'[^\w\s-]', '', self.target_name)
        # Converte para snake_case
        cleaned = re.sub(r'[-\s]+', '_', cleaned)
        return cleaned.lower()


class TableSchema:
    """Define o esquema de uma tabela."""
    
    def __init__(self, table_name: str, schema_name: str = "public"):
        self.table_name = table_name
        self.schema_name = schema_name
        self.columns: Dict[str, ColumnDefinition] = {}
        self.mappings: Dict[str, ColumnMapping] = {}
        self.indexes: List[Dict[str, Any]] = []
        self.constraints: List[Dict[str, Any]] = []
        
    def add_column(self, column: ColumnDefinition) -> 'TableSchema':
        """Adiciona uma definição de coluna."""
        self.columns[column.name] = column
        return self
        
    def add_mapping(self, mapping: ColumnMapping) -> 'TableSchema':
        """Adiciona um mapeamento de coluna."""
        self.mappings[mapping.source_name] = mapping
        return self
        
    def add_index(self, columns: List[str], unique: bool = False, name: Optional[str] = None) -> 'TableSchema':
        """Adiciona um índice."""
        index_name = name or f"idx_{self.table_name}_{'_'.join(columns)}"
        self.indexes.append({
            "name": index_name,
            "columns": columns,
            "unique": unique
        })
        return self
        
    def generate_create_table_sql(self) -> str:
        """Gera o SQL para criar a tabela."""
        column_defs = []
        
        for col in self.columns.values():
            col_sql = f"{col.name} {col.to_sql_type()}"
            
            if col.primary_key:
                col_sql += " PRIMARY KEY"
            if not col.nullable:
                col_sql += " NOT NULL"
            if col.unique:
                col_sql += " UNIQUE"
            if col.default is not None:
                col_sql += f" DEFAULT {col.default}"
                
            column_defs.append(col_sql)
            
        sql = f"CREATE TABLE IF NOT EXISTS {self.schema_name}.{self.table_name} (\n"
        sql += ",\n".join(f"    {cd}" for cd in column_defs)
        sql += "\n);"
        
        return sql


class ColumnMapper:
    """Classe principal para mapeamento de colunas."""
    
    def __init__(self):
        self.schemas: Dict[str, TableSchema] = {}
        self.global_transformations: List[Dict[str, Any]] = []
        
    def register_schema(self, schema: TableSchema) -> 'ColumnMapper':
        """Registra um esquema de tabela."""
        self.schemas[schema.table_name] = schema
        return self
        
    def add_global_transformation(self, transformation: Dict[str, Any]) -> 'ColumnMapper':
        """Adiciona uma transformação global."""
        self.global_transformations.append(transformation)
        return self
        
    def map_data(self, table_name: str, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia dados de origem para o formato de destino."""
        if table_name not in self.schemas:
            raise ValueError(f"Schema não encontrado para tabela: {table_name}")
            
        schema = self.schemas[table_name]
        mapped_data = {}
        
        for source_col, value in source_data.items():
            if source_col in schema.mappings:
                mapping = schema.mappings[source_col]
                
                # Pular se vazio e configurado para isso
                if mapping.skip_if_empty and not value:
                    continue
                    
                # Aplicar valor padrão se necessário
                if value is None or value == "":
                    value = mapping.default_value
                    
                # Aplicar transformações
                for transform in mapping.transformations:
                    value = self._apply_transformation(value, transform)
                    
                # Mapear para o nome de destino
                target_name = mapping.clean_name()
                mapped_data[target_name] = value
                
        return mapped_data
        
    def _apply_transformation(self, value: Any, transformation: Dict[str, Any]) -> Any:
        """Aplica uma transformação ao valor."""
        transform_type = transformation.get("type")
        
        if transform_type == "uppercase":
            return str(value).upper() if value else value
        elif transform_type == "lowercase":
            return str(value).lower() if value else value
        elif transform_type == "trim":
            return str(value).strip() if value else value
        elif transform_type == "replace":
            pattern = transformation.get("pattern", "")
            replacement = transformation.get("replacement", "")
            return str(value).replace(pattern, replacement) if value else value
        elif transform_type == "regex":
            pattern = transformation.get("pattern", "")
            replacement = transformation.get("replacement", "")
            return re.sub(pattern, replacement, str(value)) if value else value
        elif transform_type == "custom":
            func = transformation.get("function")
            return func(value) if func and callable(func) else value
            
        return value
        
    def validate_mapping(self, table_name: str, source_columns: List[str]) -> Dict[str, Any]:
        """Valida se todas as colunas necessárias estão mapeadas."""
        if table_name not in self.schemas:
            return {"valid": False, "error": f"Schema não encontrado para tabela: {table_name}"}
            
        schema = self.schemas[table_name]
        mapped_sources = set(schema.mappings.keys())
        source_set = set(source_columns)
        
        # Colunas não mapeadas
        unmapped = source_set - mapped_sources
        
        # Colunas obrigatórias sem mapeamento
        required_columns = {
            col.name for col in schema.columns.values() 
            if not col.nullable and col.default is None
        }
        
        mapped_targets = {mapping.target_name for mapping in schema.mappings.values()}
        missing_required = required_columns - mapped_targets
        
        return {
            "valid": len(missing_required) == 0,
            "unmapped_sources": list(unmapped),
            "missing_required": list(missing_required),
            "mapped_count": len(mapped_sources),
            "total_source_columns": len(source_columns)
        }