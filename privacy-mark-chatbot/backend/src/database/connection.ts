import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const initializeDatabase = async (): Promise<void> => {
  try {
    // データベース接続テスト
    const client = await pool.connect();
    await client.query('SELECT NOW()');
    client.release();
    
    console.log('✅ Database connected successfully');
    
    // テーブル作成（必要に応じて）
    await createTables();
  } catch (error) {
    console.error('❌ Database connection failed:', error);
    throw error;
  }
};

const createTables = async (): Promise<void> => {
  const queries = [
    // ユーザーテーブル
    `CREATE TABLE IF NOT EXISTS users (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      email VARCHAR(255) UNIQUE,
      name VARCHAR(255),
      company_name VARCHAR(255),
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    )`,
    
    // セッションテーブル
    `CREATE TABLE IF NOT EXISTS chat_sessions (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID REFERENCES users(id),
      context JSONB,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    )`,
    
    // 会話履歴テーブル
    `CREATE TABLE IF NOT EXISTS conversation_history (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      session_id UUID REFERENCES chat_sessions(id),
      role VARCHAR(50),
      content TEXT,
      metadata JSONB,
      created_at TIMESTAMP DEFAULT NOW()
    )`,
    
    // 進捗管理テーブル
    `CREATE TABLE IF NOT EXISTS application_progress (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID REFERENCES users(id),
      current_step VARCHAR(100),
      completed_steps JSONB,
      remaining_tasks JSONB,
      metadata JSONB,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    )`,
    
    // ドキュメントテーブル
    `CREATE TABLE IF NOT EXISTS documents (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID REFERENCES users(id),
      document_type VARCHAR(100),
      file_name VARCHAR(255),
      file_path VARCHAR(500),
      status VARCHAR(50),
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    )`
  ];
  
  for (const query of queries) {
    try {
      await pool.query(query);
    } catch (error) {
      console.error('Table creation error:', error);
    }
  }
  
  console.log('✅ Database tables initialized');
};

export { pool };