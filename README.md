# DoAnCaNhanAI
![GiaoDien](https://github.com/user-attachments/assets/3941f0c8-044c-40de-bcfd-d297d5f7337b)
## 1. Mục tiêu
### Bài tập cá nhân này sử dụng các thuật toán tìm kiếm để giải quyết bài toán 8-puzzle. Cụ thể, đề tài tập trung vào 6 nhóm thuật toán chính:
- Thuật toán tìm kiếm không có thông tin (Uninformed Search) như BFS, DFS, IDS và UCS, giúp khảo sát khả năng tìm lời giải khi không có thông tin định hướng.
- Thuật toán tìm kiếm có thông tin (Informed Search) như A*, IDA* và Greedy Best-First Search, sử dụng heuristic để tối ưu hóa hiệu quả tìm kiếm.
- Bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problems - CSP) như Forward-Checking, Backtracking và Min-Conflicts nhằm khảo sát khả năng biểu diễn 8-puzzle dưới dạng hệ thống ràng buộc logic.
- Tìm kiếm cục bộ (Local Search) như Simple Hill Climbing, Steepest Ascent Hill Climbing, Stochastic Hill Climbing và Beam Search, Simulated Annealing, Genetic Algorithm tập trung vào việc cải thiện nghiệm cục bộ mà không cần duy trì toàn bộ không gian trạng thái.
- Tìm kiếm trong môi trường phức tạp (Searching in Complex Environments) như AND-OR Graph Search, Searching for a partially observation, Sensorless mở rộng khả năng ứng dụng sang các bài toán có tính động và không chắc chắn, định hướng cho các nghiên cứu nâng cao.
- Học Tăng cường (Reinforcement Learning) như Q-Learning. Mô hình hóa quá trình học thông qua tương tác giữa tác nhân (agent) và môi trường (environment). Q-Learning giúp tác nhân tối đa hóa phần thưởng tích lũy bằng cách học chính sách tối ưu từ kinh nghiệm, không cần mô hình môi trường.
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
#### Iterative Deepening A - IDA*
- Là phiên bản tiết kiệm bộ nhớ của A*.
- Duyệt theo chiều sâu với ngưỡng f(n) tăng dần (thay vì độ sâu như IDS).
- Mỗi vòng lặp DFS chỉ mở rộng các nút có f(n) không vượt quá ngưỡng hiện tại.
- Ưu điểm: Tìm lời giải tối ưu như A*, tiết kiệm bộ nhớ hơn vì không cần lưu toàn bộ cây.
- Nhược điểm: Phải duyệt lại các nút trong nhiều vòng lặp → tốn thời gian hơn A* trong một số trường hợp.
![InformedSearchAlgorithms](https://github.com/user-attachments/assets/579d6088-8e12-4f8a-80a1-2a62f3e40af5)
### Bài toán Thỏa mãn Ràng buộc (Constraint Satisfaction Problems - CSP)
Bài toán thỏa mãn ràng buộc (CSP) là bài toán trong đó lời giải là một tập hợp các giá trị gán cho một số biến sao cho mọi ràng buộc (constraints) đều được thỏa mãn.
#### Backtracking (Tìm kiếm quay lui)
- Là phương pháp cơ bản nhất: thử từng giá trị khả dĩ cho từng biến theo thứ tự, kiểm tra ràng buộc, và quay lui nếu có xung đột.
- Quy trình: Gán giá trị cho biến đầu tiên. Kiểm tra các ràng buộc. Nếu hợp lệ → tiếp tục với biến kế tiếp. Nếu không hợp lệ → quay lui và thử giá trị khác.
- Ưu điểm: Dễ cài đặt, hiệu quả cho các bài toán nhỏ.
- Nhược điểm: Tốn thời gian với không gian tìm kiếm lớn, hông tận dụng nhiều thông tin về ràng buộc trong quá trình tìm kiếm.
#### Forward Checking (Dự đoán trước)
- Là cải tiến của Backtracking. Khi gán giá trị cho một biến, thuật toán loại bỏ các giá trị không hợp lệ khỏi miền của các biến chưa gán.
- Cách hoạt động: Mỗi khi gán một giá trị cho biến, kiểm tra xem liệu ràng buộc với các biến còn lại có làm miền của chúng rỗng hay không.
- Ưu điểm: Giảm số lượng nhánh vô ích, tăng tốc độ tìm kiếm bằng cách phát hiện xung đột sớm.
- Nhược điểm: Cần thêm chi phí để duy trì miền biến cập nhật.
#### Min-Conflicts (Giải thuật xung đột tối thiểu)
Là thuật toán tìm kiếm cục bộ (local search), thường dùng cho bài toán có lời giải lớn như giải ô chữ, Sudoku, n-queens.
- Cách hoạt động: Khởi tạo gán giá trị ngẫu nhiên. Tại mỗi bước, chọn biến đang vi phạm ràng buộc. Gán lại giá trị cho biến đó sao cho số lượng ràng buộc bị vi phạm là ít nhất. Lặp lại cho đến khi không còn xung đột.
- Ưu điểm: Hiệu quả với bài toán có không gian trạng thái lớn, không cần quay lui.
- Nhược điểm: Không đảm bảo tìm được lời giải nếu bị mắc kẹt tại cực trị cục bộ, không áp dụng tốt cho bài toán có ít hoặc không có lời giải.
![ConstraintSatisfactionProblems](https://github.com/user-attachments/assets/61e31eed-8652-4000-b906-19e4a17cbba1)
### Tìm kiếm Cục bộ (Local Search Algorithms)
Local Search là một phương pháp tìm kiếm không khám phá toàn bộ không gian trạng thái, mà chỉ tập trung vào việc cải thiện nghiệm hiện tại bằng cách di chuyển đến trạng thái lân cận tốt hơn. Phù hợp với các bài toán tối ưu hóa và khi không cần biết rõ trạng thái đích, chỉ cần tìm một nghiệm "tốt".
#### Simple Hill Climbing
- Di chuyển đến trạng thái lân cận đầu tiên tốt hơn trạng thái hiện tại.
- Nếu không có trạng thái lân cận nào tốt hơn, thuật toán sẽ dừng lại (rơi vào cực trị cục bộ).
- Ưu điểm: Dễ hiểu, dễ triển khai.
- Nhược điểm: Dễ bị kẹt ở điểm cực trị cục bộ, không xét tất cả lân cận, nên dễ bỏ lỡ nghiệm tốt hơn.
#### Steepest Ascent Hill Climbing
- Xét tất cả các trạng thái lân cận và chọn trạng thái có giá trị tốt nhất để di chuyển.
- Ưu điểm: Tìm được hướng đi tốt nhất trong mỗi bước.
- Nhược điểm: Tốn thời gian hơn so với Simple Hill Climbing, vẫn có nguy cơ rơi vào cực trị cục bộ.
#### Stochastic Hill Climbing
- Thay vì chọn lân cận tốt nhất, thuật toán chọn ngẫu nhiên một lân cận tốt hơn để tránh rơi vào các điểm cực trị cục bộ quá sớm.
- Ưu điểm: Giảm xác suất kẹt ở cực trị cục bộ, dễ triển khai.
- Nhược điểm: Kết quả có thể không ổn định, không đảm bảo luôn tìm được nghiệm tối ưu.
#### Beam Search
- Giữ k trạng thái tốt nhất tại mỗi bước (thay vì 1 trạng thái như Hill Climbing).
- Ưu điểm: Khám phá được nhiều hướng đi cùng lúc, dễ mở rộng và song song hóa.
- Nhược điểm: Tốn nhiều bộ nhớ hơn, nếu k nhỏ, dễ bỏ qua hướng đi tối ưu.
#### Simulated Annealing
- Cho phép di chuyển đến trạng thái kém hơn một cách ngẫu nhiên, với xác suất giảm dần theo thời gian (theo "nhiệt độ").
- Ưu điểm: Có khả năng thoát khỏi cực trị cục bộ, hiệu quả cho các bài toán tối ưu phức tạp.
- Nhược điểm: Cần điều chỉnh tham số “nhiệt độ” phù hợp, chậm khi nhiệt độ giảm quá thấp.
#### Genetic Algorithm
- Mô phỏng quá trình tiến hóa tự nhiên:
- Khởi tạo quần thể cá thể ngẫu nhiên.
- Lựa chọn, lai ghép, đột biến để tạo cá thể mới.
- Lặp lại qua nhiều thế hệ để cải thiện chất lượng nghiệm.
- Ưu điểm: Khả năng tìm kiếm toàn cục cao, tốt cho bài toán có không gian trạng thái lớn và phức tạp.
- Nhược điểm: Cần điều chỉnh nhiều tham số (tỷ lệ lai, tỷ lệ đột biến…), tốn thời gian và tài nguyên.
![LocalSearchAlgorithms](https://github.com/user-attachments/assets/5ce44d23-06a6-4351-b5f4-9eeee159717e)
### Tìm kiếm trong Môi trường Phức tạp (Searching in Complex Environments)
Khi giải quyết các bài toán trong môi trường phức tạp, thuật toán tìm kiếm không chỉ cần xử lý không gian trạng thái lớn mà còn phải đối phó với tình huống quan sát không đầy đủ hoặc cấu trúc mạng phức tạp. Các thuật toán tìm kiếm trong môi trường phức tạp cung cấp phương pháp để lập kế hoạch và tìm kiếm hiệu quả trong những môi trường không chắc chắn và phức tạp.
#### AND-OR Graph Search
- AND-OR Graph Search được sử dụng trong các bài toán có cấu trúc AND-OR, nơi một trạng thái có thể yêu cầu kết hợp các hành động (AND) hoặc lựa chọn giữa các hành động (OR).
- Quy trình: AND: Tất cả các hành động trong nhánh phải được thực hiện để đạt được mục tiêu. OR: Chỉ cần thực hiện một trong các hành động có thể để đạt được mục tiêu.
- Ứng dụng: Được sử dụng trong các bài toán quyết định như lập kế hoạch hành động với các lựa chọn thay thế (choices).
- Ưu điểm: Có thể mô tả các bài toán phức tạp với các lựa chọn thay thế hoặc sự kết hợp hành động.
- Nhược điểm: Tìm kiếm phức tạp hơn, cần sử dụng cấu trúc đồ thị đặc biệt.
#### Searching for a Partially Observable Environment
Bài toán tìm kiếm trong môi trường quan sát một phần là khi một hệ thống không thể quan sát đầy đủ mọi trạng thái của môi trường, ví dụ trong các hệ thống robot tự động hoặc hệ thống trí tuệ nhân tạo với dữ liệu đầu vào bị giới hạn.
- Cách tiếp cận: Partially Observable Markov Decision Process (POMDP): Đây là một mô hình quyết định trong môi trường không hoàn toàn quan sát được, giúp mô tả các hành động và quyết định trong môi trường có thông tin không đầy đủ, heuristic-based search: Sử dụng các chiến lược dự đoán thông qua các yếu tố như cảm biến hoặc dữ liệu lịch sử.
- Ưu điểm: Hữu ích trong các ứng dụng AI thực tế, nơi không thể có thông tin đầy đủ về trạng thái môi trường, dễ dàng áp dụng trong các bài toán robot và tự động hóa.
- Nhược điểm: Tính toán phức tạp do môi trường không thể quan sát toàn diện, cần các mô hình xác suất phức tạp.
#### Sensorless Search
Sensorless Search là thuật toán tìm kiếm được áp dụng trong các bài toán mà hệ thống không có khả năng cảm biến để quan sát trực tiếp trạng thái hiện tại của môi trường. Thay vì sử dụng cảm biến trực tiếp, thuật toán dựa vào các giả thuyết hoặc ước lượng để tiên đoán trạng thái môi trường.
- Cách hoạt động: Thuật toán dựa vào các dự đoán từ thông tin lịch sử và các hành động đã thực hiện trước đó để ước lượng trạng thái hiện tại, thường được sử dụng trong bài toán robot tự hành khi không thể có thông tin trực tiếp từ cảm biến.
- Ưu điểm: Hiệu quả trong môi trường không có cảm biến hoặc khi việc sử dụng cảm biến là không khả thi, giảm bớt phụ thuộc vào phần cứng cảm biến.
- Nhược điểm: Khó khăn trong việc duy trì độ chính xác cao trong suốt quá trình tìm kiếm, ddễ gặp phải lỗi khi dự đoán sai trạng thái.
![SearchinginComplexEnvironments](https://github.com/user-attachments/assets/bb837d01-fcb5-4281-8287-933def4269d0)
### Học tăng cường (Reinforcement Learning)
Reinforcement Learning (Học tăng cường) là một phương pháp học máy trong đó tác nhân (agent) học cách hành động trong môi trường bằng cách tương tác và nhận phản hồi (reward). Mục tiêu của tác nhân là tối đa hóa phần thưởng tích lũy theo thời gian.
#### Q-Learning
Q-Learning là một thuật toán học tăng cường không cần mô hình môi trường (model-free). Nó sử dụng bảng Q (Q-table) để ước lượng giá trị hành động tại mỗi trạng thái.  
Quy trình hoạt động:  
- Khởi tạo Q-table với các giá trị bằng 0 hoặc ngẫu nhiên.
- Lặp lại cho đến khi đạt điều kiện dừng:
- Chọn hành động a tại trạng thái s theo chiến lược ε-greedy.
- Thực hiện hành động, nhận phần thưởng r và trạng thái kế tiếp s'.
- Cập nhật Q(s, a) bằng công thức trên.
- Chuyển sang trạng thái mới s'.
  
Ưu điểm:  
- Đơn giản, dễ cài đặt.
- Hiệu quả trong môi trường có không gian trạng thái hữu hạn.
- Không cần mô hình môi trường.
  
Nhược điểm:  
- Q-table không hiệu quả cho môi trường có không gian trạng thái lớn hoặc liên tục (→ cần Deep Q-Learning).
- Hiệu suất phụ thuộc vào chiến lược chọn hành động và tham số học.
![ReinforcementLearning](https://github.com/user-attachments/assets/e178dfcb-ab5f-4bce-922f-b23e0bd6138f)
