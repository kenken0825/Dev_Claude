import { Router, Request, Response } from 'express';
import { ChatbotService } from '../services/chatbot.service';
import { validateChatMessage } from '../validators/chat.validator';
import { ConversationContext } from '../types/chat.types';

const router = Router();
const chatbotService = new ChatbotService();

// セッション管理用の簡易ストア（本番環境ではRedisやDBを使用）
const sessionStore = new Map<string, ConversationContext>();

/**
 * POST /api/v1/chat/message
 * チャットメッセージを処理
 */
router.post('/message', validateChatMessage, async (req: Request, res: Response) => {
  try {
    const { message, sessionId, userId } = req.body;
    
    // セッションコンテキストを取得または作成
    let context = sessionStore.get(sessionId);
    if (!context) {
      context = {
        sessionId,
        userId,
        conversationHistory: [],
        applicationProgress: {
          currentStep: 'initial',
          completedSteps: [],
          remainingTasks: []
        }
      };
      sessionStore.set(sessionId, context);
    }
    
    // メッセージを処理
    const response = await chatbotService.processMessage(message, context);
    
    // セッションを更新
    sessionStore.set(sessionId, context);
    
    res.json({
      success: true,
      data: response
    });
  } catch (error) {
    console.error('Chat message processing error:', error);
    res.status(500).json({
      success: false,
      error: 'メッセージの処理中にエラーが発生しました'
    });
  }
});

/**
 * GET /api/v1/chat/session/:sessionId
 * セッション情報を取得
 */
router.get('/session/:sessionId', (req: Request, res: Response) => {
  try {
    const { sessionId } = req.params;
    const context = sessionStore.get(sessionId);
    
    if (!context) {
      return res.status(404).json({
        success: false,
        error: 'セッションが見つかりません'
      });
    }
    
    res.json({
      success: true,
      data: {
        sessionId: context.sessionId,
        applicationProgress: context.applicationProgress,
        messageCount: context.conversationHistory.length
      }
    });
  } catch (error) {
    console.error('Session retrieval error:', error);
    res.status(500).json({
      success: false,
      error: 'セッション情報の取得中にエラーが発生しました'
    });
  }
});

/**
 * DELETE /api/v1/chat/session/:sessionId
 * セッションをリセット
 */
router.delete('/session/:sessionId', (req: Request, res: Response) => {
  try {
    const { sessionId } = req.params;
    sessionStore.delete(sessionId);
    
    res.json({
      success: true,
      message: 'セッションがリセットされました'
    });
  } catch (error) {
    console.error('Session reset error:', error);
    res.status(500).json({
      success: false,
      error: 'セッションのリセット中にエラーが発生しました'
    });
  }
});

export { router as ChatRouter };