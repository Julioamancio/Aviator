import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useWebSocket } from './WebSocketContext';

// Types
interface BotConfig {
  site_url: string;
  game_url: string;
  headless: boolean;
  wait_timeout: number;
  strategy_threshold: number;
  history_size: number;
  min_strategy_checks: number;
  update_interval: number;
  max_retries: number;
}

interface ElementConfig {
  cookies_button: string;
  username_field: string;
  password_field: string;
  login_button: string;
  game_iframe: string;
  result_history: string;
  bet_input: string;
  bet_button: string;
  cashout_button: string;
  multiplier_display: string;
  balance_display: string;
}

interface BotStatus {
  status: string;
  is_running: boolean;
  is_betting: boolean;
  current_balance?: number;
  last_multiplier?: number;
  last_update: string;
  error_message?: string;
  current_strategy?: any;
  recent_results: number[];
}

interface SessionStats {
  start_time: string;
  total_rounds: number;
  strategies_found: number;
  bets_placed: number;
  wins: number;
  losses: number;
  total_bet: number;
  total_profit: number;
  current_balance?: number;
  max_multiplier: number;
  avg_multiplier: number;
  errors: number;
  uptime?: string;
}

interface BettingStrategy {
  amount: number;
  strategy_type: string;
  auto_cashout?: number;
  max_loss?: number;
  max_win?: number;
  stop_on_loss: boolean;
  stop_on_win: boolean;
  progressive_betting: boolean;
  progression_factor: number;
  reset_on_win: boolean;
}

interface BotContextType {
  // State
  botConfig: BotConfig | null;
  elementConfig: ElementConfig | null;
  botStatus: BotStatus | null;
  sessionStats: SessionStats | null;
  bettingStrategy: BettingStrategy | null;
  loading: boolean;
  error: string | null;

  // Actions
  fetchBotConfig: () => Promise<void>;
  updateBotConfig: (config: Partial<BotConfig>) => Promise<void>;
  fetchElementConfig: () => Promise<void>;
  updateElementConfig: (elements: Partial<ElementConfig>) => Promise<void>;
  setCredentials: (username: string, password: string) => Promise<void>;
  startBot: () => Promise<void>;
  stopBot: () => Promise<void>;
  startBetting: (strategy: BettingStrategy) => Promise<void>;
  stopBetting: () => Promise<void>;
  fetchBotStatus: () => Promise<void>;
  fetchSessionStats: () => Promise<void>;
  refreshAll: () => Promise<void>;
}

const BotContext = createContext<BotContextType | undefined>(undefined);

// API Configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    const message = error.response?.data?.detail || error.message || 'Erro na API';
    toast.error(message, { duration: 4000 });
    return Promise.reject(error);
  }
);

interface BotProviderProps {
  children: React.ReactNode;
}

