import React from 'react';
import './Header.css';

interface HeaderProps {
  onReset: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onReset }) => {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="logo">
          <span className="logo-icon">🛡️</span>
          <h1>プライバシーマーク取得支援</h1>
        </div>
      </div>
      
      <div className="header-center">
        <nav className="nav-menu">
          <button className="nav-item active">チャット</button>
          <button className="nav-item">書類管理</button>
          <button className="nav-item">進捗確認</button>
          <button className="nav-item">FAQ</button>
        </nav>
      </div>
      
      <div className="header-right">
        <button className="icon-button" title="通知">
          🔔
        </button>
        <button className="icon-button" title="ヘルプ">
          ❓
        </button>
        <button className="reset-button" onClick={onReset} title="リセット">
          🔄 リセット
        </button>
      </div>
    </header>
  );
};