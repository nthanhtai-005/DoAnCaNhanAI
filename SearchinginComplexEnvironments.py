import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
from collections import deque
import heapq
import random
import math
import threading
import platform

# Constants
GRID_SIZE = 3
CELL_SIZE = 120
PADDING = 12
ANIMATION_SPEED = 50
MAX_STATES_VISITED = 50000
MAX_TIME = 15
MAX_DEPTH = 50

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

# Initial and goal states
INITIAL_STATE = np.array([
     [1, 2, 3],
    [5, 0, 6],
    [4, 7, 8]
])
GOAL_STATE = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

# Precompute goal positions for heuristic optimization
GOAL_POSITIONS = {value: np.where(GOAL_STATE == value)[0][0] * 3 + np.where(GOAL_STATE == value)[1][0]
                  for value in range(1, 9)}
GOAL_POSITIONS[0] = 8

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
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.draw()

    def draw(self):
        self.delete("all")
        if self.value != 0:
            self.create_rectangle(5, 5, self.size-5, self.size-5, fill=SECONDARY_COLOR, outline="")
            self.create_rectangle(3, 3, self.size-7, self.size-7, fill=self["bg"], outline="")
            self.create_text(self.size/2, self.size/2, text=str(self.value),
                            font=("Segoe UI", 22, "bold"), fill=TEXT_COLOR)

    def on_hover(self, event):
        if self.value != 0:
            self.config(bg=HOVER_COLOR)
            self.draw()

    def on_leave(self, event):
        if self.value != 0:
            self.config(bg=TILE_COLOR)
            self.draw()

    def update_value(self, value):
        self.value = value
        if value == 0:
            self.config(bg=EMPTY_COLOR)
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
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                value = self.state[i, j]
                color = EMPTY_COLOR if value == 0 else TILE_COLOR
                cell = PuzzleTile(self, value, bg=color)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.grid_cells.append(row)

    def update_grid(self, state):
        self.state = state.copy()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.grid_cells[i][j].update_value(state[i, j])

    def highlight_move(self, old_pos, new_pos):
        old_x, old_y = old_pos
        new_x, new_y = new_pos
        self.grid_cells[old_x][old_y].config(bg="#d7e5f0")
        self.grid_cells[old_x][old_y].draw()
        self.grid_cells[new_x][new_y].config(bg="#d7e5f0")
        self.grid_cells[new_x][new_y].draw()
        self.after(300, lambda: self.update_grid(self.state))

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
        self.create_info_field("Số trạng thái đã thăm", "0")
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

    def update_info(self, algorithm=None, steps=None, states=None, runtime=None):
        if algorithm is not None:
            self.thuật_toán_value.config(text=algorithm)
        if steps is not None:
            self.số_bước_value.config(text=str(steps))
        if states is not None:
            self.số_trạng_thái_đã_thăm_value.config(text=str(states))
        if runtime is not None:
            self.thời_gian_chạy_value.config(text=f"{runtime:.2f} giây")

