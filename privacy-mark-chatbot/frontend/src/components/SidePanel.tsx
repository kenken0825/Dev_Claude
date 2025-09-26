import React from 'react';
import { ApplicationProgress } from '../types';
import './SidePanel.css';

interface SidePanelProps {
  progress: ApplicationProgress;
  onNavigate: (step: string) => void;
}

const steps = [
  { id: 'preparation', name: '事前準備', icon: '📋' },
  { id: 'document_preparation', name: '書類準備', icon: '📄' },
  { id: 'submission', name: '申請提出', icon: '📮' },
  { id: 'document_review', name: '文書審査', icon: '🔍' },
  { id: 'onsite_audit', name: '現地審査', icon: '🏢' },
  { id: 'result', name: '結果通知', icon: '📨' },
  { id: 'contract', name: '付与契約', icon: '✅' }
];

export const SidePanel: React.FC<SidePanelProps> = ({
  progress,
  onNavigate
}) => {
  const getStepStatus = (stepId: string) => {
    if (progress.completedSteps.includes(stepId)) return 'completed';
    if (progress.currentStep === stepId) return 'current';
    return 'pending';
  };
  
  const completionRate = Math.round(
    (progress.completedSteps.length / steps.length) * 100
  );
  
  return (
    <div className="side-panel">
      <div className="panel-header">
        <h3>申請進捗</h3>
        <div className="progress-summary">
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${completionRate}%` }}
            />
          </div>
          <span className="progress-text">{completionRate}% 完了</span>
        </div>
      </div>
      
      <div className="steps-container">
        {steps.map((step, index) => {
          const status = getStepStatus(step.id);
          return (
            <div
              key={step.id}
              className={`step-item ${status}`}
              onClick={() => onNavigate(step.name)}
            >
              <div className="step-number">{index + 1}</div>
              <div className="step-content">
                <span className="step-icon">{step.icon}</span>
                <span className="step-name">{step.name}</span>
              </div>
              <div className="step-status">
                {status === 'completed' && '✓'}
                {status === 'current' && '▶'}
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="panel-footer">
        <h4>残りのタスク</h4>
        <div className="task-list">
          {progress.remainingTasks.length > 0 ? (
            progress.remainingTasks.slice(0, 3).map((task, index) => (
              <div key={index} className="task-item">
                • {task}
              </div>
            ))
          ) : (
            <div className="no-tasks">タスクはありません</div>
          )}
        </div>
      </div>
    </div>
  );
};