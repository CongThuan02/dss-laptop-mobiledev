# DSS lựa chọn laptop cho sinh viên lập trình di động

**Học viên:** Hoàng Công Thuận – **2528105014**

Project dùng hard filter + min–max + WSM để xếp hạng laptop mô phỏng theo Android, iOS hoặc cross-platform. Bảy tiêu chí: giá, CPU, GPU, RAM, SSD, pin và khối lượng. Nền tảng Windows/macOS/Linux là điều kiện tương thích.

> Toàn bộ laptop và thông số là dữ liệu mô phỏng, không dùng để mua hàng thực tế.

## Chạy nhanh trên macOS/Linux

```bash
cd /Users/hoangthuan/learn/ho_tro_ra_quyet_dinh/HoangCongThuan
chmod +x run.sh
./run.sh
```

Sau đó mở: <http://127.0.0.1:5000>.

`./run.sh` dùng Flask dev server nên sẽ in dòng "WARNING: This is a development server..." — bình thường, không phải lỗi, phù hợp chạy local/demo/chấm bài.

Muốn bỏ cảnh báo và chạy bằng WSGI server thật (Gunicorn, dùng khi có nhiều người truy cập cùng lúc):

```bash
chmod +x run_prod.sh
./run_prod.sh
```

## Dùng dữ liệu của riêng bạn

1. Bấm **"Tải file mẫu (CSV)"** trên giao diện (hoặc mở `/mau-du-lieu`) để tải `mau_du_lieu_laptop.csv`.
2. Điền/thay các dòng ví dụ bằng laptop bạn muốn so sánh, giữ nguyên tên cột (`laptop_id, model, os_platform, price_million_vnd, cpu_score, gpu_score, ram_gb, ssd_gb, battery_hours, weight_kg`).
3. Chọn file đã điền ở mục **"Tải lên file đã điền"** rồi bấm **"Phân tích lại"**. Hệ thống áp dụng đúng hard filter + min–max + WSM lên các dòng bạn cung cấp.
4. Đổi kịch bản/ngân sách/nền tảng ở các lần submit sau không cần tải lại file. Bấm **"Dùng lại dữ liệu mặc định"** để quay về 24 laptop mô phỏng.

File không đúng cột hoặc có dữ liệu không hợp lệ sẽ hiện thông báo lỗi cụ thể và giữ nguyên dữ liệu đang dùng.

## Chạy từng bước

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python src/run_analysis.py
python app.py
```

## Cấu trúc

```text
├── 01_DE_XUAT_VA_DAC_TA.md       # Đặc tả đã xác nhận
├── app.py                         # Giao diện Flask
├── data/
│   ├── raw/laptops_simulated.csv # 24 phương án mô phỏng
│   ├── template/mau_du_lieu_dau_vao.csv # File mẫu để người dùng tự điền và tải lên
│   └── data_dictionary.md
├── diagrams/drawio/               # 6 sơ đồ Draw.io và ảnh PNG
├── report/BAO_CAO_THEO_MAU_DIEM_B_new.md
├── report/HoangCongThuan_DiemA.docx  # Báo cáo cuối, đúng mẫu Điểm A
├── results/                       # Kết quả tái lập CSV/JSON
├── src/dss/model.py               # Lõi hard filter/min–max/WSM
├── src/run_analysis.py            # Phân tích hàng loạt và What-if
├── static/ và templates/          # Giao diện
└── tests/test_model.py            # Kiểm thử tự động
```

## Kết quả mặc định

Với Android, ngân sách 40 triệu, RAM ≥ 16 GB, SSD ≥ 512 GB và kịch bản cân bằng: 18/24 phương án hợp lệ; Top 1 là **L14 – Penguin Pro 14**, điểm **0,677627**. Kết quả chỉ có ý nghĩa trong tập dữ liệu mô phỏng.
