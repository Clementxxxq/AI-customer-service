'use client';

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { MessageList } from './MessageList';
import { InputBox } from './InputBox';
import './DentalChat.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export function DentalChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId] = useState(() => `chat_${Date.now()}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initial greeting
  useEffect(() => {
    setMessages([
      {
        id: 'init',
        role: 'assistant',
        content: 'Which doctor would you like to see?',
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/chat/message', {
        content,
        user_id: 1,
        conversation_id: conversationId,
      });

      const data = response.data;
      
      // Add AI response
      const aiMessage: Message = {
        id: data.message_id,
        role: 'assistant',
        content: data.bot_response,
        timestamp: data.timestamp,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🦷 AI Dental Assistant</h1>
      </div>
      <MessageList messages={messages} ref={messagesEndRef} />
      <InputBox onSendMessage={handleSendMessage} disabled={loading} />
    </div>
  );
}
