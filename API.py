import os
from g4f.client import Client
import pdfplumber

# Khởi tạo client của `g4f`
client = Client()

# Hàm đọc nội dung từ nhiều file PDF trong thư mục và giới hạn theo số trang
def read_pdfs_from_directory(directory_path, max_pages=5):
    all_text = ""
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            with pdfplumber.open(file_path) as pdf:
                num_pages = min(len(pdf.pages), max_pages)
                for page_num in range(num_pages):
                    page = pdf.pages[page_num]
                    all_text += page.extract_text() + "\n"
    return all_text

# Hàm đọc dữ liệu từ nhiều file TXT trong thư mục
def read_txt_files_from_directory(directory_path):
    all_data = ""
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):  # Lọc các file .txt
            file_path = os.path.join(directory_path, filename)
            try:
                # Đọc file TXT và chuyển thành chuỗi văn bản
                with open(file_path, 'r', encoding='utf-8') as file:
                    all_data += file.read() + "\n"  # Gộp lại tất cả dữ liệu TXT
                print(f"Đã đọc tệp TXT: {filename}")  # Thêm thông báo khi đọc file TXT
            except Exception as e:
                print(f"Không thể đọc tệp TXT {filename}: {str(e)}")
    return all_data

# Hàm trả lời câu hỏi dựa trên nội dung PDF và TXT
def generate_response(question, pdf_text, txt_content):
    try:
        prompt = (
            f"Đây là nội dung từ các tệp TXT:\n{txt_content}\n\n"
            f"Đây là nội dung từ các tài liệu PDF:\n{pdf_text}\n\n"
            f"Câu hỏi: {question}\nTrả lời:"
        )

        # Gọi mô hình OpenAI để trả lời câu hỏi
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

# Đọc nội dung từ các file PDF và TXT
pdf_directory = 'data/'  # Thư mục chứa các file PDF
txt_directory = 'data/'  # Thư mục chứa các file TXT

max_pages = 5  # Giới hạn số trang đọc từ mỗi file PDF

# Đọc nội dung từ các file PDF và TXT
pdf_text = read_pdfs_from_directory(pdf_directory, max_pages)
txt_content = read_txt_files_from_directory(txt_directory)

# Ví dụ sử dụng
if __name__ == "__main__":
    while True:
        question = input("Bạn: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = generate_response(question, pdf_text, txt_content)
        print("chuyen gia:", answer)
