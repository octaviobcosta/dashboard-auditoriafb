#!/usr/bin/env python3
"""
🚀 DEV ASSISTANT - Seus Superpoderes de Desenvolvimento
Assistente inteligente para automação completa do projeto
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

class DevAssistant:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / "dev-config.json"
        self.load_config()
    
    def load_config(self):
        """Carrega configurações do projeto"""
        default_config = {
            "auto_commit": True,
            "auto_format": True,
            "auto_test": True,
            "monitor_files": ["src/", "templates/", "static/"],
            "performance_tracking": True,
            "ux_analytics": True
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = {**default_config, **json.load(f)}
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Salva configurações"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def analyze_code_quality(self):
        """Análise automática de qualidade do código"""
        print("🔍 Analisando qualidade do código...")
        
        issues = []
        
        # Verifica arquivos Python
        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Verifica complexidade
                if len(lines) > 200:
                    issues.append(f"📝 {py_file.name}: Arquivo muito longo ({len(lines)} linhas)")
                
                # Verifica funções grandes
                function_lines = []
                in_function = False
                for i, line in enumerate(lines):
                    if line.strip().startswith('def '):
                        if in_function and len(function_lines) > 50:
                            issues.append(f"⚡ {py_file.name}:{i}: Função muito longa")
                        function_lines = []
                        in_function = True
                    elif in_function:
                        function_lines.append(line)
        
        return issues
    
    def performance_monitor(self):
        """Monitor de performance do dashboard"""
        print("📊 Monitorando performance...")
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "memory_usage": self.get_memory_usage(),
            "response_time": self.test_response_time(),
            "database_queries": self.analyze_db_queries()
        }
        
        # Salva métricas
        metrics_file = self.project_root / "metrics" / f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        metrics_file.parent.mkdir(exist_ok=True)
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return metrics
    
    def get_memory_usage(self):
        """Verifica uso de memória"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'python' in line and 'app.py' in line:
                    parts = line.split()
                    return float(parts[3]) if len(parts) > 3 else 0
        except:
            pass
        return 0
    
    def test_response_time(self):
        """Testa tempo de resposta"""
        import requests
        try:
            start_time = time.time()
            response = requests.get('http://localhost:5000', timeout=5)
            end_time = time.time()
            return (end_time - start_time) * 1000  # ms
        except:
            return -1
    
    def analyze_db_queries(self):
        """Analisa queries do banco"""
        # Placeholder para análise de queries
        return {"slow_queries": 0, "total_queries": 0}
    
    def auto_optimize(self):
        """Otimização automática do código"""
        print("⚡ Executando otimizações automáticas...")
        
        optimizations = []
        
        # Remove imports não utilizados
        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                result = subprocess.run(['autoflake', '--check', str(py_file)], 
                                     capture_output=True, text=True)
                if result.returncode != 0:
                    optimizations.append(f"🧹 {py_file.name}: Imports não utilizados detectados")
            except:
                pass
        
        return optimizations
    
    def ux_analysis(self):
        """Análise UX/UI automática"""
        print("🎨 Analisando UX/UI...")
        
        ux_issues = []
        
        # Analisa templates HTML
        for template in self.project_root.rglob("*.html"):
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Verifica acessibilidade
                if 'alt=' not in content and '<img' in content:
                    ux_issues.append(f"♿ {template.name}: Imagens sem texto alternativo")
                
                # Verifica responsividade
                if 'viewport' not in content:
                    ux_issues.append(f"📱 {template.name}: Meta viewport ausente")
                
                # Verifica contraste
                if 'color:' in content and 'background' in content:
                    ux_issues.append(f"🌈 {template.name}: Verificar contraste de cores")
        
        return ux_issues
    
    def generate_report(self):
        """Gera relatório completo"""
        print("📋 Gerando relatório completo...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "code_quality": self.analyze_code_quality(),
            "performance": self.performance_monitor(),
            "optimizations": self.auto_optimize(),
            "ux_analysis": self.ux_analysis()
        }
        
        # Gera relatório HTML
        html_report = self.generate_html_report(report)
        report_file = self.project_root / "reports" / f"dev_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ Relatório salvo em: {report_file}")
        return report
    
    def generate_html_report(self, report):
        """Gera relatório HTML bonito"""
        return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Dev Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }}
        .section {{ margin: 30px 0; padding: 20px; background: #f9f9f9; border-radius: 6px; }}
        .issue {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; }}
        .success {{ background: #d4edda; border-left: 4px solid #28a745; padding: 10px; margin: 10px 0; }}
        .metric {{ display: inline-block; background: #007acc; color: white; padding: 10px 15px; margin: 5px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Dashboard Development Report</h1>
        <p><strong>Gerado em:</strong> {report['timestamp']}</p>
        
        <div class="section">
            <h2>📊 Métricas de Performance</h2>
            <div class="metric">Memória: {report['performance']['memory_usage']:.1f}%</div>
            <div class="metric">Tempo Resposta: {report['performance']['response_time']:.0f}ms</div>
        </div>
        
        <div class="section">
            <h2>🔍 Qualidade do Código</h2>
            {self._format_issues(report['code_quality'])}
        </div>
        
        <div class="section">
            <h2>🎨 Análise UX/UI</h2>
            {self._format_issues(report['ux_analysis'])}
        </div>
        
        <div class="section">
            <h2>⚡ Otimizações Sugeridas</h2>
            {self._format_issues(report['optimizations'])}
        </div>
    </div>
</body>
</html>
        """
    
    def _format_issues(self, issues):
        """Formata issues para HTML"""
        if not issues:
            return '<div class="success">✅ Nenhum problema encontrado!</div>'
        
        html = ""
        for issue in issues:
            html += f'<div class="issue">{issue}</div>'
        return html

if __name__ == "__main__":
    assistant = DevAssistant()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "analyze":
            assistant.analyze_code_quality()
        elif command == "monitor":
            assistant.performance_monitor()
        elif command == "optimize":
            assistant.auto_optimize()
        elif command == "ux":
            assistant.ux_analysis()
        elif command == "report":
            assistant.generate_report()
    else:
        print("🚀 Dev Assistant - Escolha uma opção:")
        print("python dev-assistant.py analyze   - Análise de código")
        print("python dev-assistant.py monitor   - Monitor de performance")
        print("python dev-assistant.py optimize  - Otimizações automáticas")
        print("python dev-assistant.py ux        - Análise UX/UI")
        print("python dev-assistant.py report    - Relatório completo")