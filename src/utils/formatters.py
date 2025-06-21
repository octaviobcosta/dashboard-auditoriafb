"""
Funções utilitárias para formatação de valores.
"""

def format_currency(value: float) -> str:
    """
    Formata valores monetários seguindo o padrão:
    - R$1.25M para milhões
    - R$10.2k para milhares
    - R$100.50 para valores menores
    """
    if value >= 1000000:
        return f"R${value/1000000:.2f}M"
    elif value >= 1000:
        return f"R${value/1000:.1f}k"
    else:
        return f"R${value:.2f}"

def format_number(value: float) -> str:
    """
    Formata números seguindo o padrão:
    - 1M para milhões
    - 10k para milhares
    - 100 para valores menores
    """
    if value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.0f}k"
    else:
        return f"{value:.0f}"

def format_percentage(value: float) -> str:
    """
    Formata percentuais.
    """
    return f"{value:.2f}%"