class ControlPanel(tk.Frame):
    def __init__(self, parent, start_callback, stop_callback, reset_callback, **kwargs):
        super().__init__(parent, bg=FRAME_BG, padx=PADDING, pady=PADDING, **kwargs)
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.reset_callback = reset_callback
        self.selected_algorithm = "AND-OR Tree Search"
        self.speed_factor = tk.IntVar(value=1)
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

        self.algorithms = [
            "AND-OR Tree Search",
            "Partially Observable Search"
        ]

        self.algorithm_var = tk.StringVar(value=self.selected_algorithm)
        self.algorithm_dropdown = ttk.Combobox(alg_frame, textvariable=self.algorithm_var,
                                             values=self.algorithms, width=30, state="readonly",
                                             font=("Segoe UI", 10))
        self.algorithm_dropdown.pack(side="left", fill="x", expand=True)
        self.algorithm_dropdown.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        speed_frame = tk.Frame(self, bg=FRAME_BG)
        speed_frame.pack(fill="x", pady=(0, 15))

        speed_label = tk.Label(speed_frame, text="Tốc độ:", font=("Segoe UI", 11),
                               bg=FRAME_BG, fg=TEXT_COLOR)
        speed_label.pack(side="left", padx=(0, 5))

        button_frame = tk.Frame(speed_frame, bg=FRAME_BG)
        button_frame.pack(side="left", fill="x", expand=True)

        self.speed_buttons = []
        for speed, text in [(1, "x1"), (2, "x2"), (5, "x5")]:
            btn = tk.Button(button_frame, text=text, font=("Segoe UI", 10),
                           width=5, bg=PRIMARY_COLOR if speed == self.speed_factor.get() else SECONDARY_COLOR,
                           fg="white", bd=0, padx=10, pady=3,
                           command=lambda s=speed: self.set_speed(s))
            btn.pack(side="left", padx=4)
            self.speed_buttons.append((speed, btn))

        self.start_btn = tk.Button(self, text="Bắt đầu giải", font=("Segoe UI", 11, "bold"),
                                  bg=ACCENT_COLOR, fg="white", padx=15, pady=8, bd=0,
                                  command=self.start_callback)
        self.start_btn.pack(fill="x", pady=(10, 5))

        action_frame = tk.Frame(self, bg=FRAME_BG)
        action_frame.pack(fill="x")

        self.stop_btn = tk.Button(action_frame, text="Dừng", font=("Segoe UI", 11, "bold"),
                                 bg=STOP_COLOR, fg="white", padx=15, pady=8, bd=0,
                                 command=self.stop_callback, state="disabled")
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.reset_btn = tk.Button(action_frame, text="Đặt lại", font=("Segoe UI", 11, "bold"),
                                  bg=RESET_COLOR, fg="white", padx=15, pady=8, bd=0,
                                  command=self.reset_callback)
        self.reset_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        ModernTooltip(title, "Ứng dụng giải 8-Puzzle bằng nhiều thuật toán tìm kiếm")
        ModernTooltip(self.algorithm_dropdown, "Chọn thuật toán để giải bài toán")
        ModernTooltip(self.start_btn, "Bắt đầu giải với thuật toán đã chọn")
        ModernTooltip(self.stop_btn, "Dừng quá trình giải hiện tại")
        ModernTooltip(self.reset_btn, "Đặt lại bài toán về trạng thái ban đầu")

    def on_algorithm_change(self, event):
        self.selected_algorithm = self.algorithm_var.get()

    def set_speed(self, speed):
        self.speed_factor.set(speed)
        for s, btn in self.speed_buttons:
            btn.config(bg=PRIMARY_COLOR if s == speed else SECONDARY_COLOR)

    def get_algorithm(self):
        return self.selected_algorithm

    def get_speed(self):
        return self.speed_factor.get()

    def disable_controls(self):
        self.algorithm_dropdown.config(state="disabled")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.reset_btn.config(state="normal")

    def enable_controls(self):
        self.algorithm_dropdown.config(state="readonly")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

class StatusBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PRIMARY_COLOR, **kwargs)
        self.status_label = tk.Label(self, text="Sẵn sàng", font=("Segoe UI", 10),
                                    bg=PRIMARY_COLOR, fg="white", padx=10, pady=4)
        self.status_label.pack(side="left", fill="x")

    def update_status(self, text):
        self.status_label.config(text=text)

