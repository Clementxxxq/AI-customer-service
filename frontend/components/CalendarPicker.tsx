'use client';

import { useState } from 'react';
import './CalendarPicker.css';

interface TimeSlot {
  date: string;
  day_of_week?: string;
  slots: string[];
}

interface CalendarPickerProps {
  availableDates: TimeSlot[];
  suggestedDate?: string;
  suggestedTime?: string;
  onSelectDateTime: (date: string, time: string) => void;
}

/**
 * Calendar component for selecting appointment date and time
 * Displays available dates and time slots
 */
export function CalendarPicker({
  availableDates,
  suggestedDate,
  suggestedTime,
  onSelectDateTime,
}: CalendarPickerProps) {
  const [selectedDate, setSelectedDate] = useState<string | null>(
    suggestedDate || availableDates[0]?.date || null
  );

  // Parse available dates into a Set for easy lookup
  const availableDateSet = new Set(availableDates.map(d => d.date));

  // Find time slots for selected date
  const selectedDateInfo = availableDates.find(d => d.date === selectedDate);
  const availableTimes = selectedDateInfo?.slots || [];

  // Convert string dates to Date objects for DayPicker
  const disabledDates = availableDates.length > 0 
    ? new Date().getFullYear() === 2026 
      ? { before: new Date(2026, 0, 1), after: new Date(2026, 1, 15) }
      : undefined
    : undefined;

  const handleDateSelect = (date: string) => {
    setSelectedDate(date);
  };

  const handleTimeSelect = (time: string) => {
    if (selectedDate) {
      onSelectDateTime(selectedDate, time);
    }
  };

  return (
    <div className="calendar-picker">
      <div className="calendar-container">
        <h3 className="calendar-title">Select a Date</h3>
        
        {/* Date List View (simpler than calendar) */}
        <div className="date-list">
          {availableDates.map((dateInfo) => (
            <button
              key={dateInfo.date}
              className={`date-button ${selectedDate === dateInfo.date ? 'selected' : ''}`}
              onClick={() => handleDateSelect(dateInfo.date)}
            >
              <div className="date-label">
                {new Date(dateInfo.date).toLocaleDateString('en-US', {
                  month: 'short',
                  day: 'numeric',
                  weekday: 'short',
                })}
              </div>
              <div className="slot-count">{dateInfo.slots.length} slots</div>
            </button>
          ))}
        </div>
      </div>

      {/* Time Slots */}
      {selectedDate && (
        <div className="time-container">
          <h3 className="time-title">Select a Time</h3>
          <div className="time-grid">
            {availableTimes.map((time) => (
              <button
                key={`${selectedDate}-${time}`}
                className="time-button"
                onClick={() => handleTimeSelect(time)}
              >
                {time}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Suggestion */}
      {suggestedDate && suggestedTime && selectedDate === suggestedDate && (
        <div className="suggestion-hint">
          💡 Suggested time: <strong>{suggestedTime}</strong>
        </div>
      )}
    </div>
  );
}
