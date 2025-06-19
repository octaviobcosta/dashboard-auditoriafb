// Sistema unificado de formatação de valores

/**
 * Formata valores monetários com abreviação (K, M, B)
 * @param {number} valor - Valor a ser formatado
 * @param {boolean} mostrarCentavos - Se deve mostrar centavos para valores pequenos
 * @returns {string} Valor formatado (ex: R$ 1.5M, R$ 125k)
 */
function formatarValorAbreviado(valor, mostrarCentavos = false) {
    if (valor === null || valor === undefined || isNaN(valor)) return 'R$ 0';
    
    const absValor = Math.abs(valor);
    const sinal = valor < 0 ? '-' : '';
    
    if (absValor >= 1e9) {
        const num = absValor / 1e9;
        const casas = num < 10 ? 2 : 1;
        return `${sinal}R$ ${num.toFixed(casas).replace('.', ',')}B`;
    } else if (absValor >= 1e6) {
        const num = absValor / 1e6;
        const casas = num < 10 ? 2 : 1;
        return `${sinal}R$ ${num.toFixed(casas).replace('.', ',')}M`;
    } else if (absValor >= 1e3) {
        const num = absValor / 1e3;
        const casas = num < 10 ? 2 : 1;
        return `${sinal}R$ ${num.toFixed(casas).replace('.', ',')}k`;
    } else {
        const casas = mostrarCentavos ? 2 : 0;
        return `${sinal}R$ ${absValor.toFixed(casas).replace('.', ',')}`;
    }
}

/**
 * Formata números com abreviação (K, M, B)
 * @param {number} numero - Número a ser formatado
 * @returns {string} Número formatado (ex: 1.5k, 12.3M)
 */
function formatarNumeroAbreviado(numero) {
    if (numero === null || numero === undefined || isNaN(numero)) return '0';
    
    const absNumero = Math.abs(numero);
    const sinal = numero < 0 ? '-' : '';
    
    if (absNumero >= 1e9) {
        const num = absNumero / 1e9;
        const casas = num < 10 ? 2 : 1;
        return `${sinal}${num.toFixed(casas).replace('.', ',')}B`;
    } else if (absNumero >= 1e6) {
        const num = absNumero / 1e6;
        const casas = num < 10 ? 2 : 1;
        return `${sinal}${num.toFixed(casas).replace('.', ',')}M`;
    } else if (absNumero >= 1e3) {
        const num = absNumero / 1e3;
        const casas = num < 10 ? 2 : 1;
        return `${sinal}${num.toFixed(casas).replace('.', ',')}k`;
    } else {
        return `${sinal}${absNumero.toFixed(0)}`;
    }
}

/**
 * Formata percentuais
 * @param {number} valor - Valor percentual
 * @param {number} casasDecimais - Número de casas decimais (padrão: automático)
 * @returns {string} Percentual formatado (ex: 12.5%, 1.25%)
 */
function formatarPercentual(valor, casasDecimais = null) {
    if (valor === null || valor === undefined || isNaN(valor)) return '0%';
    
    const absValor = Math.abs(valor);
    const sinal = valor < 0 ? '-' : '';
    
    // Se casas decimais não especificadas, usa regra automática
    if (casasDecimais === null) {
        casasDecimais = absValor < 10 ? 2 : 1;
    }
    
    return `${sinal}${absValor.toFixed(casasDecimais).replace('.', ',')}%`;
}

/**
 * Formata valores monetários completos (sem abreviação)
 * @param {number} valor - Valor a ser formatado
 * @returns {string} Valor formatado (ex: R$ 1.234.567,89)
 */
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor || 0);
}

/**
 * Formata números completos (sem abreviação)
 * @param {number} numero - Número a ser formatado
 * @returns {string} Número formatado (ex: 1.234.567)
 */
function formatarNumero(numero) {
    return new Intl.NumberFormat('pt-BR').format(numero || 0);
}

/**
 * Formata valores para exibição em gráficos (eixos)
 * @param {number} valor - Valor a ser formatado
 * @param {string} tipo - Tipo de formatação ('moeda', 'numero', 'percentual')
 * @returns {string} Valor formatado para gráfico
 */
function formatarParaGrafico(valor, tipo = 'moeda') {
    switch (tipo) {
        case 'moeda':
            return formatarValorAbreviado(valor);
        case 'numero':
            return formatarNumeroAbreviado(valor);
        case 'percentual':
            return formatarPercentual(valor);
        default:
            return valor.toString();
    }
}

/**
 * Formata diferença/variação com sinal e cor
 * @param {number} valor - Valor da variação
 * @param {string} tipo - Tipo de formatação ('moeda', 'numero', 'percentual')
 * @returns {object} Objeto com valor formatado e classe CSS
 */
function formatarVariacao(valor, tipo = 'percentual') {
    const isPositive = valor > 0;
    const isNegative = valor < 0;
    
    let valorFormatado;
    switch (tipo) {
        case 'moeda':
            valorFormatado = formatarValorAbreviado(valor);
            break;
        case 'numero':
            valorFormatado = formatarNumeroAbreviado(valor);
            break;
        case 'percentual':
            valorFormatado = formatarPercentual(valor);
            break;
        default:
            valorFormatado = valor.toString();
    }
    
    // Adiciona sinal + para valores positivos
    if (isPositive && !valorFormatado.startsWith('+')) {
        valorFormatado = '+' + valorFormatado;
    }
    
    return {
        valor: valorFormatado,
        classe: isPositive ? 'text-success' : isNegative ? 'text-danger' : 'text-muted',
        icone: isPositive ? 'fa-arrow-up' : isNegative ? 'fa-arrow-down' : 'fa-minus'
    };
}