export const BotProvider: React.FC<BotProviderProps> = ({ children }) => {
  // State
  const [botConfig, setBotConfig] = useState<BotConfig | null>(null);
  const [elementConfig, setElementConfig] = useState<ElementConfig | null>(null);
  const [botStatus, setBotStatus] = useState<BotStatus | null>(null);
  const [sessionStats, setSessionStats] = useState<SessionStats | null>(null);
  const [bettingStrategy, setBettingStrategy] = useState<BettingStrategy | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { lastMessage, isConnected } = useWebSocket();

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      switch (lastMessage.type) {
        case 'status_update':
          if (lastMessage.data.status) {
            setBotStatus(lastMessage.data.status);
          }
          if (lastMessage.data.stats) {
            setSessionStats(lastMessage.data.stats);
          }
          break;
        case 'config_updated':
          setBotConfig(lastMessage.data);
          break;
        case 'elements_updated':
          setElementConfig(lastMessage.data);
          break;
        case 'betting_started':
          setBettingStrategy(lastMessage.data);
          break;
        case 'betting_stopped':
          setBettingStrategy(null);
          break;
        case 'error':
          setError(lastMessage.data.message);
          break;
      }
    }
  }, [lastMessage]);

  // API Functions
  const fetchBotConfig = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get('/config');
      setBotConfig(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateBotConfig = useCallback(async (config: Partial<BotConfig>) => {
    try {
      setLoading(true);
      const response = await api.put('/config', config);
      setBotConfig(response.data.config);
      toast.success('Configuração atualizada com sucesso');
      setError(null);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchElementConfig = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get('/elements');
      setElementConfig(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateElementConfig = useCallback(async (elements: Partial<ElementConfig>) => {
    try {
      setLoading(true);
      const response = await api.put('/elements', elements);
      setElementConfig(response.data.elements);
      toast.success('Elementos atualizados com sucesso');
      setError(null);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const setCredentials = useCallback(async (username: string, password: string) => {
    try {
      setLoading(true);
      await api.post('/credentials', { username, password });
      toast.success('Credenciais definidas com sucesso');
      setError(null);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const startBot = useCallback(async () => {
    try {
      setLoading(true);
      await api.post('/bot/start');
      toast.success('Bot iniciado com sucesso', { icon: '🚀' });
      setError(null);
      // Atualizar status após um delay
      setTimeout(fetchBotStatus, 1000);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const stopBot = useCallback(async () => {
    try {
      setLoading(true);
      await api.post('/bot/stop');
      toast.success('Bot parado com sucesso', { icon: '⏹️' });
      setError(null);
      // Atualizar status após um delay
      setTimeout(fetchBotStatus, 1000);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const startBetting = useCallback(async (strategy: BettingStrategy) => {
    try {
      setLoading(true);
      const response = await api.post('/betting/start', strategy);
      setBettingStrategy(response.data.strategy);
      toast.success('Apostas automáticas iniciadas', { icon: '🎰' });
      setError(null);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const stopBetting = useCallback(async () => {
    try {
      setLoading(true);
      await api.post('/betting/stop');
      setBettingStrategy(null);
      toast.success('Apostas automáticas paradas');
      setError(null);
    } catch (err: any) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchBotStatus = useCallback(async () => {
    try {
      const response = await api.get('/bot/status');
      setBotStatus(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  const fetchSessionStats = useCallback(async () => {
    try {
      const response = await api.get('/bot/stats');
      setSessionStats(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  const refreshAll = useCallback(async () => {
    try {
      setLoading(true);
      await Promise.all([
        fetchBotConfig(),
        fetchElementConfig(),
        fetchBotStatus(),
        fetchSessionStats(),
      ]);
      toast.success('Dados atualizados');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [fetchBotConfig, fetchElementConfig, fetchBotStatus, fetchSessionStats]);

  // Initial data fetch
  useEffect(() => {
    refreshAll();
  }, []);

  // Periodic status updates when connected
  useEffect(() => {
    if (isConnected && botStatus?.is_running) {
      const interval = setInterval(() => {
        fetchBotStatus();
        fetchSessionStats();
      }, 5000); // Update every 5 seconds

      return () => clearInterval(interval);
    }
  }, [isConnected, botStatus?.is_running, fetchBotStatus, fetchSessionStats]);

  const value: BotContextType = {
    // State
    botConfig,
    elementConfig,
    botStatus,
    sessionStats,
    bettingStrategy,
    loading,
    error,

    // Actions
    fetchBotConfig,
    updateBotConfig,
    fetchElementConfig,
    updateElementConfig,
    setCredentials,
    startBot,
    stopBot,
    startBetting,
    stopBetting,
    fetchBotStatus,
    fetchSessionStats,
    refreshAll,
  };

  return (
    <BotContext.Provider value={value}>
      {children}
    </BotContext.Provider>
  );
};

export const useBotContext = (): BotContextType => {
  const context = useContext(BotContext);
  if (context === undefined) {
    throw new Error('useBotContext deve ser usado dentro de um BotProvider');
  }
  return context;
};

export default BotContext;