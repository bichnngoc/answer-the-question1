import os
import pdfplumber
from g4f.client import Client

# Khởi tạo client của `g4f`
client = Client()

# Hàm đọc nội dung từ nhiều file PDF
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

# Hàm đọc nội dung từ file TXT
def read_txt_files_from_directory(directory_path):
    all_data = ""
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    all_data += file.read() + "\n"
            except Exception as e:
                print(f"Không thể đọc tệp TXT {filename}: {str(e)}")
    return all_data

# Hàm tìm kiếm nội dung liên quan trong PDF và TXT dựa trên câu hỏi
def find_relevant_content(question, pdf_text, txt_content):
    relevant_content = ""
    for content in (pdf_text + "\n" + txt_content).split("\n"):
        if any(keyword in content.lower() for keyword in question.lower().split()):
            relevant_content += content + "\n"
    return relevant_content[:2000]  # Giới hạn độ dài chuỗi

# Hàm trả lời câu hỏi dựa trên nội dung liên quan
def generate_response(question, pdf_text, txt_content):
    try:
        # Chỉ lấy nội dung liên quan
        relevant_content = find_relevant_content(question, pdf_text, txt_content)

        # Tạo prompt với nội dung liên quan
        prompt = (
            f"Đây là nội dung liên quan đến câu hỏi từ các tài liệu:\n{relevant_content}\n\n"
            f"Câu hỏi: {question}\nTrả lời:"
        )

        # Gọi mô hình AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

# Đọc nội dung từ các file PDF và TXT
pdf_directory = 'data/'  # Thư mục chứa các file PDF
txt_directory = 'data/'  # Thư mục chứa các file TXT
max_pages = 5

pdf_text = read_pdfs_from_directory(pdf_directory, max_pages)
txt_content = read_txt_files_from_directory(txt_directory)

# Ví dụ sử dụng
if __name__ == "__main__":
    while True:
        question = input("Bạn: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = generate_response(question, pdf_text, txt_content)
        print("Chatbot:", answer)
