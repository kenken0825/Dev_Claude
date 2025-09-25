import * as fs from 'fs';
import * as yaml from 'js-yaml';
import path from 'path';

interface ApplicationStep {
  id: string;
  name: string;
  description: string;
  requiredDocuments: string[];
  estimatedDuration: string;
  nextSteps: string[];
  tips: string[];
}

interface DocumentTemplate {
  id: string;
  name: string;
  description: string;
  requiredFields: string[];
  sampleUrl?: string;
}

interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: string;
  keywords: string[];
  relatedQuestions?: string[];
}

export class PrivacyMarkKnowledgeBase {
  private knowledgeData: any;
  private applicationSteps: Map<string, ApplicationStep>;
  private documentTemplates: Map<string, DocumentTemplate>;
  private faqs: FAQ[];

  constructor() {
    this.loadKnowledgeBase();
    this.initializeApplicationSteps();
    this.initializeDocumentTemplates();
    this.initializeFAQs();
  }

  /**
   * YAMLファイルから知識ベースを読み込み
   */
  private loadKnowledgeBase(): void {
    try {
      const filePath = path.join(__dirname, '../../../generated_contexts/privacy_mark_context.yaml');
      const fileContents = fs.readFileSync(filePath, 'utf8');
      this.knowledgeData = yaml.load(fileContents);
    } catch (error) {
      console.error('Failed to load knowledge base:', error);
      // フォールバック用のデフォルトデータを設定
      this.knowledgeData = this.getDefaultKnowledgeData();
    }
  }

  /**
   * 申請ステップ情報の初期化
   */
  private initializeApplicationSteps(): void {
    this.applicationSteps = new Map();
    
    const steps: ApplicationStep[] = [
      {
        id: 'preparation',
        name: '事前準備',
        description: 'JIS Q 15001:2023に準拠した個人情報保護マネジメントシステム（PMS）を構築し、PDCAサイクルを最低1回実施します。',
        requiredDocuments: ['個人情報保護方針', '内部規程', '手順書'],
        estimatedDuration: '3-6ヶ月',
        nextSteps: ['document_preparation'],
        tips: [
          '全従業者への教育を忘れずに実施してください',
          '内部監査は全部門を対象に実施する必要があります',
          'マネジメントレビューには経営層の参加が必須です'
        ]
      },
      {
        id: 'document_preparation',
        name: '申請書類準備',
        description: '申請に必要な各種書類を準備し、記入漏れや不備がないか確認します。',
        requiredDocuments: [
          '申請様式1-8',
          '登記事項証明書',
          '定款',
          '教育記録',
          '内部監査記録'
        ],
        estimatedDuration: '2-4週間',
        nextSteps: ['submission'],
        tips: [
          '書類はコピーを提出し、原本は保管してください',
          '記載内容の整合性を必ず確認してください'
        ]
      },
      {
        id: 'submission',
        name: '申請書提出',
        description: 'オンラインまたは郵送で申請書類を提出します。',
        requiredDocuments: ['全申請書類一式'],
        estimatedDuration: '1日',
        nextSteps: ['document_review'],
        tips: [
          'オンライン申請の方が処理が早い傾向があります',
          '郵送の場合は配達記録が残る方法を選んでください'
        ]
      },
      {
        id: 'document_review',
        name: '文書審査',
        description: '提出書類の内容が審査基準に適合しているか審査されます。',
        requiredDocuments: [],
        estimatedDuration: '3-4週間',
        nextSteps: ['onsite_audit'],
        tips: [
          '追加資料を求められた場合は迅速に対応してください',
          '質問には正確かつ具体的に回答してください'
        ]
      },
      {
        id: 'onsite_audit',
        name: '現地審査',
        description: '審査員が事業所を訪問し、実際の運用状況を確認します。',
        requiredDocuments: ['運用記録', '最新のPMS文書'],
        estimatedDuration: '1-2日',
        nextSteps: ['result_notification'],
        tips: [
          '従業者への事前周知を行ってください',
          '審査当日は経営層の同席が必要です',
          '現場の実態と文書の内容が一致しているか確認してください'
        ]
      }
    ];
    
    steps.forEach(step => {
      this.applicationSteps.set(step.id, step);
    });
  }

  /**
   * 書類テンプレート情報の初期化
   */
  private initializeDocumentTemplates(): void {
    this.documentTemplates = new Map();
    
    const templates: DocumentTemplate[] = [
      {
        id: 'application_form',
        name: 'プライバシーマーク付与適格性審査申請書',
        description: '申請の基本情報を記載する書類',
        requiredFields: [
          '法人名',
          '代表者名',
          '所在地',
          '事業内容',
          '従業者数'
        ]
      },
      {
        id: 'education_summary',
        name: '教育実施サマリー',
        description: '全従業者への教育実施状況を報告する書類',
        requiredFields: [
          '教育実施日',
          '教育内容',
          '受講者リスト',
          '教育資料',
          '理解度確認結果'
        ]
      },
      {
        id: 'audit_summary',
        name: '内部監査実施サマリー',
        description: '内部監査の実施状況と結果を報告する書類',
        requiredFields: [
          '監査実施日',
          '監査対象部門',
          '監査員',
          '指摘事項',
          '改善状況'
        ]
      }
    ];
    
    templates.forEach(template => {
      this.documentTemplates.set(template.id, template);
    });
  }

