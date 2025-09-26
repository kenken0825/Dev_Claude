import { Router, Request, Response } from 'express';
import path from 'path';

const router = Router();

// 書類テンプレート情報
const documentTemplates = [
  {
    id: 'form-1',
    name: 'プライバシーマーク付与適格性審査申請書',
    category: '新規申請',
    format: 'Word',
    downloadUrl: '/templates/form-1.docx'
  },
  {
    id: 'form-6',
    name: '個人情報保護マネジメントシステム文書の一覧',
    category: '新規申請',
    format: 'Excel',
    downloadUrl: '/templates/form-6.xlsx'
  },
  {
    id: 'form-7',
    name: '教育実施サマリー',
    category: '新規申請',
    format: 'Word',
    downloadUrl: '/templates/form-7.docx'
  },
  {
    id: 'form-8',
    name: '内部監査・マネジメントレビュー実施サマリー',
    category: '新規申請',
    format: 'Word',
    downloadUrl: '/templates/form-8.docx'
  }
];

/**
 * GET /api/v1/documents
 * 書類テンプレート一覧を取得
 */
router.get('/', (req: Request, res: Response) => {
  try {
    const { category } = req.query;
    
    let templates = documentTemplates;
    if (category) {
      templates = templates.filter(t => t.category === category);
    }
    
    res.json({
      success: true,
      data: templates
    });
  } catch (error) {
    console.error('Document list error:', error);
    res.status(500).json({
      success: false,
      error: '書類一覧の取得中にエラーが発生しました'
    });
  }
});

/**
 * GET /api/v1/documents/:id
 * 特定の書類テンプレート情報を取得
 */
router.get('/:id', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const template = documentTemplates.find(t => t.id === id);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        error: '書類が見つかりません'
      });
    }
    
    res.json({
      success: true,
      data: template
    });
  } catch (error) {
    console.error('Document retrieval error:', error);
    res.status(500).json({
      success: false,
      error: '書類情報の取得中にエラーが発生しました'
    });
  }
});

/**
 * GET /api/v1/documents/:id/download
 * 書類テンプレートをダウンロード
 */
router.get('/:id/download', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const template = documentTemplates.find(t => t.id === id);
    
    if (!template) {
      return res.status(404).json({
        success: false,
        error: '書類が見つかりません'
      });
    }
    
    // 実際のファイルパス（本番環境では適切なストレージから取得）
    const filePath = path.join(__dirname, '../../templates', `${id}.docx`);
    
    res.download(filePath, template.name, (err) => {
      if (err) {
        console.error('Download error:', err);
        res.status(500).json({
          success: false,
          error: 'ファイルのダウンロード中にエラーが発生しました'
        });
      }
    });
  } catch (error) {
    console.error('Document download error:', error);
    res.status(500).json({
      success: false,
      error: 'ダウンロード処理中にエラーが発生しました'
    });
  }
});

export { router as DocumentRouter };