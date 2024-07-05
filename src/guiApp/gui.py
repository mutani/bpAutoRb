# tkinterモジュールをインポート
import tkinter as tk
import rbRunApp.rbRun as rbRun

#定数を定義
TITLE = 'bpAutoRb'
WIDTH = 250
HEIGHT = 100
#関数定義
def guiLunch():
    # メインウィンドウを作成
    root = tk.Tk()
    def on_esc(event=None):
        root.destroy()

    root.title(TITLE)
    # ウィンドウサイズを設定
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))

    # ラベルウィジェットを作成して配置
    label = tk.Label(root, text="rb.run")
    label.pack()

    root.bind('<Escape>', on_esc)  # ESCキーが押されたときにon_esc関数を呼び出す
    # ボタンウィジェットを作成して配置、クリック時にrbRunを実行　ESCで終了
    button = tk.Button(root, text="Run", command=rbRun.rbRun)
    button.pack()

    # アプリケーションのメインループを開始
    root.mainloop()


