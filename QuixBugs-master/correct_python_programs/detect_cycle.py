import streamlit as st
import ollama
import time
import pandas as pd

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Logic & Syntax Benchmark", layout="wide")
st.title("⚡ Benchmark: Lỗi Logic & Syntax Phổ Biến")

MODELS = ['yi-coder:1.5b', 'qwen2.5-coder:1.5b', 'llama3.2:1b']

# --- 2. BỘ DỮ LIỆU "LỖI KINH ĐIỂN" (Hardcoded) ---
DATASET = [
    {
        "name": "Python_IndexError.py",
        "lang": "Python",
        "desc": "Lỗi vòng lặp chạy quá độ dài mảng (Off-by-one)",
        "code": """def print_list(items):
    # BUG: range(len(items) + 1) sẽ gây lỗi 'Index out of range' ở vòng lặp cuối
    for i in range(len(items) + 1):
        print(items[i])"""
    },
    {
        "name": "Java_StringCompare.java",
        "lang": "Java",
        "desc": "Lỗi so sánh chuỗi sai (Dùng == thay vì equals)",
        "code": """public class CheckLogin {
    public boolean check(String inputPass) {
        String secret = "123456";
        // BUG: Trong Java, so sánh nội dung chuỗi phải dùng .equals(), dùng == là sai
        if (inputPass == secret) {
            return true;
        }
        return false;
    }
}"""
    },
    {
        "name": "C_IntegerDivision.c",
        "lang": "C",
        "desc": "Lỗi chia số nguyên (Kết quả bị mất phần thập phân)",
        "code": """#include <stdio.h>
int main() {
    int a = 5;
    int b = 2;
    // BUG: Chia 2 số nguyên (5/2) sẽ ra 2 thay vì 2.5. Phải ép kiểu float.
    float result = a / b; 
    printf("Result: %f", result);
    return 0;
}"""
    }
]

# --- 3. HÀM CHẠY BENCHMARK ---
def run_benchmark():
    st.info("🚀 Đang chạy test trên 3 model... Vui lòng đợi.")
    
    results = []
    progress = st.progress(0)
    table_area = st.empty()
    
    total_steps = len(DATASET) * len(MODELS)
    step = 0
    
    for item in DATASET:
        for model in MODELS:
            try:
                start = time.time()
                
                # Prompt yêu cầu sửa lỗi
                prompt = f"Fix the bug in this {item['lang']} code:\n```\n{item['code']}\n```"
                
                # Gọi AI (keep_alive=0 để đo tốc độ thực)
                ollama.chat(model=model, keep_alive=0, messages=[
                    {'role': 'user', 'content': prompt}
                ])
                
                dur = round(time.time() - start, 2)
                
                results.append({
                    "Model": model,
                    "Language": item['lang'],
                    "Bug Type": item['desc'],
                    "Time (s)": dur
                })
                
            except Exception as e:
                results.append({"Model": model, "Time (s)": 0})
            
            step += 1
            progress.progress(step / total_steps)
            
            # Cập nhật bảng realtime
            table_area.dataframe(pd.DataFrame(results), use_container_width=True)

    progress.empty()
    st.success("✅ Hoàn tất!")
    return pd.DataFrame(results)

# --- 4. GIAO DIỆN ---
st.markdown("### Dữ liệu Test (Logic & Syntax)")
col1, col2, col3 = st.columns(3)
with col1: st.code(DATASET[0]['code'], language='python')
with col2: st.code(DATASET[1]['code'], language='java')
with col3: st.code(DATASET[2]['code'], language='c')

if st.button("🔥 CHẠY BENCHMARK NGAY", type="primary"):
    df = run_benchmark()
    
    st.divider()
    st.subheader("📊 Kết quả Hiệu năng")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Tốc độ trung bình (Giây)**")
        avg = df.groupby("Model")["Time (s)"].mean().sort_values()
        st.bar_chart(avg, color="#FF4B4B")
        
    with c2:
        st.markdown("**Bảng chi tiết**")
        st.dataframe(df, use_container_width=True)