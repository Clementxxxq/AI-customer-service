'use client';

import { forwardRef } from 'react';
import { CalendarPicker } from './CalendarPicker';
import './MessageList.css';

interface TimeSlot {
  date: string;
  day_of_week?: string;
  slots: string[];
}

interface AvailabilityData {
  available_dates: TimeSlot[];
  suggested?: {
    date: string;
    time: string;
  };
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  availability?: AvailabilityData;
  onSelectDateTime?: (date: string, time: string) => void;
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
              
              {/* Show calendar picker if availability data is present */}
              {message.availability && message.onSelectDateTime && (
                <CalendarPicker
                  availableDates={message.availability.available_dates}
                  suggestedDate={message.availability.suggested?.date}
                  suggestedTime={message.availability.suggested?.time}
                  onSelectDateTime={message.onSelectDateTime}
                />
              )}
            </div>
          </div>
        ))}
        <div ref={ref} />
      </div>
    );
  }
);

MessageList.displayName = 'MessageList';
