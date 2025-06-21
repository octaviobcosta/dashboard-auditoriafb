"""
Classes para validação e sanitização de dados.
"""

from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass
from datetime import datetime, date
import re
from decimal import Decimal, InvalidOperation


@dataclass
class ValidationRule:
    """Define uma regra de validação."""
    name: str
    validator: Callable[[Any], bool]
    error_message: str
    sanitizer: Optional[Callable[[Any], Any]] = None


@dataclass
class ValidationResult:
    """Resultado de uma validação."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_value: Any
    

class DataValidator:
    """Validador de dados com regras customizáveis."""
    
    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = {}
        self._init_default_rules()
        
    def _init_default_rules(self):
        """Inicializa regras de validação padrão."""
        # Regras para texto
        self.add_rule("text", ValidationRule(
            name="not_empty",
            validator=lambda x: x is not None and str(x).strip() != "",
            error_message="Valor não pode estar vazio",
            sanitizer=lambda x: str(x).strip() if x is not None else ""
        ))
        
        self.add_rule("text", ValidationRule(
            name="max_length",
            validator=lambda x, max_len=255: len(str(x)) <= max_len if x else True,
            error_message="Texto excede o tamanho máximo permitido"
        ))
        
        # Regras para números
        self.add_rule("integer", ValidationRule(
            name="is_integer",
            validator=lambda x: isinstance(x, int) or (isinstance(x, str) and x.isdigit()),
            error_message="Valor deve ser um número inteiro",
            sanitizer=lambda x: int(x) if x else None
        ))
        
        self.add_rule("float", ValidationRule(
            name="is_float",
            validator=lambda x: isinstance(x, (int, float)) or self._is_valid_float(x),
            error_message="Valor deve ser um número decimal",
            sanitizer=lambda x: self._sanitize_float(x)
        ))
        
        # Regras para datas
        self.add_rule("date", ValidationRule(
            name="is_date",
            validator=lambda x: self._is_valid_date(x),
            error_message="Data inválida",
            sanitizer=lambda x: self._sanitize_date(x)
        ))
        
        # Regras para email
        self.add_rule("email", ValidationRule(
            name="is_email",
            validator=lambda x: self._is_valid_email(x),
            error_message="Email inválido",
            sanitizer=lambda x: str(x).lower().strip() if x else None
        ))
        
        # Regras para CPF/CNPJ
        self.add_rule("cpf", ValidationRule(
            name="is_cpf",
            validator=lambda x: self._is_valid_cpf(x),
            error_message="CPF inválido",
            sanitizer=lambda x: re.sub(r'\D', '', str(x)) if x else None
        ))
        
        self.add_rule("cnpj", ValidationRule(
            name="is_cnpj",
            validator=lambda x: self._is_valid_cnpj(x),
            error_message="CNPJ inválido",
            sanitizer=lambda x: re.sub(r'\D', '', str(x)) if x else None
        ))
        
        # Regras para valores monetários
        self.add_rule("money", ValidationRule(
            name="is_money",
            validator=lambda x: self._is_valid_money(x),
            error_message="Valor monetário inválido",
            sanitizer=lambda x: self._sanitize_money(x)
        ))
        
    def add_rule(self, data_type: str, rule: ValidationRule):
        """Adiciona uma regra de validação para um tipo de dados."""
        if data_type not in self.rules:
            self.rules[data_type] = []
        self.rules[data_type].append(rule)
        
    def validate(self, value: Any, data_type: str, additional_rules: Optional[List[ValidationRule]] = None) -> ValidationResult:
        """Valida um valor de acordo com seu tipo e regras adicionais."""
        errors = []
        warnings = []
        sanitized_value = value
        
        # Aplicar regras do tipo de dados
        if data_type in self.rules:
            for rule in self.rules[data_type]:
                try:
                    # Aplicar sanitização se disponível
                    if rule.sanitizer:
                        sanitized_value = rule.sanitizer(sanitized_value)
                    
                    # Validar
                    if not rule.validator(sanitized_value):
                        errors.append(f"{rule.name}: {rule.error_message}")
                except Exception as e:
                    errors.append(f"{rule.name}: Erro na validação - {str(e)}")
        
        # Aplicar regras adicionais
        if additional_rules:
            for rule in additional_rules:
                try:
                    if rule.sanitizer:
                        sanitized_value = rule.sanitizer(sanitized_value)
                    
                    if not rule.validator(sanitized_value):
                        errors.append(f"{rule.name}: {rule.error_message}")
                except Exception as e:
                    errors.append(f"{rule.name}: Erro na validação - {str(e)}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_value=sanitized_value
        )
        
    def validate_row(self, row: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, ValidationResult]:
        """Valida uma linha completa de dados."""
        results = {}
        
        for column, value in row.items():
            if column in schema:
                data_type = schema[column]
                results[column] = self.validate(value, data_type)
            else:
                # Coluna não mapeada
                results[column] = ValidationResult(
                    is_valid=True,
                    errors=[],
                    warnings=["Coluna não mapeada no schema"],
                    sanitized_value=value
                )
                
        return results
        
    # Métodos auxiliares de validação
    def _is_valid_float(self, value: Any) -> bool:
        """Verifica se é um float válido."""
        try:
            float(str(value).replace(',', '.'))
            return True
        except (ValueError, TypeError):
            return False
            
    def _sanitize_float(self, value: Any) -> Optional[float]:
        """Sanitiza valor para float."""
        if value is None or value == "":
            return None
        try:
            # Trata formato brasileiro de números
            clean_value = str(value).replace('.', '').replace(',', '.')
            return float(clean_value)
        except (ValueError, TypeError):
            return None
            
    def _is_valid_date(self, value: Any) -> bool:
        """Verifica se é uma data válida."""
        if isinstance(value, (date, datetime)):
            return True
            
        if not value:
            return False
            
        # Tenta diferentes formatos de data
        date_formats = [
            "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y",
            "%Y/%m/%d", "%d.%m.%Y"
        ]
        
        for fmt in date_formats:
            try:
                datetime.strptime(str(value), fmt)
                return True
            except ValueError:
                continue
                
        return False
        
    def _sanitize_date(self, value: Any) -> Optional[str]:
        """Sanitiza valor para data no formato ISO."""
        if not value:
            return None
            
        if isinstance(value, datetime):
            return value.date().isoformat()
        elif isinstance(value, date):
            return value.isoformat()
            
        # Tenta diferentes formatos
        date_formats = [
            "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y",
            "%Y/%m/%d", "%d.%m.%Y"
        ]
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(str(value), fmt)
                return dt.date().isoformat()
            except ValueError:
                continue
                
        return None
        
    def _is_valid_email(self, value: Any) -> bool:
        """Valida formato de email."""
        if not value:
            return False
            
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(value)))
        
    def _is_valid_cpf(self, value: Any) -> bool:
        """Valida CPF."""
        if not value:
            return False
            
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', str(value))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
            
        # Verifica se não é sequência de números iguais
        if cpf == cpf[0] * 11:
            return False
            
        # Validação dos dígitos verificadores
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                return False
                
        return True
        
    def _is_valid_cnpj(self, value: Any) -> bool:
        """Valida CNPJ."""
        if not value:
            return False
            
        # Remove caracteres não numéricos
        cnpj = re.sub(r'\D', '', str(value))
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
            
        # Verifica se não é sequência de números iguais
        if cnpj == cnpj[0] * 14:
            return False
            
        # Validação dos dígitos verificadores
        size = len(cnpj) - 2
        numbers = cnpj[:size]
        digits = cnpj[size:]
        sum_val = 0
        pos = size - 7
        
        for i in range(size, 0, -1):
            sum_val += int(numbers[size - i]) * pos
            pos -= 1
            if pos < 2:
                pos = 9
                
        result = 0 if sum_val % 11 < 2 else 11 - sum_val % 11
        
        if result != int(digits[0]):
            return False
            
        size += 1
        numbers = cnpj[:size]
        sum_val = 0
        pos = size - 7
        
        for i in range(size, 0, -1):
            sum_val += int(numbers[size - i]) * pos
            pos -= 1
            if pos < 2:
                pos = 9
                
        result = 0 if sum_val % 11 < 2 else 11 - sum_val % 11
        
        return result == int(digits[1])
        
    def _is_valid_money(self, value: Any) -> bool:
        """Valida valor monetário."""
        if value is None:
            return False
            
        try:
            # Remove símbolos monetários e espaços
            clean_value = re.sub(r'[R$\s]', '', str(value))
            # Trata formato brasileiro
            clean_value = clean_value.replace('.', '').replace(',', '.')
            Decimal(clean_value)
            return True
        except (InvalidOperation, ValueError):
            return False
            
    def _sanitize_money(self, value: Any) -> Optional[Decimal]:
        """Sanitiza valor monetário."""
        if value is None or value == "":
            return None
            
        try:
            # Remove símbolos monetários e espaços
            clean_value = re.sub(r'[R$\s]', '', str(value))
            # Trata formato brasileiro
            clean_value = clean_value.replace('.', '').replace(',', '.')
            return Decimal(clean_value)
        except (InvalidOperation, ValueError):
            return None