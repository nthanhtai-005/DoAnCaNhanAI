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
- Ưu điểm: Tốc độ nhanh trong nhiều trường hợp thực tế, cấu trúc đơn giản, dễ triển khai.
- Nhược điểm: Không đảm bảo tìm được lời giải tối ưu, dễ bị lạc trong nhánh sai nếu heuristic không chính xác.
#### Tìm kiếm A (A-Star Search)
- Mở rộng nút có giá trị f(n) = g(n) + h(n) nhỏ nhất.
- Kết hợp giữa chi phí thực tế g(n) và ước lượng đến đích h(n).
- Sử dụng hàng đợi ưu tiên theo giá trị f(n).
- Ưu điểm: Tìm được lời giải tối ưu nếu heuristic là admissibkhông đảm bảo tối ưu nếu beam width quá nhỏ
