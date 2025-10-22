jsonファイルに適当に用語入れればベクトル変換すルよ
# 仮想環境作成（推奨）
python -m venv venv

# 仮想環境の有効化
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# パッケージインストール
pip install -r requirements.txt

3. GCPの設定3-1. Firestoreの有効化bash# Google Cloudプロジェクト確認
gcloud config get-value project

# プロジェクトIDを設定（必要に応じて）
gcloud config set project YOUR_PROJECT_ID

# Firestoreデータベース作成
gcloud firestore databases create --region=asia-northeast1

3. GCPの設定3-1. Firestoreの有効化bash# Google Cloudプロジェクト確認
gcloud config get-value project

# プロジェクトIDを設定（必要に応じて）
gcloud config set project YOUR_PROJECT_ID

# Firestoreデータベース作成
gcloud firestore databases create --region=asia-northeast1
