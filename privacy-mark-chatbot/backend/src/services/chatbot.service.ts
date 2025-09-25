import { PrivacyMarkKnowledgeBase } from '../knowledge/privacyMarkKnowledge';
import { ConversationContext, ChatMessage, ChatResponse } from '../types/chat.types';

export class ChatbotService {
  private knowledgeBase: PrivacyMarkKnowledgeBase;

  constructor() {
    this.knowledgeBase = new PrivacyMarkKnowledgeBase();
  }

  /**
   * メッセージを処理して適切な応答を生成
   */
  async processMessage(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    try {
      // インテント分類
      const intent = await this.classifyIntent(message);
      
      // コンテキストに基づく応答生成
      let response: ChatResponse;
      
      switch (intent.type) {
        case 'application_flow':
          response = await this.handleApplicationFlow(message, context);
          break;
        
        case 'document_inquiry':
          response = await this.handleDocumentInquiry(message, context);
          break;
        
        case 'requirement_check':
          response = await this.handleRequirementCheck(message, context);
          break;
        
        case 'progress_status':
          response = await this.handleProgressStatus(message, context);
          break;
        
        case 'faq':
          response = await this.handleFAQ(message, context);
          break;
        
        default:
          response = await this.handleGeneralInquiry(message, context);
      }
      
      // コンテキスト更新
      await this.updateContext(context, message, response);
      
      return response;
    } catch (error) {
      console.error('Error processing message:', error);
      return this.createErrorResponse();
    }
  }

  /**
   * 申請フローに関する問い合わせ処理
   */
  private async handleApplicationFlow(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    const flowInfo = this.knowledgeBase.getApplicationFlowInfo();
    const currentStep = context.applicationProgress?.currentStep || 'initial';
    
    const response: ChatResponse = {
      message: '',
      suggestions: [],
      attachments: [],
      quickReplies: []
    };

    // 現在のステップに応じた情報提供
    if (currentStep === 'initial') {
      response.message = `プライバシーマーク取得の申請フローについてご案内します。

**申請の主要ステップ:**
1. 事前準備（PMS構築・PDCAサイクル実施）
2. 申請書類の準備
3. 申請書の提出
4. 文書審査
5. 現地審査
6. 審査結果通知
7. 付与契約締結

まずは、貴社の現在の準備状況を確認させてください。
個人情報保護マネジメントシステム（PMS）は既に構築されていますか？`;
      
      response.quickReplies = [
        'PMSは構築済みです',
        'PMSを構築中です',
        'PMSはこれから構築予定です',
        'PMSについて詳しく知りたい'
      ];
    } else {
      // 次のステップの案内
      const nextStepInfo = this.knowledgeBase.getNextStepInfo(currentStep);
      response.message = nextStepInfo.description;
      response.suggestions = nextStepInfo.actions;
    }
    
    return response;
  }

  /**
   * 書類に関する問い合わせ処理
   */
  private async handleDocumentInquiry(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    const documentInfo = this.knowledgeBase.getDocumentInfo();
    
    const response: ChatResponse = {
      message: `プライバシーマーク申請に必要な書類についてご案内します。

**新規申請の必要書類:**
1. プライバシーマーク付与適格性審査申請書（申請様式1）
2. 個人情報を取扱う業務の概要（申請様式4）
3. すべての事業所の所在地及び業務内容（申請様式5）
4. 個人情報保護マネジメントシステム文書の一覧（申請様式6）
5. 教育実施サマリー（申請様式7）
6. 内部監査・マネジメントレビュー実施サマリー（申請様式8）

その他、登記事項証明書、定款、個人情報保護方針などが必要です。

どの書類について詳しく知りたいですか？`,
      suggestions: [],
      attachments: [],
      quickReplies: [
        '申請書の記入方法',
        '教育実施サマリーの作成方法',
        '内部監査記録の準備',
        '書類のテンプレート'
      ]
    };
    
    return response;
  }

