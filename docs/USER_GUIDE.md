# Manual do Usuário - Dashboard Auditoria FB 📖

## Índice
- [Introdução](#introdução)
- [Primeiros Passos](#primeiros-passos)
- [Dashboard Principal](#dashboard-principal)
- [Indicadores](#indicadores)
- [Importação de Dados](#importação-de-dados)
- [Relatórios](#relatórios)
- [Configurações](#configurações)
- [Dicas e Truques](#dicas-e-truques)
- [Solução de Problemas](#solução-de-problemas)

## Introdução

Bem-vindo ao Dashboard Auditoria FB! Este sistema foi desenvolvido para facilitar a análise e visualização de dados de auditoria, vendas e indicadores de performance.

### Para que serve?
- 📊 Visualizar indicadores em tempo real
- 📈 Analisar tendências e padrões
- 📤 Importar dados de planilhas
- 📑 Gerar relatórios customizados
- 👥 Colaborar com sua equipe

## Primeiros Passos

### 1. Fazendo Login

1. Acesse o sistema através do navegador
2. Na tela de login, insira:
   - **Email**: Seu email corporativo
   - **Senha**: Senha fornecida pelo administrador
3. Clique em "Entrar"

![Tela de Login](images/login-screen.png)

### 2. Primeiro Acesso

No primeiro acesso, recomendamos:
- Alterar sua senha (Menu → Perfil → Alterar Senha)
- Verificar suas informações pessoais
- Explorar o dashboard

### 3. Navegação Principal

A interface possui:
- **Menu Lateral**: Acesso às principais funcionalidades
- **Barra Superior**: Informações do usuário e notificações
- **Área Central**: Conteúdo principal

## Dashboard Principal

### Visão Geral

O dashboard principal apresenta um resumo dos indicadores mais importantes:

![Dashboard Principal](images/dashboard-main.png)

#### Componentes:

1. **Cards de KPIs**
   - Total de Vendas
   - Ticket Médio
   - Taxa de Conversão
   - Satisfação do Cliente

2. **Gráfico de Tendências**
   - Visualização temporal dos indicadores
   - Comparação com períodos anteriores

3. **Top Produtos**
   - Lista dos produtos mais vendidos
   - Participação percentual

4. **Filtros**
   - Por período (dia, semana, mês, ano)
   - Por unidade/loja
   - Por categoria

### Como Usar os Filtros

1. **Filtro de Data**:
   ```
   - Clique no campo de data
   - Selecione o período desejado
   - Use os atalhos: "Hoje", "Esta Semana", "Este Mês"
   ```

2. **Filtro de Unidade**:
   ```
   - Dropdown com todas as unidades
   - Permite seleção múltipla
   - "Todas" para visão consolidada
   ```

3. **Aplicar Filtros**:
   - Clique em "Aplicar" após selecionar
   - "Limpar" remove todos os filtros

## Indicadores

### Acessando Indicadores Detalhados

Menu → Indicadores

### Tipos de Indicadores

#### 1. Indicadores de Vendas
- Faturamento Total
- Quantidade de Produtos Vendidos
- Ticket Médio
- Taxa de Conversão

#### 2. Indicadores Operacionais
- Taxa de Estorno
- Tempo Médio de Atendimento
- Índice de Cancelamento
- Eficiência Operacional

#### 3. Indicadores Financeiros
- Margem de Lucro
- ROI (Retorno sobre Investimento)
- Custos Operacionais
- Fluxo de Caixa

### Visualizando Indicadores

1. **Seleção de Indicador**:
   - Use a barra de busca ou
   - Navegue pelas categorias

2. **Configuração de Visualização**:
   - Tipo de gráfico (linha, barra, pizza)
   - Período de análise
   - Granularidade (dia, semana, mês)

3. **Comparações**:
   - Compare com período anterior
   - Compare entre unidades
   - Benchmark com metas

### Exportando Indicadores

1. Clique no ícone de exportação (↓)
2. Escolha o formato:
   - PDF (relatório completo)
   - Excel (dados brutos)
   - Imagem (PNG/JPG)
3. Configure opções de exportação
4. Clique em "Exportar"

## Importação de Dados

### Formatos Suportados
- Excel (.xlsx, .xls)
- CSV (.csv)
- JSON (.json)

### Processo de Importação

#### 1. Preparando o Arquivo

**Formato Excel Esperado**:
```
| UNIDADE | DATA       | PRODUTO    | QUANTIDADE | VALOR    |
|---------|------------|------------|------------|----------|
| Loja A  | 01/01/2024 | Produto X  | 10         | 1.000,00 |
| Loja B  | 01/01/2024 | Produto Y  | 5          | 500,00   |
```

**Regras Importantes**:
- Primeira linha deve conter cabeçalhos
- Datas no formato DD/MM/AAAA
- Valores monetários podem usar vírgula
- Sem linhas vazias no meio dos dados

#### 2. Fazendo Upload

1. Menu → Importar Dados
2. Clique em "Selecionar Arquivo" ou arraste
3. Visualize preview dos dados
4. Confirme mapeamento de colunas
5. Clique em "Importar"

#### 3. Mapeamento de Colunas

O sistema tentará mapear automaticamente, mas você pode ajustar:

![Mapeamento de Colunas](images/column-mapping.png)

- **Coluna Origem**: Nome no seu arquivo
- **Coluna Destino**: Campo no sistema
- **Tipo de Dado**: Texto, Número, Data, etc.

#### 4. Validação

O sistema valida:
- ✅ Formatos de data
- ✅ Valores numéricos
- ✅ Campos obrigatórios
- ✅ Duplicatas

Erros comuns:
- ❌ "Data inválida" → Verificar formato DD/MM/AAAA
- ❌ "Valor inválido" → Remover caracteres especiais
- ❌ "Campo obrigatório" → Preencher células vazias

#### 5. Acompanhamento

Após iniciar:
- Barra de progresso mostra status
- Lista de erros (se houver)
- Relatório final com estatísticas

## Relatórios

### Tipos de Relatórios

1. **Relatório de Vendas**
   - Resumo por período
   - Detalhamento por produto
   - Análise por categoria

2. **Relatório de Estornos**
   - Taxa de estorno por unidade
   - Motivos mais comuns
   - Evolução temporal

3. **Relatório Gerencial**
   - KPIs consolidados
   - Comparativos
   - Projeções

### Gerando Relatórios

1. Menu → Relatórios
2. Selecione o tipo
3. Configure parâmetros:
   - Período
   - Unidades
   - Nível de detalhe
4. Clique em "Gerar"

### Agendamento de Relatórios

Para receber relatórios automaticamente:

1. Ao gerar um relatório, marque "Agendar"
2. Configure:
   - Frequência (diária, semanal, mensal)
   - Horário de envio
   - Destinatários (emails)
3. Salve agendamento

## Configurações

### Perfil do Usuário

Menu → Meu Perfil

- **Informações Pessoais**: Nome, email, cargo
- **Senha**: Alterar senha
- **Preferências**: Idioma, fuso horário
- **Notificações**: Email, sistema

### Preferências do Sistema

(Apenas para administradores)

Menu → Configurações

- **Aparência**: Tema (claro/escuro)
- **Dados**: Período padrão, unidade padrão
- **Importação**: Limites, validações
- **Segurança**: Tempo de sessão, 2FA

## Dicas e Truques

### Atalhos de Teclado

- `Ctrl + /`: Busca rápida
- `Ctrl + F`: Filtros
- `Ctrl + E`: Exportar
- `Esc`: Fechar modal/menu

### Favoritos

Marque indicadores como favoritos:
1. Clique na ⭐ ao lado do nome
2. Acesse rapidamente em "Meus Favoritos"

### Dashboards Personalizados

Crie seu próprio dashboard:
1. Menu → Dashboards → Novo
2. Arraste widgets desejados
3. Configure cada widget
4. Salve e compartilhe

### Filtros Salvos

Salve combinações de filtros frequentes:
1. Configure filtros desejados
2. Clique em "Salvar Filtro"
3. Nomeie (ex: "Vendas SP - Último Mês")
4. Acesse em "Filtros Salvos"

## Solução de Problemas

### Problemas Comuns

#### 1. "Página não carrega"
- Verifique conexão internet
- Limpe cache do navegador (Ctrl + F5)
- Tente outro navegador

#### 2. "Erro ao importar arquivo"
- Verifique formato do arquivo
- Tamanho máximo: 16MB
- Remova formatações especiais

#### 3. "Gráficos não aparecem"
- Habilite JavaScript
- Desabilite bloqueadores de anúncios
- Atualize navegador

#### 4. "Dados desatualizados"
- Verifique filtros aplicados
- Clique em "Atualizar" (🔄)
- Confirme última importação

### Mensagens de Erro

| Erro | Significado | Solução |
|------|-------------|---------|
| 401 | Não autorizado | Faça login novamente |
| 403 | Sem permissão | Contate administrador |
| 404 | Não encontrado | Verifique URL/dados |
| 500 | Erro servidor | Aguarde e tente novamente |

### Navegadores Suportados

✅ Recomendados:
- Google Chrome 90+
- Mozilla Firefox 88+
- Microsoft Edge 90+
- Safari 14+

⚠️ Limitados:
- Internet Explorer (não suportado)
- Versões antigas dos navegadores

## Suporte

### Canais de Atendimento

1. **Email**: suporte@auditoriafb.com.br
2. **Chat**: Ícone no canto inferior direito
3. **Telefone**: (11) 1234-5678

### Informações Úteis ao Contatar

Forneça sempre:
- Nome e email
- Descrição detalhada do problema
- Passos para reproduzir
- Screenshots (se possível)
- Navegador e versão

### FAQ Rápido

**P: Esqueci minha senha**
R: Clique em "Esqueci minha senha" na tela de login

**P: Como exporto dados?**
R: Use o botão de exportação (↓) presente em tabelas e gráficos

**P: Posso acessar pelo celular?**
R: Sim, o sistema é responsivo e funciona em dispositivos móveis

**P: Quanto tempo os dados ficam disponíveis?**
R: Dados históricos são mantidos por 2 anos

---

Para mais informações, consulte nossa [Base de Conhecimento](https://kb.auditoriafb.com.br) ou entre em contato com o suporte.