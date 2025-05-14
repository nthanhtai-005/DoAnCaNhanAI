import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
import random
import threading
import platform
import queue

# Constants
GRID_SIZE = 3
CELL_SIZE = 120
PADDING = 12
MAX_TIME = 15

# Colors
BG_COLOR = "#eef2f7"
FRAME_BG = "#ffffff"
PRIMARY_COLOR = "#4a6fa5"
SECONDARY_COLOR = "#6b8cae"
ACCENT_COLOR = "#28a745"
TEXT_COLOR = "#2c3e50"
EMPTY_COLOR = "#f8f9fa"
TILE_COLOR = "#e9ecef"
HOVER_COLOR = "#dee2e6"
STOP_COLOR = "#dc3545"
RESET_COLOR = "#ffc107"
GRAY = "#CD5C5C"

# Initial and goal states
INITIAL_STATE = np.array([
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1]
])
GOAL_STATE = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

class ModernTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert") if self.widget.bbox("insert") else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        frame = tk.Frame(self.tooltip, background=TEXT_COLOR, bd=1)
        frame.pack(fill="both", expand=True)
        label = tk.Label(frame, text=self.text, justify="left", background=TEXT_COLOR, foreground="white",
                         relief="solid", borderwidth=0, padx=5, pady=3, font=("Segoe UI", 10))
        label.pack(fill="both", expand=True)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class PuzzleTile(tk.Canvas):
    def __init__(self, parent, value, size=CELL_SIZE, bg=TILE_COLOR, **kwargs):
        super().__init__(parent, width=size, height=size, bg=bg, highlightthickness=0, **kwargs)
        self.value = value
        self.size = size
        self.draw()

    def draw(self):
        self.delete("all")
        if self.value == -1:
            self.create_rectangle(5, 5, self.size-5, self.size-5, fill=EMPTY_COLOR, outline="")
            self.create_text(self.size/2, self.size/2, text="?", font=("Segoe UI", 22, "bold"), fill=TEXT_COLOR)
        elif self.value == 0:
            self.create_rectangle(5, 5, self.size-5, self.size-5, fill=GRAY, outline="")
        else:
            self.create_rectangle(5, 5, self.size-5, self.size-5, fill=SECONDARY_COLOR, outline="")
            self.create_rectangle(3, 3, self.size-7, self.size-7, fill=self["bg"], outline="")
            self.create_text(self.size/2, self.size/2, text=str(self.value), font=("Segoe UI", 22, "bold"), fill=TEXT_COLOR)
        print(f"Vẽ ô với giá trị: {self.value} tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")

    def update_value(self, value):
        print(f"Cập nhật ô với giá trị: {value} tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
        self.value = value
        if value == -1:
            self.config(bg=EMPTY_COLOR)
        elif value == 0:
            self.config(bg=GRAY)
        else:
            self.config(bg=TILE_COLOR)
        self.draw()

class PuzzleGrid(tk.Frame):
    def __init__(self, parent, state=INITIAL_STATE, **kwargs):
        super().__init__(parent, bg=FRAME_BG, padx=PADDING, pady=PADDING, **kwargs)
        self.state = state.copy()
        self.grid_cells = []
        self.create_grid()

    def create_grid(self):
        print("Khởi tạo lưới với trạng thái ban đầu:")
        print(self.state)
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                value = self.state[i, j]
                color = EMPTY_COLOR if value == -1 else (GRAY if value == 0 else TILE_COLOR)
                cell = PuzzleTile(self, value, bg=color)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.grid_cells.append(row)

    def update_grid(self, state):
        print(f"Cập nhật lưới với trạng thái:\n{state} tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
        self.state = state.copy()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.grid_cells[i][j].update_value(state[i, j])

    def highlight_move(self, pos):
        i, j = pos
        print(f"Highlight ô tại vị trí: ({i}, {j}) tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
        self.grid_cells[i][j].config(bg="#ffb6c1")
        self.grid_cells[i][j].draw()

class AlgorithmInfoFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=FRAME_BG, padx=PADDING, pady=PADDING, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.info_label = tk.Label(self, text="Thông tin thuật toán", font=("Segoe UI", 14, "bold"),
                                   bg=FRAME_BG, fg=TEXT_COLOR)
        self.info_label.pack(anchor="w", pady=(0, 12))
        self.info_frame = tk.Frame(self, bg=FRAME_BG)
        self.info_frame.pack(fill="x", expand=True)
        self.create_info_field("Thuật toán", "Chọn một thuật toán")
        self.create_info_field("Số bước", "0")
        self.create_info_field("Thời gian chạy", "0.00 giây")

    def create_info_field(self, label_text, value_text):
        frame = tk.Frame(self.info_frame, bg=FRAME_BG)
        frame.pack(fill="x", pady=3)
        label = tk.Label(frame, text=f"{label_text}:", font=("Segoe UI", 11),
                         bg=FRAME_BG, fg=TEXT_COLOR, width=20, anchor="w")
        label.pack(side="left")
        value = tk.Label(frame, text=value_text, font=("Segoe UI", 11),
                         bg=FRAME_BG, fg=PRIMARY_COLOR)
        value.pack(side="left", fill="x", expand=True)
        setattr(self, f"{label_text.lower().replace(' ', '_')}_value", value)

    def update_info(self, algorithm=None, steps=None, runtime=None):
        if algorithm is not None:
            self.thuật_toán_value.config(text=algorithm)
        if steps is not None:
            self.số_bước_value.config(text=str(steps))
        if runtime is not None:
            self.thời_gian_chạy_value.config(text=f"{runtime:.2f} giây")

class ControlPanel(tk.Frame):
    def __init__(self, parent, start_callback, reset_callback, **kwargs):
        super().__init__(parent, bg=FRAME_BG, padx=PADDING, pady=PADDING, **kwargs)
        self.start_callback = start_callback
        self.reset_callback = reset_callback
        self.selected_algorithm = "Backtracking"
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="8-Puzzle Solver", font=("Segoe UI", 18, "bold"),
                         bg=FRAME_BG, fg=PRIMARY_COLOR)
        title.pack(anchor="w", pady=(0, 15))

        alg_frame = tk.Frame(self, bg=FRAME_BG)
        alg_frame.pack(fill="x", pady=(0, 12))
        alg_label = tk.Label(alg_frame, text="Thuật toán:", font=("Segoe UI", 11),
                             bg=FRAME_BG, fg=TEXT_COLOR)
        alg_label.pack(side="left", padx=(0, 5))

        self.algorithms = ["Backtracking", "Backtracking Forward", "Min-Conflicts"]
        self.algorithm_var = tk.StringVar(value=self.selected_algorithm)
        self.algorithm_dropdown = ttk.Combobox(alg_frame, textvariable=self.algorithm_var,
                                              values=self.algorithms, width=30, state="readonly",
                                              font=("Segoe UI", 10))
        self.algorithm_dropdown.pack(side="left", fill="x", expand=True)
        self.algorithm_dropdown.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        self.start_btn = tk.Button(self, text="Bắt đầu giải", font=("Segoe UI", 11, "bold"),
                                   bg=ACCENT_COLOR, fg="white", padx=15, pady=8, bd=0,
                                   command=self.start_callback)
        self.start_btn.pack(fill="x", pady=(10, 5))

        self.reset_btn = tk.Button(self, text="Đặt lại", font=("Segoe UI", 11, "bold"),
                                   bg=RESET_COLOR, fg="white", padx=15, pady=8, bd=0,
                                   command=self.reset_callback)
        self.reset_btn.pack(fill="x", pady=(5, 0))

        ModernTooltip(title, "Ứng dụng giải 8-Puzzle bằng nhiều thuật toán")
        ModernTooltip(self.algorithm_dropdown, "Chọn thuật toán để giải bài toán")
        ModernTooltip(self.start_btn, "Bắt đầu giải với thuật toán đã chọn")
        ModernTooltip(self.reset_btn, "Đặt lại bài toán về trạng thái ban đầu")

    def on_algorithm_change(self, event):
        self.selected_algorithm = self.algorithm_var.get()

    def get_algorithm(self):
        return self.selected_algorithm

    def disable_controls(self):
        self.algorithm_dropdown.config(state="disabled")
        self.start_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

    def enable_controls(self):
        self.algorithm_dropdown.config(state="readonly")
        self.start_btn.config(state="normal")
        self.reset_btn.config(state="normal")

class StatusBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PRIMARY_COLOR, **kwargs)
        self.status_label = tk.Label(self, text="Sẵn sàng", font=("Segoe UI", 10),
                                    bg=PRIMARY_COLOR, fg="white", padx=10, pady=4)
        self.status_label.pack(side="left", fill="x")

    def update_status(self, text):
        self.status_label.config(text=text)

def min_conflicts(start, goal, stop_flag, state_queue=None):
    start_time = time.time()
    steps = 0
    solution = []
    
    # Nếu không có state_queue, tạo một queue giả
    if state_queue is None:
        state_queue = queue.Queue()
    
    # Khởi tạo trạng thái ngẫu nhiên
    numbers = list(range(9))
    random.shuffle(numbers)
    state = np.full((3, 3), -1, dtype=int)
    
    # Đảm bảo trạng thái ban đầu được hiển thị
    state_queue.put((state.copy(), None))
    
    # Điền các số vào trạng thái ban đầu
    idx = 0
    for i in range(3):
        for j in range(3):
            if idx < len(numbers):
                state[i, j] = numbers[idx]
                solution.append(((i, j), numbers[idx]))
                # Gửi từng trạng thái vào queue để hiển thị
                state_queue.put((state.copy(), (i, j)))
                idx += 1
    
    steps = len(solution)

    def count_conflicts(state):
        conflicts = 0
        for i in range(3):
            for j in range(3):
                if state[i, j] != -1 and state[i, j] != goal[i, j]:
                    conflicts += 1
        return conflicts

    max_steps = 1000
    for step in range(max_steps):
        # Kiểm tra điều kiện dừng
        if stop_flag or time.time() - start_time > MAX_TIME:
            return None, steps, time.time() - start_time
        
        # Kiểm tra nếu đã đạt trạng thái mục tiêu
        if np.array_equal(state, goal):
            return solution, steps, time.time() - start_time
        
        # Tìm các ô có xung đột
        conflicted_cells = [
            (i, j) for i in range(3) for j in range(3) 
            if state[i, j] != -1 and state[i, j] != goal[i, j]
        ]
        
        if not conflicted_cells:
            break
        
        # Chọn ngẫu nhiên một ô có xung đột
        i, j = random.choice(conflicted_cells)
        
        # Tìm vị trí hoán đổi với số lượng xung đột tối thiểu
        min_conflicts = float('inf')
        best_swaps = []
        
        for ni in range(3):
            for nj in range(3):
                if (ni, nj) != (i, j) and state[ni, nj] != -1:
                    # Tạo trạng thái mới bằng cách hoán đổi
                    new_state = state.copy()
                    new_state[i, j], new_state[ni, nj] = new_state[ni, nj], new_state[i, j]
                    
                    # Đếm số lượng xung đột
                    conflicts = count_conflicts(new_state)
                    
                    # Cập nhật các vị trí hoán đổi tối ưu
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_swaps = [(ni, nj)]
                    elif conflicts == min_conflicts:
                        best_swaps.append((ni, nj))
        
        # Chọn ngẫu nhiên một vị trí hoán đổi trong các vị trí tối ưu
        if best_swaps:
            ni, nj = random.choice(best_swaps)
            
            # Hoán đổi và cập nhật solution
            state[i, j], state[ni, nj] = state[ni, nj], state[i, j]
            solution.append(((i, j), state[i, j]))
            steps += 1
            
            # Gửi trạng thái mới vào queue để hiển thị
            state_queue.put((state.copy(), (i, j)))
            state_queue.put((state.copy(), (ni, nj)))
    
    return None, steps, time.time() - start_time


class PuzzleSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(900, 600)
        try:
            if platform.system() == "Windows":
                self.root.state('zoomed')
            else:
                self.root.attributes('-zoomed', True)
        except:
            self.root.maxsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", fieldbackground=FRAME_BG, background=FRAME_BG)
        self.setup_ui()
        self.running = False
        self.stop_flag = False
        self.solution_thread = None
        self.current_solution = None
        self.current_state = None
        self.current_initial_state = INITIAL_STATE.copy()
        self.state_queue = queue.Queue()
        self.check_queue()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        left_panel = tk.Frame(main_frame, bg=BG_COLOR)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.control_panel = ControlPanel(left_panel, self.start_solving, self.reset_solving)
        self.control_panel.pack(fill="x", pady=(0, 12))
        grid_frame = tk.Frame(left_panel, bg=FRAME_BG, padx=PADDING, pady=PADDING)
        grid_frame.pack(fill="both", expand=True)
        grid_label = tk.Label(grid_frame, text="Trạng thái hiện tại", font=("Segoe UI", 14, "bold"),
                             bg=FRAME_BG, fg=TEXT_COLOR)
        grid_label.pack(anchor="w", pady=(0, 12))
        self.puzzle_grid = PuzzleGrid(grid_frame, state=INITIAL_STATE)
        self.puzzle_grid.pack(pady=10)
        right_panel = tk.Frame(main_frame, bg=BG_COLOR)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.algorithm_info = AlgorithmInfoFrame(right_panel)
        self.algorithm_info.pack(fill="x", pady=(0, 12))
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side="bottom", fill="x")

    def check_queue(self):
        print(f"Đang kiểm tra hàng đợi, kích thước queue: {self.state_queue.qsize()} tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
        try:
            state, pos = self.state_queue.get(timeout=0.1)
            print(f"Lấy trạng thái từ queue: \n{state}, Vị trí: {pos} tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
            self.puzzle_grid.update_grid(state)
            if pos:
                self.puzzle_grid.highlight_move(pos)
            self.root.update_idletasks()
            self.root.update()
            print(f"Đã cập nhật giao diện với trạng thái: \n{state} tại thời gian: {time.time()}")
            self.root.after(2000, self.check_queue)  # Độ trễ 2 giây
        except queue.Empty:
            print(f"Hàng đợi trạng thái trống tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
            self.root.after(100, self.check_queue)  # Kiểm tra lại sau 100ms

    def reset_solving(self):
        self.stop_flag = True
        self.running = False
        self.status_bar.update_status("Đang đặt lại...")
        if self.solution_thread is not None and self.solution_thread.is_alive():
            try:
                self.solution_thread.join(timeout=3.0)
            except:
                pass
        self.solution_thread = None
        self.current_solution = None
        self.current_state = None
        self.current_initial_state = INITIAL_STATE.copy()
        self.puzzle_grid.update_grid(INITIAL_STATE)
        self.algorithm_info.update_info(algorithm="Chọn một thuật toán", steps=0, runtime=0)
        self.status_bar.update_status("Sẵn sàng")
        self.control_panel.enable_controls()
        with self.state_queue.mutex:
            self.state_queue.queue.clear()

    def start_solving(self):
        if self.running:
            return
        if self.solution_thread is not None and self.solution_thread.is_alive():
            messagebox.showwarning("Cảnh báo", "Thuật toán trước đó vẫn đang chạy. Vui lòng chờ hoặc đặt lại.")
            return
        algorithm = self.control_panel.get_algorithm()
        self.running = True
        self.stop_flag = False
        self.control_panel.disable_controls()
        self.status_bar.update_status(f"Đang giải với {algorithm}...")
        self.algorithm_info.update_info(algorithm=algorithm)
        self.puzzle_grid.update_grid(INITIAL_STATE)
        self.state_queue.put((INITIAL_STATE.copy(), None))
        print(f"Gửi trạng thái ban đầu vào queue: \n{INITIAL_STATE} tại thời gian: {time.time()}")
        self.solution_thread = threading.Thread(target=self.solve_puzzle, args=(algorithm,))
        self.solution_thread.daemon = True
        self.solution_thread.start()

    def solve_puzzle(self, algorithm):
        try:
            solution, steps, runtime = self.run_algorithm(algorithm)
            self.current_solution = solution
            self.root.after(15000, lambda: self.finalize(algorithm, solution, steps, runtime))  # Chờ 15 giây
        except Exception as error:
            print(f"Lỗi trong {algorithm}: {str(error)} tại thời gian: {time.time()}")
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi trong {algorithm}: {str(error)}"))
            self.root.after(0, lambda: self.status_bar.update_status(f"Lỗi trong {algorithm}"))
            self.root.after(0, lambda: self.control_panel.enable_controls())
            self.running = False

    def finalize(self, algorithm, solution, steps, runtime):
        self.running = False
        if solution:
            self.algorithm_info.update_info(steps=steps, runtime=runtime)
            self.status_bar.update_status(
                f"Đã giải với {algorithm} trong {steps} bước. Thời gian: {runtime:.2f}s")
        else:
            self.algorithm_info.update_info(steps=steps, runtime=runtime)
            self.status_bar.update_status(
                f"Không tìm thấy lời giải với {algorithm}. Thời gian: {runtime:.2f}s")
        self.control_panel.enable_controls()

    def run_algorithm(self, algorithm_name):
        start_state = self.current_initial_state.copy()
        algorithm_map = {
            "Backtracking": lambda s, g, sf: backtracking_process(s, g, sf, self.state_queue),
            "Backtracking Forward": lambda s, g, sf: backtracking_forward_checking(s, g, sf, self.state_queue),
            "Min-Conflicts": lambda s, g, sf: min_conflicts(s, g, sf, state_queue=self.state_queue)
        }
        if algorithm_name not in algorithm_map:
            raise ValueError(f"Thuật toán {algorithm_name} không được hỗ trợ")
        return algorithm_map[algorithm_name](start_state, GOAL_STATE, self.stop_flag)

def forward_check(state, used_numbers):
    remaining_numbers = set(range(9)) - used_numbers
    unassigned_positions = [(i, j) for i in range(3) for j in range(3) if state[i, j] == -1]
    required_numbers = {GOAL_STATE[i, j] for i, j in unassigned_positions if GOAL_STATE[i, j] != 0}
    return len(remaining_numbers) >= len(unassigned_positions) and required_numbers.issubset(remaining_numbers)

def backtracking_process(start, goal, stop_flag, state_queue):
    start_time = time.time()
    steps = 0
    solution = []
    print("Bắt đầu Backtracking với trạng thái ban đầu:")
    print(start)

    def backtrack(state, depth):
        nonlocal steps, stop_flag
        if stop_flag or time.time() - start_time > MAX_TIME:
            print(f"Dừng tại độ sâu {depth} do stop_flag hoặc vượt quá MAX_TIME")
            return False
        print(f"\nBước {depth}:")
        print("Trạng thái hiện tại:")
        print(state)
        if np.array_equal(state, goal):
            print(f"Đạt trạng thái mục tiêu tại bước {depth}:")
            print(state)
            state_queue.put((state.copy(), None))
            return True
        unassigned = [(i, j) for i in range(3) for j in range(3) if state[i, j] == -1]
        if not unassigned:
            print("Không còn ô trống, nhưng chưa đạt mục tiêu")
            return False
        i, j = unassigned[0]
        used_numbers = set(state.flatten()) - {-1}
        for num in range(9):
            if num not in used_numbers:
                state[i, j] = num
                steps += 1
                print(f"Gán số {num} vào ô ({i}, {j}) tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
                print("Trạng thái sau khi gán:")
                print(state)
                solution.append(((i, j), num))
                print(f"Solution hiện tại: {solution}")
                state_queue.put((state.copy(), (i, j)))
                print(f"Gửi trạng thái vào queue: \n{state}, Vị trí: ({i}, {j}) tại thời gian: {time.time()}")
                if backtrack(state, depth + 1):
                    return True
                state[i, j] = -1
                solution.pop()
                steps += 1
                print(f"Quay lui: Xóa số {num} khỏi ô ({i}, {j}) tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
                print("Trạng thái sau khi quay lui:")
                print(state)
                state_queue.put((state.copy(), None))
                print(f"Gửi trạng thái quay lui vào queue: \n{state}, Vị trí: None tại thời gian: {time.time()}")
        print(f"Không tìm thấy giải pháp tại bước {depth}")
        return False

    state = start.copy()
    success = backtrack(state, 0)
    end_time = time.time()
    print(f"Kết thúc Backtracking: {'Thành công' if success else 'Thất bại'}")
    print(f"Số bước: {steps}, Thời gian: {end_time - start_time:.2f}s")
    print(f"Solution cuối cùng: {solution if success else 'Không có'}")
    return (solution if success else None, steps, end_time - start_time)

def backtracking_forward_checking(start, goal, stop_flag, state_queue):
    start_time = time.time()
    steps = 0
    solution = []
    print("Bắt đầu Backtracking Forward Checking với trạng thái ban đầu:")
    print(start)

    def backtrack(state, depth):
        nonlocal steps, stop_flag
        if stop_flag or time.time() - start_time > MAX_TIME:
            print(f"Dừng tại độ sâu {depth} do stop_flag hoặc vượt quá MAX_TIME")
            return False
        print(f"\nBước {depth}:")
        print("Trạng thái hiện tại:")
        print(state)
        if np.array_equal(state, goal):
            print(f"Đạt trạng thái mục tiêu tại bước {depth}:")
            print(state)
            state_queue.put((state.copy(), None))
            return True
        unassigned = [(i, j) for i in range(3) for j in range(3) if state[i, j] == -1]
        if not unassigned:
            print("Không còn ô trống, nhưng chưa đạt mục tiêu")
            return False
        i, j = unassigned[0]
        used_numbers = set(state.flatten()) - {-1}
        for num in range(9):
            if num not in used_numbers:
                state[i, j] = num
                steps += 1
                if forward_check(state, used_numbers | {num}):
                    solution.append(((i, j), num))
                    print(f"Gán số {num} vào ô ({i}, {j}) tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
                    print("Trạng thái sau khi gán:")
                    print(state)
                    print(f"Solution hiện tại: {solution}")
                    state_queue.put((state.copy(), (i, j)))
                    print(f"Gửi trạng thái vào queue: \n{state}, Vị trí: ({i}, {j}) tại thời gian: {time.time()}")
                    if backtrack(state, depth + 1):
                        return True
                state[i, j] = -1
                if solution and solution[-1][0] == (i, j):
                    solution.pop()
                steps += 1
                print(f"Quay lui: Xóa số {num} khỏi ô ({i}, {j}) tại thời gian: {time.time()}, luồng: {threading.current_thread().name}")
                print("Trạng thái sau khi quay lui:")
                print(state)
                state_queue.put((state.copy(), None))
                print(f"Gửi trạng thái quay lui vào queue: \n{state}, Vị trí: None tại thời gian: {time.time()}")
        print(f"Không tìm thấy giải pháp tại bước {depth}")
        return False

    state = start.copy()
    success = backtrack(state, 0)
    end_time = time.time()
    print(f"Kết thúc Backtracking Forward Checking: {'Thành công' if success else 'Thất bại'}")
    print(f"Số bước: {steps}, Thời gian: {end_time - start_time:.2f}s")
    print(f"Solution cuối cùng: {solution if success else 'Không có'}")
    return (solution if success else None, steps, end_time - start_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleSolverApp(root)
    root.mainloop()