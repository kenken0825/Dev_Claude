import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { ChatResponse, Message, ApplicationProgress } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api/v1';

class ChatService {
  private sessionId: string;
  
  constructor() {
    this.sessionId = this.getOrCreateSessionId();
  }
  
  private getOrCreateSessionId(): string {
    const stored = localStorage.getItem('chatSessionId');
    if (stored) return stored;
    
    const newId = uuidv4();
    localStorage.setItem('chatSessionId', newId);
    return newId;
  }
  
  async sendMessage(
    message: string,
    context: {
      applicationProgress: ApplicationProgress;
      conversationHistory: Message[];
    }
  ): Promise<ChatResponse['data']> {
    try {
      const response = await axios.post<ChatResponse>(
        `${API_BASE_URL}/chat/message`,
        {
          message,
          sessionId: this.sessionId,
          userId: localStorage.getItem('userId') || undefined
        }
      );
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      }
      
      throw new Error(response.data.error || 'Unknown error');
    } catch (error) {
      console.error('Chat service error:', error);
      
      // フォールバック応答
      return {
        message: '申し訳ございません。現在システムに接続できません。しばらくしてからもう一度お試しください。',
        quickReplies: ['最初から始める', 'サポートに連絡']
      };
    }
  }
  
  async resetSession(): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/chat/session/${this.sessionId}`);
      this.sessionId = uuidv4();
      localStorage.setItem('chatSessionId', this.sessionId);
    } catch (error) {
      console.error('Session reset error:', error);
    }
  }
  
  async getSessionInfo(): Promise<any> {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/session/${this.sessionId}`);
      return response.data.data;
    } catch (error) {
      console.error('Session info error:', error);
      return null;
    }
  }
}

export const chatService = new ChatService();