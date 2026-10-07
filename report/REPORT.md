# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin sinh viên và cấu hình

- Họ tên: Kiều Đình Đoàn
- Mã sinh viên: 2A202602936
- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: DeepSeek (`deepseek-flash` qua OpenAI-compatible endpoint tại `https://api.deepseek.com/v1`), `LAB_TEMPERATURE=0`, `recursion_limit=100`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11 x64, chạy trực tiếp trên Virtualenv Python 3.11 với `SafeLocalShellBackend` (Git Bash sh.exe).
- Số lần chạy tác vụ đã dùng / ngân sách: 21 lần chạy tác vụ (3 learn baseline, 3 learn subagents, 3 learn test skills Phần 3.4, 3 eval baseline, 3 eval subagents, 6 tasks all skills-auto) / Ngân sách cấp phát API key cá nhân.
- Commit của tag `freeze`: `aa44f35` (commit message: `freeze skills`).

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): `subagents` sẽ KHÔNG cải thiện điểm số đáng kể trên cả tác vụ học và đánh giá (điểm tương đương hoặc chỉ tăng nhẹ <= 0.1), nhưng chi phí token sẽ tăng đột biến (dự kiến gấp 2x - 4x) và thời gian thực thi lâu hơn. Căn cứ: Phân loại lỗi ở baseline cho thấy các check thất bại 100% thuộc nhóm E (thiếu quy ước ẩn của Acme: type hints, changelog, cents, metadata) chứ không phải do năng lực giải quyết vấn đề kỹ thuật (nhóm B/C/D agent đơn lẻ đã pass 100%). Việc chia nhỏ cho subagents mà không có tài liệu quy ước Acme thì subagents cũng "mù thông tin" tương tự main agent, cộng thêm overhead giao tiếp (context duplication).
- H2 (skills-auto so với baseline): `skills-auto` sẽ cải thiện vượt bậc điểm số trên tác vụ học (từ ~60% lên ~85-90%) nhờ giải quyết triệt để các lỗi quy ước Acme (Nhóm E). Tuy nhiên, trên tác vụ ĐÁNH GIÁ (eval), `skills-auto` chỉ cải thiện một phần (chuyển giao được các quy ước dùng chung đã học như changelog format, cents unit, meta block), nhưng sẽ thất bại ở các quy ước MỚI xuất hiện riêng ở eval (như rule_markdown_summary hay schema riêng của eval). Căn cứ theo lý thuyết Agent Skills (Anthropic 2024 / Wang et al., 2024) và hiện tượng distribution shift trong RL/In-context Learning.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm số trung bình trên tác vụ học sẽ cao hơn đáng kể tác vụ đánh giá đối với điều kiện `skills-auto` (chênh lệch dự kiến delta >= 0.15 - 0.20), phản ánh hiện tượng quá khớp thủ tục (procedural overfitting) vào tập học. Ngược lại, ở `baseline` và `subagents`, điểm số giữa học và đánh giá sẽ tương đương nhau vì agent đều giải được phần kỹ thuật lõi và cùng "tạch" các rule ẩn Acme chưa từng được tiếp cận.

## 3. Làm quen Deep Agents (Phần 0.3)

1. **Công cụ tác tử mặc định:** Tác tử mặc định được cung cấp 9 công cụ gồm 7 công cụ tệp (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), 1 công cụ thực thi shell (`execute`) và 1 công cụ gọi tác tử con (`task`). Trong đó, công cụ cho phép chạy lệnh là `execute` (thực thi câu lệnh shell trong môi trường cách ly sandbox).
2. **Subagent `general-purpose`:** Mô tả của công cụ `task` cho biết `general-purpose` là tác tử đa năng dùng để tra cứu câu hỏi phức tạp, tìm kiếm file/nội dung khi chưa tự tin tìm đúng ngay trong vài lần đầu, và thực thi các tác vụ nhiều bước; nó có quyền truy cập toàn bộ công cụ như tác tử chính. Về ngữ cảnh: Mỗi lần gọi subagent là độc lập và phi trạng thái (stateless) theo mặc định, subagent chỉ nhìn thấy prompt được giao và trả về một báo cáo kết quả duy nhất (không nhìn thấy lịch sử hội thoại của tác tử chính trừ khi được cấu hình kế thừa hội thoại).
3. **Trích dẫn hướng dẫn hành vi:**
   - Trích từ mô tả công cụ `task`: *"Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - Trích từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `code-learn` | `tests_not_modified` | C | `the original files in tests/ must not be modified (new test files are allowed)` - Agent sửa file test có sẵn để test pass thay vì chỉ thêm test mới. |
