import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '🦷 AI Dental Assistant',
  description: 'Chat with AI to book dental appointments',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
