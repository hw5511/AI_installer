import os
from pathlib import Path


def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def collect_python_files(root_path):
    file_data = []
    total_lines = 0

    root = Path(root_path)

    for py_file in sorted(root.rglob('*.py')):
        if '__pycache__' in str(py_file) or 'build_auto' in str(py_file) or 'dist_auto' in str(py_file):
            continue

        lines = count_lines_in_file(py_file)
        total_lines += lines

        relative_path = py_file.relative_to(root)
        file_data.append((relative_path, lines))

    return file_data, total_lines


def build_directory_tree(file_data):
    tree = {}

    for file_path, lines in file_data:
        parts = file_path.parts
        current = tree

        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = lines
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]

    return tree


def calculate_dir_lines(tree):
    totals = {}

    def recurse(node, path=''):
        total = 0
        for key, value in node.items():
            current_path = f"{path}/{key}" if path else key

            if isinstance(value, int):
                total += value
            else:
                subtotal = recurse(value, current_path)
                total += subtotal
                totals[current_path] = subtotal

        return total

    recurse(tree)
    return totals


def print_tree(tree, dir_totals, prefix='', path=''):
    items = sorted(tree.items())

    for i, (name, value) in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = '└── ' if is_last else '├── '
        current_path = f"{path}/{name}" if path else name

        if isinstance(value, int):
            print(f"{prefix}{connector}{name}  ({value} lines)")
        else:
            total = dir_totals.get(current_path, 0)
            print(f"{prefix}{connector}{name}/  ({total} lines)")

            extension = '    ' if is_last else '│   '
            print_tree(value, dir_totals, prefix + extension, current_path)


def main():
    root_path = Path(__file__).parent.parent

    print("=" * 70)
    print("Simple AI Setup Tool - Python Code Analysis")
    print("=" * 70)
    print()

    file_data, total_lines = collect_python_files(root_path)
    tree = build_directory_tree(file_data)
    dir_totals = calculate_dir_lines(tree)

    print("new_ai_setup/")
    print_tree(tree, dir_totals, '', '')

    print()
    print("=" * 70)
    print(f"Total Python Code Lines: {total_lines:,}")
    print("=" * 70)


if __name__ == '__main__':
    main()
