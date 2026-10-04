#!/usr/bin/env python3
"""Sắp xếp báo cáo theo mục lục của DSS_Mau_Diem_B.pdf."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "report" / "BAO_CAO.md").read_text(encoding="utf-8")
front = source.split("# 1. Giới thiệu", 1)[0]
tail = "# 5. Dữ liệu và tiền xử lý" + source.split("# 5. Dữ liệu và tiền xử lý", 1)[1]

chapters = r'''# CHƯƠNG I. GIỚI THIỆU

## 1. Bối cảnh bài toán

### 1.1. Thực trạng lựa chọn laptop của sinh viên CNTT

Laptop là công cụ học tập chính của nhiều sinh viên CNTT. Đối với lập trình di động, máy phải chạy đồng thời IDE, trình biên dịch, dịch vụ nền và một hoặc nhiều emulator. Nhu cầu này làm cho RAM, CPU và SSD quan trọng hơn so với tác vụ văn phòng thông thường. Tuy nhiên, sinh viên còn bị giới hạn bởi ngân sách và thường xuyên mang máy đến lớp nên pin và khối lượng cũng cần được xem xét.

Thị trường có nhiều cấu hình và nền tảng khác nhau. Nếu chỉ so sánh giá, sinh viên có thể chọn máy thiếu tài nguyên; nếu chỉ chọn hiệu năng cao nhất, chi phí, pin và khối lượng có thể không phù hợp. Đây là quyết định đa tiêu chí có sự đánh đổi giữa lợi ích và chi phí.

### 1.2. Những vấn đề cấp thiết và thách thức

Nền tảng hệ điều hành tạo ra một ràng buộc không thể xử lý đơn thuần bằng cộng điểm. Android Studio và bộ công cụ Android có thể vận hành trên Windows, macOS hoặc Linux. Ngược lại, quy trình build iOS cục bộ bằng Xcode phụ thuộc macOS. Một máy Windows có hiệu năng cao vẫn không khả thi nếu sinh viên bắt buộc build và kiểm thử iOS cục bộ.

Các tiêu chí còn có đơn vị khác nhau: giá tính bằng triệu đồng, RAM/SSD tính bằng GB, pin tính bằng giờ, khối lượng tính bằng kg và hiệu năng dùng điểm. Quyết định cũng thay đổi theo người dùng: người ưu tiên build nhanh khác người ưu tiên pin hoặc ngân sách. DSS phù hợp vì kết hợp dữ liệu, mô hình và tương tác để hỗ trợ bài toán bán cấu trúc (Trần Thị Hòa, 2025).

## 2. Mục tiêu của hệ thống DSS

### 2.1. Mục tiêu tổng quát

Xây dựng một DSS minh bạch và chạy được, hỗ trợ sinh viên CNTT lọc, đánh giá và xếp hạng laptop theo ngân sách, mục tiêu nền tảng và nhu cầu lập trình di động. Hệ thống chỉ cung cấp thông tin hỗ trợ; quyết định mua cuối cùng thuộc về sinh viên.

### 2.2. Mục tiêu cụ thể

- Xây dựng tập 24 laptop mô phỏng, gắn nhãn nguồn gốc rõ ràng.
- Đánh giá theo bảy tiêu chí: giá, CPU, GPU, RAM, SSD, pin và khối lượng.
- Xử lý Windows/macOS/Linux như điều kiện tương thích nền tảng.
- Áp dụng hard filter, min–max và Weighted Sum Model (WSM).
- Cung cấp Top 5, bảng xếp hạng và lý do loại cho từng phương án.
- Phân tích What-if theo trọng số, ngân sách và mục tiêu Android/iOS.
- Xây dựng giao diện web, code Python, kiểm thử và phụ lục tái lập.

### 2.3. Phạm vi nghiên cứu

Project dùng dữ liệu mô phỏng và ngân sách mặc định 40 triệu đồng. Điểm CPU, GPU và pin nằm trên thang mô phỏng nội bộ. Hệ thống không đo benchmark thật, không thu thập giá thị trường và không dự đoán độ bền; vì vậy kết quả không phải tư vấn mua hàng thực tế.

# CHƯƠNG II. TỔNG QUAN HỆ HỖ TRỢ RA QUYẾT ĐỊNH

## 1. Khái niệm Hệ hỗ trợ ra quyết định

### 1.1. Khái niệm

DSS là hệ thống thông tin tương tác sử dụng dữ liệu và mô hình để hỗ trợ người dùng giải quyết vấn đề, đặc biệt với quyết định bán cấu trúc hoặc phi cấu trúc. DSS giúp khảo sát phương án, kiểm tra giả định và phân tích hậu quả của thay đổi tham số nhưng không thay thế hoàn toàn người ra quyết định (Trần Thị Hòa, 2025).

### 1.2. Các thành phần cơ bản của DSS

- **Data Management Subsystem:** quản lý laptop, tiêu chí, ngưỡng, trọng số và kết quả.
- **Model Management Subsystem:** kiểm tra dữ liệu, hard filter, chuẩn hóa, WSM và What-if.
- **User Interface/Dialogue Subsystem:** tiếp nhận nhu cầu và trình bày xếp hạng, điểm, lý do loại.

Ba phân hệ tách trách nhiệm nhưng liên kết qua lớp ứng dụng. CSV không chứa logic tính điểm; giao diện không tự tính WSM; model không quyết định thay người dùng.

## 2. Phân loại

### 2.1. Phân loại bài toán quyết định

Quyết định có cấu trúc có quy tắc và đầu vào rõ; quyết định phi cấu trúc phụ thuộc nhiều vào phán đoán; quyết định bán cấu trúc kết hợp hai phần. Bài toán chọn laptop là bán cấu trúc. Ngưỡng, công thức và xếp hạng là phần có cấu trúc; việc chọn trọng số, mục tiêu nền tảng và chấp nhận đánh đổi là phần cần phán đoán.

### 2.2. Vai trò của DSS trong lựa chọn thiết bị học tập

DSS giúp chuẩn hóa so sánh, làm rõ tiêu chí benefit/cost, loại phương án không khả thi và giải thích vì sao thứ hạng thay đổi. What-if cho phép sinh viên thấy tác động khi giảm ngân sách, ưu tiên hiệu năng hoặc chuyển từ Android sang iOS. Giá trị của DSS nằm ở tính minh bạch và linh hoạt, không nằm ở việc tuyên bố một máy tốt nhất cho mọi người.

## 3. Mô hình Tổng trọng số (Weighted Sum Model – WSM) trong DSS

WSM phù hợp khi có tập phương án hữu hạn và các tiêu chí có thể chuẩn hóa. Giá trị chuẩn hóa được nhân với trọng số rồi cộng thành điểm tổng. Phương pháp đơn giản, nhanh và dễ giải thích nhưng giả định tuyến tính và cho phép bù trừ giữa tiêu chí. Project áp dụng hard filter trước WSM để ngăn một máy không đáp ứng ngân sách, RAM, SSD hoặc nền tảng được bù bởi tiêu chí khác.

# CHƯƠNG III. PHÂN TÍCH BÀI TOÁN RA QUYẾT ĐỊNH

## 1. Mô tả bài toán ra quyết định

Câu hỏi là: “Trong tập laptop mô phỏng, phương án nào phù hợp nhất với ngân sách tối đa 40 triệu đồng, mục tiêu nền tảng và ưu tiên của sinh viên lập trình di động?”. Người dùng chính là sinh viên; cố vấn có thể hỗ trợ thiết lập trọng số. Đầu ra gồm danh sách bị loại, bảng xếp hạng, Top 5 và so sánh What-if.

## 2. Các mục tiêu của bài toán

- Tối đa hóa khả năng chạy IDE, emulator và tác vụ build qua CPU, GPU, RAM, SSD.
- Kiểm soát chi phí trong giới hạn ngân sách sinh viên.
- Tăng tính di động thông qua pin cao và khối lượng thấp.
- Bảo đảm tương thích nền tảng đối với Android, iOS hoặc cross-platform.
- Cung cấp giải thích và cho phép thay đổi ưu tiên.

## 3. Các ràng buộc và tiêu chí đánh giá (Criteria)

| STT | Tiêu chí | Cột dữ liệu | Đơn vị | Loại | Ràng buộc mặc định |
|---:|---|---|---|---|---|
| 1 | Giá | `price_million_vnd` | triệu VNĐ | Cost | ≤ 40 triệu |
| 2 | CPU | `cpu_score` | điểm mô phỏng | Benefit | Không có ngưỡng |
| 3 | GPU | `gpu_score` | điểm mô phỏng | Benefit | Không có ngưỡng |
| 4 | RAM | `ram_gb` | GB | Benefit | ≥ 16 GB |
| 5 | SSD | `ssd_gb` | GB | Benefit | ≥ 512 GB |
| 6 | Pin | `battery_hours` | giờ mô phỏng | Benefit | Không có ngưỡng |
| 7 | Khối lượng | `weight_kg` | kg | Cost | Không có ngưỡng |

`os_platform` là điều kiện phân loại, không cộng điểm. Android chấp nhận Windows/macOS/Linux; iOS hoặc cross-platform có build iOS cục bộ yêu cầu macOS để sử dụng Xcode.

## 4. Quy trình ra quyết định trong hệ thống

1. Chọn mục tiêu Android, iOS hoặc cross-platform.
2. Nhập ngân sách, RAM và SSD tối thiểu.
3. Chọn kịch bản cân bằng, hiệu năng, tiết kiệm hoặc di động.
4. Đọc, chuyển kiểu và kiểm tra dữ liệu.
5. Lọc cứng và lưu toàn bộ lý do loại.
6. Tính min/max trên tập phương án hợp lệ.
7. Chuẩn hóa, tính đóng góp và điểm WSM.
8. Sắp xếp, hiển thị Top 5 và bảng đầy đủ.
9. Thay đổi tham số để phân tích What-if.

# CHƯƠNG IV. THIẾT KẾ HỆ THỐNG DSS

## 1. Cơ sở thiết kế hệ thống

Thiết kế dựa trên kiến trúc DSS kinh điển gồm Data–Model–Interface và quy trình phát triển lặp. Mục tiêu thiết kế là minh bạch, mô-đun, tái lập và dễ trình diễn. Cùng một lõi `model.py` phục vụ CLI và giao diện để tránh sai khác kết quả.

## 2. Kiến trúc tổng thể của hệ thống

Hệ thống sử dụng ba lớp: Presentation (Flask/Jinja/CSS), Application (controller) và Data (CSV/JSON). Model Management chứa validation, hard filter, min–max, WSM và What-if. Data Management lưu dữ liệu mô phỏng, cấu hình và kết quả.

![Hình 4.1. Sơ đồ khối kiến trúc tổng thể hệ thống](diagrams/drawio/exported/01-kien-truc-tong-the.png){width=90%}

## 3. Thiết kế tầng User Interface Subsystem

Giao diện ưu tiên thao tác đơn giản, thông tin giải thích và cảnh báo dữ liệu mô phỏng. Hệ thống mặc định chạy cục bộ tại `127.0.0.1:5000`.

### 3.1. Các màn hình chính

- Màn hình thiết lập mục tiêu Android/iOS/cross-platform.
- Biểu mẫu ngân sách, RAM và SSD tối thiểu.
- Danh sách kịch bản trọng số.
- Khu vực Top 5 và bảng xếp hạng đầy đủ.
- Khu vực hiển thị trọng số và lý do loại.
- Thông báo khi không còn phương án hợp lệ.

### 3.2. Sơ đồ Use Case

Actor chính là Sinh viên; Cố vấn hỗ trợ chọn kịch bản và What-if; Quản trị dữ liệu duy trì tập mô phỏng. Các use case cấu hình đều dẫn tới use case chạy hard filter và WSM.

![Hình 4.2. Use Case Diagram](diagrams/drawio/exported/02-use-case.png){width=90%}

### 3.3. Sơ đồ Activity Diagram

Activity Diagram mô tả nhánh đạt/không đạt hard filter, trường hợp tập hợp lệ rỗng và vòng lặp What-if. Hệ thống không tính WSM nếu không còn phương án.

![Hình 4.3. Activity Diagram quy trình ra quyết định](diagrams/drawio/exported/03-activity.png){width=90%}

## 4. Thiết kế tầng Data Management Subsystem

Dữ liệu gốc nằm tại `data/raw/laptops_simulated.csv` và không bị ghi đè. Module đọc dữ liệu kiểm tra cột bắt buộc, ID duy nhất, nền tảng hợp lệ và số dương hữu hạn. Kết quả hàng loạt được ghi CSV/JSON trong `results/`.

### 4.1. Mô hình dữ liệu (Entity–Relationship/Class Model)

Các thực thể đề xuất gồm Laptop, Criterion, Scenario, DecisionRun và RankingResult. DecisionRun lưu tham số của từng lần chạy; RankingResult liên kết laptop với hạng, điểm hoặc lý do loại.

![Hình 4.4. Sơ đồ lớp/mô hình dữ liệu](diagrams/drawio/exported/04-class-diagram.png){width=90%}

## 5. Thiết kế tầng Model Management Subsystem

Model nhận danh sách laptop, ràng buộc và trọng số; trả về ranking, rejected, min/max, normalized và contributions. Trọng số phải không âm, hữu hạn và có tổng bằng 1.

### 5.1. Quy trình lọc cứng (Hard Filtering)

Hệ thống loại máy vượt ngân sách, RAM/SSD dưới ngưỡng hoặc không tương thích iOS. Một máy có thể có nhiều lý do loại. Hard filter chạy trước chuẩn hóa để phương án không khả thi không ảnh hưởng min/max.

### 5.2. Chuẩn hóa giá trị (Normalization)

Benefit: `r_ij = (x_ij - min_j)/(max_j - min_j)`. Cost: `r_ij = (max_j - x_ij)/(max_j - min_j)`. Nếu max bằng min, mọi phương án nhận cùng giá trị 1 vì tiêu chí không tạo khác biệt.

### 5.3. Mô hình Weighted Sum (WSM)

Điểm tổng `Z_i = Σ(w_j × r_ij)`, với `w_j ≥ 0` và `Σw_j = 1`. Hệ thống lưu từng đóng góp để người dùng truy vết điểm tổng. Khi bằng điểm, thứ tự phụ là giá thấp hơn, CPU cao hơn rồi ID.

### 5.4. Phân tích What-if

What-if thay đổi vector trọng số, ngân sách hoặc mục tiêu nền tảng rồi chạy lại toàn bộ pipeline. Việc tính lại cả hard filter và min/max là cần thiết vì tập phương án có thể thay đổi.

![Hình 4.5. Sơ đồ tuần tự quy trình xếp hạng](diagrams/drawio/exported/05-sequence.png){width=90%}

## 6. Thiết kế triển khai và công nghệ

Project dùng Python 3, Flask 3.1, HTML, CSS, CSV và JSON. Giao diện, controller và DSS Engine chạy trong một tiến trình cục bộ; dữ liệu và kết quả là file. Kiến trúc phù hợp trình diễn, không yêu cầu database server.

### 6.1. Component/Deployment Diagram

Component Diagram tách Client, Application và Data. Khi triển khai Internet cần tắt debug, dùng WSGI server, HTTPS, xác thực và logging; phiên bản hiện tại chỉ phục vụ localhost.

![Hình 4.6. Component/Deployment Diagram](diagrams/drawio/exported/06-component-deployment.png){width=90%}

## 7. Đánh giá thiết kế

Thiết kế có tính linh hoạt nhờ kịch bản và ngưỡng; tính mở rộng nhờ bảng tiêu chí; tính giải thích nhờ đóng góp và lý do loại; tính tái lập nhờ CSV, JSON và test. Hạn chế là chưa lưu lịch sử trong CSDL, chưa cho sửa từng trọng số trên UI và chưa có xác thực người dùng.

'''

replacements = {
    "# 5. Dữ liệu và tiền xử lý": "# CHƯƠNG V. DỮ LIỆU VÀ TIỀN XỬ LÝ",
    "# 6. Mô hình ra quyết định và kết quả baseline": "# CHƯƠNG VI. MÔ HÌNH RA QUYẾT ĐỊNH",
    "# 7. Phân tích What-if": "# CHƯƠNG VII. PHÂN TÍCH WHAT-IF",
    "# 8. Hướng nâng cấp DSS": "# CHƯƠNG VIII. NÂNG CẤP DSS",
    "# 9. Đánh giá và thảo luận": "# CHƯƠNG IX. ĐÁNH GIÁ VÀ THẢO LUẬN",
    "# 10. Kết luận": "# CHƯƠNG X. KẾT LUẬN",
    "# Tài liệu tham khảo": "# CHƯƠNG XI. TÀI LIỆU THAM KHẢO",
    "- Sơ đồ: `diagrams/*.mmd`.": "- Sơ đồ draw.io chỉnh sửa được: `diagrams/drawio/*.drawio`.\n- Ảnh sơ đồ: `diagrams/drawio/exported/*.png`.",
}
for old, new in replacements.items():
    tail = tail.replace(old, new)

output = front + chapters + tail
(ROOT / "report" / "BAO_CAO_THEO_MAU_DIEM_B.md").write_text(output, encoding="utf-8")
print("Đã tạo report/BAO_CAO_THEO_MAU_DIEM_B.md")
