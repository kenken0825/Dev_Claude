import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { ChatRouter } from './routes/chat.routes';
import { DocumentRouter } from './routes/document.routes';
import { ProgressRouter } from './routes/progress.routes';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/logger';
import { initializeDatabase } from './database/connection';

// 環境変数の読み込み
dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 3000;

// ミドルウェア設定
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

// ヘルスチェックエンドポイント
app.get('/health', (req: Request, res: Response) => {
  res.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.API_VERSION || '1.0.0'
  });
});

// APIルーター設定
app.use('/api/v1/chat', ChatRouter);
app.use('/api/v1/documents', DocumentRouter);
app.use('/api/v1/progress', ProgressRouter);

// エラーハンドリング
app.use(errorHandler);

// サーバー起動
const startServer = async () => {
  try {
    // データベース接続初期化
    await initializeDatabase();
    
    app.listen(PORT, () => {
      console.log(`🚀 Server is running on port ${PORT}`);
      console.log(`📝 Privacy Mark Chatbot API v${process.env.API_VERSION || '1.0.0'}`);
      console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
};

startServer();

export default app;