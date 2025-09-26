export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  quickReplies?: string[];
  attachments?: Attachment[];
}

export interface Attachment {
  type: 'document' | 'link' | 'image';
  name: string;
  url: string;
  description?: string;
}

export interface ApplicationProgress {
  currentStep: string;
  completedSteps: string[];
  remainingTasks: string[];
}

export interface ChatContext {
  sessionId: string;
  userId?: string;
  conversationHistory: Message[];
  applicationProgress: ApplicationProgress;
}

export interface ChatResponse {
  success: boolean;
  data?: {
    message: string;
    suggestions?: string[];
    attachments?: Attachment[];
    quickReplies?: string[];
    progressUpdate?: ApplicationProgress;
  };
  error?: string;
}