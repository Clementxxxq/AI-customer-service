# 🦷 AI Dental Assistant Frontend

A modern Next.js chat interface for the AI Dental Assistant backend.

## Features

- **Message List**: Display conversation history
- **Input Box**: Send messages to the AI assistant
- **Session Management**: Maintains conversation_id throughout the session
- **Real-time Updates**: Auto-scroll to latest messages
- **Responsive Design**: Works on desktop and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations

## Setup

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Running the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
npm run start
```

## Components

### DentalChat
Main component that manages the chat state and API communication.

**Features:**
- Maintains unique `conversation_id` for each session
- Handles message sending and receiving
- Error handling with user-friendly messages
- Auto-scroll to latest message

### MessageList
Displays all messages in the conversation.

**Features:**
- Shows user and AI messages with different styling
- Auto-scroll to bottom on new messages
- Responsive layout

### InputBox
Input field and send button for user messages.

**Features:**
- Send on Enter key (Shift+Enter for new line)
- Disabled state during loading
- Send button with loading indicator

## API Integration

The frontend connects to the backend API:

```
POST http://127.0.0.1:8000/api/chat/message
```

**Request:**
```json
{
  "content": "user message",
  "user_id": 1,
  "conversation_id": "chat_1234567890"
}
```

**Response:**
```json
{
  "message_id": "msg_1234567890",
  "user_message": "user message",
  "bot_response": "AI response",
  "timestamp": "2026-01-06T10:00:00",
  "conversation_id": "chat_1234567890",
  "intent": "appointment",
  "confidence": 0.95,
  "entities": {...},
  "action_result": null
}
```

## Styling

The application uses CSS modules and inline styles with:
- Gradient backgrounds (purple/blue)
- Smooth animations and transitions
- Modern chat UI design
- Mobile-responsive layout

## Files Structure

```
frontend/
├── app/
│   ├── page.tsx           # Main page
│   ├── globals.css        # Global styles
├── components/
│   ├── DentalChat.tsx     # Main chat component
│   ├── DentalChat.css
│   ├── MessageList.tsx    # Message display
│   ├── MessageList.css
│   ├── InputBox.tsx       # Input field
│   ├── InputBox.css
├── package.json
├── tsconfig.json
└── next.config.js
```

## Notes

- Make sure the backend is running on `http://127.0.0.1:8000`
- The `conversation_id` is generated per session and remains unchanged
- The application requires the `/api/chat/message` endpoint to be available
