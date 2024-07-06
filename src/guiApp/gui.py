import tkinter as tk
from tkinter import ttk
import threading
import ctypes
import keyboard
import rbRunApp.rbRun as rbRunApp
import time
import psutil
import multiprocessing
from datetime import timedelta
from ttkbootstrap import Style
from PIL import Image, ImageTk

CLASS_OPTIONS = ["blitzLancer", "blastArcher", "none"]

class RbRunGUI:
    def __init__(self, master):
        self.master = master
        style = Style(theme='superhero')
        self.master = style.master
        self.master.title("rbRun GUI")
        self.master.geometry("290x400")
        self.master.resizable(False, False)
        icon = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        icon = ImageTk.PhotoImage(icon)
        self.master.wm_iconphoto(True, icon)
        self.create_widgets()

        self.thread = None
        self.hotkey = None
        self.start_time = None
        self.running = False

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)

        # クラスセレクトボックス
        ttk.Label(main_frame, text="クラス:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.arg1 = ttk.Combobox(main_frame, values=CLASS_OPTIONS, style='primary.TCombobox')
        self.arg1.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=10)
        self.arg1.set("blitzLancer")

        # ラッシュセレクトボックス
        ttk.Label(main_frame, text="ラッシュバトル").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.arg2 = ttk.Combobox(main_frame, values=["1", "3", "4"], style='primary.TCombobox')
        self.arg2.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=10)
        self.arg2.set("3")

        # 強制終了ボタンのセレクトボックス
        ttk.Label(main_frame, text="強制終了ボタン").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.stop_key = ttk.Combobox(main_frame, values=["esc", "F10"], style='primary.TCombobox')
        self.stop_key.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=10)
        self.stop_key.set("esc")

        # rbRun実行ボタン
        self.run_button = ttk.Button(main_frame, text="rbRun実行", command=self.start_rbRun, style='success.TButton')
        self.run_button.grid(row=3, column=0, columnspan=2, pady=20)

        # 実行状態表示
        self.status_var = tk.StringVar(value="待機中")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Helvetica', 12, 'bold'))
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

        # 実行時間表示
        ttk.Label(main_frame, text="時間:", font=('Helvetica', 12)).grid(row=5, column=0, sticky=tk.W, pady=10)
        self.time_var = tk.StringVar(value="00:00:00")
        self.time_label = ttk.Label(main_frame, textvariable=self.time_var, font=('Helvetica', 12))
        self.time_label.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=10)

        # カウント表示
        ttk.Label(main_frame, text="周回:", font=('Helvetica', 12)).grid(row=6, column=0, sticky=tk.W, pady=10)
        self.count_var = tk.StringVar(value="0")
        self.count_label = ttk.Label(main_frame, textvariable=self.count_var, font=('Helvetica', 12))
        self.count_label.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=10)

        # プロセスID
        self.process_id = multiprocessing.Value(ctypes.c_int)

        # プログレスバー
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', style='info.Horizontal.TProgressbar')
        self.progress.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

    def start_rbRun(self):
        if self.thread and self.thread.is_alive():
            print("rbRunは既に実行中です")
            return

        arg1 = self.arg1.get()
        arg2 = self.arg2.get()
        self.thread = threading.Thread(target=self.run_with_timer, args=(arg1, arg2))
        self.thread.start()

        # グローバルホットキーを設定
        stop_key = self.stop_key.get()
        self.hotkey = keyboard.add_hotkey(stop_key, self.stop_rbRun)

        self.status_var.set("実行中")
        self.run_button.config(state='disabled')
        self.progress.start()

    def run_with_timer(self, arg1, arg2):
        self.start_time = time.time()
        self.running = True
        self.update_timer()
        rbRunApp.rbRun(arg1, arg2, self.count_var, self.process_id)
        self.running = False
        self.master.after(0, self.update_status, "完了")

    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.time_var.set(str(timedelta(seconds=int(elapsed_time))))
            self.master.after(1000, self.update_timer)

    def stop_rbRun(self):
        if self.thread and self.thread.is_alive():
            if self.process_id.value != 0:
                self.terminate_process(self.process_id)
                print("プロセスを終了しました")
            thread_id = self.thread.ident
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), None)
                self.update_status("強制終了失敗")
            else:
                self.update_status("強制終了")
            
            # ホットキーを削除
            if self.hotkey:
                keyboard.remove_hotkey(self.hotkey)
                self.hotkey = None
        else:
            self.update_status("実行中のrbRunなし")

    def terminate_process(self, pid):
        try:
            # pid が Synchronized オブジェクトの場合、.value を使用して整数値を取得
            if isinstance(pid, multiprocessing.sharedctypes.Synchronized):
                pid = pid.value
            p = psutil.Process(pid)
            p.terminate()  # プロセスを終了させる
            p.wait(timeout=3)
        except psutil.NoSuchProcess:
            print(f"プロセス {pid} は存在しません。")
        except psutil.TimeoutExpired:
            print(f"プロセス {pid} の終了がタイムアウトしました。強制終了を試みます。")
            p.kill()
        except Exception as e:
            print(f"プロセス {pid} の終了中にエラーが発生しました: {e}")

    def update_status(self, status):
        self.status_var.set(status)
        self.run_button.config(state='normal')
        self.running = False
        self.progress.stop()

    def on_closing(self):
        # ウィンドウが閉じられるときにホットキーを削除
        if self.hotkey:
            keyboard.remove_hotkey(self.hotkey)
        self.master.destroy()

def bpAutoRb_gui_Launch():
    root = tk.Tk()
    app = RbRunGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    bpAutoRb_gui_Launch()
