# DoAnCaNhanAI
![GiaoDien](https://github.com/user-attachments/assets/3941f0c8-044c-40de-bcfd-d297d5f7337b)
## 1. Mục tiêu
### Bài tập cá nhân này sử dụng các thuật toán tìm kiếm để giải quyết bài toán 8-puzzle. Cụ thể, đề tài tập trung vào 6 nhóm thuật toán chính:
- Thuật toán tìm kiếm không có thông tin (Uninformed Search) như BFS, DFS, IDS và UCS, giúp khảo sát khả năng tìm lời giải khi không có thông tin định hướng.
- Thuật toán tìm kiếm có thông tin (Informed Search) như A*, IDA* và Greedy Best-First Search, sử dụng heuristic để tối ưu hóa hiệu quả tìm kiếm.
- Bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problems - CSP) như Forward-Checking, Backtracking và Min-Conflicts nhằm khảo sát khả năng biểu diễn 8-puzzle dưới dạng hệ thống ràng buộc logic.
- Tìm kiếm cục bộ (Local Search) như Hill Climbing, Steepest Ascent Hill Climbing, Simple Hill Climbing Simulated Annealing, Stochastic Hill Climbing và Beam Search tập trung vào việc cải thiện nghiệm cục bộ mà không cần duy trì toàn bộ không gian trạng thái.
- Tìm kiếm trong môi trường phức tạp (Searching in Complex Environments) như AND-OR Graph Search, Searching for a partially observation, Sensorless mở rộng khả năng ứng dụng sang các bài toán có tính động và không chắc chắn, định hướng cho các nghiên cứu nâng cao.
## 2. Nội dung
### Thuật toán Tìm kiếm Không Thông tin (Uninformed Search Algorithms)
Thuật toán tìm kiếm không thông tin là nhóm thuật toán không sử dụng bất kỳ thông tin nào về đích hoặc khoảng cách đến đích trong quá trình tìm kiếm. Chúng chỉ dựa vào cấu trúc của không gian trạng thái để tìm kiếm lời giải.
#### Tìm kiếm theo chiều rộng (Breadth-First Search - BFS)
- Không gian trạng thái (State Space):
- Là tập hợp tất cả các trạng thái có thể xảy ra của bài toán.
- Trạng thái khởi đầu (Initial State):
- Là trạng thái ban đầu mà hệ thống bắt đầu tìm kiếm.
#### Tìm kiếm theo chiều sâu (Depth-First Search - DFS)
- Mở rộng nút con sâu nhất trước, sau đó quay lại nếu gặp ngõ cụt.
- Sử dụng ngăn xếp (Stack) để quản lý các nút.
- Ưu điểm: Tốn ít bộ nhớ hơn BFS.
- Nhược điểm: Có thể rơi vào vòng lặp vô hạn, không đảm bảo tìm được lời giải tối ưu.
#### Tìm kiếm theo chiều sâu lặp lại (Iterative Deepening Search - IDS)
- Kết hợp giữa BFS và DFS.
- Thực hiện DFS với giới hạn độ sâu tăng dần cho đến khi tìm được lời giải.
- Ưu điểm: Tìm được lời giải tối ưu như BFS nhưng tiết kiệm bộ nhớ như DFS.
- Nhược điểm: Phải duyệt lại nhiều lần các nút đã đi qua trong các vòng lặp trước.
#### Tìm kiếm theo chi phí đều (Uniform Cost Search - UCS)
- Luôn mở rộng nút có tổng chi phí từ gốc đến hiện tại là nhỏ nhất.
- Sử dụng hàng đợi ưu tiên (Priority Queue) dựa trên tổng chi phí đường đi.
- Ưu điểm: Tìm được lời giải tối ưu, áp dụng tốt khi chi phí hành động khác nhau.
- Nhược điểm: Tốc độ chậm, tốn bộ nhớ nếu không gian trạng thái lớn.
![IUninformedSearchAlgorithms](https://github.com/user-attachments/assets/ff993811-a1fa-4ab1-8119-d068dd65c84c)
### Informed Search Algorithms (Thuật toán tìm kiếm có thông tin)
Thuật toán tìm kiếm có thông tin là nhóm thuật toán sử dụng thêm thông tin ước lượng (heuristic) để định hướng quá trình tìm kiếm, giúp rút ngắn thời gian và tăng hiệu quả tìm lời giải. Heuristic là hàm đánh giá khoảng cách ước lượng từ một trạng thái hiện tại đến trạng thái đích.
#### Tìm kiếm tham lam tốt nhất (Greedy Best-First Search)
- Chọn nút có giá trị heuristic h(n) nhỏ nhất để mở rộng, nghĩa là nút được đánh giá là gần mục tiêu nhất.
- Bỏ qua chi phí đã đi (g(n)), chỉ quan tâm đến khoảng cách còn lại.
- Sử dụng hàng đợi ưu tiên (Priority Queue) theo h(n).
- Ưu điểm:
✔️ Tốc độ nhanh trong nhiều trường hợp thực tế.
✔️ Cấu trúc đơn giản, dễ triển khai.
- Nhược điểm:
❌ Không đảm bảo tìm được lời giải tối ưu.
❌ Dễ bị lạc trong nhánh sai nếu heuristic không chính xác.
#### Tìm kiếm A (A-Star Search)
- Mở rộng nút có giá trị f(n) = g(n) + h(n) nhỏ nhất.
- Kết hợp giữa chi phí thực tế g(n) và ước lượng đến đích h(n).
- Sử dụng hàng đợi ưu tiên theo giá trị f(n).
- Ưu điểm:
✔️ Tìm được lời giải tối ưu nếu heuristic là admissible (không đánh giá quá cao chi phí).
✔️ Hiệu quả cao nếu h(n) gần đúng.
- Nhược điểm:
❌ Tốn nhiều bộ nhớ do phải lưu trữ nhiều trạng thái.
❌ Hiệu suất giảm nếu heuristic yếu.
#### Tìm kiếm A lặp lại theo độ sâu (Iterative Deepening A - IDA*)
- Là phiên bản tiết kiệm bộ nhớ của A*.
- Duyệt theo chiều sâu với ngưỡng f(n) tăng dần (thay vì độ sâu như IDS).
- Mỗi vòng lặp DFS chỉ mở rộng các nút có f(n) không vượt quá ngưỡng hiện tại.
- Ưu điểm:
✔️ Tìm lời giải tối ưu như A*.
✔️ Tiết kiệm bộ nhớ hơn vì không cần lưu toàn bộ cây.
- Nhược điểm:
❌ Phải duyệt lại các nút trong nhiều vòng lặp → tốn thời gian hơn A* trong một số trường hợp.
![IInformedSearchAlgorithms](https://github.com/user-attachments/assets/fa432c8c-baae-409c-9206-78124a9263e3)
### Bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problems - CSP)
Bài toán thỏa mãn ràng buộc (CSP) là bài toán trong đó lời giải là một tập hợp các giá trị gán cho một số biến sao cho mọi ràng buộc (constraints) đều được thỏa mãn.
#### Backtracking (Tìm kiếm quay lui)
- Là phương pháp cơ bản nhất: thử từng giá trị khả dĩ cho từng biến theo thứ tự, kiểm tra ràng buộc, và quay lui nếu có xung đột.
- Quy trình:
  Gán giá trị cho biến đầu tiên.
  Kiểm tra các ràng buộc.
  Nếu hợp lệ → tiếp tục với biến kế tiếp.
  Nếu không hợp lệ → quay lui và thử giá trị khác.
- Ưu điểm:
✔️ Dễ cài đặt, hiệu quả cho các bài toán nhỏ.
- Nhược điểm:
❌ Tốn thời gian với không gian tìm kiếm lớn.
❌ Không tận dụng nhiều thông tin về ràng buộc trong quá trình tìm kiếm.
#### Forward Checking (Dự đoán trước)
- Là cải tiến của Backtracking. Khi gán giá trị cho một biến, thuật toán loại bỏ các giá trị không hợp lệ khỏi miền của các biến chưa gán.
- Cách hoạt động:Mỗi khi gán một giá trị cho biến, kiểm tra xem liệu ràng buộc với các biến còn lại có làm miền của chúng rỗng hay không.
- Ưu điểm:
✔️ Giảm số lượng nhánh vô ích.
✔️ Tăng tốc độ tìm kiếm bằng cách phát hiện xung đột sớm.
- Nhược điểm:
❌ Cần thêm chi phí để duy trì miền biến cập nhật.
#### Min-Conflicts (Giải thuật xung đột tối thiểu)
- Là thuật toán tìm kiếm cục bộ (local search), thường dùng cho bài toán có lời giải lớn như giải ô chữ, Sudoku, n-queens.
- Cách hoạt động:
  Khởi tạo gán giá trị ngẫu nhiên.
  Tại mỗi bước, chọn biến đang vi phạm ràng buộc.
  Gán lại giá trị cho biến đó sao cho số lượng ràng buộc bị vi phạm là ít nhất.
  Lặp lại cho đến khi không còn xung đột.
- Ưu điểm:
✔️ Hiệu quả với bài toán có không gian trạng thái lớn.
✔️ Không cần quay lui.
- Nhược điểm:
❌ Không đảm bảo tìm được lời giải nếu bị mắc kẹt tại cực trị cục bộ.
❌ Không áp dụng tốt cho bài toán có ít hoặc không có lời giải.

### Tìm kiếm cục bộ (Local Search)
Tìm kiếm cục bộ là nhóm thuật toán dùng để tìm lời giải bằng cách cải thiện dần một trạng thái duy nhất, thay vì xây dựng toàn bộ cây tìm kiếm. Phù hợp với các bài toán có không gian trạng thái rất lớn hoặc khó biểu diễn lời giải hoàn chỉnh ngay từ đầu.
#### Simple Hill Climbing
- Tại mỗi bước, chuyển sang trạng thái kế cận đầu tiên tốt hơn trạng thái hiện tại.
- Ưu điểm:
✔️ Dễ cài đặt
✔️ Hoạt động tốt khi có ít điểm cực trị cục bộ
- Nhược điểm:
❌ Dễ bị kẹt tại cực trị cục bộ
❌ Không quan sát được toàn bộ không gian kế cận
#### Steepest Ascent Hill Climbing
- Ở mỗi bước, xem xét tất cả các trạng thái lân cận và chọn trạng thái có giá trị đánh giá tốt nhất.
- Ưu điểm:
✔️ Cải thiện hiệu quả tìm kiếm
✔️ Giảm nguy cơ chọn nhầm bước tồi
- Nhược điểm:
❌ Vẫn có thể kẹt tại cực trị cục bộ hoặc điểm cao nguyên (plateau)
#### Stochastic Hill Climbing
- Tương tự như Hill Climbing nhưng chọn ngẫu nhiên một trạng thái tốt hơn trong số các trạng thái lân cận.
- Ưu điểm:
✔️ Giảm khả năng bị kẹt ở điểm cao nguyên
✔️ Đa dạng hướng đi
- Nhược điểm:
❌ Không đảm bảo luôn chọn hướng tốt nhất
❌ Kết quả có thể không ổn định
#### Simulated Annealing
- Cho phép di chuyển sang trạng thái kém hơn tạm thời với xác suất giảm dần theo thời gian, nhằm thoát khỏi cực trị cục bộ.
- Cơ chế giống quá trình làm nguội kim loại (annealing).
- Ưu điểm:
✔️ Có khả năng tìm được lời giải toàn cục
✔️ Tránh được bẫy cục bộ hiệu quả
- Nhược điểm:
❌ Hiệu suất phụ thuộc vào tham số nhiệt độ và tốc độ làm nguội
❌ Cần điều chỉnh cẩn thận
#### Beam Search
- Mở rộng k nút tốt nhất ở mỗi mức thay vì một nút như Hill Climbing (k gọi là "beam width").
- Là sự kết hợp giữa tìm kiếm theo chiều rộng và local search.
- Ưu điểm:
✔️ Giảm nguy cơ mắc kẹt tại cực trị
✔️ Có thể mở rộng với nhiều luồng song song
- Nhược điểm:
❌ Tốn tài nguyên hơn
❌ Không đảm bảo tối ưu nếu beam width quá nhỏ
