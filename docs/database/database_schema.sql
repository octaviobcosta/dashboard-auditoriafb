-- Criação das tabelas para o Dashboard de Controladoria

-- Tabela de categorias de indicadores
CREATE TABLE IF NOT EXISTS categorias (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    cor VARCHAR(7) DEFAULT '#000000',
    icone VARCHAR(50),
    ordem INTEGER DEFAULT 0,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de indicadores
CREATE TABLE IF NOT EXISTS indicadores (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    categoria_id UUID REFERENCES categorias(id) ON DELETE SET NULL,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    unidade VARCHAR(50),
    tipo VARCHAR(50) CHECK (tipo IN ('valor', 'percentual', 'quantidade', 'moeda')),
    meta_valor DECIMAL(15,2),
    meta_tipo VARCHAR(20) CHECK (meta_tipo IN ('maior_melhor', 'menor_melhor', 'igual_melhor')),
    frequencia VARCHAR(20) CHECK (frequencia IN ('diario', 'semanal', 'mensal', 'trimestral', 'anual')),
    formula TEXT,
    responsavel VARCHAR(100),
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de dados dos indicadores
CREATE TABLE IF NOT EXISTS dados_indicadores (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    indicador_id UUID REFERENCES indicadores(id) ON DELETE CASCADE,
    data_referencia DATE NOT NULL,
    valor DECIMAL(15,4) NOT NULL,
    meta DECIMAL(15,4),
    observacoes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(indicador_id, data_referencia)
);

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(200) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    departamento VARCHAR(100),
    perfil VARCHAR(50) CHECK (perfil IN ('admin', 'gestor', 'visualizador')) DEFAULT 'visualizador',
    ativo BOOLEAN DEFAULT true,
    ultimo_acesso TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de configurações
CREATE TABLE IF NOT EXISTS configuracoes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    chave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT,
    tipo VARCHAR(50) CHECK (tipo IN ('texto', 'numero', 'boolean', 'json')),
    descricao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de logs de auditoria
CREATE TABLE IF NOT EXISTS logs_auditoria (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    acao VARCHAR(100) NOT NULL,
    tabela VARCHAR(100),
    registro_id UUID,
    dados_anteriores JSONB,
    dados_novos JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de dashboards personalizados
CREATE TABLE IF NOT EXISTS dashboards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    configuracao JSONB,
    publico BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de widgets do dashboard
CREATE TABLE IF NOT EXISTS dashboard_widgets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    dashboard_id UUID REFERENCES dashboards(id) ON DELETE CASCADE,
    indicador_id UUID REFERENCES indicadores(id) ON DELETE CASCADE,
    tipo_visualizacao VARCHAR(50) CHECK (tipo_visualizacao IN ('card', 'grafico_linha', 'grafico_barra', 'grafico_pizza', 'tabela', 'gauge')),
    configuracao JSONB,
    posicao_x INTEGER DEFAULT 0,
    posicao_y INTEGER DEFAULT 0,
    largura INTEGER DEFAULT 4,
    altura INTEGER DEFAULT 4,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para melhorar performance
CREATE INDEX idx_dados_indicadores_indicador_id ON dados_indicadores(indicador_id);
CREATE INDEX idx_dados_indicadores_data_referencia ON dados_indicadores(data_referencia);
CREATE INDEX idx_indicadores_categoria_id ON indicadores(categoria_id);
CREATE INDEX idx_logs_auditoria_usuario_id ON logs_auditoria(usuario_id);
CREATE INDEX idx_logs_auditoria_created_at ON logs_auditoria(created_at);

-- Triggers para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_categorias_updated_at BEFORE UPDATE ON categorias
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_indicadores_updated_at BEFORE UPDATE ON indicadores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dados_indicadores_updated_at BEFORE UPDATE ON dados_indicadores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_configuracoes_updated_at BEFORE UPDATE ON configuracoes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dashboards_updated_at BEFORE UPDATE ON dashboards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dashboard_widgets_updated_at BEFORE UPDATE ON dashboard_widgets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Inserir configurações padrão
INSERT INTO configuracoes (chave, valor, tipo, descricao) VALUES
    ('nome_empresa', 'Empresa', 'texto', 'Nome da empresa'),
    ('logo_url', '/static/images/logo.png', 'texto', 'URL do logo da empresa'),
    ('periodo_padrao_dias', '30', 'numero', 'Período padrão para exibição de dados em dias'),
    ('tema_padrao', 'light', 'texto', 'Tema padrão do sistema (light/dark)'),
    ('formato_data', 'DD/MM/YYYY', 'texto', 'Formato de exibição de datas'),
    ('formato_moeda', 'BRL', 'texto', 'Código da moeda padrão')
ON CONFLICT (chave) DO NOTHING;

-- Inserir categorias padrão
INSERT INTO categorias (nome, descricao, cor, icone, ordem) VALUES
    ('Financeiro', 'Indicadores financeiros e de resultado', '#4CAF50', 'attach_money', 1),
    ('Operacional', 'Indicadores de eficiência operacional', '#2196F3', 'settings', 2),
    ('Qualidade', 'Indicadores de qualidade e satisfação', '#FF9800', 'star', 3),
    ('Pessoas', 'Indicadores de recursos humanos', '#9C27B0', 'people', 4),
    ('Vendas', 'Indicadores comerciais e de vendas', '#F44336', 'shopping_cart', 5)
ON CONFLICT DO NOTHING;