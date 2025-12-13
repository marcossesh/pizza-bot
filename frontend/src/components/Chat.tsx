import React, { useState, useRef, useEffect } from 'react';
import { sendMessage } from '../services/api';
import './Chat.css';

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
}

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, text: 'Olá! Bem-vindo à Pizza Bot. Gostaria de ver o cardápio ou fazer um pedido?', sender: 'bot' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;

        const newUserMessage: Message = {
            id: Date.now(),
            text: inputValue,
            sender: 'user',
        };

        setMessages((prev) => [...prev, newUserMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const responseText = await sendMessage(newUserMessage.text);
            const newBotMessage: Message = {
                id: Date.now() + 1,
                text: responseText,
                sender: 'bot',
            };
            setMessages((prev) => [...prev, newBotMessage]);
        } catch (error) {
            const errorMessage: Message = {
                id: Date.now() + 1,
                text: 'Desculpe, ocorreu um erro ao processar sua mensagem.',
                sender: 'bot',
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>🍕 Pizza Bot</h1>
            </div>
            <div className="messages-container">
                {messages.map((msg) => (
                    <div key={msg.id} className={`message ${msg.sender}`}>
                        <div className="message-content">
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message bot">
                        <div className="message-content typing">
                            <span>.</span><span>.</span><span>.</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Digite sua mensagem..."
                    disabled={isLoading}
                />
                <button onClick={handleSendMessage} disabled={isLoading || !inputValue.trim()}>
                    Enviar
                </button>
            </div>
        </div>
    );
};

export default Chat;
