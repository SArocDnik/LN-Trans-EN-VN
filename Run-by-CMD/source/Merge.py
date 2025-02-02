import os
import json
from docx import Document

# Đọc cấu hình từ file settings.json
def load_settings():
    try:
        with open("Translate-Light-Novel-to-Vietnamese-using-AI-IDE/source/settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file settings.json: {e}")
        return None

# Gộp tất cả các file .txt thành một file .docx
def merge_files_to_docx(input_dir, output_file):
    """
    Gộp tất cả các file .txt trong thư mục input_dir thành một file .docx.
    """
    # Tạo đối tượng Document mới
    doc = Document()

    try:
        # Lấy danh sách tất cả file trong thư mục đầu vào
        files = [f for f in os.listdir(input_dir) if f.startswith("part_") and f.endswith(".txt")]

        # Sắp xếp file theo thứ tự tăng dần của số <num> trong tên file
        files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

        print(f"Tìm thấy {len(files)} file trong thư mục {input_dir}.")

        for file in files:
            file_path = os.path.join(input_dir, file)

            # Kiểm tra nếu file tồn tại
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                print(f"Đang thêm nội dung từ file: {file}")

                # Thêm nội dung vào tài liệu Word
                doc.add_paragraph(file_content)
            else:
                print(f"File không tồn tại: {file}")

        # Lưu tài liệu Word vào file đầu ra
        doc.save(output_file)
        print(f"Đã gộp tất cả các file thành: {output_file}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Hàm chính để thực hiện quy trình
def main():
    settings = load_settings()
    if not settings:
        print("Không thể tải cấu hình từ settings.json.")
        return

    directories = settings["directories"]
    input_dir = directories["output_dir"]
    output_file = directories["output_file"]

    # Gộp các file .txt thành một file .docx
    merge_files_to_docx(input_dir, output_file)

if __name__ == "__main__":
    main()