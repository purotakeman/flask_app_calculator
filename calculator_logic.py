""" 
GUI版専用
計算ロジックの「関数化」

1.入力と計算を処理するcaluculate()関数を作成
2.エラー処理を含めた計算ロジックを関数内に移動する
3.メインの実行部分(コンソールでの入出力をしていた部分)を、関数を呼び出す形に書き換える

"""

def calculate(num1: float, operator: str, num2: float) -> (float, str):
    """
    2つの数値と演算子を受け取り、計算結果と完全な計算式文字列を返す関数。
    
    引数:
        num1 (float): 最初の数値
        operator (str): 演算子 (+, -, *, /)
        num2 (float): 2番目の数値
    
    戻り値:
        タプル (結果の数値, 計算式の文字列)
        エラーが発生した場合は (None, エラーメッセージ)
    """

    result = None

    expression = ""     #　計算式全体を保持する変数

    try:
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            # ゼロ除算のチェック
            if num2 == 0:
                # 戻り値として(None, エラーメッセージ）を返す
                return None, "エラー: 0で割ることはできやせん"
            else:
                result = num1 / num2

        else:
            # サポートされていない演算子
            return None, "エラー: 無効な演算子や！"
            
        return result, expression
    
    except Exception:
        # 予期せぬエラーが発生した場合
        return None, "エラー: 予期せぬエラーが発生したで、あんた何したん"
    

""" 関数の動作確認用 """
#　関数を定義したファイル自体を実行したときのみ、以下のテストコードが動く
if __name__ == "__main__":
    # テスト 1:正常な計算
    r1, e1 = calculate(10, '+', 5)
    print(f"計算結果: {r1}, 式: {e1}") # 出力:計算結果: 15.0, 式:10 + 5

    # テスト 2: ゼロ除算エラー
    r2, e2 = calculate(10, '/', 0)
    print(f"計算結果: {r2}, 式: {e2}") # 出力: 計算結果: None, 式: エラー: 0で割ることはできません
    
    # テスト 3: 無効な演算子
    r3, e3 = calculate(10, '!', 5)
    print(f"計算結果: {r3}, 式: {e3}") # 出力: 計算結果: None, 式: エラー: 無効な演算子です
        
            













