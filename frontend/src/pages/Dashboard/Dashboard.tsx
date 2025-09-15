import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  IconButton,
  Tooltip,
  useTheme,
  alpha,
  Paper,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Casino as CasinoIcon,
  Visibility as VisibilityIcon,
  Timeline as TimelineIcon,
  Speed as SpeedIcon,
  AccountBalance as BalanceIcon,
  EmojiEvents as TrophyIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { useBotContext } from '../../contexts/BotContext';
import { useWebSocket } from '../../contexts/WebSocketContext';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  color: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  loading?: boolean;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  color,
  trend,
  trendValue,
  loading = false,
}) => {
  const theme = useTheme();

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon sx={{ fontSize: 16, color: theme.palette.success.main }} />;
      case 'down':
        return <TrendingDownIcon sx={{ fontSize: 16, color: theme.palette.error.main }} />;
      default:
        return null;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return theme.palette.success.main;
      case 'down':
        return theme.palette.error.main;
      default:
        return theme.palette.text.secondary;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        sx={{
          height: '100%',
          background: theme.palette.mode === 'dark'
            ? `linear-gradient(135deg, ${alpha(color, 0.1)} 0%, ${alpha(color, 0.05)} 100%)`
            : `linear-gradient(135deg, ${alpha(color, 0.05)} 0%, ${alpha(color, 0.02)} 100%)`,
          border: `1px solid ${alpha(color, 0.2)}`,
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: `0 8px 25px ${alpha(color, 0.2)}`,
          },
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {title}
              </Typography>
              {loading ? (
                <Box sx={{ width: 80, height: 32, mb: 1 }}>
                  <LinearProgress sx={{ height: 8, borderRadius: 4 }} />
                </Box>
              ) : (
                <Typography variant="h4" fontWeight={700} color={color}>
                  {value}
                </Typography>
              )}
              {subtitle && (
                <Typography variant="caption" color="text.secondary">
                  {subtitle}
                </Typography>
              )}
            </Box>
            <Avatar
              sx={{
                backgroundColor: alpha(color, 0.1),
                color: color,
                width: 48,
                height: 48,
              }}
            >
              {icon}
            </Avatar>
          </Box>
          
          {trendValue && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              {getTrendIcon()}
              <Typography variant="caption" color={getTrendColor()} fontWeight={500}>
                {trendValue}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const { botStatus, sessionStats, startBot, stopBot, loading, refreshAll } = useBotContext();
  const { isConnected } = useWebSocket();
  const [chartData, setChartData] = useState<any[]>([]);

  // Generate mock chart data for demonstration
  useEffect(() => {
    const generateChartData = () => {
      const data = [];
      const now = new Date();
      for (let i = 29; i >= 0; i--) {
        const time = new Date(now.getTime() - i * 60000); // 1 minute intervals
        data.push({
          time: time.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
          multiplier: Math.random() * 10 + 1,
          profit: (Math.random() - 0.5) * 100,
        });
      }
      return data;
    };

    setChartData(generateChartData());
    
    // Update chart data periodically
    const interval = setInterval(() => {
      setChartData(generateChartData());
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const handleBotToggle = async () => {
    try {
      if (botStatus?.is_running) {
        await stopBot();
      } else {
        await startBot();
      }
    } catch (error) {
      console.error('Erro ao alternar bot:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
      case 'monitoring':
      case 'betting':
        return theme.palette.success.main;
      case 'stopped':
        return theme.palette.error.main;
      case 'starting':
      case 'stopping':
        return theme.palette.warning.main;
      case 'error':
        return theme.palette.error.main;
      default:
        return theme.palette.grey[500];
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'running':
        return 'Executando';
      case 'stopped':
        return 'Parado';
      case 'starting':
        return 'Iniciando';
      case 'stopping':
        return 'Parando';
      case 'monitoring':
        return 'Monitorando';
      case 'betting':
        return 'Apostando';
      case 'error':
        return 'Erro';
      default:
        return 'Desconhecido';
    }
  };

  const isRunning = botStatus?.is_running || false;
  const currentBalance = botStatus?.current_balance || 0;
  const totalProfit = sessionStats?.total_profit || 0;
  const winRate = sessionStats?.bets_placed ? (sessionStats.wins / sessionStats.bets_placed) * 100 : 0;
  const uptime = sessionStats?.uptime || '00:00:00';

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header Section */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Controle e monitoramento do Aviator Bot
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            {/* Connection Status */}
            <Chip
              icon={
                <Box
                  sx={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    backgroundColor: isConnected ? theme.palette.success.main : theme.palette.error.main,
                    animation: isConnected ? 'pulse 2s infinite' : 'none',
                  }}
                />
              }
              label={isConnected ? 'Conectado' : 'Desconectado'}
              size="small"
              variant="outlined"
              sx={{
                borderColor: isConnected ? theme.palette.success.main : theme.palette.error.main,
                color: isConnected ? theme.palette.success.main : theme.palette.error.main,
              }}
            />
            
            {/* Refresh Button */}
            <Tooltip title="Atualizar dados">
              <IconButton onClick={refreshAll} disabled={loading}>
                <RefreshIcon className={loading ? 'spin' : ''} />
              </IconButton>
            </Tooltip>
            
            {/* Bot Control Button */}
            <Button
              variant="contained"
              size="large"
              startIcon={isRunning ? <StopIcon /> : <PlayIcon />}
              onClick={handleBotToggle}
              disabled={loading || botStatus?.status === 'starting' || botStatus?.status === 'stopping'}
              sx={{
                backgroundColor: isRunning ? theme.palette.error.main : theme.palette.success.main,
                '&:hover': {
                  backgroundColor: isRunning ? theme.palette.error.dark : theme.palette.success.dark,
                },
                minWidth: 120,
              }}
            >
              {isRunning ? 'Parar Bot' : 'Iniciar Bot'}
            </Button>
          </Box>
        </Box>
        
        {/* Status Bar */}
        <Paper
          sx={{
            p: 2,
            background: alpha(getStatusColor(botStatus?.status || 'stopped'), 0.1),
            border: `1px solid ${alpha(getStatusColor(botStatus?.status || 'stopped'), 0.2)}`,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Box
                sx={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  backgroundColor: getStatusColor(botStatus?.status || 'stopped'),
                  animation: isRunning ? 'pulse 2s infinite' : 'none',
                }}
              />
              <Typography variant="h6" fontWeight={600}>
                Status: {getStatusText(botStatus?.status || 'stopped')}
              </Typography>
              {botStatus?.error_message && (
                <Chip
                  icon={<WarningIcon />}
                  label="Erro"
                  size="small"
                  color="error"
                  variant="outlined"
                />
              )}
            </Box>
            
            <Typography variant="body2" color="text.secondary">
              Tempo ativo: {uptime}
            </Typography>
          </Box>
        </Paper>
      </Box>

      {/* Stats Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Saldo Atual"
            value={`R$ ${currentBalance.toFixed(2)}`}
            subtitle="Saldo da conta"
            icon={<BalanceIcon />}
            color={theme.palette.primary.main}
            loading={loading}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Lucro Total"
            value={`R$ ${totalProfit.toFixed(2)}`}
            subtitle="Lucro da sessão"
            icon={totalProfit >= 0 ? <TrendingUpIcon /> : <TrendingDownIcon />}
            color={totalProfit >= 0 ? theme.palette.success.main : theme.palette.error.main}
            trend={totalProfit >= 0 ? 'up' : 'down'}
            trendValue={`${totalProfit >= 0 ? '+' : ''}${totalProfit.toFixed(2)}`}
            loading={loading}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Taxa de Vitória"
            value={`${winRate.toFixed(1)}%`}
            subtitle={`${sessionStats?.wins || 0}/${sessionStats?.bets_placed || 0} apostas`}
            icon={<TrophyIcon />}
            color={theme.palette.info.main}
            trend={winRate >= 50 ? 'up' : winRate > 0 ? 'down' : 'neutral'}
            trendValue={`${sessionStats?.wins || 0} vitórias`}
            loading={loading}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Estratégias"
            value={sessionStats?.strategies_found || 0}
            subtitle={`${sessionStats?.total_rounds || 0} rodadas`}
            icon={<SpeedIcon />}
            color={theme.palette.secondary.main}
            trend={sessionStats?.strategies_found ? 'up' : 'neutral'}
            trendValue={`${sessionStats?.total_rounds || 0} monitoradas`}
            loading={loading}
          />
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} lg={8}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Histórico de Multiplicadores
              </Typography>
              <Box sx={{ height: 320, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke={alpha(theme.palette.divider, 0.3)} />
                    <XAxis 
                      dataKey="time" 
                      stroke={theme.palette.text.secondary}
                      fontSize={12}
                    />
                    <YAxis 
                      stroke={theme.palette.text.secondary}
                      fontSize={12}
                    />
                    <RechartsTooltip 
                      contentStyle={{
                        backgroundColor: theme.palette.background.paper,
                        border: `1px solid ${theme.palette.divider}`,
                        borderRadius: 8,
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="multiplier"
                      stroke={theme.palette.primary.main}
                      fill={alpha(theme.palette.primary.main, 0.2)}
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resultados Recentes
              </Typography>
              <Box sx={{ mt: 2 }}>
                <AnimatePresence>
                  {botStatus?.recent_results?.slice(0, 8).map((result, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Box
                        sx={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          p: 1.5,
                          mb: 1,
                          borderRadius: 1,
                          backgroundColor: result >= 2 
                            ? alpha(theme.palette.success.main, 0.1)
                            : alpha(theme.palette.error.main, 0.1),
                          border: `1px solid ${alpha(
                            result >= 2 ? theme.palette.success.main : theme.palette.error.main,
                            0.2
                          )}`,
                        }}
                      >
                        <Typography variant="body2" color="text.secondary">
                          Rodada #{index + 1}
                        </Typography>
                        <Chip
                          label={`${result.toFixed(2)}x`}
                          size="small"
                          sx={{
                            backgroundColor: result >= 2 
                              ? theme.palette.success.main 
                              : theme.palette.error.main,
                            color: 'white',
                            fontWeight: 600,
                          }}
                        />
                      </Box>
                    </motion.div>
                  )) || (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="body2" color="text.secondary">
                        Nenhum resultado disponível
                      </Typography>
                    </Box>
                  )}
                </AnimatePresence>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Ações Rápidas
          </Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<CasinoIcon />}
                sx={{ py: 1.5 }}
              >
                Configurar Apostas
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<VisibilityIcon />}
                sx={{ py: 1.5 }}
              >
                Ver Monitoramento
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<TimelineIcon />}
                sx={{ py: 1.5 }}
              >
                Análise Detalhada
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={refreshAll}
                disabled={loading}
                sx={{ py: 1.5 }}
              >
                Atualizar Tudo
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;