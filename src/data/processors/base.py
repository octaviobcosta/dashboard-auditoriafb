"""
Classes para processamento de dados com logging e tratamento de erros.
"""

from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json
import traceback
from enum import Enum
import pandas as pd


class ProcessingStatus(Enum):
    """Status do processamento."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class ProcessingError:
    """Representa um erro durante o processamento."""
    row_index: Optional[int]
    column: Optional[str]
    error_type: str
    error_message: str
    raw_value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    stack_trace: Optional[str] = None


@dataclass
class ProcessingResult:
    """Resultado do processamento de dados."""
    status: ProcessingStatus
    total_rows: int
    processed_rows: int
    failed_rows: int
    errors: List[ProcessingError]
    warnings: List[str]
    processing_time: float
    output_data: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataProcessor:
    """Processador de dados com logging e tratamento de erros."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or self._setup_default_logger()
        self.errors: List[ProcessingError] = []
        self.warnings: List[str] = []
        self.processing_steps: List[Callable] = []
        
    def _setup_default_logger(self) -> logging.Logger:
        """Configura logger padrão."""
        logger = logging.getLogger("DataProcessor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def add_processing_step(self, step: Callable, name: Optional[str] = None):
        """Adiciona uma etapa de processamento."""
        step_wrapper = {
            "function": step,
            "name": name or step.__name__
        }
        self.processing_steps.append(step_wrapper)
        self.logger.info(f"Etapa de processamento adicionada: {step_wrapper['name']}")
        
    def process(self, data: Union[pd.DataFrame, List[Dict], Dict]) -> ProcessingResult:
        """Processa os dados através de todas as etapas configuradas."""
        start_time = datetime.now()
        self.errors = []
        self.warnings = []
        
        # Determina o tipo de dados e total de linhas
        if isinstance(data, pd.DataFrame):
            total_rows = len(data)
            current_data = data.copy()
        elif isinstance(data, list):
            total_rows = len(data)
            current_data = data.copy()
        else:
            total_rows = 1
            current_data = data
            
        processed_rows = 0
        failed_rows = 0
        
        self.logger.info(f"Iniciando processamento de {total_rows} registros")
        
        try:
            # Executa cada etapa de processamento
            for step_info in self.processing_steps:
                step_name = step_info["name"]
                step_func = step_info["function"]
                
                self.logger.info(f"Executando etapa: {step_name}")
                
                try:
                    current_data = step_func(current_data)
                    
                    # Atualiza contagem após cada etapa
                    if isinstance(current_data, pd.DataFrame):
                        processed_rows = len(current_data)
                    elif isinstance(current_data, list):
                        processed_rows = len(current_data)
                    else:
                        processed_rows = 1
                        
                except Exception as e:
                    error_msg = f"Erro na etapa {step_name}: {str(e)}"
                    self.logger.error(error_msg)
                    
                    self.errors.append(ProcessingError(
                        row_index=None,
                        column=None,
                        error_type="ProcessingStepError",
                        error_message=error_msg,
                        raw_value=None,
                        stack_trace=traceback.format_exc()
                    ))
                    
                    # Decide se continua ou para o processamento
                    if self._should_stop_on_error():
                        raise
                        
            # Calcula estatísticas finais
            failed_rows = total_rows - processed_rows
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Determina status
            if len(self.errors) == 0:
                status = ProcessingStatus.COMPLETED
            elif processed_rows == 0:
                status = ProcessingStatus.FAILED
            else:
                status = ProcessingStatus.PARTIAL
                
            self.logger.info(
                f"Processamento concluído: {processed_rows}/{total_rows} registros processados"
            )
            
            return ProcessingResult(
                status=status,
                total_rows=total_rows,
                processed_rows=processed_rows,
                failed_rows=failed_rows,
                errors=self.errors,
                warnings=self.warnings,
                processing_time=processing_time,
                output_data=current_data,
                metadata={
                    "start_time": start_time.isoformat(),
                    "end_time": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Erro crítico no processamento: {str(e)}")
            
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                total_rows=total_rows,
                processed_rows=processed_rows,
                failed_rows=total_rows - processed_rows,
                errors=self.errors,
                warnings=self.warnings,
                processing_time=(datetime.now() - start_time).total_seconds(),
                output_data=None,
                metadata={
                    "start_time": start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "critical_error": str(e)
                }
            )
            
    def process_row(self, row: Dict[str, Any], row_index: int) -> Optional[Dict[str, Any]]:
        """Processa uma única linha de dados."""
        try:
            processed_row = row.copy()
            
            for step_info in self.processing_steps:
                step_name = step_info["name"]
                step_func = step_info["function"]
                
                try:
                    processed_row = step_func(processed_row)
                except Exception as e:
                    self._handle_row_error(row_index, None, step_name, str(e), row)
                    
                    if self._should_stop_on_error():
                        return None
                        
            return processed_row
            
        except Exception as e:
            self._handle_row_error(row_index, None, "process_row", str(e), row)
            return None
            
    def validate_schema(self, data: pd.DataFrame, expected_schema: Dict[str, type]) -> bool:
        """Valida se o DataFrame corresponde ao schema esperado."""
        self.logger.info("Validando schema dos dados")
        
        # Verifica colunas faltando
        missing_columns = set(expected_schema.keys()) - set(data.columns)
        if missing_columns:
            error_msg = f"Colunas faltando: {missing_columns}"
            self.logger.error(error_msg)
            self.errors.append(ProcessingError(
                row_index=None,
                column=None,
                error_type="SchemaValidationError",
                error_message=error_msg,
                raw_value=None
            ))
            return False
            
        # Verifica tipos de dados
        for column, expected_type in expected_schema.items():
            if column in data.columns:
                actual_type = data[column].dtype
                
                # Mapeia tipos pandas para tipos Python
                type_mapping = {
                    'int64': int,
                    'float64': float,
                    'object': str,
                    'bool': bool,
                    'datetime64[ns]': datetime
                }
                
                mapped_type = type_mapping.get(str(actual_type), object)
                
                if not issubclass(mapped_type, expected_type):
                    warning_msg = f"Tipo incompatível na coluna {column}: esperado {expected_type}, encontrado {mapped_type}"
                    self.logger.warning(warning_msg)
                    self.warnings.append(warning_msg)
                    
        return len(self.errors) == 0
        
    def _handle_row_error(self, row_index: int, column: Optional[str], 
                         operation: str, error_msg: str, raw_value: Any):
        """Trata erro em uma linha específica."""
        error = ProcessingError(
            row_index=row_index,
            column=column,
            error_type=f"{operation}Error",
            error_message=error_msg,
            raw_value=raw_value,
            stack_trace=traceback.format_exc()
        )
        
        self.errors.append(error)
        self.logger.error(
            f"Erro na linha {row_index}"
            f"{f', coluna {column}' if column else ''}: {error_msg}"
        )
        
    def _should_stop_on_error(self) -> bool:
        """Determina se deve parar o processamento em caso de erro."""
        # Por padrão, continua processamento
        # Pode ser configurado para parar após N erros
        max_errors = getattr(self, 'max_errors', float('inf'))
        return len(self.errors) >= max_errors
        
    def export_errors(self, filepath: str, format: str = "json"):
        """Exporta erros para arquivo."""
        if format == "json":
            errors_data = [
                {
                    "row_index": e.row_index,
                    "column": e.column,
                    "error_type": e.error_type,
                    "error_message": e.error_message,
                    "raw_value": str(e.raw_value),
                    "timestamp": e.timestamp.isoformat()
                }
                for e in self.errors
            ]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(errors_data, f, ensure_ascii=False, indent=2)
                
        elif format == "csv":
            import csv
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "row_index", "column", "error_type", 
                    "error_message", "raw_value", "timestamp"
                ])
                
                for e in self.errors:
                    writer.writerow([
                        e.row_index, e.column, e.error_type,
                        e.error_message, str(e.raw_value), 
                        e.timestamp.isoformat()
                    ])
                    
        self.logger.info(f"Erros exportados para: {filepath}")
        
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo do processamento."""
        error_types = {}
        for error in self.errors:
            error_types[error.error_type] = error_types.get(error.error_type, 0) + 1
            
        return {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "error_types": error_types,
            "errors_by_column": self._group_errors_by_column(),
            "sample_errors": [
                {
                    "row": e.row_index,
                    "column": e.column,
                    "message": e.error_message
                }
                for e in self.errors[:5]  # Primeiros 5 erros
            ]
        }
        
    def _group_errors_by_column(self) -> Dict[str, int]:
        """Agrupa erros por coluna."""
        errors_by_column = {}
        for error in self.errors:
            if error.column:
                errors_by_column[error.column] = errors_by_column.get(error.column, 0) + 1
        return errors_by_column