class SolutionVisualizer(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=FRAME_BG, padx=PADDING, pady=PADDING, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Các bước giải", font=("Segoe UI", 14, "bold"),
                                   bg=FRAME_BG, fg=TEXT_COLOR)
        self.title_label.pack(anchor="w", pady=(0, 12))

        self.steps_list = tk.Frame(self, bg=FRAME_BG)
        self.steps_list.pack(fill="both", expand=True)

        self.placeholder = tk.Label(self.steps_list, text="Chưa có lời giải",
                                   font=("Segoe UI", 11), bg=FRAME_BG, fg=TEXT_COLOR)
        self.placeholder.pack(pady=20)

    def display_solution(self, solution_path, algorithm, initial_state=INITIAL_STATE):
        for widget in self.steps_list.winfo_children():
            widget.destroy()

        if not solution_path:
            self.placeholder = tk.Label(self.steps_list, text="Không tìm thấy lời giải",
                                    font=("Segoe UI", 11), bg=FRAME_BG, fg=TEXT_COLOR)
            self.placeholder.pack(pady=20)
            return

        self.title_label.config(text=f"Các bước giải ({algorithm})")

        canvas_frame = tk.Frame(self.steps_list, bg=FRAME_BG)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=FRAME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg=FRAME_BG)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Hiển thị ma trận trạng thái cho tất cả thuật toán
        current_state = initial_state.copy()
        states = [current_state.copy()]
        for new_x, new_y in solution_path:
            try:
                x, y = location(current_state)
                current_state = swap(current_state, x, y, new_x, new_y)
                states.append(current_state.copy())
            except ValueError as e:
                print(f"Lỗi khi tính trạng thái: {e}")
                break

        for i, state in enumerate(states):
            step_frame = tk.Frame(inner_frame, bg=FRAME_BG, padx=5, pady=5)
            step_frame.pack(fill="x", pady=10)

            step_label = tk.Label(step_frame, text=f"Bước {i}:",
                                font=("Segoe UI", 11, "bold"), bg=FRAME_BG, fg=TEXT_COLOR)
            step_label.pack(anchor="w")

            matrix_frame = tk.Frame(step_frame, bg=FRAME_BG)
            matrix_frame.pack(anchor="w", padx=10, pady=5)

            for r in range(3):
                row_text = "["
                for c in range(3):
                    value = state[r, c]
                    row_text += f"{value:2}" if value != 0 else "  "
                    if c < 2:
                        row_text += " "
                row_text += "]"
                tk.Label(matrix_frame, text=row_text, font=("Courier", 14), bg=FRAME_BG, fg=TEXT_COLOR,
                        anchor="w").pack(anchor="w")

        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

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

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_panel = tk.Frame(main_frame, bg=BG_COLOR)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.control_panel = ControlPanel(left_panel, self.start_solving, self.stop_solving, self.reset_solving)
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

        self.solution_viz = SolutionVisualizer(right_panel)
        self.solution_viz.pack(fill="both", expand=True)

        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side="bottom", fill="x")

    def reset_state(self):
        self.running = False
        self.stop_flag = True
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
        self.algorithm_info.update_info(algorithm="Chọn một thuật toán", steps=0, states=0, runtime=0)
        self.solution_viz.display_solution([], "Không có")
        self.status_bar.update_status("Sẵn sàng")
        self.control_panel.enable_controls()

    def start_solving(self):
        if self.running:
            return
        if self.solution_thread is not None and self.solution_thread.is_alive():
            messagebox.showwarning("Cảnh báo", "Thuật toán trước đó vẫn đang chạy. Vui lòng chờ hoặc đặt lại.")
            return

        algorithm = self.control_panel.get_algorithm()
        speed = self.control_panel.get_speed()

        self.current_initial_state = INITIAL_STATE.copy()
        #if algorithm == "Genetic Algorithm":
        #    self.current_initial_state = np.array([[1, 2, 3], [4, 5, 6], [7, 0, 8]])

        if not is_solvable(self.current_initial_state, GOAL_STATE):
            messagebox.showwarning("Cảnh báo", "Trạng thái ban đầu không thể giải được!")
            self.status_bar.update_status("Bài toán không thể giải")
            return

        self.running = True
        self.stop_flag = False
        self.control_panel.disable_controls()
        self.status_bar.update_status(f"Đang giải với {algorithm}...")
        self.algorithm_info.update_info(algorithm=algorithm)

        self.solution_thread = threading.Thread(target=self.solve_puzzle, args=(algorithm, speed))
        self.solution_thread.daemon = True
        self.solution_thread.start()

    def stop_solving(self):
        if self.running:
            self.stop_flag = True
            self.running = False
            self.status_bar.update_status("Đã dừng giải")
            self.control_panel.enable_controls()

    def reset_solving(self):
        # Dừng mọi luồng đang chạy
        self.stop_flag = True
        self.running = False
        self.status_bar.update_status("Đang đặt lại...")
        # Hủy luồng giải nếu đang tồn tại
        if self.solution_thread is not None and self.solution_thread.is_alive():
            try:
                # Đợi luồng kết thúc với timeout
                self.solution_thread.join(timeout=3.0)
            except Exception as e:
                print(f"Lỗi khi đóng luồng: {str(e)}")

        # Đặt lại các biến trạng thái
        self.solution_thread = None
        self.current_solution = None
        self.current_state = None
        self.current_initial_state = INITIAL_STATE.copy()

        # Cập nhật grid về trạng thái ban đầu
        self.puzzle_grid.update_grid(INITIAL_STATE)

        # Đặt lại thông tin thuật toán
        self.algorithm_info.update_info(
            algorithm="Chọn một thuật toán", 
            steps=0, 
            states=0, 
            runtime=0
        )
        
        # Sử dụng solution_viz để reset label
        self.solution_viz.title_label.config(text="Các bước giải")
        
        # Đặt lại hiển thị giải pháp
        self.solution_viz.display_solution([], "Không có")

        # Cập nhật thanh trạng thái
        self.status_bar.update_status("Sẵn sàng")

        # Kích hoạt lại các điều khiển
        self.control_panel.enable_controls()
    
    def solve_puzzle(self, algorithm, speed):
        try:
            solution, states_visited, runtime, _ = self.run_algorithm(algorithm)
            self.current_solution = solution

            if self.stop_flag:
                self.root.after(0, lambda: self.control_panel.enable_controls())
                return

            if solution:
                steps = len(solution)
                self.root.after(0, lambda: self.algorithm_info.update_info(
                    steps=steps, states=states_visited, runtime=runtime))
                self.root.after(0, lambda: self.solution_viz.display_solution(solution, algorithm, self.current_initial_state))
                self.root.after(0, lambda: self.status_bar.update_status(
                    f"Đã giải với {algorithm} trong {steps} bước. Thời gian: {runtime:.2f}s"))

                self.root.after(0, lambda: self.animate_solution(self.current_initial_state.copy(), solution))
            else:
                self.root.after(0, lambda: self.algorithm_info.update_info(
                    states=states_visited, runtime=runtime))
                self.root.after(0, lambda: self.status_bar.update_status(
                    f"Không tìm thấy lời giải với {algorithm}. Thời gian: {runtime:.2f}s"))
                self.root.after(0, lambda: self.solution_viz.display_solution(None, algorithm, self.current_initial_state))
                self.root.after(0, lambda: self.control_panel.enable_controls())

        except Exception as error:
            import traceback
            print(traceback.format_exc())
            self.root.after(0, lambda err=error: messagebox.showerror("Lỗi", f"Lỗi trong {algorithm}: {str(err)}"))
            self.root.after(0, lambda: self.status_bar.update_status(f"Lỗi trong {algorithm}"))
            self.root.after(0, lambda: self.control_panel.enable_controls())

    def animate_solution(self, state, solution):
        if not solution or self.stop_flag:
            self.puzzle_grid.update_grid(state)
            self.control_panel.enable_controls()
            self.running = False
            return

        self.current_state = state.copy()
        try:
            x, y = location(state)
            new_x, new_y = solution[0]

            if not (0 <= new_x <= 2 and 0 <= new_y <= 2):
                raise ValueError(f"Tọa độ di chuyển không hợp lệ: ({new_x}, {new_y})")

            self.puzzle_grid.highlight_move((x, y), (new_x, new_y))
            state[x, y], state[new_x, new_y] = state[new_x, new_y], state[x, y]
            self.puzzle_grid.update_grid(state)

            delay = max(100, 600 // self.control_panel.get_speed())
            if len(solution) > 1 and not self.stop_flag:
                self.root.after(delay, lambda: self.animate_solution(state, solution[1:]))
            else:
                self.control_panel.enable_controls()
                self.running = False
        except ValueError as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi hoạt hình: {str(e)}"))
            self.control_panel.enable_controls()
            self.running = False
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi không xác định: {str(e)}"))
            self.control_panel.enable_controls()
            self.running = False

    def run_algorithm(self, algorithm_name):
        start_state = self.current_initial_state.copy()

        algorithm_map = {
            "AND-OR Tree Search": and_or_tree_search,
            "Partially Observable Search": partially_observable_search,
        }

        if algorithm_name in algorithm_map:
            try:
                result = algorithm_map[algorithm_name](start_state, GOAL_STATE, self.stop_flag)
                if result is not None:
                    return (result[0], result[1], result[2], set())
            except ValueError as e:
                raise ValueError(f"Trạng thái không hợp lệ trong {algorithm_name}: {str(e)}")
        return None, 0, 0, set()

def validate_state(state, context=""):
    if not isinstance(state, np.ndarray) or state.shape != (3, 3):
        raise ValueError(f"Mảng trạng thái không hợp lệ trong {context}: không phải mảng NumPy 3x3")
    if not np.all(np.isin(state, range(9))):
        raise ValueError(f"Mảng trạng thái không hợp lệ trong {context}: chứa giá trị ngoài [0-8]")
    if len(np.unique(state)) != 9:
        raise ValueError(f"Mảng trạng thái không hợp lệ trong {context}: không chứa đúng một giá trị mỗi loại [0-8]")

def location(state):
    validate_state(state, "location")
    result = np.where(state == 0)
    if len(result[0]) == 0:
        raise ValueError("Không tìm thấy ô trống (0) trong trạng thái")
    x, y = result[0][0], result[1][0]
    return x, y

def swap(state, x1, y1, x2, y2):
    validate_state(state, "swap")
    if not (0 <= x1 <= 2 and 0 <= y1 <= 2 and 0 <= x2 <= 2 and 0 <= y2 <= 2):
        raise ValueError("Tọa độ không hợp lệ cho swap")
    new_state = state.copy()
    new_state[x1, y1], new_state[x2, y2] = new_state[x2, y2], new_state[x1, y1]
    validate_state(new_state, "swap result")
    return new_state

def is_solvable(state, goal):
    validate_state(state, "is_solvable state")
    flat = state.flatten()
    nums = [x for x in flat if x != 0]
    inversions = sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > nums[j])
    return inversions % 2 == 0

