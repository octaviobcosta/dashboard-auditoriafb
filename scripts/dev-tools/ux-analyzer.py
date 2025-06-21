#!/usr/bin/env python3
"""
🎨 UX/UI ANALYZER - Seu Time de Design Completo
Análise automática de UX/UI com insights de design senior
"""

import re
import json
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class UXIssue:
    type: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    file: str
    line: int
    description: str
    suggestion: str
    impact: str

class UXAnalyzer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = []
        
        # Padrões de design do projeto (tema grafite/dourado)
        self.design_patterns = {
            'colors': {
                'primary': ['#F1C232', '#f9d71c', '#E6B800'],
                'secondary': ['#FFD966', '#FFF2CC', '#FFEB9C'],
                'dark_bg': ['#1a1a1a', '#0f0f0f', '#2d2d2d'],
                'success': ['#34A853', '#28a745', '#1e7e34'],
                'warning': ['#FBBC04', '#ffc107', '#e0a800'],
                'danger': ['#EA4335', '#dc3545', '#c82333']
            },
            'typography': {
                'fonts': ['Inter', 'Poppins', 'Segoe UI', 'Roboto'],
                'sizes': {'h1': '2.5rem', 'h2': '2rem', 'h3': '1.75rem', 'body': '1rem'}
            },
            'spacing': {
                'margins': ['0.25rem', '0.5rem', '1rem', '1.5rem', '2rem', '3rem'],
                'padding': ['0.25rem', '0.5rem', '1rem', '1.5rem', '2rem']
            }
        }
    
    def analyze_html_templates(self):
        """Analisa templates HTML para issues de UX/UI"""
        print("🎨 Analisando templates HTML...")
        
        for template_file in self.project_root.rglob("*.html"):
            if "venv" in str(template_file):
                continue
                
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                self._check_accessibility(template_file, content, lines)
                self._check_responsive_design(template_file, content, lines)
                self._check_performance(template_file, content, lines)
                self._check_semantic_html(template_file, content, lines)
                self._check_visual_hierarchy(template_file, content, lines)
    
    def _check_accessibility(self, file_path, content, lines):
        """Verifica questões de acessibilidade"""
        # Imagens sem alt
        img_pattern = r'<img(?![^>]*alt=)[^>]*>'
        for i, line in enumerate(lines):
            if re.search(img_pattern, line):
                self.issues.append(UXIssue(
                    type="accessibility",
                    severity="critical",
                    file=str(file_path),
                    line=i+1,
                    description="Imagem sem texto alternativo",
                    suggestion="Adicione atributo alt='descrição da imagem'",
                    impact="Impede usuários com deficiência visual de entender o conteúdo"
                ))
        
        # Formulários sem labels
        input_pattern = r'<input(?![^>]*aria-label)(?![^>]*id=)[^>]*>'
        for i, line in enumerate(lines):
            if re.search(input_pattern, line) and '<label' not in line:
                self.issues.append(UXIssue(
                    type="accessibility",
                    severity="high",
                    file=str(file_path),
                    line=i+1,
                    description="Input sem label associado",
                    suggestion="Adicione <label> ou aria-label",
                    impact="Dificulta navegação por teclado e leitores de tela"
                ))
        
        # Contraste de cores (considerando tema escuro)
        if 'style=' in content:
            color_matches = re.findall(r'color:\s*([^;]+)', content)
            bg_matches = re.findall(r'background[^:]*:\s*([^;]+)', content)
            
            # Verifica se está usando cores do projeto
            project_colors = ['#F1C232', '#f9d71c', '#1a1a1a', '#0f0f0f']
            has_project_colors = any(color in content for color in project_colors)
            
            if color_matches and bg_matches and not has_project_colors:
                self.issues.append(UXIssue(
                    type="design",
                    severity="medium",
                    file=str(file_path),
                    line=1,
                    description="Cores não seguem padrão do projeto",
                    suggestion="Use cores do projeto: --primary-color: #F1C232, --dark-bg: #1a1a1a",
                    impact="Inconsistência visual com o design system"
                ))
            elif color_matches and bg_matches:
                self.issues.append(UXIssue(
                    type="accessibility",
                    severity="low",
                    file=str(file_path),
                    line=1,
                    description="Verificar contraste em tema escuro",
                    suggestion="Contraste mínimo 3:1 para tema escuro, ideal 4.5:1",
                    impact="Pode dificultar leitura em tema escuro"
                ))
    
    def _check_responsive_design(self, file_path, content, lines):
        """Verifica design responsivo"""
        # Meta viewport
        if 'viewport' not in content:
            self.issues.append(UXIssue(
                type="responsive",
                severity="critical",
                file=str(file_path),
                line=1,
                description="Meta viewport ausente",
                suggestion="Adicione <meta name='viewport' content='width=device-width, initial-scale=1'>",
                impact="Layout quebrado em dispositivos móveis"
            ))
        
        # Media queries
        if '@media' not in content and 'media=' not in content:
            self.issues.append(UXIssue(
                type="responsive",
                severity="high",
                file=str(file_path),
                line=1,
                description="Sem media queries para responsividade",
                suggestion="Implemente breakpoints: 576px, 768px, 992px, 1200px",
                impact="Experiência ruim em diferentes tamanhos de tela"
            ))
        
        # Unidades fixas
        px_pattern = r'width:\s*\d+px|height:\s*\d+px'
        for i, line in enumerate(lines):
            if re.search(px_pattern, line):
                self.issues.append(UXIssue(
                    type="responsive",
                    severity="medium",
                    file=str(file_path),
                    line=i+1,
                    description="Uso de unidades fixas (px)",
                    suggestion="Use unidades relativas: rem, em, %, vw, vh",
                    impact="Layout menos flexível"
                ))
    
    def _check_performance(self, file_path, content, lines):
        """Verifica performance de UX"""
        # Muitas requisições CSS/JS
        css_count = len(re.findall(r'<link[^>]*rel=["\']stylesheet["\']', content))
        js_count = len(re.findall(r'<script[^>]*src=', content))
        
        if css_count > 3:
            self.issues.append(UXIssue(
                type="performance",
                severity="medium",
                file=str(file_path),
                line=1,
                description=f"Muitos arquivos CSS ({css_count})",
                suggestion="Combine arquivos CSS ou use bundler",
                impact="Tempo de carregamento lento"
            ))
        
        if js_count > 3:
            self.issues.append(UXIssue(
                type="performance",
                severity="medium",
                file=str(file_path),
                line=1,
                description=f"Muitos arquivos JavaScript ({js_count})",
                suggestion="Combine e minifique arquivos JS",
                impact="Tempo de carregamento lento"
            ))
        
        # Imagens sem lazy loading
        img_pattern = r'<img(?![^>]*loading=)[^>]*>'
        for i, line in enumerate(lines):
            if re.search(img_pattern, line):
                self.issues.append(UXIssue(
                    type="performance",
                    severity="low",
                    file=str(file_path),
                    line=i+1,
                    description="Imagem sem lazy loading",
                    suggestion="Adicione loading='lazy' para imagens below-the-fold",
                    impact="Carregamento inicial mais lento"
                ))
    
    def _check_semantic_html(self, file_path, content, lines):
        """Verifica HTML semântico"""
        # Falta de tags semânticas
        semantic_tags = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        has_semantic = any(tag in content for tag in semantic_tags)
        
        if not has_semantic and len(lines) > 20:
            self.issues.append(UXIssue(
                type="semantic",
                severity="medium",
                file=str(file_path),
                line=1,
                description="Falta de HTML semântico",
                suggestion="Use tags semânticas: <header>, <nav>, <main>, <section>, <footer>",
                impact="Pior SEO e acessibilidade"
            ))
        
        # Uso excessivo de divs
        div_count = len(re.findall(r'<div', content))
        if div_count > 10:
            self.issues.append(UXIssue(
                type="semantic",
                severity="low",
                file=str(file_path),
                line=1,
                description=f"Uso excessivo de divs ({div_count})",
                suggestion="Substitua por tags semânticas apropriadas",
                impact="HTML menos semântico"
            ))
    
    def _check_visual_hierarchy(self, file_path, content, lines):
        """Verifica hierarquia visual"""
        # Sequência de headings
        h_tags = re.findall(r'<h([1-6])', content)
        if h_tags:
            h_levels = [int(tag) for tag in h_tags]
            for i in range(1, len(h_levels)):
                if h_levels[i] > h_levels[i-1] + 1:
                    self.issues.append(UXIssue(
                        type="hierarchy",
                        severity="medium",
                        file=str(file_path),
                        line=1,
                        description="Hierarquia de headings quebrada",
                        suggestion="Use sequência lógica: h1 > h2 > h3",
                        impact="Confunde estrutura para leitores de tela"
                    ))
    
    def analyze_css_files(self):
        """Analisa arquivos CSS"""
        print("🎨 Analisando arquivos CSS...")
        
        for css_file in self.project_root.rglob("*.css"):
            if "venv" in str(css_file):
                continue
                
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                self._check_css_best_practices(css_file, content, lines)
                self._check_css_performance(css_file, content, lines)
                self._check_design_consistency(css_file, content, lines)
    
    def _check_css_best_practices(self, file_path, content, lines):
        """Verifica boas práticas CSS"""
        # IDs em CSS
        id_selectors = len(re.findall(r'#[a-zA-Z]', content))
        if id_selectors > 2:
            self.issues.append(UXIssue(
                type="css",
                severity="medium",
                file=str(file_path),
                line=1,
                description=f"Uso excessivo de seletores ID ({id_selectors})",
                suggestion="Prefira classes para estilização",
                impact="CSS menos reutilizável"
            ))
        
        # !important
        important_count = len(re.findall(r'!important', content))
        if important_count > 3:
            self.issues.append(UXIssue(
                type="css",
                severity="high",
                file=str(file_path),
                line=1,
                description=f"Uso excessivo de !important ({important_count})",
                suggestion="Reestruture CSS para evitar !important",
                impact="Dificulta manutenção e customização"
            ))
    
    def _check_css_performance(self, file_path, content, lines):
        """Verifica performance CSS"""
        # Seletores complexos
        complex_selectors = re.findall(r'[^{]+{[^}]*}', content)
        for selector in complex_selectors:
            if selector.count(' ') > 4:  # Mais de 4 níveis
                self.issues.append(UXIssue(
                    type="performance",
                    severity="low",
                    file=str(file_path),
                    line=1,
                    description="Seletor CSS muito específico",
                    suggestion="Simplifique seletores para melhor performance",
                    impact="Renderização mais lenta"
                ))
    
    def _check_design_consistency(self, file_path, content, lines):
        """Verifica consistência de design"""
        # Cores hardcoded
        color_pattern = r'#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)'
        colors = re.findall(color_pattern, content)
        
        # Verifica se usa variáveis CSS do projeto
        css_vars = ['--primary-color', '--secondary-color', '--dark-bg', '--darker-bg']
        uses_css_vars = any(var in content for var in css_vars)
        
        if len(set(colors)) > 8 and not uses_css_vars:
            self.issues.append(UXIssue(
                type="design",
                severity="high",
                file=str(file_path),
                line=1,
                description=f"Muitas cores hardcoded ({len(set(colors))})",
                suggestion="Use variáveis CSS: --primary-color: #F1C232, --dark-bg: #1a1a1a",
                impact="Design inconsistente com o tema grafite/dourado"
            ))
        
        # Verifica fontes do projeto
        project_fonts = ['Inter', 'Poppins']
        font_pattern = r'font-family:\s*[\'"]?([^;,\'"]+)'
        fonts_used = re.findall(font_pattern, content)
        
        if fonts_used and not any(font in str(fonts_used) for font in project_fonts):
            self.issues.append(UXIssue(
                type="design",
                severity="medium",
                file=str(file_path),
                line=1,
                description="Fontes não seguem padrão do projeto",
                suggestion="Use fontes do projeto: Inter ou Poppins",
                impact="Inconsistência tipográfica"
            ))
    
    def generate_ux_report(self):
        """Gera relatório completo de UX/UI"""
        print("📊 Gerando relatório UX/UI...")
        
        # Agrupa issues por tipo e severidade
        issues_by_type = {}
        issues_by_severity = {}
        
        for issue in self.issues:
            issues_by_type.setdefault(issue.type, []).append(issue)
            issues_by_severity.setdefault(issue.severity, []).append(issue)
        
        # Calcula score UX
        ux_score = self._calculate_ux_score()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'ux_score': ux_score,
            'total_issues': len(self.issues),
            'issues_by_type': {k: len(v) for k, v in issues_by_type.items()},
            'issues_by_severity': {k: len(v) for k, v in issues_by_severity.items()},
            'recommendations': self._generate_recommendations(),
            'detailed_issues': [
                {
                    'type': issue.type,
                    'severity': issue.severity,
                    'file': issue.file,
                    'line': issue.line,
                    'description': issue.description,
                    'suggestion': issue.suggestion,
                    'impact': issue.impact
                }
                for issue in self.issues
            ]
        }
        
        # Salva relatório
        report_file = self.project_root / "reports" / f"ux_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Gera relatório HTML
        html_report = self._generate_html_report(report)
        html_file = report_file.with_suffix('.html')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ Relatório UX/UI salvo em: {html_file}")
        return report
    
    def _calculate_ux_score(self):
        """Calcula score UX baseado nos issues"""
        base_score = 100
        
        severity_weights = {
            'critical': 20,
            'high': 10,
            'medium': 5,
            'low': 2
        }
        
        for issue in self.issues:
            base_score -= severity_weights.get(issue.severity, 1)
        
        return max(0, base_score)
    
    def _generate_recommendations(self):
        """Gera recomendações baseadas nos issues"""
        recommendations = []
        
        # Issues críticos
        critical_issues = [i for i in self.issues if i.severity == 'critical']
        if critical_issues:
            recommendations.append({
                'priority': 'Urgente',
                'title': 'Corrigir Issues Críticos',
                'description': f'Existem {len(critical_issues)} problemas críticos que devem ser corrigidos imediatamente.',
                'impact': 'Alto impacto na experiência do usuário'
            })
        
        # Acessibilidade
        accessibility_issues = [i for i in self.issues if i.type == 'accessibility']
        if len(accessibility_issues) > 3:
            recommendations.append({
                'priority': 'Alta',
                'title': 'Melhorar Acessibilidade',
                'description': 'Implementar diretrizes WCAG 2.1 para tornar o site mais acessível.',
                'impact': 'Inclusão de usuários com deficiência'
            })
        
        # Performance
        performance_issues = [i for i in self.issues if i.type == 'performance']
        if len(performance_issues) > 5:
            recommendations.append({
                'priority': 'Média',
                'title': 'Otimizar Performance',
                'description': 'Implementar lazy loading, minificação e compressão de assets.',
                'impact': 'Melhor experiência de carregamento'
            })
        
        return recommendations
    
    def _generate_html_report(self, report):
        """Gera relatório HTML estilizado"""
        severity_colors = {
            'critical': '#EA4335',
            'high': '#FBBC04', 
            'medium': '#F1C232',
            'low': '#6c757d'
        }
        
        issues_html = ''
        for issue in report['detailed_issues']:
            color = severity_colors.get(issue['severity'], '#6c757d')
            issues_html += f"""
            <div class="issue-card" style="border-left: 4px solid {color};">
                <div class="issue-header">
                    <span class="issue-type">{issue['type'].upper()}</span>
                    <span class="issue-severity" style="background: {color};">{issue['severity'].upper()}</span>
                </div>
                <h4>{issue['description']}</h4>
                <p><strong>Arquivo:</strong> {issue['file']}:{issue['line']}</p>
                <p><strong>Sugestão:</strong> {issue['suggestion']}</p>
                <p><strong>Impacto:</strong> {issue['impact']}</p>
            </div>
            """
        
        return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório UX/UI - Dashboard</title>
    <style>
        :root {{
            --primary-color: #F1C232;
            --secondary-color: #f9d71c;
            --dark-bg: #1a1a1a;
            --darker-bg: #0f0f0f;
            --text-light: #ffffff;
            --text-muted: #b0b0b0;
        }}
        
        body {{ 
            font-family: 'Inter', 'Poppins', sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: var(--dark-bg); 
            color: var(--text-light);
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        .header {{ 
            background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 50%, var(--primary-color) 100%); 
            color: var(--text-light); 
            padding: 40px; 
            border-radius: 12px; 
            margin-bottom: 30px;
            border: 1px solid var(--primary-color);
        }}
        
        .score {{ 
            font-size: 3rem; 
            font-weight: 700; 
            text-align: center; 
            color: var(--primary-color);
            text-shadow: 0 0 20px rgba(241, 194, 50, 0.3);
        }}
        
        .score-label {{ font-size: 1.2rem; opacity: 0.9; }}
        
        .stats {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 30px 0; 
        }}
        
        .stat-card {{ 
            background: var(--darker-bg); 
            padding: 20px; 
            border-radius: 8px; 
            border: 1px solid #333;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }}
        
        .stat-number {{ 
            font-size: 2rem; 
            font-weight: bold; 
            color: var(--primary-color); 
        }}
        
        .stat-label {{ color: var(--text-muted); margin-top: 5px; }}
        
        .issue-card {{ 
            background: var(--darker-bg); 
            margin: 15px 0; 
            padding: 20px; 
            border-radius: 8px; 
            border: 1px solid #333;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        .issue-header {{ display: flex; justify-content: space-between; margin-bottom: 10px; }}
        
        .issue-type {{ 
            background: #333; 
            color: var(--text-light);
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 0.8rem; 
        }}
        
        .issue-severity {{ 
            color: var(--darker-bg); 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 0.8rem; 
            font-weight: 600;
        }}
        
        .recommendations {{ 
            background: var(--darker-bg); 
            padding: 30px; 
            border-radius: 8px; 
            margin: 30px 0; 
            border: 1px solid var(--primary-color);
        }}
        
        h1, h2, h3 {{ margin-top: 0; color: var(--text-light); }}
        h2 {{ color: var(--primary-color); }}
        
        .priority-urgente {{ border-left: 4px solid #EA4335; }}
        .priority-alta {{ border-left: 4px solid #FBBC04; }}
        .priority-media {{ border-left: 4px solid var(--primary-color); }}
        .priority-média {{ border-left: 4px solid var(--primary-color); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Relatório UX/UI Dashboard</h1>
            <div class="score">{report['ux_score']}/100</div>
            <div class="score-label">Score UX</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{report['total_issues']}</div>
                <div class="stat-label">Total de Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{report['issues_by_severity'].get('critical', 0)}</div>
                <div class="stat-label">Issues Críticos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{report['issues_by_severity'].get('high', 0)}</div>
                <div class="stat-label">Issues Altos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(report['recommendations'])}</div>
                <div class="stat-label">Recomendações</div>
            </div>
        </div>
        
        <div class="recommendations">
            <h2>📋 Recomendações Prioritárias</h2>
            {''.join([f'<div class="issue-card priority-{rec["priority"].lower()}"><h3>{rec["title"]}</h3><p>{rec["description"]}</p><p><strong>Impacto:</strong> {rec["impact"]}</p></div>' for rec in report['recommendations']])}
        </div>
        
        <div>
            <h2>🔍 Issues Detalhados</h2>
            {issues_html}
        </div>
    </div>
</body>
</html>
        """
    
    def run_full_analysis(self):
        """Executa análise completa"""
        print("🚀 Iniciando análise UX/UI completa...")
        
        self.analyze_html_templates()
        self.analyze_css_files()
        
        return self.generate_ux_report()

if __name__ == "__main__":
    analyzer = UXAnalyzer()
    report = analyzer.run_full_analysis()
    
    print(f"\n🎯 Análise concluída!")
    print(f"Score UX: {report['ux_score']}/100")
    print(f"Total de issues: {report['total_issues']}")
    print(f"Recomendações: {len(report['recommendations'])}")