# Google Cloud Vision API - Kindle本OCR実装コンテキスト

## 🎯 目的
macOS環境でKindle本のスクリーンショットからテキストを抽出し、構造化されたコンテキストを生成するシステムの開発

## 📚 L1: Cloud Vision API概要

### 1.1 主要機能カテゴリ
- **画像解析**: ラベル検出、顔認識、ランドマーク識別
- **テキスト抽出**: OCR、ドキュメントテキスト検出、手書き認識
- **コンテンツ管理**: 明示的コンテンツのタグ付け、画像属性

### 1.2 プロダクト位置づけ
- **用途**: 画像からの情報抽出と分析
- **代替選択肢**: 
  - Vertex AI (カスタムビジョンモデル用)
  - ML Kit (モバイル特化実装用)
  - Document AI (高度な文書処理用)

## 📖 L2: OCR機能詳細

### 2.1 OCRメソッドタイプ

#### TEXT_DETECTION
- **用途**: 一般的な画像からのテキスト抽出（看板、ラベル等）
- **特徴**: シンプルなテキスト抽出
- **推奨**: 疎なテキスト、単純なレイアウト

#### DOCUMENT_TEXT_DETECTION
- **用途**: 密度の高いテキストと文書用に最適化
- **特徴**: 
  - ページ/ブロック/段落/単語の階層構造
  - より詳細な位置情報
  - 読み順序の保持
- **推奨**: **Kindle本のOCRにはこちらを使用**

### 2.2 サポート形式と制限

#### 画像フォーマット
```yaml
supported_formats:
  - JPEG
  - PNG (PNG8, PNG24)
  - GIF (最初のフレームのみ)
  - BMP
  - WEBP
  - RAW
  - ICO
  - PDF (Cloud Storage経由)
  - TIFF (Cloud Storage経由)
```

#### サイズ制限
```yaml
limits:
  max_file_size: 20MB
  max_json_request: 10MB
  max_pixels: 75,000,000 (75M)
  pdf_max_pages: 2000
  recommended_resolution:
    ocr: "1024 x 768"
    optimal: "1600 x 1200"
```

## 🔧 L3: 実装詳細

### 3.1 API呼び出し方法

#### Python実装例
```python
from google.cloud import vision
import io

def extract_text_from_image(image_path):
    """Kindle本のスクリーンショットからテキストを抽出"""
    client = vision.ImageAnnotatorClient()
    
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    
    # DOCUMENT_TEXT_DETECTIONを使用（書籍に最適）
    response = client.document_text_detection(
        image=image,
        image_context={'language_hints': ['ja']}  # 日本語ヒント
    )
    
    return response.full_text_annotation
```

### 3.2 レスポンス構造

```json
{
  "fullTextAnnotation": {
    "pages": [{
      "blocks": [{
        "paragraphs": [{
          "words": [{
            "symbols": [{
              "text": "文",
              "boundingBox": {...},
              "confidence": 0.99
            }]
          }]
        }]
      }]
    }],
    "text": "完全なテキスト内容"
  },
  "textAnnotations": [{
    "description": "検出されたテキスト",
    "boundingPoly": {
      "vertices": [
        {"x": 0, "y": 0},
        {"x": 100, "y": 0},
        {"x": 100, "y": 50},
        {"x": 0, "y": 50}
      ]
    }
  }]
}
```

### 3.3 言語サポート

#### 日本語OCR設定
```python
image_context = {
    'language_hints': ['ja'],  # 日本語優先
    # または自動検出（推奨）
    'language_hints': []
}
```

#### 手書き認識
```python
# 手書き日本語の場合
image_context = {
    'language_hints': ['ja-t-i0-handwrit']
}
```

## 💰 L4: 実装仕様とベストプラクティス

### 4.1 料金体系

```yaml
pricing:
  free_tier: 
    units: 1000
    period: monthly
  
  document_text_detection:
    tier1:
      range: "1,001 - 5,000,000"
      price: "$1.50 per 1,000 units"
    tier2:
      range: "5,000,001+"
      price: "$0.60 per 1,000 units"
```

### 4.2 Kindle本OCR最適化設定

#### 推奨前処理
```python
def preprocess_kindle_screenshot(image_path):
    """Kindle本のスクリーンショット前処理"""
    from PIL import Image
    
    img = Image.open(image_path)
    
    # 推奨設定
    optimal_width = 1600
    optimal_height = 1200
    
    # アスペクト比を保持してリサイズ
    img.thumbnail((optimal_width, optimal_height), Image.LANCZOS)
    
    # グレースケール変換（オプション）
    # img = img.convert('L')
    
    # コントラスト調整
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    return img
```

### 4.3 バッチ処理実装