  /**
   * FAQ情報の初期化
   */
  private initializeFAQs(): void {
    this.faqs = [
      {
        id: 'faq_001',
        question: 'プライバシーマーク取得にかかる期間はどれくらいですか？',
        answer: '準備から認証取得まで、一般的に6ヶ月から1年程度かかります。準備段階でPMS構築とPDCAサイクルの実施に3-6ヶ月、申請から認証まで2-4ヶ月が目安です。',
        category: '期間',
        keywords: ['期間', '時間', 'スケジュール'],
        relatedQuestions: ['費用はどれくらいかかりますか？']
      },
      {
        id: 'faq_002',
        question: 'プライバシーマーク取得の費用はどれくらいですか？',
        answer: '事業規模により異なりますが、小規模事業者（従業者5名以下）で約20万円、中規模（30名以下）で約50万円、大規模（30名超）で約100万円以上が目安です。これには申請料、審査料、付与登録料が含まれます。',
        category: '費用',
        keywords: ['費用', '料金', '金額', 'コスト'],
        relatedQuestions: ['支払いタイミングはいつですか？']
      },
      {
        id: 'faq_003',
        question: 'PMSとは何ですか？',
        answer: '個人情報保護マネジメントシステム（Personal information protection Management System）の略称です。JIS Q 15001に基づき、組織が個人情報を適切に管理するための仕組みです。方針、体制、計画、実施、点検、改善のPDCAサイクルで構成されます。',
        category: '用語',
        keywords: ['PMS', 'マネジメントシステム', '個人情報保護'],
        relatedQuestions: ['PDCAサイクルとは何ですか？']
      },
      {
        id: 'faq_004',
        question: '更新はどのくらいの頻度で必要ですか？',
        answer: 'プライバシーマークの有効期間は2年間です。更新申請は有効期間満了の8ヶ月前から4ヶ月前までの間に行う必要があります。',
        category: '更新',
        keywords: ['更新', '有効期間', '期限'],
        relatedQuestions: ['更新費用はいくらですか？']
      }
    ];
  }

  /**
   * 申請フロー情報の取得
   */
  getApplicationFlowInfo(): any {
    return {
      steps: Array.from(this.applicationSteps.values()),
      totalDuration: '6-12ヶ月',
      criticalPoints: [
        'PDCAサイクルを最低1回実施済みであること',
        '全従業者への教育が完了していること',
        '全部門の内部監査が完了していること'
      ]
    };
  }

  /**
   * 次のステップ情報の取得
   */
  getNextStepInfo(currentStepId: string): any {
    const currentStep = this.applicationSteps.get(currentStepId);
    if (!currentStep) {
      return this.getApplicationFlowInfo();
    }
    
    const nextStepId = currentStep.nextSteps[0];
    const nextStep = this.applicationSteps.get(nextStepId);
    
    return {
      currentStep: currentStep.name,
      nextStep: nextStep?.name || '完了',
      description: nextStep?.description || 'おめでとうございます！全てのステップが完了しました。',
      actions: nextStep?.tips || ['認証の維持管理を継続してください']
    };
  }

  /**
   * 書類情報の取得
   */
  getDocumentInfo(): any {
    return {
      templates: Array.from(this.documentTemplates.values()),
      totalDocuments: this.documentTemplates.size,
      categories: [
        '申請書類',
        '運用記録',
        '監査記録',
        '教育記録'
      ]
    };
  }

  /**
   * 要件情報の取得
   */
  getRequirements(): any {
    return {
      basic: [
        '日本国内に事業拠点があること',
        '法人単位での申請であること',
        'JIS Q 15001:2023準拠のPMS構築',
        'PDCAサイクル1回以上実施'
      ],
      documentation: [
        '個人情報保護方針の策定',
        '内部規程の整備',
        '運用記録の保管',
        '教育記録の保管',
        '監査記録の保管'
      ]
    };
  }

  /**
   * FAQ検索
   */
  async searchFAQ(query: string): Promise<FAQ | null> {
    const lowerQuery = query.toLowerCase();
    
    // キーワードマッチング
    for (const faq of this.faqs) {
      const keywordMatch = faq.keywords.some(keyword => 
        lowerQuery.includes(keyword.toLowerCase())
      );
      
      if (keywordMatch) {
        return faq;
      }
      
      // 質問文の部分一致
      if (faq.question.toLowerCase().includes(lowerQuery) ||
          lowerQuery.includes(faq.question.toLowerCase().substring(0, 10))) {
        return faq;
      }
    }
    
    return null;
  }

  /**
   * デフォルトの知識データ
   */
  private getDefaultKnowledgeData(): any {
    return {
      privacyMark: {
        overview: 'プライバシーマークは個人情報を適切に管理している事業者を認証する制度',
        certificationBody: 'JIPDEC',
        validityPeriod: '2年間'
      }
    };
  }
}