| `code-learn` | `rule_type_hints` | E | `RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value.` |
| `code-learn` | `rule_regression_tests` | E | `RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass.` |
| `code-learn` | `rule_changelog` | E | `RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets).` |
| `data-learn` | `rule_money_in_cents` | E | `RULE: money values in answer.json are integer cents (1606.67 USD is written 160667).` |
| `data-learn` | `rule_meta_block` | E | `RULE: answer.json has an object meta = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}.` |
| `data-learn` | `rule_clean_csv` | E | `RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount...` |
| `logs-learn` | `rule_service_names` | E | `RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service).` |
| `logs-learn` | `rule_sorted_errors` | E | `RULE: errors is sorted by service, then by timestamp_utc, ascending.` |
| `logs-learn` | `rule_schema_header` | E | `RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage".` |

**Nhận xét:**
- Nhóm lỗi **E (Vi phạm quy ước tổ chức ngầm của Acme)** chiếm đa số áp đảo: 9/10 check thất bại thuộc nhóm E. Đề bài tác vụ ban đầu hoàn toàn không cung cấp các quy định tổ chức này (như định dạng CHANGELOG, đơn vị tiền tệ bằng cents, cấu trúc block meta, schema headers, hay đổi dấu gạch ngang service name).
- **Bằng chứng phủ định cho nhóm A-D:** Tác tử giải quyết rất tốt các yêu cầu kỹ thuật lõi. Số check kỹ thuật đạt trên tập học là **17/18** (đạt 94.4%, theo thống kê từ `scripts/check_breakdown.py`). Tác tử đọc kỹ đề, không bỏ sót dữ liệu bẩn và thuật toán xử lý dữ liệu/phân tích log đều chính xác.
- Một bộ skill chuẩn hóa hoàn toàn có thể phòng ngừa nhóm lỗi E bằng cách cung cấp danh sách kiểm tra (checklist) các quy ước bắt buộc của tổ chức trước khi bàn giao sản phẩm.

## 5. Điều kiện `subagents` (Phần 2.3)

- **Các subagent đã định nghĩa:**
  - `explorer`: Vai trò chuyên khám phá không gian làm việc, đọc file, đọc docstring, kiểm tra cấu trúc thư mục, schema dữ liệu và file log mà không sửa file. Thiết kế để cô lập quá trình thu thập thông tin, tránh làm ô nhiễm context của tác tử chính.
  - `implementer`: Vai trò thực thi thay đổi mã nguồn/dữ liệu cụ thể, chạy các script Python và lệnh kiểm thử theo chỉ định rõ ràng.
  - `reviewer`: Vai trò kiểm thử và đánh giá độc lập các file đã chỉnh sửa, đối chiếu edge-case với đặc tả yêu cầu mà không chỉnh sửa file.
- **`subagent_calls` ở từng tác vụ và nhận xét:**
  - `code-learn`: 2 calls (`explorer`)
  - `data-learn`: 1 call (`explorer`)
  - `logs-learn`: 1 call (`explorer`)
  - `code-eval`: 1 call (`explorer`)
  - `data-eval`: 1 call (`explorer`)
  - `logs-eval`: 1 call (`explorer`)
  - *Nhận xét:* Tác tử chính luôn chủ động gọi `explorer` ở đầu mỗi tác vụ để kiểm tra workspace và log. Tuy nhiên, tác tử chính không ủy quyền khâu sửa đổi file hay đánh giá cho `implementer`/`reviewer` mà tự mình thực thi các công cụ `edit_file`, `write_file`, `execute` sau khi nhận được báo cáo từ `explorer`.
