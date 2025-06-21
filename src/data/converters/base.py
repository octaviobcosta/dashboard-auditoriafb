"""
Classes para conversão de tipos de dados entre diferentes formatos.
"""

from typing import Any, Optional, Dict, List, Union, Callable
from datetime import datetime, date, time
from decimal import Decimal, InvalidOperation
import json
import pandas as pd
import numpy as np


class TypeConverter:
    """Conversor de tipos de dados com suporte a múltiplos formatos."""
    
    def __init__(self):
        self.custom_converters: Dict[str, Callable] = {}
        self._init_date_formats()
        
    def _init_date_formats(self):
        """Inicializa formatos de data suportados."""
        self.date_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%d.%m.%Y",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d.%m.%Y %H:%M:%S"
        ]
        
    def register_converter(self, type_name: str, converter: Callable[[Any], Any]):
        """Registra um conversor customizado."""
        self.custom_converters[type_name] = converter
        
    def convert(self, value: Any, target_type: str, **kwargs) -> Any:
        """Converte um valor para o tipo alvo."""
        if value is None:
            return None
            
        # Verifica conversores customizados primeiro
        if target_type in self.custom_converters:
            return self.custom_converters[target_type](value)
            
        # Conversões padrão
        converters = {
            "text": self.to_text,
            "integer": self.to_integer,
            "float": self.to_float,
            "decimal": self.to_decimal,
            "boolean": self.to_boolean,
            "date": self.to_date,
            "datetime": self.to_datetime,
            "time": self.to_time,
            "json": self.to_json,
            "array": self.to_array,
            "money": self.to_money
        }
        
        converter = converters.get(target_type.lower())
        if converter:
            return converter(value, **kwargs)
        else:
            raise ValueError(f"Tipo de conversão não suportado: {target_type}")
            
    def to_text(self, value: Any, **kwargs) -> Optional[str]:
        """Converte para texto."""
        if value is None:
            return None
            
        # Trata arrays e objetos
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False)
            
        # Trata datas
        if isinstance(value, (date, datetime)):
            return value.isoformat()
            
        # Trata decimais
        if isinstance(value, Decimal):
            return str(value)
            
        return str(value)
        
    def to_integer(self, value: Any, **kwargs) -> Optional[int]:
        """Converte para inteiro."""
        if value is None or value == "":
            return None
            
        try:
            # Trata booleanos
            if isinstance(value, bool):
                return 1 if value else 0
                
            # Trata strings
            if isinstance(value, str):
                # Remove espaços e caracteres não numéricos comuns
                cleaned = value.strip().replace(" ", "")
                
                # Trata valores monetários
                if "R$" in cleaned:
                    cleaned = cleaned.replace("R$", "").replace(".", "").replace(",", ".")
                    
                return int(float(cleaned))
                
            # Trata floats e decimais
            if isinstance(value, (float, Decimal)):
                return int(value)
                
            return int(value)
            
        except (ValueError, TypeError, InvalidOperation):
            return None
            
    def to_float(self, value: Any, **kwargs) -> Optional[float]:
        """Converte para float."""
        if value is None or value == "":
            return None
            
        try:
            # Trata strings
            if isinstance(value, str):
                # Remove espaços
                cleaned = value.strip().replace(" ", "")
                
                # Trata formato brasileiro de números
                if "," in cleaned:
                    # Verifica se é formato brasileiro (1.234,56)
                    if "." in cleaned and cleaned.rindex(",") > cleaned.rindex("."):
                        cleaned = cleaned.replace(".", "").replace(",", ".")
                    else:
                        cleaned = cleaned.replace(",", ".")
                        
                # Remove símbolos monetários
                cleaned = cleaned.replace("R$", "").replace("$", "")
                
                return float(cleaned)
                
            return float(value)
            
        except (ValueError, TypeError):
            return None
            
    def to_decimal(self, value: Any, **kwargs) -> Optional[Decimal]:
        """Converte para Decimal."""
        if value is None or value == "":
            return None
            
        try:
            # Usa to_float primeiro para tratar formatações
            float_value = self.to_float(value)
            if float_value is not None:
                return Decimal(str(float_value))
                
            return None
            
        except (ValueError, InvalidOperation):
            return None
            
    def to_boolean(self, value: Any, **kwargs) -> Optional[bool]:
        """Converte para booleano."""
        if value is None:
            return None
            
        # Valores já booleanos
        if isinstance(value, bool):
            return value
            
        # Strings
        if isinstance(value, str):
            value_lower = value.lower().strip()
            
            # Valores verdadeiros
            if value_lower in ["true", "verdadeiro", "sim", "yes", "s", "y", "1", "t", "v"]:
                return True
                
            # Valores falsos
            if value_lower in ["false", "falso", "não", "nao", "no", "n", "0", "f"]:
                return False
                
        # Números
        if isinstance(value, (int, float)):
            return bool(value)
            
        return None
        
    def to_date(self, value: Any, **kwargs) -> Optional[str]:
        """Converte para data (formato ISO)."""
        if value is None or value == "":
            return None
            
        # Já é uma data
        if isinstance(value, date) and not isinstance(value, datetime):
            return value.isoformat()
            
        # É um datetime
        if isinstance(value, datetime):
            return value.date().isoformat()
            
        # É um pandas Timestamp
        if pd and isinstance(value, pd.Timestamp):
            return value.date().isoformat()
            
        # É um numpy datetime64
        if np and isinstance(value, np.datetime64):
            return pd.Timestamp(value).date().isoformat()
            
        # Trata números (possível timestamp ou data Excel)
        if isinstance(value, (int, float)):
            try:
                # Tenta como data Excel
                if value > 25569:  # 01/01/1970 em Excel
                    excel_date = pd.Timestamp('1899-12-30') + pd.Timedelta(days=value)
                    return excel_date.date().isoformat()
                    
                # Tenta como timestamp Unix
                dt = datetime.fromtimestamp(value)
                return dt.date().isoformat()
            except:
                pass
                
        # Trata strings
        if isinstance(value, str):
            value = value.strip()
            
            # Tenta cada formato de data
            for fmt in self.date_formats:
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.date().isoformat()
                except ValueError:
                    continue
                    
        return None
        
    def to_datetime(self, value: Any, **kwargs) -> Optional[str]:
        """Converte para datetime (formato ISO)."""
        if value is None or value == "":
            return None
            
        # Já é um datetime
        if isinstance(value, datetime):
            return value.isoformat()
            
        # É uma data
        if isinstance(value, date):
            dt = datetime.combine(value, time.min)
            return dt.isoformat()
            
        # Usa to_date e adiciona horário mínimo se conseguir
        date_str = self.to_date(value)
        if date_str:
            return f"{date_str}T00:00:00"
            
        return None
        
    def to_time(self, value: Any, **kwargs) -> Optional[str]:
        """Converte para hora (formato ISO)."""
        if value is None or value == "":
            return None
            
        # Já é um time
        if isinstance(value, time):
            return value.isoformat()
            
        # É um datetime
        if isinstance(value, datetime):
            return value.time().isoformat()
            
        # Trata strings
        if isinstance(value, str):
            time_formats = ["%H:%M:%S", "%H:%M", "%H%M%S", "%H%M"]
            
            for fmt in time_formats:
                try:
                    t = datetime.strptime(value.strip(), fmt).time()
                    return t.isoformat()
                except ValueError:
                    continue
                    
        return None
        
    def to_json(self, value: Any, **kwargs) -> Optional[str]:
        """Converte para JSON."""
        if value is None:
            return None
            
        # Já é uma string JSON
        if isinstance(value, str):
            try:
                # Valida se é JSON válido
                json.loads(value)
                return value
            except json.JSONDecodeError:
                # Tenta converter string para JSON
                return json.dumps(value)
                
        # Converte objetos Python para JSON
        try:
            return json.dumps(value, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            return None
            
    def to_array(self, value: Any, **kwargs) -> Optional[List]:
        """Converte para array."""
        if value is None:
            return None
            
        # Já é uma lista
        if isinstance(value, list):
            return value
            
        # É uma tupla ou set
        if isinstance(value, (tuple, set)):
            return list(value)
            
        # É uma string que pode ser JSON
        if isinstance(value, str):
            # Remove espaços extras
            value = value.strip()
            
            # Tenta parsear como JSON
            if value.startswith("[") and value.endswith("]"):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    pass
                    
            # Trata como CSV
            delimiter = kwargs.get("delimiter", ",")
            return [item.strip() for item in value.split(delimiter) if item.strip()]
            
        # Converte item único para lista
        return [value]
        
    def to_money(self, value: Any, **kwargs) -> Optional[Decimal]:
        """Converte para valor monetário (Decimal com 2 casas)."""
        if value is None or value == "":
            return None
            
        try:
            # Usa to_decimal para conversão base
            decimal_value = self.to_decimal(value)
            
            if decimal_value is not None:
                # Arredonda para 2 casas decimais
                return decimal_value.quantize(Decimal('0.01'))
                
            return None
            
        except (ValueError, InvalidOperation):
            return None
            
    def batch_convert(self, values: List[Any], target_type: str, **kwargs) -> List[Any]:
        """Converte uma lista de valores."""
        return [self.convert(value, target_type, **kwargs) for value in values]
        
    def convert_dataframe(self, df: pd.DataFrame, type_mapping: Dict[str, str], **kwargs) -> pd.DataFrame:
        """Converte colunas de um DataFrame para os tipos especificados."""
        df_converted = df.copy()
        
        for column, target_type in type_mapping.items():
            if column in df_converted.columns:
                df_converted[column] = self.batch_convert(
                    df_converted[column].tolist(),
                    target_type,
                    **kwargs
                )
                
        return df_converted