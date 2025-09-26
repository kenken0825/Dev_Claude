import React, { useState, KeyboardEvent } from 'react';
import './MessageInput.css';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false
}) => {
  const [message, setMessage] = useState('');
  
  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };
  
  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <div className="message-input-container">
      <div className="input-wrapper">
        <textarea
          className="message-input"
          placeholder="メッセージを入力してください..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={disabled}
          rows={1}
          maxLength={1000}
        />
        <div className="input-actions">
          <button
            className="attach-button"
            title="ファイルを添付"
            disabled={disabled}
          >
            📎
          </button>
          <button
            className="send-button"
            onClick={handleSend}
            disabled={disabled || !message.trim()}
            title="送信"
          >
            ➤
          </button>
        </div>
      </div>
      <div className="input-info">
        <span className="char-count">{message.length}/1000</span>
        <span className="input-hint">Shift+Enter で改行</span>
      </div>
    </div>
  );
};