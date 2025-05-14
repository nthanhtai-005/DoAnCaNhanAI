# DoAnCaNhanAI
![GiaoDien](https://github.com/user-attachments/assets/3941f0c8-044c-40de-bcfd-d297d5f7337b)
## 1. Mục tiêu
### Bài tập cá nhân này sử dụng các thuật toán tìm kiếm để giải quyết bài toán 8-puzzle. Cụ thể, đề tài tập trung vào 6 nhóm thuật toán chính:

- Thuật toán tìm kiếm không có thông tin (Uninformed Search) như BFS, DFS, IDS và UCS, giúp khảo sát khả năng tìm lời giải khi không có thông tin định hướng.
- Thuật toán tìm kiếm có thông tin (Informed Search) như A*, IDA* và Greedy Best-First Search, sử dụng heuristic để tối ưu hóa hiệu quả tìm kiếm.
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
####Tìm kiếm theo chiều sâu (Depth-First Search - DFS)
- Mở rộng nút con sâu nhất trước, sau đó quay lại nếu gặp ngõ cụt.
- Sử dụng ngăn xếp (Stack) để quản lý các nút.
- Ưu điểm: Tốn ít bộ nhớ hơn BFS.
- Nhược điểm: Có thể rơi vào vòng lặp vô hạn, không đảm bảo tìm được lời giải tối ưu.
####Tìm kiếm theo chiều sâu lặp lại (Iterative Deepening Search - IDS)
- Kết hợp giữa BFS và DFS.
- Thực hiện DFS với giới hạn độ sâu tăng dần cho đến khi tìm được lời giải.
- Ưu điểm: Tìm được lời giải tối ưu như BFS nhưng tiết kiệm bộ nhớ như DFS.
- Nhược điểm: Phải duyệt lại nhiều lần các nút đã đi qua trong các vòng lặp trước.
####Tìm kiếm theo chi phí đều (Uniform Cost Search - UCS)
- Luôn mở rộng nút có tổng chi phí từ gốc đến hiện tại là nhỏ nhất.
- Sử dụng hàng đợi ưu tiên (Priority Queue) dựa trên tổng chi phí đường đi.
- Ưu điểm: Tìm được lời giải tối ưu, áp dụng tốt khi chi phí hành động khác nhau.
- Nhược điểm: Tốc độ chậm, tốn bộ nhớ nếu không gian trạng thái lớn.
![IUninformedSearchAlgorithms](https://github.com/user-attachments/assets/ff993811-a1fa-4ab1-8119-d068dd65c84c)
### Informed Search Algorithms (Thuật toán tìm kiếm có thông tin)
Thuật toán tìm kiếm có thông tin là nhóm thuật toán sử dụng thêm thông tin ước lượng (heuristic) để định hướng quá trình tìm kiếm, giúp rút ngắn thời gian và tăng hiệu quả tìm lời giải. Heuristic là hàm đánh giá khoảng cách ước lượng từ một trạng thái hiện tại đến trạng thái đích.
![IInformedSearchAlgorithms](https://github.com/user-attachments/assets/fa432c8c-baae-409c-9206-78124a9263e3)
Một bài toán CSP được mô hình hóa bởi 3 thành phần chính:
- Biến (Variables)
Là các đối tượng cần gán giá trị. Gọi là X1, X2, ..., Xn.
- Miền giá trị (Domains)
Tập giá trị khả dĩ của từng biến. Ví dụ: D1 = {1,2,3} với biến X1.
- Ràng buộc (Constraints)
Các điều kiện giới hạn tổ hợp các giá trị được gán cho các biến.

### Tìm kiếm cục bộ (Local Search)
Trong quá trình giải bài toán bằng tìm kiếm, ta cần xác định rõ một số thành phần cơ bản để mô hình hóa và giải quyết vấn đề một cách hiệu quả:
- Trạng thái khởi đầu:
Đây là điểm xuất phát, nơi hệ thống bắt đầu quá trình tìm kiếm lời giải.
- Trạng thái mục tiêu:
Là đích đến mà bài toán yêu cầu đạt được, thường được mô tả bằng điều kiện thỏa mãn.
- Tập hành động:
Bao gồm các bước hoặc thao tác có thể áp dụng để chuyển từ trạng thái hiện tại sang trạng thái mới.
- Hàm chi phí:
Xác định mức chi phí cần thiết để thực hiện một hành động, qua đó giúp so sánh và lựa chọn hành trình tối ưu.
- Hàm đánh giá (Heuristic): Dùng để ước lượng khoảng cách hoặc độ phù hợp giữa trạng thái hiện tại và trạng thái mục tiêu, đặc biệt hữu ích trong các thuật toán tìm kiếm có định hướng.
- Giải pháp: Là chuỗi các hành động (hoặc trạng thái) nối tiếp nhau từ điểm bắt đầu đến đích, sao cho thỏa mãn yêu cầu của bài toán đề ra.
