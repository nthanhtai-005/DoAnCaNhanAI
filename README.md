# DoAnCaNhanAI
## 1. Mục tiêu
### Bài tập cá nhân này sử dụng các thuật toán tìm kiếm để giải quyết bài toán 8-puzzle. Cụ thể, đề tài tập trung vào 6 nhóm thuật toán chính:

- Thuật toán tìm kiếm không có thông tin (Uninformed Search) như BFS, DFS, IDS và UCS, giúp khảo sát khả năng tìm lời giải khi không có thông tin định hướng.
- Thuật toán tìm kiếm có thông tin (Informed Search) như A*, IDA* và Greedy Best-First Search, sử dụng heuristic để tối ưu hóa hiệu quả tìm kiếm.
- Tìm kiếm cục bộ (Local Search) như Hill Climbing, Steepest Ascent Hill Climbing, Simple Hill Climbing Simulated Annealing, Stochastic Hill Climbing và Beam Search tập trung vào việc cải thiện nghiệm cục bộ mà không cần duy trì toàn bộ không gian trạng thái.
- Tìm kiếm trong môi trường phức tạp (Searching in Complex Environments) như AND-OR Graph Search, Searching for a partially observation, Sensorless mở rộng khả năng ứng dụng sang các bài toán có tính động và không chắc chắn, định hướng cho các nghiên cứu nâng cao.
## 2. Nội dung
### Thuật toán Tìm kiếm Không Thông tin (Uninformed Search Algorithms)
Trong trí tuệ nhân tạo, một bài toán tìm kiếm thường được mô hình hóa với các thành phần cơ bản như sau:
- Không gian trạng thái (State Space):
Là tập hợp tất cả các trạng thái có thể xảy ra của bài toán.
Trạng thái khởi đầu (Initial State):
Là trạng thái ban đầu mà hệ thống bắt đầu tìm kiếm.
- Trạng thái đích (Goal State):
Là trạng thái (hoặc tập các trạng thái) mà hệ thống hướng tới và muốn đạt được.
- Hàm chuyển trạng thái (Transition Function):
Mô tả các phép biến đổi hợp lệ cho phép di chuyển từ trạng thái hiện tại sang trạng thái mới.
- Hàm kiểm tra mục tiêu (Goal Test):
Xác định xem trạng thái hiện tại có phải là trạng thái đích hay không.
- Hàm chi phí (Cost Function): (tùy chọn)
Xác định chi phí để thực hiện một bước chuyển từ trạng thái này sang trạng thái khác.
- Giải pháp (Solution):
Là một chuỗi các hành động hoặc trạng thái dẫn từ trạng thái khởi đầu đến trạng thái đích. Đây là kết quả mà thuật toán tìm kiếm trả về khi tìm được đường đi thỏa mãn yêu cầu bài toán.