- **Thông tin thiếu hoặc thừa khi giao việc:** Lời giao việc cho `explorer` rất rõ ràng và đúng trọng tâm thu thập dữ liệu/cấu trúc file. Tuy nhiên, cả tác tử chính và subagent đều không có thông tin về các quy ước tổ chức Acme (nhóm E), nên việc phân rã tác vụ không thể giúp phát hiện các quy ước ẩn này.
- **Ảnh hưởng đến token và thời gian:**
  - Lượng token tiêu thụ tăng đáng kể: Trung bình **445,968 tokens/run** ở điều kiện `subagents` so với **347,730 tokens/run** ở `baseline`. Đặc biệt trên tập học (`learn`), số token tiêu thụ vọt lên **672,440 tokens/run** (gấp 2.5 lần so với 267,490 ở baseline).
  - Điểm số không có bất kỳ sự cải thiện nào (cùng đạt 0.63 trên tập học và 0.57 trên tập đánh giá). Việc sử dụng đa tác tử trong bối cảnh này gây lãng phí tài nguyên tính toán do overhead trao đổi ngữ cảnh mà không giải quyết được nguyên nhân gốc rễ của thất bại (thiếu quy ước ngầm).

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 1 lần. Số skill bị xóa: 0. Cả 3 skill do curator tự động trích xuất từ phản hồi `detail` và vết của tập học baseline đều có cấu trúc YAML frontmatter hợp lệ, nội dung ngắn gọn và chuẩn xác.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `code-fix-repo-conventions` | **Tổng quát:** Áp dụng cho mọi tác vụ sửa lỗi code trong repo có test và quy ước (bổ sung test hồi quy, cập nhật changelog, gắn type hints cho hàm public, không sửa test cũ). | **Đúng:** Các nguyên tắc đưa ra hoàn toàn chính xác theo chuẩn kỹ thuật phần mềm và phù hợp với quy ước của Acme. | 20 dòng. Description rõ ràng: kích hoạt khi sửa bug/chỉnh sửa file nguồn trong repo có test và conventions. `skills_read=3`. |
| `data-normalization-and-determinism` | **Tổng quát:** Áp dụng cho các bài toán xử lý dữ liệu thô (log, CSV, sales) cần chuẩn hóa đơn vị, định danh, định dạng thời gian và tính tiền định (sort deterministically). | **Đúng:** Hướng dẫn đúng về chuyển đổi tiền tệ sang đơn vị nhỏ nhất (cents), chuẩn hóa timezone UTC, sort theo khóa. | 19 dòng. Description kích hoạt khi biến đổi dữ liệu thô thành output có đơn vị/quy ước cụ thể. `skills_read=3`. |
| `output-spec-compliance` | **Tổng quát:** Áp dụng cho mọi tác vụ xuất artifact (JSON, CSV, báo cáo) cần tuân thủ schema, kèm file bổ trợ và metadata. | **Đúng:** Hướng dẫn kiểm tra toàn diện hợp đồng đầu ra (meta block, companion files như clean.csv). | 19 dòng. Description kích hoạt khi tạo artifact output cần tuân thủ schema. `skills_read=3`. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

### Bảng so sánh (`report/table.md`)

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 6/10 | 6/10 | 8/10 |
| data-learn | 5/8 | 5/8 | 5/8 |
| logs-learn | 6/9 | 6/9 | 6/9 |
| code-eval | 6/11 | 6/11 | 8/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.63 | 0.63 | 0.70 |
| **Mean score - evaluation tasks** | 0.57 | 0.57 | 0.63 |
| **Mean tokens per run** | 347,730 | 445,968 | 429,966 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

