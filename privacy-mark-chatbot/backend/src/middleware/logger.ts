import { Request, Response, NextFunction } from 'express';

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  const startTime = Date.now();
  
  // レスポンスが送信された後にログを記録
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    const logData = {
      timestamp: new Date().toISOString(),
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip || req.connection.remoteAddress,
      userAgent: req.get('user-agent') || 'unknown'
    };
    
    // ステータスコードに応じて色を変える
    if (res.statusCode >= 500) {
      console.error('❌', JSON.stringify(logData));
    } else if (res.statusCode >= 400) {
      console.warn('⚠️', JSON.stringify(logData));
    } else {
      console.log('✅', JSON.stringify(logData));
    }
  });
  
  next();
};