def and_or_tree_search(start, goal, stop_flag):
    start_time = time.time()
    validate_state(start, "AND-OR Tree Search start")
    validate_state(goal, "AND-OR Tree Search goal")
    
    MAX_DEPTH = 20
    
    visited = set()
    visited.add(tuple(start.flatten()))
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    states_visited = 0

    def expand_node(state, path, depth):
        nonlocal states_visited
        
        if (stop_flag or 
            states_visited >= MAX_STATES_VISITED or 
            time.time() - start_time >= MAX_TIME or 
            depth >= MAX_DEPTH):
            return None

        validate_state(state, "AND-OR expand_node")
        
        if np.array_equal(state, goal):
            return path

        try:
            x, y = location(state)
        except ValueError as e:
            raise ValueError(f"Trạng thái không hợp lệ trong AND-OR Tree Search: {str(e)}")

        possible_moves = []
        for dx, dy in steps:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x <= 2 and 0 <= new_y <= 2:
                new_state = swap(state, x, y, new_x, new_y)
                state_tuple = tuple(new_state.flatten())
                
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    states_visited += 1
                    possible_moves.append((new_state, path + [(new_x, new_y)], depth + 1))

        for child_state, child_path, child_depth in possible_moves:
            result = expand_node(child_state, child_path, child_depth)
            if result is not None:
                return result

        return None

    result = expand_node(start, [], 0)

    end_time = time.time()
    
    if result is not None:
        return result, states_visited, end_time - start_time, visited
    else:
        return None, states_visited, end_time - start_time, visited
    
