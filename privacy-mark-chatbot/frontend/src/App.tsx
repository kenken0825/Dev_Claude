import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import { ChatWindow } from './components/ChatWindow';
import { MessageInput } from './components/MessageInput';
import { SidePanel } from './components/SidePanel';
import { Header } from './components/Header';
import { Message, ApplicationProgress } from './types';
import { chatService } from './services/chatService';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'こんにちは！プライバシーマーク取得支援チャットボットです。\n\nプライバシーマークの取得に関するご質問にお答えします。\n以下のような内容についてお手伝いできます：\n\n• 申請手続きの流れ\n• 必要書類の準備\n• 審査基準と要件\n• 費用とスケジュール\n• よくある質問\n\nどのようなことをお知りになりたいですか？',
      sender: 'bot',
      timestamp: new Date(),
      quickReplies: [
        '申請の流れを知りたい',
        '必要書類について',
        '費用を確認したい',
        '要件をチェックしたい'
      ]
    }
  ]);
  
  const [isTyping, setIsTyping] = useState(false);
  const [applicationProgress, setApplicationProgress] = useState<ApplicationProgress>({
    currentStep: 'initial',
    completedSteps: [],
    remainingTasks: []
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    // ユーザーメッセージを追加
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    
    try {
      // バックエンドAPIを呼び出し
      const response = await chatService.sendMessage(text, {
        applicationProgress,
        conversationHistory: messages
      });
      
      // ボットの応答を追加
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.message,
        sender: 'bot',
        timestamp: new Date(),
        quickReplies: response.quickReplies,
        attachments: response.attachments
      };
      
      setMessages(prev => [...prev, botMessage]);
      
      // 進捗状況を更新
      if (response.progressUpdate) {
        setApplicationProgress(response.progressUpdate);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: '申し訳ございません。メッセージの送信中にエラーが発生しました。',
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickReply = (text: string) => {
    handleSendMessage(text);
  };

  const handleReset = () => {
    setMessages([
      {
        id: '1',
        text: 'チャットをリセットしました。最初から始めましょう。\n\nプライバシーマークの取得について、どのようなことをお知りになりたいですか？',
        sender: 'bot',
        timestamp: new Date(),
        quickReplies: [
          '申請の流れを知りたい',
          '必要書類について',
          '費用を確認したい',
          '要件をチェックしたい'
        ]
      }
    ]);
    setApplicationProgress({
      currentStep: 'initial',
      completedSteps: [],
      remainingTasks: []
    });
  };

  return (
    <div className="app">
      <Header onReset={handleReset} />
      
      <div className="app-body">
        <SidePanel 
          progress={applicationProgress}
          onNavigate={(step) => handleSendMessage(`${step}について詳しく教えてください`)}
        />
        
        <div className="chat-container">
          <ChatWindow 
            messages={messages}
            isTyping={isTyping}
            onQuickReply={handleQuickReply}
          />
          
          <MessageInput 
            onSendMessage={handleSendMessage}
            disabled={isTyping}
          />
          
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  );
};

export default App;