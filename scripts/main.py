import os
import json
import argparse
import shutil


# Đường dẫn cơ sở và thư mục addons/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(BASE_DIR, 'export')
os.makedirs(EXPORT_DIR, exist_ok=True)
ADDONS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'addons'))

# Đọc nội dung các file trong folder
def collect_files_content(root_folder):
    excluded_dirs = {'.git', '__pycache__', '.vscode', '.idea', 'node_modules'}
    files_dict = {}
    for foldername, dirnames, filenames in os.walk(root_folder):
        # Loại bỏ thư mục không mong muốn
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            rel_path = os.path.relpath(file_path, root_folder)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                content = '[binary or non-text file]'
            files_dict[rel_path] = content
    return files_dict


# Ghi cấu trúc thư mục dạng cây (Markdown)
def write_folder_structure(root_folder, output_file):
    def tree(dir_path, prefix=''):
        entries = sorted(os.listdir(dir_path))
        entries = [e for e in entries if not e.startswith('.')]
        pointers = ['├──'] * (len(entries) - 1) + ['└──']
        for pointer, name in zip(pointers, entries):
            path = os.path.join(dir_path, name)
            yield f"{prefix}{pointer} {name}\n"
            if os.path.isdir(path):
                extension = '│   ' if pointer == '├──' else '    '
                yield from tree(path, prefix + extension)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Structure of `{os.path.basename(root_folder)}`\n\n")
        f.write("```\n")
        f.write(f"{os.path.basename(root_folder)}/\n")
        for line in tree(root_folder):
            f.write(line)
        f.write("```\n")

# Ghi tổng hợp: cấu trúc + nội dung file (Markdown)
def write_combined_structure_and_content(root_folder, content_dict, output_file):
    def tree_lines(dir_path, prefix=''):
        entries = sorted(os.listdir(dir_path))
        entries = [e for e in entries if not e.startswith('.') and e not in {'__pycache__'}]
        pointers = ['├──'] * (len(entries) - 1) + ['└──']
        for pointer, name in zip(pointers, entries):
            path = os.path.join(dir_path, name)
            line = f"{prefix}{pointer} {name}\n"
            yield line
            if os.path.isdir(path):
                extension = '│   ' if pointer == '├──' else '    '
                yield from tree_lines(path, prefix + extension)

    def detect_lang(filename):
        ext = os.path.splitext(filename)[1]
        return {
            '.py': 'python',
            '.xml': 'xml',
            '.json': 'json',
            '.js': 'javascript',
            '.css': 'css',
            '.html': 'html',
            '.csv': 'csv',
        }.get(ext, 'text')

    with open(output_file, 'w', encoding='utf-8') as f:
        # Header: structure
        f.write(f"# Structure of `{os.path.basename(root_folder)}`\n\n")
        f.write("```\n")
        f.write(f"{os.path.basename(root_folder)}/\n")
        for line in tree_lines(root_folder):
            f.write(line)
        f.write("```\n\n")
        f.write("---\n\n")

        # Nội dung file
        f.write("# File Contents\n\n")
        for rel_path, content in content_dict.items():
            lang = detect_lang(rel_path)
            f.write(f"## `{rel_path}`\n\n")
            f.write(f"```{lang}\n")
            f.write(content.strip() + "\n")
            f.write("```\n\n")

def copy_to_downloads(file_path):
    downloads_root = "/mnt/c/Users"
    excluded_users = {"default", "all users", "public", "default user", "desktop.ini", "wsiaccount"}

    try:
        possible_users = os.listdir(downloads_root)
    except FileNotFoundError:
        print("⚠️ Không thể truy cập ổ C: từ WSL.")
        return

    for user in possible_users:
        if user.lower() in excluded_users:
            continue

        user_downloads = os.path.join(downloads_root, user, "Downloads")
        if os.path.isdir(user_downloads) and os.access(user_downloads, os.W_OK):
            export_dir = os.path.join(user_downloads, "export")
            os.makedirs(export_dir, exist_ok=True)  # ✅ tạo nếu chưa có

            dest_path = os.path.join(export_dir, os.path.basename(file_path))
            try:
                shutil.copy2(file_path, dest_path)
                print(f"📁 Đã sao chép tới: {dest_path}")
            except Exception as e:
                print(f"⚠️ Không thể sao chép tới {export_dir}: {e}")
            return

    print("⚠️ Không tìm thấy thư mục Downloads hợp lệ.")

# Chương trình chính
def main():
    parser = argparse.ArgumentParser(description="Export Odoo addon structure and content")
    parser.add_argument('--full', action='store_true', help='Chỉ xuất file Markdown tổng hợp (structure + content)')
    args = parser.parse_args()

    # Liệt kê thư mục trong addons/
    folders = [f for f in os.listdir(ADDONS_DIR) if os.path.isdir(os.path.join(ADDONS_DIR, f))]
    if not folders:
        print("❌ Không có thư mục nào trong addons/")
        return

    # Hiển thị danh sách
    print("Chọn thư mục:")
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    try:
        choice = int(input("Nhập số thứ tự thư mục: ").strip())
        folder_name = folders[choice - 1]
    except (ValueError, IndexError):
        print("❌ Lựa chọn không hợp lệ.")
        return

    target_dir = os.path.join(ADDONS_DIR, folder_name)
    content_data = collect_files_content(target_dir)

    # Nếu chỉ xuất bản đầy đủ
    if args.full:
        full_md_path = os.path.join(EXPORT_DIR, f"{folder_name}_full.md")
        write_combined_structure_and_content(target_dir, content_data, full_md_path)
        print(f"✅ Đã lưu tổng hợp Markdown vào {full_md_path}")
        copy_to_downloads(full_md_path)
        return

    # Ngược lại: tạo cả 3 file
    json_path = os.path.join(EXPORT_DIR, f"{folder_name}_content.json")
    structure_md_path = os.path.join(EXPORT_DIR, f"{folder_name}_structure.md")
    full_md_path = os.path.join(EXPORT_DIR, f"{folder_name}_full.md")

    with open(json_path, 'w', encoding='utf-8') as f_json:
        json.dump(content_data, f_json, ensure_ascii=False, indent=2)
    print(f"✅ Đã lưu nội dung file vào {json_path}")
    copy_to_downloads(json_path)

    write_folder_structure(target_dir, structure_md_path)
    print(f"✅ Đã lưu cấu trúc thư mục vào {structure_md_path}")
    copy_to_downloads(json_path)

    write_combined_structure_and_content(target_dir, content_data, full_md_path)
    print(f"✅ Đã lưu tổng hợp Markdown vào {full_md_path}")
    copy_to_downloads(json_path)

if __name__ == "__main__":
    main()
