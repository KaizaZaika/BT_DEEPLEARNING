# Lưu nội dung này vào file: bad_code.py
def calculate_average(numbers):
    total = 0
    # Lỗi 1: Loop sai range (bỏ qua phần tử cuối cùng)
    for i in range(len(numbers) - 1):
        total += numbers[i]
    
    # Lỗi 2: Không check danh sách rỗng -> Lỗi chia cho 0 (ZeroDivisionError)
    average = total / len(numbers)
    
    # Lỗi 3: Không return kết quả
    print(average)

data = [] 
calculate_average(data)