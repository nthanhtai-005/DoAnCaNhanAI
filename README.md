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
![UninformedSearchAlgorithms](https://github.com/user-attachments/assets/07168c8f-68ac-49dd-827f-44789f2184d1)
### Nhận xét
- BFS có thể thăm rất nhiều trạng thái, đặc biệt là trong các bài toán có không gian trạng thái rộng và sâu. Tuy nhiên, nó đảm bảo tìm được giải pháp tối ưu nếu có giải pháp, nhưng thời gian thực thi sẽ chậm khi độ sâu của giải pháp lớn, vì phải lưu trữ tất cả các trạng thái đã thăm.
- DFS có thể thăm ít trạng thái hơn trong một số trường hợp, đặc biệt khi giải pháp gần gốc, nhưng không thể đảm bảo tìm được giải pháp tối ưu và có thể rơi vào tình trạng không kết thúc nếu không có giải pháp. Thời gian thực thi có thể nhanh trong một số trường hợp, nhưng dễ gặp phải vòng lặp và thiếu tính ổn định trong việc tìm giải pháp.
- UCS có thể thăm nhiều trạng thái hơn BFS vì phải kiểm tra các trạng thái có chi phí thấp nhất trước, nhưng lại đảm bảo tìm được giải pháp tối ưu. Tuy nhiên, UCS tốn thời gian và bộ nhớ hơn so với BFS, vì phải xử lý và lưu trữ các trạng thái theo chi phí của chúng.
- IDS có thể thăm ít trạng thái hơn BFS hoặc UCS vì chỉ duyệt qua các độ sâu một lần, nhưng lại thăm lại các trạng thái ở các độ sâu thấp nhiều lần, điều này làm tăng số lượng trạng thái đã thăm trong trường hợp độ sâu của bài toán lớn. Mặc dù IDS tiết kiệm bộ nhớ, nhưng thời gian thực thi có thể tốn kém do phải kiểm tra lại các trạng thái ở mỗi độ sâu.
