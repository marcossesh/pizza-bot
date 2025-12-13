import React, { useState, useRef, useEffect } from 'react';
import { sendMessage } from '../services/api';
import './Chat.css';

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
}

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>(() => {
        const saved = localStorage.getItem('chat_history');
        if (saved) {
            return JSON.parse(saved);
        }
        return [{ id: 1, text: 'Olá! Bem-vindo à Pizza Bot. Gostaria de ver o cardápio ou fazer um pedido?', sender: 'bot' }];
    });
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        localStorage.setItem('chat_history', JSON.stringify(messages));
        scrollToBottom();
    }, [messages, isLoading]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage: Message = {
            id: Date.now(),
            text: input,
            sender: 'user'
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await sendMessage(input);
            const botMessage: Message = {
                id: Date.now() + 1,
                text: response,
                sender: 'bot'
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage: Message = {
                id: Date.now() + 1,
                text: 'Desculpe, ocorreu um erro ao processar sua mensagem.',
                sender: 'bot'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>🍕 Pizza Bot</h1>
            </div>
            <div className="messages-container">
                {messages.map((msg) => (
                    <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
                        <div className="avatar">
                            {msg.sender === 'bot' ? '🤖' : '👤'}
                        </div>
                        <div className={`message ${msg.sender}`}>
                            <div className="message-content">
                                {msg.text}
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message-wrapper bot">
                        <div className="avatar">🤖</div>
                        <div className="message bot">
                            <div className="typing-indicator">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Digite sua mensagem..."
                    disabled={isLoading}
                />
                <button onClick={handleSend} disabled={isLoading}>
                    Enviar
                </button>
            </div>
        </div>
    );
};

export default Chat;
