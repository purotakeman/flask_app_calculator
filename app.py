""" 
GUI版では使いません。 
"""
from flask import Flask, render_template, request  # フォームからデータを受け取るためにreqestをインポート

app = Flask(__name__) # nameはPythonで実行しているファイル名を指す

@app.route('/')

def index():

    return render_template('index.html', result=None)
    # index.htmlを読み込み、ブラウザに表示する
    # result=Noneを渡すことで、最初の結果表示部分が非表示になる

@app.route('/calculate', methods=['POST'])
def calculate():
    # フォームから送信されたデータを取り出す
    # request.form.get('name')で、HTMLのname="name"の値を取得する

    # 1.数値1を取得し、float型(小数点も扱える数値型)に変換する
    num1_str = request.form.get('num1')
    num2_str = request.form.get('num2')

    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        # 数値に変換できないエラーが発生した場合
        return render_template('index.html', result="エラー：無効な数値が入力されました", error=True)

    # 2.演算子を取得
    operator = request.form.get('operator')

    result = None

    # 3.演算子に応じて計算を実行
    if operator == 'add':
        result = num1 + num2
    elif operator == 'subtract':
        result = num1 - num2
    elif operator == 'multiply':
        result = num1 * num2
    elif operator == 'divide':
        # 0での割り算を防ぐ処理
        if num2 != 0:
            result = num1 / num2
        else:
            result = "エラー:0で割ることはできません"
    
    # 4.計算結果を index.html テンプレートに渡して再表示する
    # index.html の{{ result }} 部分に、計算された値が埋め込まれて表示される
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)