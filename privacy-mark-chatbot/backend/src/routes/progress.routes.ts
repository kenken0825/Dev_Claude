import { Router, Request, Response } from 'express';

const router = Router();

// 進捗管理用の簡易ストア（本番環境ではDBを使用）
const progressStore = new Map<string, any>();

/**
 * GET /api/v1/progress/:userId
 * ユーザーの申請進捗を取得
 */
router.get('/:userId', (req: Request, res: Response) => {
  try {
    const { userId } = req.params;
    const progress = progressStore.get(userId) || {
      userId,
      currentStep: 'initial',
      completedSteps: [],
      totalSteps: 7,
      startDate: null,
      lastUpdated: null,
      tasks: []
    };
    
    res.json({
      success: true,
      data: progress
    });
  } catch (error) {
    console.error('Progress retrieval error:', error);
    res.status(500).json({
      success: false,
      error: '進捗情報の取得中にエラーが発生しました'
    });
  }
});

/**
 * PUT /api/v1/progress/:userId
 * 進捗を更新
 */
router.put('/:userId', (req: Request, res: Response) => {
  try {
    const { userId } = req.params;
    const { currentStep, completedSteps, tasks } = req.body;
    
    const existingProgress = progressStore.get(userId) || {
      userId,
      startDate: new Date().toISOString(),
      totalSteps: 7
    };
    
    const updatedProgress = {
      ...existingProgress,
      currentStep: currentStep || existingProgress.currentStep,
      completedSteps: completedSteps || existingProgress.completedSteps,
      tasks: tasks || existingProgress.tasks,
      lastUpdated: new Date().toISOString()
    };
    
    progressStore.set(userId, updatedProgress);
    
    res.json({
      success: true,
      data: updatedProgress
    });
  } catch (error) {
    console.error('Progress update error:', error);
    res.status(500).json({
      success: false,
      error: '進捗の更新中にエラーが発生しました'
    });
  }
});

/**
 * POST /api/v1/progress/:userId/tasks
 * タスクを追加
 */
router.post('/:userId/tasks', (req: Request, res: Response) => {
  try {
    const { userId } = req.params;
    const { task } = req.body;
    
    if (!task || !task.name) {
      return res.status(400).json({
        success: false,
        error: 'タスク名は必須です'
      });
    }
    
    const progress = progressStore.get(userId) || {
      userId,
      currentStep: 'initial',
      completedSteps: [],
      tasks: []
    };
    
    const newTask = {
      id: Date.now().toString(),
      name: task.name,
      description: task.description || '',
      status: 'pending',
      createdAt: new Date().toISOString(),
      dueDate: task.dueDate || null
    };
    
    progress.tasks.push(newTask);
    progressStore.set(userId, progress);
    
    res.json({
      success: true,
      data: newTask
    });
  } catch (error) {
    console.error('Task creation error:', error);
    res.status(500).json({
      success: false,
      error: 'タスクの作成中にエラーが発生しました'
    });
  }
});

/**
 * PUT /api/v1/progress/:userId/tasks/:taskId
 * タスクのステータスを更新
 */
router.put('/:userId/tasks/:taskId', (req: Request, res: Response) => {
  try {
    const { userId, taskId } = req.params;
    const { status } = req.body;
    
    const progress = progressStore.get(userId);
    if (!progress) {
      return res.status(404).json({
        success: false,
        error: '進捗情報が見つかりません'
      });
    }
    
    const task = progress.tasks.find((t: any) => t.id === taskId);
    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'タスクが見つかりません'
      });
    }
    
    task.status = status;
    task.updatedAt = new Date().toISOString();
    
    if (status === 'completed') {
      task.completedAt = new Date().toISOString();
    }
    
    progressStore.set(userId, progress);
    
    res.json({
      success: true,
      data: task
    });
  } catch (error) {
    console.error('Task update error:', error);
    res.status(500).json({
      success: false,
      error: 'タスクの更新中にエラーが発生しました'
    });
  }
});

export { router as ProgressRouter };