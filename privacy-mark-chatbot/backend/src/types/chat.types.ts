export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

export interface ApplicationProgress {
  currentStep: string;
  completedSteps: string[];
  remainingTasks: string[];
}

export interface ConversationContext {
  sessionId: string;
  userId?: string;
  conversationHistory: ChatMessage[];
  applicationProgress?: ApplicationProgress;
  preferences?: Record<string, any>;
}

export interface ChatResponse {
  message: string;
  suggestions?: string[];
  attachments?: Attachment[];
  quickReplies?: string[];
  progressUpdate?: ApplicationProgress;
}

export interface Attachment {
  type: 'document' | 'link' | 'image';
  name: string;
  url: string;
  description?: string;
}