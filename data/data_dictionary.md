# Từ điển dữ liệu

Toàn bộ dữ liệu tại `raw/laptops_simulated.csv` là **mô phỏng**.

| Cột | Kiểu | Đơn vị/miền | Vai trò |
|---|---|---|---|
| `laptop_id` | text | duy nhất | Định danh |
| `model` | text | tên giả lập | Hiển thị |
| `os_platform` | category | Windows/macOS/Linux | Hard filter tương thích |
| `price_million_vnd` | float | triệu VNĐ, > 0 | Cost, hard filter ngân sách |
| `cpu_score` | float | điểm mô phỏng, > 0 | Benefit |
| `gpu_score` | float | điểm mô phỏng, > 0 | Benefit |
| `ram_gb` | integer | GB, > 0 | Benefit, hard filter |
| `ssd_gb` | integer | GB, > 0 | Benefit, hard filter |
| `battery_hours` | float | giờ, > 0 | Benefit |
| `weight_kg` | float | kg, > 0 | Cost |
| `simulation_note` | text | nhãn nguồn | Kiểm soát nguồn gốc |

Các model và thông số không đại diện cho sản phẩm thương mại. Điểm CPU/GPU dùng cùng thang mô phỏng nội bộ để minh họa chuẩn hóa và WSM.
