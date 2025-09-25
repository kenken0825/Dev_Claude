import { ChatbotService } from '../services/chatbot.service';
import { ConversationContext } from '../types/chat.types';

describe('ChatbotService', () => {
  let chatbotService: ChatbotService;
  let mockContext: ConversationContext;

  beforeEach(() => {
    chatbotService = new ChatbotService();
    mockContext = {
      sessionId: 'test-session-123',
      userId: 'test-user-456',
      conversationHistory: [],
      applicationProgress: {
        currentStep: 'initial',
        completedSteps: [],
        remainingTasks: []
      },
      preferences: {}
    };
  });

  describe('processMessage', () => {
    it('should handle application flow inquiries correctly', async () => {
      const message = '申請の流れを教えてください';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toContain('申請フロー');
      expect(response.quickReplies).toBeDefined();
      expect(response.quickReplies.length).toBeGreaterThan(0);
    });

    it('should handle document inquiries correctly', async () => {
      const message = '必要書類について教えてください';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toContain('必要書類');
      expect(response.message).toContain('申請様式');
    });

    it('should handle requirement check inquiries', async () => {
      const message = '申請要件を確認したい';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toContain('要件');
      expect(response.message).toContain('チェックリスト');
    });

    it('should handle progress status inquiries', async () => {
      mockContext.applicationProgress = {
        currentStep: 'document_preparation',
        completedSteps: ['preparation'],
        remainingTasks: ['submission', 'review']
      };

      const message = '現在の進捗状況を教えて';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toContain('進捗');
      expect(response.message).toContain('完了済みタスク');
    });

    it('should handle FAQ questions', async () => {
      const message = 'プライバシーマーク取得にかかる期間は？';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toContain('期間');
      expect(response.message).toMatch(/\d+ヶ月/);
    });

    it('should handle general inquiries gracefully', async () => {
      const message = 'こんにちは';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response).toBeDefined();
      expect(response.quickReplies).toBeDefined();
      expect(response.quickReplies.length).toBeGreaterThan(0);
    });

    it('should update conversation context after processing', async () => {
      const message = 'テストメッセージ';
      const initialHistoryLength = mockContext.conversationHistory.length;
      
      await chatbotService.processMessage(message, mockContext);
      
      expect(mockContext.conversationHistory.length).toBe(initialHistoryLength + 2);
      expect(mockContext.conversationHistory[initialHistoryLength].role).toBe('user');
      expect(mockContext.conversationHistory[initialHistoryLength + 1].role).toBe('assistant');
    });

    it('should handle errors gracefully', async () => {
      // Force an error by passing null context
      const response = await chatbotService.processMessage('test', null as any);
      
      expect(response).toBeDefined();
      expect(response.message).toContain('エラー');
      expect(response.suggestions).toContain('最初から始める');
    });
  });

  describe('Intent Classification', () => {
    it('should classify application flow intent correctly', async () => {
      const testMessages = [
        '申請の流れを教えて',
        '手続きについて知りたい',
        'フローを確認したい'
      ];

      for (const msg of testMessages) {
        const response = await chatbotService.processMessage(msg, mockContext);
        expect(response.message).toContain('申請');
      }
    });

    it('should classify document inquiry intent correctly', async () => {
      const testMessages = [
        '書類を準備したい',
        '様式について教えて',
        'テンプレートはありますか'
      ];

      for (const msg of testMessages) {
        const response = await chatbotService.processMessage(msg, mockContext);
        expect(response.message).toMatch(/書類|様式/);
      }
    });

    it('should classify requirement check intent correctly', async () => {
      const testMessages = [
        '要件を確認',
        '条件について',
        '申請資格は？'
      ];

      for (const msg of testMessages) {
        const response = await chatbotService.processMessage(msg, mockContext);
        expect(response.message).toMatch(/要件|条件|資格/);
      }
    });
  });

  describe('Context Management', () => {
    it('should maintain conversation history', async () => {
      const messages = ['質問1', '質問2', '質問3'];
      
      for (const msg of messages) {
        await chatbotService.processMessage(msg, mockContext);
      }
      
      expect(mockContext.conversationHistory.length).toBe(6); // 3 user + 3 bot messages
    });

    it('should track application progress correctly', async () => {
      mockContext.applicationProgress.currentStep = 'initial';
      
      const message = 'PMSは構築済みです';
      await chatbotService.processMessage(message, mockContext);
      
      // Progress should be updated based on user response
      expect(mockContext.applicationProgress).toBeDefined();
    });

    it('should handle context with existing history', async () => {
      mockContext.conversationHistory = [
        { role: 'user', content: '以前の質問', timestamp: new Date() },
        { role: 'assistant', content: '以前の回答', timestamp: new Date() }
      ];
      
      const message = '新しい質問';
      await chatbotService.processMessage(message, mockContext);
      
      expect(mockContext.conversationHistory.length).toBe(4);
      expect(mockContext.conversationHistory[2].content).toBe(message);
    });
  });

  describe('Quick Replies', () => {
    it('should provide appropriate quick replies for initial state', async () => {
      const message = 'プライバシーマークについて教えて';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response.quickReplies).toBeDefined();
      expect(response.quickReplies).toContain('申請手続きを知りたい');
    });

    it('should provide context-specific quick replies', async () => {
      mockContext.applicationProgress.currentStep = 'preparation';
      
      const message = 'PMSについて詳しく';
      const response = await chatbotService.processMessage(message, mockContext);
      
      expect(response.quickReplies).toBeDefined();
      expect(response.quickReplies.length).toBeGreaterThan(0);
    });
  });

  describe('Error Handling', () => {
    it('should handle null message gracefully', async () => {
      const response = await chatbotService.processMessage(null as any, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toBeDefined();
    });

    it('should handle empty message', async () => {
      const response = await chatbotService.processMessage('', mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toBeDefined();
    });

    it('should handle very long messages', async () => {
      const longMessage = 'a'.repeat(10000);
      const response = await chatbotService.processMessage(longMessage, mockContext);
      
      expect(response).toBeDefined();
      expect(response.message).toBeDefined();
    });
  });
});