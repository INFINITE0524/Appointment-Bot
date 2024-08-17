from flask import Flask, request, jsonify, render_template

# 初始化 Flask 應用
app = Flask(__name__)

# 網頁首頁
@app.route('/appointment')
def index():
    return render_template('appointment.html')

if __name__ == '__main__':
    # 啟動應用
    app.run(debug=True, host='0.0.0.0')
