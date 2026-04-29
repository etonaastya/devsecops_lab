#Конвертер отчётов ZAP: JSON → упрощённый текстовый вывод

import json
import sys
from pathlib import Path

def parse_zap_json(report_path: str):
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Отчёт ZAP: {report_path}")
    print(f"Сайт: {data.get('site', 'N/A')}")
    print(f"Всего алертов: {len(data.get('alerts', []))}")
    
    # Группировка по уровню риска
    risk_counts = {}
    for alert in data.get('alerts', []):
        risk = alert.get('risk', 'Unknown')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    print("\nРаспределение по рискам:")
    for risk, count in sorted(risk_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {risk}: {count}")
    
    # Вывод High/Medium алертов
    print("\nКритические находки (High/Medium):")
    for alert in data.get('alerts', []):
        if alert.get('risk') in ['High', 'Medium']:
            print(f"  - [{alert['risk']}] {alert['alert']}")
            print(f"    URL: {alert.get('url', 'N/A')}")
            print(f"    CWE: {alert.get('cweid', 'N/A')}")
            solution = alert.get('solution', 'N/A')
            if len(solution) > 100:
                solution = solution[:100] + "..."
            print(f"    Решение: {solution}")
            print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python convert_reports.py <path_to_zap_report.json>")
        sys.exit(1)
    
    parse_zap_json(sys.argv[1])