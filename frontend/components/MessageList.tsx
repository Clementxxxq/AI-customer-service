'use client';

import { forwardRef } from 'react';
import './MessageList.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface MessageListProps {
  messages: Message[];
}

export const MessageList = forwardRef<HTMLDivElement, MessageListProps>(
  ({ messages }, ref) => {
    return (
      <div className="message-list">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
          >
            <div className="message-bubble">
              <p>{message.content}</p>
            </div>
          </div>
        ))}
        <div ref={ref} />
      </div>
    );
  }
);

MessageList.displayName = 'MessageList';
