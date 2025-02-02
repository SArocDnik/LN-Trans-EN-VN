import os
import json
from docx import Document

# Đọc cấu hình từ file settings.json
def load_settings():
    try:
        with open("LN-Trans-EN-VN/Run-by-CMD/source/settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file settings.json: {e}")
        return None

def read_docx(file_path):
    """Đọc nội dung từ file .docx."""
    print(f"Đang kiểm tra file: {os.path.abspath(file_path)}")  # In ra đường dẫn tuyệt đối
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
    try:
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        print(f"Số đoạn văn bản đọc được: {len(paragraphs)}")  # Debug: In số đoạn văn bản
        return paragraphs
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file .docx: {e}")

def split_content(paragraphs, max_chars):
    """
    Chia nhỏ nội dung thành các phần dựa trên quy tắc:
    - Mỗi phần không vượt quá MAX_CHARS ký tự.
    - Nếu đang trong đoạn trích dẫn ("..."), tìm dấu chấm (.) gần nhất để kết thúc.
    - Nếu đang giữa đoạn văn, tìm dấu chấm (.) gần nhất để kết thúc.
    - Loại bỏ đoạn trống hoặc chỉ chứa khoảng trắng.
    """
    chunks = []  # Danh sách chứa các phần đã chia nhỏ
    current_chunk = []  # Phần hiện tại đang xây dựng
    current_char_count = 0  # Số ký tự trong phần hiện tại

    for para in paragraphs:
        # Loại bỏ khoảng trắng thừa và kiểm tra nếu đoạn văn bản trống
        para = para.strip()
        if not para:
            continue  # Bỏ qua đoạn văn bản trống

        # Tính tổng số ký tự nếu thêm đoạn này vào phần hiện tại
        total_chars_if_added = current_char_count + len(para)

        # Nếu thêm đoạn này vượt quá giới hạn ký tự
        if total_chars_if_added > max_chars:
            # Kiểm tra nếu đoạn này là một đoạn trích dẫn
            if para.startswith('"') and para.endswith('"'):
                # Tìm dấu chấm gần nhất trong đoạn trích dẫn
                last_period_index = para.rfind(".")
                if last_period_index != -1:
                    part_to_add = para[:last_period_index + 1].strip()  # Phần trước dấu chấm
                    remaining_part = para[last_period_index + 1:].strip()  # Phần còn lại

                    # Thêm phần đã chia vào chunk hiện tại
                    current_chunk.append(part_to_add)
                    chunks.append("\n".join(current_chunk))

                    # Bắt đầu chunk mới với phần còn lại
                    current_chunk = [remaining_part] if remaining_part else []
                    current_char_count = len(remaining_part) if remaining_part else 0
                else:
                    # Nếu không có dấu chấm, thêm toàn bộ đoạn trích dẫn vào chunk hiện tại
                    current_chunk.append(para)
                    chunks.append("\n".join(current_chunk))
                    current_chunk = []
                    current_char_count = 0
            else:
                # Nếu không phải đoạn trích dẫn, tìm dấu chấm gần nhất trong đoạn
                last_period_index = para.rfind(".")
                if last_period_index != -1:
                    part_to_add = para[:last_period_index + 1].strip()  # Phần trước dấu chấm
                    remaining_part = para[last_period_index + 1:].strip()  # Phần còn lại

                    # Thêm phần đã chia vào chunk hiện tại
                    current_chunk.append(part_to_add)
                    chunks.append("\n".join(current_chunk))

                    # Bắt đầu chunk mới với phần còn lại
                    current_chunk = [remaining_part] if remaining_part else []
                    current_char_count = len(remaining_part) if remaining_part else 0
                else:
                    # Nếu không có dấu chấm, thêm toàn bộ đoạn vào chunk hiện tại
                    current_chunk.append(para)
                    chunks.append("\n".join(current_chunk))
                    current_chunk = []
                    current_char_count = 0
        else:
            # Nếu không vượt quá giới hạn, thêm đoạn vào chunk hiện tại
            current_chunk.append(para)
            current_char_count += len(para)

    # Thêm phần cuối cùng nếu còn
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

def save_part(output_dir, part_index, content):
    """Lưu từng phần vào file .txt riêng biệt."""
    part_file = os.path.join(output_dir, f"part_{part_index}.txt")  # Lưu dưới dạng .txt
    with open(part_file, "w", encoding="utf-8") as f:  # Ghi file với mã hóa UTF-8
        f.write(content)

def main():
    # Đọc cấu hình từ settings.json
    settings = load_settings()
    if not settings:
        print("Không thể tải cấu hình từ settings.json.")
        return

    input_file = settings["directories"]["input_file"]
    output_dir = settings["directories"]["input_dir"]
    max_char_per_part = settings["directories"]["max_char_per_part"]

    # Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Bước 1: Đọc file đầu vào
        print(f"Thư mục hiện tại: {os.getcwd()}")  # In ra thư mục hiện tại
        paragraphs = read_docx(input_file)

        # Bước 2: Chia nhỏ nội dung
        print("Đang chia nhỏ nội dung...")
        chunks = split_content(paragraphs, max_char_per_part)

        # Bước 3: Lưu từng phần vào file .txt riêng biệt
        print("Đang lưu các phần...")
        for i, chunk in enumerate(chunks):
            save_part(output_dir, i + 1, chunk)

        print(f"Chia nhỏ hoàn tất! Các phần đã được lưu vào thư mục {output_dir}")
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()