import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import time
from collections import deque

class PuzzleSolver:
  def __init__(self, belief_states):
      self.belief_states = belief_states
      self.move_count = 0
      self.execution_time = 0

  def find_empty_tile(self, state):
      for i in range(3):
          for j in range(3):
              if state[i][j] == 0:
                  return i, j
      return None, None

  def sensorless_bfs(self):
      goal_state = [[1,2,3],[4,5,6],[7,8,0]]
      initial_belief = tuple(tuple(tuple(row) for row in state) for state in self.belief_states)
      queue = deque([(self.belief_states, [self.belief_states])])
      visited = {initial_belief}
      max_iterations = 100

      for iteration in range(max_iterations):
          if not queue:
              return None

          current_belief, path = queue.popleft()
          actions = set()
          
          for state in current_belief:
              empty_i, empty_j = self.find_empty_tile(state)
              if empty_i is None:
                  return None
              
              for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                  ni, nj = empty_i + di, empty_j + dj
                  if 0 <= ni < 3 and 0 <= nj < 3:
                      actions.add((di, dj))

          for action in actions:
              new_belief = []
              for state in current_belief:
                  empty_i, empty_j = self.find_empty_tile(state)
                  ni, nj = empty_i + action[0], empty_j + action[1]
                  
                  if not (0 <= ni < 3 and 0 <= nj < 3):
                      new_belief.append(state)
                      continue
                  
                  new_state = [row[:] for row in state]
                  new_state[empty_i][empty_j], new_state[ni][nj] = new_state[ni][nj], new_state[empty_i][empty_j]
                  new_belief.append(new_state)
              
              new_belief_tuple = tuple(tuple(tuple(row) for row in state) for state in new_belief)
              
              if new_belief_tuple not in visited:
                  visited.add(new_belief_tuple)
                  
                  if all(state == goal_state for state in new_belief):
                      return path + [new_belief]
                  
                  queue.append((new_belief, path + [new_belief]))

      return None

class PuzzleApp:
  def __init__(self, master):
      self.master = master
      master.title("8-Puzzle Sensorless Solver")
      master.geometry("1200x700")
      master.configure(bg='#f0f0f0')

      self.initial_belief_states = [
          [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
          [[1, 2, 3], [4, 5, 6], [0, 7, 8]],
          [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
      ]

      self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
      self.label_font = tkfont.Font(family="Helvetica", size=12)
      
      self.create_ui()

  def create_ui(self):
      main_frame = tk.Frame(self.master, bg='#f0f0f0')
      main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

      title_label = tk.Label(main_frame, text="8-Puzzle Sensorless Solver", 
                             font=self.title_font, bg='#f0f0f0')
      title_label.pack(pady=10)

      control_frame = tk.Frame(main_frame, bg='#f0f0f0')
      control_frame.pack(pady=10)

      self.solve_button = tk.Button(control_frame, text="Giải Bài Toán", 
                                    command=self.solve_puzzle,
                                    font=self.label_font,
                                    bg='#4CAF50', fg='white')
      self.solve_button.pack(side=tk.LEFT, padx=10)

      self.reset_button = tk.Button(control_frame, text="Đặt Lại", 
                                    command=self.reset_puzzle,
                                    font=self.label_font,
                                    bg='#f44336', fg='white')
      self.reset_button.pack(side=tk.LEFT, padx=10)

      info_frame = tk.Frame(main_frame, bg='#f0f0f0')
      info_frame.pack(pady=10)

      self.steps_label = tk.Label(info_frame, text="Số Bước: 0", 
                                  font=self.label_font, bg='#f0f0f0')
      self.steps_label.pack(side=tk.LEFT, padx=10)

      self.time_label = tk.Label(info_frame, text="Thời Gian: 0.00s", 
                                 font=self.label_font, bg='#f0f0f0')
      self.time_label.pack(side=tk.LEFT, padx=10)

      grid_frame = tk.Frame(main_frame, bg='#f0f0f0')
      grid_frame.pack(expand=True, fill=tk.BOTH)

      self.grid_frames = []
      self.grid_labels = []

      for i in range(3):
          belief_frame = tk.Frame(grid_frame, bg='#f0f0f0', bd=2, relief=tk.RAISED)
          belief_frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
          grid_frame.grid_columnconfigure(i, weight=1)

          belief_title = tk.Label(belief_frame, text=f"Niềm Tin {i+1}", 
                                  font=self.label_font, bg='#e0e0e0')
          belief_title.pack(pady=(5,10))

          sub_grid_frame = tk.Frame(belief_frame, bg='#f0f0f0')
          sub_grid_frame.pack(expand=True)

          grid_labels_row = []
          for r in range(3):
              row_labels = []
              for c in range(3):
                  label = tk.Label(sub_grid_frame, text="", 
                                   width=5, height=2, 
                                   font=self.label_font,
                                   relief=tk.RAISED, 
                                   bg='lightblue', 
                                   borderwidth=2)
                  label.grid(row=r, column=c, padx=2, pady=2)
                  row_labels.append(label)
              grid_labels_row.append(row_labels)
          
          self.grid_labels.append(grid_labels_row)
          self.grid_frames.append(belief_frame)

      self.update_grids(self.initial_belief_states)

  def solve_puzzle(self):
      self.solve_button.config(state=tk.DISABLED)
      solver = PuzzleSolver(self.initial_belief_states)
      start_time = time.time()
      path = solver.sensorless_bfs()
      end_time = time.time()
      
      if path:
          self.show_solution_steps(path, end_time - start_time)
      else:
          messagebox.showerror("Lỗi", "Không tìm thấy giải pháp!")
          self.solve_button.config(state=tk.NORMAL)

  def show_solution_steps(self, path, execution_time):
      self.time_label.config(text=f"Thời Gian: {execution_time:.2f}s")
      
      def step_generator():
          for step, belief_states in enumerate(path):
              self.steps_label.config(text=f"Số Bước: {step}")
              self.update_grids(belief_states)
              yield step

      def next_step():
          try:
              next(self.step_iter)
              self.master.after(1000, next_step)
          except StopIteration:
              messagebox.showinfo("Hoàn Thành", "Đã giải xong bài toán!")
              self.solve_button.config(state=tk.NORMAL)

      self.step_iter = step_generator()
      next_step()

  def update_grids(self, states):
      for belief_idx, state in enumerate(states):
          for i in range(3):
              for j in range(3):
                  text = str(state[i][j]) if state[i][j] != 0 else "" 
                  bg_color = 'lightgray' if state[i][j] == 0 else 'lightblue'
                  self.grid_labels[belief_idx][i][j].config(
                      text=text, 
                      bg=bg_color
                  )

  def reset_puzzle(self):
      self.steps_label.config(text="Số Bước: 0")
      self.time_label.config(text="Thời Gian: 0.00s")
      self.update_grids(self.initial_belief_states)
      self.solve_button.config(state=tk.NORMAL)

def main():
  root = tk.Tk()
  app = PuzzleApp(root)
  root.mainloop()

if __name__ == "__main__":
  main()