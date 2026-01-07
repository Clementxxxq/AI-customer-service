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

/**
 * Generate greeting based on current time (后端确定性逻辑)
 */
function getGreeting(): string {
  const hour = new Date().getHours();
  
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

/**
 * Generate complete welcome message (不让 LLM 自己决定)
 */
function getWelcomeMessage(): string {
  const greeting = getGreeting();
  
  return `${greeting}, welcome to ABC Dental Clinic. 
We provide professional dental services including cleaning, extraction, fillings, checkups, and more.
How can I help you today?`;
}

/**
 * Fetch available doctors from backend
 */
async function fetchAvailableDoctors(): Promise<string[]> {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/doctors/');
    if (Array.isArray(response.data) && response.data.length > 0) {
      return response.data.map((doc: any) => doc.name);
    }
  } catch (error) {
    console.error('Error fetching doctors:', error);
  }
  // Fallback to default doctors
  return ["Dr. Wang", "Dr. Chen", "Dr. Li"];
}

/**
 * Generate doctor selection prompt with available doctors
 */
function getDoctorSelectionPrompt(doctors: string[]): string {
  const doctorsList = doctors.join(", ");
  return `Today, we have ${doctorsList} available. Which doctor would you like to see?`;
}

export function DentalChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId] = useState(() => `chat_${Date.now()}`);
  const [doctors, setDoctors] = useState<string[]>(["Dr. Wang", "Dr. Chen", "Dr. Li"]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch doctors and initialize greeting
  useEffect(() => {
    const initializeChat = async () => {
      const availableDoctors = await fetchAvailableDoctors();
      setDoctors(availableDoctors);
      
      // Generate welcome messages
      const welcomeMessage = getWelcomeMessage();
      const doctorPrompt = getDoctorSelectionPrompt(availableDoctors);
      
      setMessages([
        {
          id: 'greeting',
          role: 'assistant',
          content: welcomeMessage,
          timestamp: new Date().toISOString(),
        },
        {
          id: 'doctor-selection',
          role: 'assistant',
          content: doctorPrompt,
          timestamp: new Date().toISOString(),
        },
      ]);
    };

    initializeChat();
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