  /**
   * 要件チェック処理
   */
  private async handleRequirementCheck(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    const requirements = this.knowledgeBase.getRequirements();
    
    const response: ChatResponse = {
      message: `プライバシーマーク取得の要件を確認します。

**基本要件チェックリスト:**
✅ 日本国内に事業拠点がある
✅ 法人として申請する
✅ JIS Q 15001:2023に準拠したPMSを構築している
✅ PMSのPDCAサイクルを最低1回実施済み
✅ 全従業者への教育を実施済み
✅ 全部門の内部監査を実施済み
✅ マネジメントレビューを実施済み

これらの要件について、現在の状況を教えてください。`,
      suggestions: ['要件診断を開始'],
      attachments: [],
      quickReplies: []
    };
    
    return response;
  }

  /**
   * 進捗状況の確認処理
   */
  private async handleProgressStatus(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    const progress = context.applicationProgress || {
      currentStep: 'initial',
      completedSteps: [],
      remainingTasks: []
    };
    
    const response: ChatResponse = {
      message: `現在の申請準備状況をお伝えします。

**完了済みタスク:** ${progress.completedSteps.length}件
**現在のステップ:** ${progress.currentStep}
**残りのタスク:** ${progress.remainingTasks.length}件

詳細な進捗レポートを確認しますか？`,
      suggestions: ['詳細レポート表示', 'タスクリスト確認'],
      attachments: [],
      quickReplies: []
    };
    
    return response;
  }

  /**
   * FAQ処理
   */
  private async handleFAQ(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    const faqAnswer = await this.knowledgeBase.searchFAQ(message);
    
    if (faqAnswer) {
      return {
        message: faqAnswer.answer,
        suggestions: faqAnswer.relatedQuestions || [],
        attachments: [],
        quickReplies: []
      };
    }
    
    return this.handleGeneralInquiry(message, context);
  }

  /**
   * 一般的な問い合わせ処理
   */
  private async handleGeneralInquiry(
    message: string,
    context: ConversationContext
  ): Promise<ChatResponse> {
    const response: ChatResponse = {
      message: `ご質問を承りました。プライバシーマークに関する以下の情報から選択いただくか、具体的な質問をお聞かせください。

• 申請手続きの流れ
• 必要書類について
• 審査基準と要件
• 費用について
• よくある質問（FAQ）`,
      suggestions: [],
      attachments: [],
      quickReplies: [
        '申請手続きを知りたい',
        '必要書類を確認したい',
        '費用を知りたい',
        'FAQを見る'
      ]
    };
    
    return response;
  }

  /**
   * インテント分類
   */
  private async classifyIntent(message: string): Promise<{ type: string; confidence: number }> {
    // 簡易的なキーワードベースの分類（実際はNLPモデルを使用）
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('申請') || lowerMessage.includes('手続き') || lowerMessage.includes('フロー')) {
      return { type: 'application_flow', confidence: 0.9 };
    }
    
    if (lowerMessage.includes('書類') || lowerMessage.includes('様式') || lowerMessage.includes('テンプレート')) {
      return { type: 'document_inquiry', confidence: 0.9 };
    }
    
    if (lowerMessage.includes('要件') || lowerMessage.includes('条件') || lowerMessage.includes('資格')) {
      return { type: 'requirement_check', confidence: 0.9 };
    }
    
    if (lowerMessage.includes('進捗') || lowerMessage.includes('状況') || lowerMessage.includes('ステータス')) {
      return { type: 'progress_status', confidence: 0.9 };
    }
    
    if (lowerMessage.includes('？') || lowerMessage.includes('教えて') || lowerMessage.includes('どう')) {
      return { type: 'faq', confidence: 0.7 };
    }
    
    return { type: 'general', confidence: 0.5 };
  }

  /**
   * コンテキスト更新
   */
  private async updateContext(
    context: ConversationContext,
    message: string,
    response: ChatResponse
  ): Promise<void> {
    // 会話履歴の更新
    context.conversationHistory.push({
      role: 'user',
      content: message,
      timestamp: new Date()
    });
    
    context.conversationHistory.push({
      role: 'assistant',
      content: response.message,
      timestamp: new Date()
    });
    
    // コンテキストの永続化（実装省略）
  }

  /**
   * エラー応答の生成
   */
  private createErrorResponse(): ChatResponse {
    return {
      message: '申し訳ございません。処理中にエラーが発生しました。もう一度お試しください。',
      suggestions: ['最初から始める', 'サポートに連絡'],
      attachments: [],
      quickReplies: []
    };
  }
}