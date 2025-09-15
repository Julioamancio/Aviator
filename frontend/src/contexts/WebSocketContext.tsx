import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import toast from 'react-hot-toast';

interface WebSocketMessage {
  type: string;
  data: any;
  timestamp?: string;
}

interface WebSocketContextType {
  socket: Socket | null;
  isConnected: boolean;
  sendMessage: (message: WebSocketMessage) => void;
  lastMessage: WebSocketMessage | null;
  connectionError: string | null;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

interface WebSocketProviderProps {
  children: React.ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [connectionError, setConnectionError] = useState<string | null>(null);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (socket && isConnected) {
      socket.emit('message', message);
    } else {
      console.warn('WebSocket não está conectado');
    }
  }, [socket, isConnected]);

  useEffect(() => {
    // Configurar conexão WebSocket
    const newSocket = io('ws://localhost:8000/ws', {
      transports: ['websocket'],
      upgrade: true,
      rememberUpgrade: true,
    });

    // Event listeners
    newSocket.on('connect', () => {
      console.log('WebSocket conectado');
      setIsConnected(true);
      setConnectionError(null);
      toast.success('Conectado ao servidor', {
        duration: 2000,
        position: 'bottom-right',
      });
    });

    newSocket.on('disconnect', (reason) => {
      console.log('WebSocket desconectado:', reason);
      setIsConnected(false);
      if (reason === 'io server disconnect') {
        // Reconectar se o servidor desconectou
        newSocket.connect();
      }
      toast.error('Conexão perdida', {
        duration: 3000,
        position: 'bottom-right',
      });
    });

    newSocket.on('connect_error', (error) => {
      console.error('Erro de conexão WebSocket:', error);
      setConnectionError(error.message);
      setIsConnected(false);
    });

    // Listener para mensagens gerais
    newSocket.on('message', (message: WebSocketMessage) => {
      console.log('Mensagem recebida:', message);
      setLastMessage(message);
      handleMessage(message);
    });

    // Listeners específicos para diferentes tipos de mensagem
    newSocket.on('status_update', (data) => {
      setLastMessage({ type: 'status_update', data });
    });

    newSocket.on('config_updated', (data) => {
      setLastMessage({ type: 'config_updated', data });
      toast.success('Configuração atualizada', {
        duration: 2000,
      });
    });

    newSocket.on('elements_updated', (data) => {
      setLastMessage({ type: 'elements_updated', data });
      toast.success('Elementos atualizados', {
        duration: 2000,
      });
    });

    newSocket.on('bot_started', (data) => {
      setLastMessage({ type: 'bot_started', data });
      toast.success('Bot iniciado com sucesso', {
        duration: 3000,
        icon: '🚀',
      });
    });

    newSocket.on('bot_stopped', (data) => {
      setLastMessage({ type: 'bot_stopped', data });
      toast.info('Bot parado', {
        duration: 2000,
        icon: '⏹️',
      });
    });

    newSocket.on('betting_started', (data) => {
      setLastMessage({ type: 'betting_started', data });
      toast.success('Apostas automáticas iniciadas', {
        duration: 3000,
        icon: '🎰',
      });
    });

    newSocket.on('betting_stopped', (data) => {
      setLastMessage({ type: 'betting_stopped', data });
      toast.info('Apostas automáticas paradas', {
        duration: 2000,
      });
    });

    newSocket.on('strategy_found', (data) => {
      setLastMessage({ type: 'strategy_found', data });
      toast.success('Estratégia encontrada!', {
        duration: 4000,
        icon: '🎯',
        style: {
          background: '#4caf50',
          color: 'white',
        },
      });
    });

    newSocket.on('bet_placed', (data) => {
      setLastMessage({ type: 'bet_placed', data });
      toast.info(`Aposta realizada: R$ ${data.amount}`, {
        duration: 3000,
        icon: '💰',
      });
    });

    newSocket.on('bet_won', (data) => {
      setLastMessage({ type: 'bet_won', data });
      toast.success(`Aposta ganha! +R$ ${data.profit}`, {
        duration: 4000,
        icon: '🎉',
        style: {
          background: '#4caf50',
          color: 'white',
        },
      });
    });

    newSocket.on('bet_lost', (data) => {
      setLastMessage({ type: 'bet_lost', data });
      toast.error(`Aposta perdida: -R$ ${data.amount}`, {
        duration: 3000,
        icon: '😞',
      });
    });

    newSocket.on('error', (data) => {
      setLastMessage({ type: 'error', data });
      toast.error(data.message || 'Erro no sistema', {
        duration: 5000,
        icon: '❌',
      });
    });

    newSocket.on('warning', (data) => {
      setLastMessage({ type: 'warning', data });
      toast.error(data.message || 'Aviso do sistema', {
        duration: 4000,
        icon: '⚠️',
      });
    });

    setSocket(newSocket);

    // Cleanup
    return () => {
      newSocket.close();
    };
  }, []);

  const handleMessage = (message: WebSocketMessage) => {
    // Processar mensagens específicas se necessário
    switch (message.type) {
      case 'heartbeat':
        // Responder ao heartbeat se necessário
        break;
      case 'notification':
        toast.info(message.data.message, {
          duration: 3000,
        });
        break;
      default:
        // Mensagem genérica
        break;
    }
  };

  const value: WebSocketContextType = {
    socket,
    isConnected,
    sendMessage,
    lastMessage,
    connectionError,
  };

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocket deve ser usado dentro de um WebSocketProvider');
  }
  return context;
};

export default WebSocketContext;