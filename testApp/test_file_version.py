import sys
import json
from collections import defaultdict

def parse_version(version_str):
    """Преобразует строку версии в список целых чисел."""
    return [int(part) for part in version_str.split('.')]

def generate_versions(template):
    """Генерирует две версии на основе шаблона."""
    return [
        template.replace('*', '1'),
        template.replace('*', '2')
    ]

def normalize_version(version, max_parts):
    """Дополняет версию нулями до указанной длины."""
    parts = parse_version(version)
    return parts + [0] * (max_parts - len(parts))

def main():
    if len(sys.argv) != 3:
        print("Использование: python script.py <версия> <файл_конфига>")
        sys.exit(1)
    
    input_ver_str = sys.argv[1]
    config_file = sys.argv[2]
    
    # Чтение и парсинг конфигурационного файла
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        sys.exit(1)
    
    # Извлечение шаблонов из конфигурации
    templates = list(config_data.values())
    
    # Генерация всех версий
    all_versions = []
    for template in templates:
        all_versions.extend(generate_versions(template))
    
    # Определение максимальной длины версии
    all_version_strings = all_versions + [input_ver_str]
    max_parts = max(len(parse_version(v)) for v in all_version_strings)
    
    # Нормализация версий для сравнения
    input_ver_normalized = normalize_version(input_ver_str, max_parts)
    normalized_versions = []
    for ver in all_versions:
        normalized = normalize_version(ver, max_parts)
        normalized_versions.append((ver, normalized))
    
    # Сортировка по нормализованным версиям
    sorted_versions = sorted(normalized_versions, key=lambda x: x[1])
    
    # Вывод отсортированных версий
    print("Отсортированный список всех полученных номеров:")
    for ver, _ in sorted_versions:
        print(ver)
    
    # Фильтрация старых версий
    older_versions = [
        ver for ver, norm in normalized_versions 
        if norm < input_ver_normalized
    ]
    
    # Вывод старых версий
    print(f"\nСписок номеров меньше(старее) версии {input_ver_str}:")
    for ver in older_versions:
        print(ver)

if __name__ == "__main__":
    main()