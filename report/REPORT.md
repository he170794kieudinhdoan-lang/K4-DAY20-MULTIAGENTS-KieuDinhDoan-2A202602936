# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin sinh viên và cấu hình

- Họ tên: [CẦN BẠN ĐIỀN / HITL - Ví dụ: Kiều Đình Đoàn]
- Mã sinh viên: [CẦN BẠN ĐIỀN / HITL - Ví dụ: 2A202602936]

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: DeepSeek (`deepseek-flash` qua OpenAI-compatible endpoint tại `https://api.deepseek.com/v1`), `LAB_TEMPERATURE=0`, `recursion_limit=100`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11 x64, chạy trực tiếp trên Virtualenv Python 3.11 với `SafeLocalShellBackend` (Git Bash sh.exe).
- Số lần chạy tác vụ đã dùng / ngân sách: 3 lần learn (baseline) + 3 lần learn (subagents) + 3 lần test skills (Section 3.4) + 12 lần eval/official / Ngân sách cấp phát API key cá nhân.
- Commit của tag `freeze`: Sẽ tự động ghi nhận hash của tag `freeze` sau bước đóng băng.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): `subagents` sẽ KHÔNG cải thiện điểm số đáng kể trên cả tác vụ học và đánh giá (điểm tương đương hoặc chỉ tăng nhẹ <= 0.1), nhưng chi phí token sẽ tăng đột biến (dự kiến gấp 2x - 4x) và thời gian thực thi lâu hơn. Căn cứ: Phân loại lỗi ở baseline cho thấy các check thất bại 100% thuộc nhóm E (thiếu quy ước ẩn của Acme: type hints, changelog, cents, metadata) chứ không phải do năng lực giải quyết vấn đề kỹ thuật (nhóm B/C/D agent đơn lẻ đã pass 100%). Việc chia nhỏ cho subagents mà không có tài liệu quy ước Acme thì subagents cũng "mù thông tin" tương tự main agent, cộng thêm overhead giao tiếp (context duplication).
- H2 (skills-auto so với baseline): `skills-auto` sẽ cải thiện vượt bậc điểm số trên tác vụ học (từ ~60% lên ~85-90%) nhờ giải quyết triệt để các lỗi quy ước Acme (Nhóm E). Tuy nhiên, trên tác vụ ĐÁNH GIÁ (eval), `skills-auto` chỉ cải thiện một phần (chuyển giao được các quy ước dùng chung đã học như changelog format, cents unit, meta block), nhưng sẽ thất bại ở các quy ước MỚI xuất hiện riêng ở eval (như rule_markdown_summary hay schema riêng của eval). Căn cứ theo lý thuyết Agent Skills (Anthropic 2024 / Wang et al., 2024) và hiện tượng distribution shift trong RL/In-context Learning.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm số trung bình trên tác vụ học sẽ cao hơn đáng kể tác vụ đánh giá đối với điều kiện `skills-auto` (chênh lệch dự kiến delta >= 0.15 - 0.20), phản ánh hiện tượng quá khớp thủ tục (procedural overfitting) vào tập học. Ngược lại, ở `baseline` và `subagents`, điểm số giữa học và đánh giá sẽ tương đương nhau vì agent đều giải được phần kỹ thuật lõi và cùng "tạch" các rule ẩn Acme chưa từng được tiếp cận.

## 3. Làm quen Deep Agents (Phần 0.3)

1.
2.
3.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| | | | |

Nhận xét: nhóm lỗi nào chiếm đa số? Skill có thể phòng ngừa nhóm đó không?

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc):
- Ảnh hưởng đến token và thời gian:

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do:

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| | | | |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Bạn đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
