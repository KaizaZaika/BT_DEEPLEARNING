import ollama
import time
import pandas as pd
import sys

# --- 1. CẤU HÌNH ---
OUTPUT_FILE = "ket_qua_benchmark.xlsx"
MODELS = ['yi-coder:1.5b', 'qwen2.5-coder:1.5b', 'llama3.2:1b']

# --- 2. BỘ DỮ LIỆU TEST (12 Cases - Python, Java, C) ---
TEST_SUITE = [
    # --- PYTHON CASES ---
    {"id": "PY_01", "lang": "Python", "type": "Logic", "name": "Off-by-one Error", 
     "code": "def get_items(arr):\n    # BUG: Index out of range\n    for i in range(len(arr) + 1):\n        print(arr[i])"},
    
    {"id": "PY_02", "lang": "Python", "type": "Security", "name": "SQL Injection", 
     "code": "def login(u, p):\n    # BUG: SQL Injection vulnerability\n    q = f\"SELECT * FROM users WHERE u='{u}' AND p='{p}'\"\n    db.execute(q)"},
    
    {"id": "PY_03", "lang": "Python", "type": "Runtime", "name": "Zero Division", 
     "code": "def average(nums):\n    total = sum(nums)\n    # BUG: Crash if nums is empty\n    return total / len(nums)"},
    
    {"id": "PY_04", "lang": "Python", "type": "Logic", "name": "Mutable Default Arg", 
     "code": "def append_to(num, target=[]):\n    # BUG: target retains value between calls\n    target.append(num)\n    return target"},

    # --- JAVA CASES ---
    {"id": "JAVA_01", "lang": "Java", "type": "Logic", "name": "String Comparison", 
     "code": "public boolean check(String s) {\n    // BUG: Using == instead of .equals\n    if (s == \"password\") return true;\n    return false;\n}"},
    
    {"id": "JAVA_02", "lang": "Java", "type": "Runtime", "name": "Null Pointer", 
     "code": "public int getLen(String s) {\n    // BUG: No null check\n    return s.length();\n}"},
    
    {"id": "JAVA_03", "lang": "Java", "type": "Logic", "name": "Infinite Loop", 
     "code": "public void loop() {\n    // BUG: Decrementing instead of incrementing\n    for (int i = 0; i < 10; i--) {\n        System.out.println(i);\n    }\n}"},
    
    {"id": "JAVA_04", "lang": "Java", "type": "Concurrency", "name": "Race Condition", 
     "code": "public class Counter {\n    private int count = 0;\n    // BUG: Not synchronized\n    public void increment() { count++; }\n}"},

    # --- C/C++ CASES ---
    {"id": "C_01", "lang": "C", "type": "Memory", "name": "Buffer Overflow", 
     "code": "void copy(char *s) {\n    char buf[5];\n    // BUG: Unsafe copy\n    strcpy(buf, s);\n}"},
    
    {"id": "C_02", "lang": "C", "type": "Memory", "name": "Memory Leak", 
     "code": "void process() {\n    int *p = malloc(sizeof(int)*10);\n    p[0] = 1;\n    // BUG: No free(p)\n}"},
    
    {"id": "C_03", "lang": "C", "type": "Logic", "name": "Integer Overflow", 
     "code": "int add(int a, int b) {\n    // BUG: Can overflow if a+b > MAX_INT\n    return a + b;\n}"},
    
    {"id": "C_04", "lang": "C", "type": "Pointer", "name": "Use After Free", 
     "code": "void func() {\n    char *p = malloc(10);\n    free(p);\n    // BUG: Accessing freed memory\n    *p = 'a';\n}"}
]

# --- 3. HÀM CHẠY BENCHMARK ---
def run_benchmark():
    results = []
    total_tasks = len(TEST_SUITE) * len(MODELS)
    current_task = 0

    print(f"🔥 BẮT ĐẦU BENCHMARK: {len(TEST_SUITE)} bài test x {len(MODELS)} model")
    print("-" * 60)

    for case in TEST_SUITE:
        print(f"📂 Đang xử lý: [{case['lang']}] {case['name']}...")
        
        for model in MODELS:
            current_task += 1
            print(f"   [{current_task}/{total_tasks}] Running {model}...", end=" ", flush=True)
            
            try:
                start_time = time.time()
                
                # Prompt tối giản
                prompt = f"Fix this {case['lang']} code. Return ONLY the fixed code block:\n```\n{case['code']}\n```"
                
                # Gọi Model (keep_alive=0 để đo tốc độ thực)
                response = ollama.chat(model=model, keep_alive=0, messages=[
                    {'role': 'user', 'content': prompt}
                ])
                
                duration = round(time.time() - start_time, 2)
                output = response['message']['content']
                
                print(f"✅ Xong ({duration}s)")
                
                # Lưu vào danh sách kết quả
                results.append({
                    "Model": model,
                    "Ngôn ngữ": case["lang"],
                    "Loại lỗi": case["type"],
                    "Bài toán": case["name"],
                    "Thời gian (s)": duration,
                    "Code Sửa (AI Output)": output  # Cột này chứa code để bạn chấm điểm
                })
                
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                results.append({
                    "Model": model,
                    "Ngôn ngữ": case["lang"],
                    "Loại lỗi": case["type"],
                    "Bài toán": case["name"],
                    "Thời gian (s)": 0,
                    "Code Sửa (AI Output)": str(e)
                })

    # --- 4. XUẤT RA EXCEL ---
    print("-" * 60)
    print("💾 Đang lưu file Excel...")
    
    df = pd.DataFrame(results)
    
    # Tính thêm bảng trung bình tốc độ (Pivot Table) để tiện làm biểu đồ
    summary_df = df.pivot_table(index="Model", columns="Ngôn ngữ", values="Thời gian (s)", aggfunc="mean")
    
    # Ghi vào file Excel (2 sheet: Chi tiết & Tóm tắt)
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Chi Tiết', index=False)
        summary_df.to_excel(writer, sheet_name='Tóm Tắt Tốc Độ')
        
    print(f"🎉 HOÀN TẤT! Mở file '{OUTPUT_FILE}' để xem kết quả.")

if __name__ == "__main__":
    run_benchmark()