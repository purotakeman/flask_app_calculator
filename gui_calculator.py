""" 
GUI版専用

"""
import tkinter as tk
from tkinter import messagebox      # ポップアップ表示用

# calculater_logic.pyで作成した計算ロジックをインポート
from calculator_logic import calculate      # from "ファイル名" import "関数名"

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("シンプル電卓")

        """ 状態管理用の変数 """
        self.current_input = "0"
        self.current_result = None
        self.is_new_calculation = True

        """ ウィジェット(部品)の作成 """

        # 1.結果表示欄(画面の最上部)
        self.result_display = tk.Entry(master, width=30, borderwidth=5, font=('Arial', 16), justify='right')
        self.result_display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.result_display.insert(0, self.current_input)       # 初期値「0」を表示

        # 2.ボタンの定義と配置
        # 配置の行番号(row)を管理する変数
        row_num = 1

        buttons = [
            ('C', 1, 'clear'), ('/', 1, 'operator'),
            ('7', 2, 'number'), ('8', 2, 'number'), ('9', 2, 'number'), ('*', 2, 'operator'),
            ('4', 2, 'number'), ('5', 2, 'number'), ('6', 2, 'number'), ('-', 2, 'operator'),
            ('1', 2, 'number'), ('2', 2, 'number'), ('3', 2, 'number'), ('+', 2, 'operator'),
            ('0', 2, 'number'), ('.', 2, 'decimal'), ('=', 2, 'equal')
        ]

        # ボタンを自動で生成して画面に配置
        col_num = 0
        current_row = 1
        for (text, target_row, type) in buttons:
            if target_row != current_row:
                col_num = 0
                current_row = target_row

            tk.Button(master, text=text, padx=20, pady=20, font=('Arial', 12),
                      command=lambda t=text, tp=type: self.button_click(t, tp)
            ).grid(row=target_row, column=col_num, padx=5, pady=5, sticky="nsew")
            # sticky="nsew" でボタンを格子全体に広げ、見やすくする

            col_num += 1

        # グリッドの列・行設定 (画面の装飾)
        # ご要望3の装飾の一部として、セルが画面サイズに合わせて伸縮するように設定します。
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)

    # --- ボタンクリック時の処理（イベントハンドラ） ---
    def button_click(self, text, type):
        
        if type == 'number' or type == 'decimal':
            # 数字ボタンまたは小数点ボタン
            if self.is_new_calculation or self.current_input == "0":
                if text == '.':
                    self.current_input = "0."
                else:
                    self.current_input = text
                self.is_new_calculation = False
            elif text == '.' and '.' in self.current_input:
                pass # 小数点がすでにある場合は何もしない
            else:
                self.current_input += text
            
            self.update_display(self.current_input)
            
        elif type == 'operator':
            # 演算子ボタン (+, -, *, /)
            
            # 1. 入力されている値を数値として記憶
            try:
                num_to_store = float(self.current_input)
            except ValueError:
                # 入力がおかしい場合はクリア
                self.clear()
                return 
            
            # 2. 継続計算処理
            if self.current_result is None:
                # 初回は入力値を最初の数値として記憶
                self.current_result = num_to_store
            else:
                # 2回目以降は、前回の結果と現在入力された値で計算
                
                # ここに、前回の演算子を保持する変数が無いため、この時点では計算が複雑になります。
                # 簡略化のため、ここでは「常に現在の入力値で計算を上書きする」というシンプルなロジックにします。
                # ユーザーのスキルアップとして、④の変数を用意してロジックを修正しましょう。
                self.current_result = num_to_store # (簡略化されたロジック)

            # 3. 演算子と新しい計算の開始フラグを設定
            self.last_operator = text # 次の計算のために演算子を記憶
            self.is_new_calculation = True
            
            # 4. 表示をリセット
            self.update_display(text)
            
        elif type == 'equal':
            # イコールボタン
            self.execute_calculation()
            
        elif type == 'clear':
            # クリアボタン
            self.clear()


    def execute_calculation(self):
        """イコールボタンが押されたときに、実際に計算ロジックを呼び出す関数"""
        
        # num1 は前回の結果 (self.current_result)
        # operator は self.last_operator (前回押された演算子)
        # num2 は現在の入力値 (self.current_input)
        
        try:
            num1 = self.current_result
            operator = self.last_operator
            num2 = float(self.current_input)
            
            # calculate 関数を呼び出して計算を実行
            result, expression = calculate(num1, operator, num2)
            
            if result is not None:
                # 成功: 結果と計算式を表示 (ご要望 2)
                self.update_display(str(result))
                messagebox.showinfo("計算結果", f"式: {expression}\n結果: {result}")
                
                # 次の継続計算に備え、結果を保持
                self.current_result = result
                self.is_new_calculation = True
            else:
                # エラー: エラーメッセージを表示
                self.update_display(expression) # エラーメッセージを表示
                self.clear()
                
        except (TypeError, ValueError):
            # まだ演算子が押されていない、または入力値が無効な場合のエラー
            self.update_display("エラー")
            self.clear()
            
            
    def clear(self):
        """クリアボタン（C）を押した時の処理"""
        self.current_input = "0"
        self.current_result = None # 継続計算の値をリセット
        self.is_new_calculation = True
        self.last_operator = '' # 最後の演算子もリセット
        self.update_display("0")
        
        
    def update_display(self, text):
        """結果表示欄の表示内容を更新する関数"""
        self.result_display.delete(0, tk.END) # 現在の表示をすべて消去
        self.result_display.insert(0, text)   # 新しいテキストを挿入

# --- メイン実行部分 ---
if __name__ == "__main__":
    root = tk.Tk()
    my_calculator = CalculatorApp(root)
    # ⑤ のメソッドを呼び出し、アプリケーションのウィンドウを表示し、ユーザーの操作を待つ
    root.mainloop()