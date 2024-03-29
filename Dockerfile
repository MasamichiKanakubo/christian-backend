# Pythonのベースイメージを作成
FROM python:3.11.3

# 作業ディレクトリを指定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

# 依存関係をインストール
RUN pip install --user --no-cache-dir -r requirements.txt --verbose

# アプリケーションファイルのコピー
COPY . .

# Uvicornを使用してアプリケーションを実行
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