```python
def batch_process_kindle_pages(image_paths, batch_size=10):
    """複数ページの一括処理"""
    from google.cloud import vision
    
    client = vision.ImageAnnotatorClient()
    results = []
    
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        requests = []
        
        for path in batch:
            with open(path, 'rb') as f:
                content = f.read()
            
            image = vision.Image(content=content)
            requests.append({
                'image': image,
                'features': [{
                    'type': vision.Feature.Type.DOCUMENT_TEXT_DETECTION
                }]
            })
        
        responses = client.batch_annotate_images(requests=requests)
        results.extend(responses.responses)
    
    return results
```

### 4.4 macOS統合のベストプラクティス

#### スクリーンショット自動取得
```python
import subprocess
import time

def capture_kindle_page():
    """macOSでKindleアプリのスクリーンショットを取得"""
    # スクリーンキャプチャコマンド
    subprocess.run([
        'screencapture', 
        '-x',  # 音を消す
        '-R', '100,100,1000,1400',  # 領域指定
        'kindle_page.png'
    ])
    time.sleep(0.5)
    return 'kindle_page.png'
```

#### Automator連携
```applescript
-- AppleScript for Kindle page turning and capture
tell application "Kindle"
    activate
    delay 1
    tell application "System Events"
        key code 124 -- Right arrow for next page
    end tell
end tell
do shell script "screencapture -x ~/Desktop/kindle_page.png"
```

### 4.5 エラーハンドリング

```python
def safe_ocr_extraction(image_path, max_retries=3):
    """エラーハンドリング付きOCR"""
    from google.cloud import vision
    from google.api_core import retry
    import time
    
    client = vision.ImageAnnotatorClient()
    
    @retry.Retry(deadline=30)
    def extract_with_retry():
        try:
            with open(image_path, 'rb') as f:
                image = vision.Image(content=f.read())
            
            response = client.document_text_detection(image=image)
            
            if response.error.message:
                raise Exception(f'API Error: {response.error.message}')
            
            return response
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            raise
    
    return extract_with_retry()
```

### 4.6 構造化出力生成

```python
def generate_structured_context(ocr_response):
    """OCR結果から構造化コンテキストを生成"""
    structured_data = {
        'metadata': {
            'source': 'kindle_screenshot',
            'extraction_date': datetime.now().isoformat(),
            'confidence': calculate_average_confidence(ocr_response)
        },
        'content': {
            'full_text': ocr_response.full_text_annotation.text,
            'pages': []
        }
    }
    
    for page in ocr_response.full_text_annotation.pages:
        page_data = {
            'blocks': [],
            'paragraphs': []
        }
        
        for block in page.blocks:
            block_text = extract_block_text(block)
            page_data['blocks'].append({
                'text': block_text,
                'confidence': block.confidence
            })
        
        structured_data['content']['pages'].append(page_data)
    
    return structured_data
```

## 🚀 実装チェックリスト

### 必須実装項目
- [ ] Google Cloud プロジェクトの作成
- [ ] Vision API の有効化
- [ ] サービスアカウントキーの生成
- [ ] Python クライアントライブラリのインストール
- [ ] DOCUMENT_TEXT_DETECTION の実装
- [ ] 日本語言語ヒントの設定
- [ ] エラーハンドリング
- [ ] バッチ処理の実装

### 推奨実装項目
- [ ] 画像前処理パイプライン
- [ ] macOS Automator スクリプト
- [ ] ページ自動めくり機能
- [ ] 構造化データ出力
- [ ] プログレスバー表示
- [ ] OCR結果のキャッシング
- [ ] 重複テキスト除去
- [ ] 章・節の自動認識

### パフォーマンス最適化
- [ ] 並列処理の実装
- [ ] 画像圧縮の最適化
- [ ] メモリ使用量の監視
- [ ] API呼び出しレート制限の実装

## 📊 期待される成果

### システム要件
```yaml
performance:
  processing_speed: "< 2秒/ページ"
  accuracy: "> 95% (日本語テキスト)"
  batch_size: "10-20ページ/バッチ"
  
cost:
  estimated_monthly: "< $10 (1000ページ/月)"
  free_tier_coverage: "最初の1000ユニット"
  
quality:
  text_preservation: "99%"
  layout_detection: "ブロック・段落レベル"
  language_detection: "自動"
```

## 🔗 関連リソース

- [Cloud Vision API ドキュメント](https://cloud.google.com/vision/docs)
- [OCR機能詳細](https://cloud.google.com/vision/docs/ocr)
- [料金計算ツール](https://cloud.google.com/vision/pricing)
- [クライアントライブラリ](https://cloud.google.com/vision/docs/libraries)
- [Document AI (高度な処理)](https://cloud.google.com/document-ai)

---

*このコンテキストは、macOS環境でKindle本のOCR処理を実装するための包括的なガイドです。*
*最終更新: 2025-08-24*