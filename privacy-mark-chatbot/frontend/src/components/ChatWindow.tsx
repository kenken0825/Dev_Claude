import React from 'react';
import { Message } from '../types';
import './ChatWindow.css';

interface ChatWindowProps {
  messages: Message[];
  isTyping: boolean;
  onQuickReply: (text: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isTyping,
  onQuickReply
}) => {
  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender === 'bot' ? 'bot-message' : 'user-message'}`}
          >
            <div className="message-avatar">
              {message.sender === 'bot' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              
              {message.attachments && message.attachments.length > 0 && (
                <div className="message-attachments">
                  {message.attachments.map((attachment, index) => (
                    <a
                      key={index}
                      href={attachment.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="attachment-link"
                    >
                      📎 {attachment.name}
                    </a>
                  ))}
                </div>
              )}
              
              {message.quickReplies && message.quickReplies.length > 0 && (
                <div className="quick-replies">
                  {message.quickReplies.map((reply, index) => (
                    <button
                      key={index}
                      className="quick-reply-button"
                      onClick={() => onQuickReply(reply)}
                    >
                      {reply}
                    </button>
                  ))}
                </div>
              )}
              
              <div className="message-time">
                {message.timestamp.toLocaleTimeString('ja-JP', {
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message bot-message typing-indicator">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};