def partially_observable_search(start, goal, stop_flag):
    start_time = time.time()
    validate_state(start, "Partially Observable Search start")
    validate_state(goal, "Partially Observable Search goal")

    initial_belief_state = {tuple(start.flatten())}
    queue = deque([(initial_belief_state, [])])
    visited = set()
    visited.add(frozenset(initial_belief_state))
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    states_visited = 0

    def get_observation(state):
        validate_state(state, "get_observation")
        x, y = location(state)
        observation = {'empty': (x, y), 'adjacent': {}}
        for dx, dy in steps:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x <= 2 and 0 <= new_y <= 2:
                observation['adjacent'][(new_x, new_y)] = state[new_x, new_y]
        return observation

    def apply_action(belief_state, action):
        new_belief_state = set()
        dx, dy = action
        for state_tuple in belief_state:
            state = np.array(state_tuple).reshape(3, 3)
            try:
                x, y = location(state)
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x <= 2 and 0 <= new_y <= 2:
                    new_state = swap(state, x, y, new_x, new_y)
                    new_belief_state.add(tuple(new_state.flatten()))
            except ValueError:
                continue
        return new_belief_state

    def is_goal_belief(belief_state):
        for state_tuple in belief_state:
            state = np.array(state_tuple).reshape(3, 3)
            if not np.array_equal(state, goal):
                return False
        return True

    while queue and not stop_flag and states_visited < MAX_STATES_VISITED and time.time() - start_time < MAX_TIME:
        belief_state, path = queue.popleft()
        
        if is_goal_belief(belief_state):
            end_time = time.time()
            return path, states_visited, end_time - start_time, visited

        for dx, dy in steps:
            new_belief_state = apply_action(belief_state, (dx, dy))
            if not new_belief_state:
                continue

            # Filter states based on observation
            filtered_belief_state = set()
            for state_tuple in new_belief_state:
                state = np.array(state_tuple).reshape(3, 3)
                observation = get_observation(state)
                # Kiểm tra xem vị trí ô trống trong trạng thái mới có khớp với vị trí dự kiến
                expected_empty_pos = None
                for prev_state_tuple in belief_state:
                    prev_state = np.array(prev_state_tuple).reshape(3, 3)
                    x, y = location(prev_state)
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x <= 2 and 0 <= new_y <= 2:
                        expected_empty_pos = (new_x, new_y)
                        break
                if expected_empty_pos and observation['empty'] == expected_empty_pos:
                    filtered_belief_state.add(state_tuple)

            if filtered_belief_state:
                belief_state_tuple = frozenset(filtered_belief_state)
                if belief_state_tuple not in visited:
                    visited.add(belief_state_tuple)
                    states_visited += len(filtered_belief_state)
                    queue.append((filtered_belief_state, path + [expected_empty_pos]))

    end_time = time.time()
    return None, states_visited, end_time - start_time, visited

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleSolverApp(root)
    root.mainloop()