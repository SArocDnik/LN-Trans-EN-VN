import os
import json
import requests

# Đọc cấu hình từ file settings.json
def load_settings():
    try:
        # Lấy đường dẫn thư mục hiện tại của script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(current_dir, "settings.json")
        
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file settings.json: {e}")
        return None

# Hàm gửi yêu cầu dịch đến API Qwen
def translate_text(text, settings):
    headers = {
        "accept": "*/*",
        "authorization": f"Bearer {settings['API_KEY']}",
        "content-type": "application/json",
    }

    # Tạo payload từ template trong settings.json
    payload = settings["payload_template"]
    payload["messages"][1]["content"] = text  # Thay thế nội dung cần dịch

    try:
        response = requests.post(settings["API_URL"], headers=headers, json=payload)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()

        # Trích xuất nội dung từ phản hồi JSON
        if (
            data
            and "choices" in data
            and isinstance(data["choices"], list)
            and len(data["choices"]) > 0
            and "message" in data["choices"][0]
            and "content" in data["choices"][0]["message"]
        ):
            return data["choices"][0]["message"]["content"]
        else:
            print("Lỗi: Cấu trúc JSON không hợp lệ hoặc thiếu trường bắt buộc.")
            return None
    except Exception as e:
        print(f"Lỗi khi gọi API Qwen: {e}")
        return None

# Hàm dịch tất cả file trong thư mục
def translate_files_in_directory(settings):
    input_dir = settings["directories"]["input_dir"]
    output_dir = settings["directories"]["output_dir"]

    # Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)

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

                print(f"Đang dịch file: {file}")
                translated_text = translate_text(file_content, settings)

                if translated_text:
                    # Lưu kết quả dịch vào file tương ứng trong thư mục đầu ra
                    output_file_path = os.path.join(output_dir, file)
                    with open(output_file_path, "w", encoding="utf-8") as f:
                        f.write(translated_text)
                    print(f"Đã lưu kết quả dịch vào: {output_file_path}")
                else:
                    print(f"Không thể dịch file: {file}")

            else:
                print(f"File không tồn tại: {file}")

        print("Hoàn thành dịch!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Thực hiện dịch các file trong thư mục input
if __name__ == "__main__":
    settings = load_settings()
    if settings:
        translate_files_in_directory(settings)