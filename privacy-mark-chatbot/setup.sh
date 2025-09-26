#!/bin/bash

# プライバシーマーク取得支援チャットボット - セットアップスクリプト

echo "🚀 プライバシーマーク取得支援チャットボット セットアップを開始します..."

# 環境変数ファイルの作成
if [ ! -f .env ]; then
    echo "📝 環境変数ファイルを作成しています..."
    cp .env.example .env
    echo "⚠️  .envファイルを編集して、必要な設定を行ってください"
fi

# 依存関係のインストール
echo "📦 バックエンドの依存関係をインストールしています..."
cd backend
npm install
cd ..

echo "📦 フロントエンドの依存関係をインストールしています..."
cd frontend
npm install
cd ..

# Dockerを使用する場合
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Dockerが検出されました"
    read -p "Dockerを使用してセットアップしますか？ (y/n): " use_docker
    
    if [ "$use_docker" = "y" ]; then
        echo "🐳 Dockerコンテナを起動しています..."
        docker-compose up -d
        
        echo "⏳ サービスの起動を待機しています..."
        sleep 10
        
        echo "✅ セットアップが完了しました！"
        echo "📍 アプリケーションURL:"
        echo "   - フロントエンド: http://localhost:3001"
        echo "   - バックエンドAPI: http://localhost:3000"
        echo "   - PostgreSQL: localhost:5432"
        echo "   - Redis: localhost:6379"
        exit 0
    fi
fi

# ローカル開発環境のセットアップ
echo "💻 ローカル開発環境をセットアップします"

# PostgreSQLの確認
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQLが検出されました"
else
    echo "⚠️  PostgreSQLがインストールされていません"
    echo "   brew install postgresql (Mac) または apt-get install postgresql (Linux) でインストールしてください"
fi

# Redisの確認
if command -v redis-server &> /dev/null; then
    echo "✅ Redisが検出されました"
else
    echo "⚠️  Redisがインストールされていません"
    echo "   brew install redis (Mac) または apt-get install redis (Linux) でインストールしてください"
fi

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "📍 アプリケーションを起動するには："
echo ""
echo "1. ターミナル1（バックエンド）:"
echo "   cd backend"
echo "   npm run dev"
echo ""
echo "2. ターミナル2（フロントエンド）:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "📝 注意事項:"
echo "   - .envファイルの設定を確認してください"
echo "   - PostgreSQLとRedisが起動していることを確認してください"
echo "   - 初回起動時はデータベースのマイグレーションが必要な場合があります"

# 実行権限の付加
chmod +x setup.sh