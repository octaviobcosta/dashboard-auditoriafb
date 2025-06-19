-- Tabela para armazenar dados de produtos vendidos
CREATE TABLE IF NOT EXISTS produtos_vendidos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sku VARCHAR(255),
    nome VARCHAR(500) NOT NULL,
    categoria VARCHAR(255),
    operacao VARCHAR(100),
    montavel BOOLEAN DEFAULT FALSE,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(15,2),
    subtotal DECIMAL(15,2),
    descontos DECIMAL(15,2) DEFAULT 0,
    valor_total DECIMAL(15,2) NOT NULL,
    data_venda DATE,
    periodo_inicio DATE,
    periodo_fim DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para melhorar performance
CREATE INDEX idx_produtos_vendidos_sku ON produtos_vendidos(sku);
CREATE INDEX idx_produtos_vendidos_categoria ON produtos_vendidos(categoria);
CREATE INDEX idx_produtos_vendidos_data_venda ON produtos_vendidos(data_venda);
CREATE INDEX idx_produtos_vendidos_periodo ON produtos_vendidos(periodo_inicio, periodo_fim);

-- Trigger para atualizar updated_at
CREATE TRIGGER update_produtos_vendidos_updated_at BEFORE UPDATE ON produtos_vendidos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Tabela para controle de importações de arquivos
CREATE TABLE IF NOT EXISTS importacoes_arquivos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nome_arquivo VARCHAR(500) NOT NULL,
    tipo_arquivo VARCHAR(50) DEFAULT 'csv',
    periodo_inicio DATE,
    periodo_fim DATE,
    total_registros INTEGER,
    registros_importados INTEGER,
    registros_erro INTEGER,
    status VARCHAR(50) CHECK (status IN ('pendente', 'processando', 'concluido', 'erro')),
    mensagem_erro TEXT,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela para log de erros de importação
CREATE TABLE IF NOT EXISTS importacoes_erros (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    importacao_id UUID REFERENCES importacoes_arquivos(id) ON DELETE CASCADE,
    linha_numero INTEGER,
    linha_conteudo TEXT,
    erro_mensagem TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);