### Bảng phân tích chi tiết kiểm tra (`scripts/check_breakdown.py`)

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     17/18         0/12         427,970      0/3     
baseline      learn    17/18         0/9          267,490      0/3     
subagents     eval     17/18         0/12         219,497      0/3     
subagents     learn    17/18         0/9          672,440      0/3     
skills-auto   eval     17/18         2/12         633,657      3/3     
skills-auto   learn    17/18         2/9          226,275      3/3     
```

*Ghi chú:* Toàn bộ các lần chạy đều hoàn thành bình thường, không có lần chạy nào bị lỗi crash (`error`), không có lần chạy nào bị `skills_modified = true`. Lệnh `scripts/verify_freeze.py` báo kết quả `checked 6 runs of skill conditions: OK`.

## 8. Phân tích

1. **Hiệu quả trên tác vụ học và đánh giá:**
   - So với `baseline`, điều kiện `skills-auto` cải thiện điểm số ở cả tác vụ **học** (từ 0.63 lên 0.70) và tác vụ **đánh giá** (từ 0.57 lên 0.63). Trong khi đó, `subagents` không cải thiện điểm số ở bất kỳ tác vụ nào (0.63 học, 0.57 đánh giá).
   - Việc `skills-auto` cải thiện đồng đều ở cả tập học và đánh giá (cùng tăng +0.07 hay +2 điểm check) chứng tỏ các kỹ năng tự sinh đã chuyển giao thành công các quy ước mang tính hệ thống (systemic conventions) chứ không chỉ đơn thuần là học vẹt dữ liệu.
2. **Tách check kỹ thuật và check quy ước (`rule_`):**
   - **Check kỹ thuật:** Đạt **17/18** trên cả 3 điều kiện và ở cả 2 vai trò (học và đánh giá). Điều này cho thấy năng lực giải quyết bài toán kỹ thuật của mô hình DeepSeek đã đạt mức trần (94.4%).
   - **Check quy ước (`rule_`):** Ở baseline và subagents, tác tử đạt **0/9** ở tập học và **0/12** ở tập đánh giá. Khi nạp `skills-auto`, tác tử vượt qua được **2/9** quy ước ở tập học và **2/12** quy ước ở tập đánh giá (cụ thể là `rule_type_hints` và `rule_regression_tests`).
   - **Quy ước mới ở tác vụ đánh giá:** Các check quy ước mới xuất hiện riêng ở eval (`rule_version_bump` ở `code-eval`, `rule_sorted_keys_format` ở `data-eval`, `rule_source_line` ở `logs-eval`) **hoàn toàn KHÔNG được skill giúp**, vì các quy ước này chưa từng xuất hiện trong phản hồi của tập học, và curator không thể "tiên tri" các quy tắc chưa biết ngoài phân phối (out-of-distribution).
3. **Cơ chế hoạt động từ vết và `skills_read`:**
   - **Check được skill giúp:** Trong `code-learn` và `code-eval`, sau khi đọc skill `code-fix-repo-conventions`, tác tử đã kiểm tra và chủ động bổ sung type annotations cho tất cả hàm public (`rule_type_hints`), đồng thời tạo mới file `tests/test_regressions.py` chứa các test case tương ứng với từng lỗi đã sửa (`rule_regression_tests`).
   - **Check không được skill giúp:** Trong `code-learn`, check `rule_changelog` vẫn không đạt dù có trong skill: tác tử đã tập trung chạy pytest và chỉnh sửa mã nguồn, sau khi thấy pytest pass thì kết luận hoàn thành tác vụ mà quên thực hiện bước ghi nhận vào `CHANGELOG.md`. Tương tự ở `data-learn`, agent đọc skill `data-normalization-and-determinism` nhưng do khối lượng xử lý dữ liệu lớn nên bỏ qua việc tạo file phụ trợ `clean.csv`.
4. **Chi phí token và hiệu quả:**
   - `baseline`: Trung bình 347,730 tokens/run.
   - `subagents`: Trung bình 445,968 tokens/run (tăng 28.2% token so với baseline, riêng tập learn tăng 151%), nhưng điểm số bằng đúng baseline. Đa tác tử **hoàn toàn không đáng chi phí** trong bài thực nghiệm này do overhead trao đổi giữa các agent mà không bổ sung được tri thức quy ước.
   - `skills-auto`: Trung bình 429,966 tokens/run (tăng 23.6% so với baseline), nhưng mang lại bước nhảy điểm số thực chất (+0.07 trên cả 2 tập), đạt hiệu quả cải thiện điểm số trên mỗi token tốt nhất.
5. **Rò rỉ dữ liệu và quá khớp:**
   - **Phòng tránh rò rỉ:** Quy trình đóng băng (Freeze protocol) được thực hiện nghiêm ngặt: Curator chỉ đọc feedback `detail` của tập learn; commit giả thuyết H1-H3 trước khi tạo tag `freeze`; kiểm tra `verify_freeze.py` đạt 100% OK với hash SHA256 đồng nhất.
   - **Quá khớp:** Không có hiện tượng rò rỉ dữ liệu. Có sự quá khớp thủ tục ở mức độ tự nhiên đối với các quy ước học được từ tập learn, dẫn đến việc skill chỉ giải quyết được các quy ước có tính chuyển giao (transferable) mà không xử lý được các quy ước mới của eval.
6. **Phân tích nhiễu:**
   - Điểm tác vụ học ở Phần 3.4 (trước đóng băng, lưu tại `results_test_skills/`): `code-learn` 8/10, `data-learn` 5/8, `logs-learn` 6/9 -> Điểm trung bình = **0.70**.
   - Điểm tác vụ học sau đóng băng (lần chạy chính thức trong `results/skills-auto/`): `code-learn` 8/10, `data-learn` 5/8, `logs-learn` 6/9 -> Điểm trung bình = **0.70**.
   - **Chênh lệch delta = 0.00**: Mức chênh lệch bằng 0 cho thấy độ ổn định và tính tái lập cực cao của quy trình thực nghiệm với `temperature=0`, chứng minh sự cải thiện điểm số không phải do nhiễu ngẫu nhiên.

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập tác vụ nhỏ:** Mỗi họ tác vụ chỉ có 1 tác vụ học và 1 tác vụ đánh giá (tổng cộng 6 tác vụ). Với số lượng tác vụ nhỏ, mỗi check kiểm tra chiếm tỷ trọng điểm số lớn (khoảng 10-15% tổng điểm của tác vụ), dẫn đến độ nhạy thống kê cao.
2. **Số lần chạy đơn lẻ (n = 1):** Mặc dù thiết lập `LAB_TEMPERATURE=0` mang lại tính tiền định cao, một số API LLM thương mại vẫn có thể tồn tại dao động nhỏ do cơ chế song song hóa hoặc batching phía máy chủ nhà cung cấp. Việc chạy 1 lần duy nhất chưa thể hiện được khoảng tin cậy (confidence interval) thống kê.
3. **Tính nhân tạo của các quy ước tổ chức:** Các quy ước ẩn (house rules) của Acme Corporation được định nghĩa có chủ đích trong bài lab. Trong môi trường phần mềm doanh nghiệp thực tế, các quy ước thường phân tán, đa dạng và đôi khi mâu thuẫn nhau giữa các dự án.
4. **Giới hạn trên một kiến trúc mô hình:** Toàn bộ thí nghiệm được tiến hành trên mô hình `deepseek-flash`. Khả năng hấp thụ skill và tương tác đa tác tử có thể biểu hiện khác nhau trên các họ mô hình lớn hơn hoặc có kiến trúc suy luận khác (như Claude 3.5 Sonnet hay GPT-4o).

## 10. Kết luận

- Bài lab đã cài đặt hoàn chỉnh bộ khung Agent Harness với Deep Agents và thực nghiệm thành công cả 3 điều kiện: baseline, đa tác tử (subagents) và tác tử tự tiến hóa (skills-auto).
- Kết quả chứng minh rằng điểm nghẽn chính của tác tử LLM không nằm ở năng lực kỹ thuật cơ sở (đạt 94.4% check kỹ thuật) mà nằm ở việc không nắm bắt được các quy ước tổ chức ẩn (0% house rules ở baseline).
- Đa tác tử (subagents) tiêu tốn nhiều token hơn (+28% đến +151%) mà không đem lại cải thiện điểm số khi tác tử con cũng thiếu thông tin ngữ cảnh.
- Tác tử tự tiến hóa (skills-auto) thông qua cơ chế Curator trích xuất phản hồi thất bại đã giúp tăng điểm số rõ rệt (+0.07 trên cả tập học và đánh giá) nhờ chuyển giao thành công các quy ước hệ thống.
- Đề xuất cải tiến tiếp theo: Tích hợp cơ chế tự động đối soát checklist (automated validation gate) bắt buộc tác tử rà soát lại các quy ước trước khi kết thúc tác vụ để loại bỏ lỗi "đọc skill nhưng quên làm theo".

## Phụ lục

- **Lệnh đã chạy (theo thứ tự):**
  1. `pytest tests/test_01_provided.py`
  2. `pytest tests/test_02_agent.py`
  3. `pytest tests/test_03_runner.py`
  4. `python scripts/tour.py`
  5. `python -m lab.runner --condition baseline --tasks data-learn code-learn logs-learn`
  6. `python -m lab.runner --condition subagents --tasks learn`
  7. `pytest tests/test_04_curator.py`
  8. `python -m lab.curator`
  9. `python -m lab.runner --condition skills-auto --tasks learn` (lưu sao lưu vào `results_test_skills/`)
  10. `git add -A && git commit -m "hypotheses..."`
  11. `git add -A && git commit --allow-empty -m "freeze skills" && git tag freeze`
  12. `python -m lab.runner --condition baseline --tasks eval`
  13. `python -m lab.runner --condition subagents --tasks eval`
  14. `python -m lab.runner --condition skills-auto --tasks all`
  15. `$env:PYTHONUTF8 = "1"; python scripts/verify_freeze.py`
  16. `$env:PYTHONUTF8 = "1"; python -m lab.compare > report/table.md`
  17. `$env:PYTHONUTF8 = "1"; python scripts/check_breakdown.py`
- **Ghi chú khác:** Không xảy ra lỗi hạ tầng hay timeout trong toàn bộ quá trình thực nghiệm.
