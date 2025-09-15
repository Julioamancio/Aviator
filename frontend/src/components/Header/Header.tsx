import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  Chip,
  Tooltip,
  useTheme,
  alpha,
  Badge,
} from '@mui/material';
import {
  Menu as MenuIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useBotContext } from '../../contexts/BotContext';
import { useLocation } from 'react-router-dom';

interface HeaderProps {
  onToggleSidebar: () => void;
  onToggleDarkMode: () => void;
  darkMode: boolean;
  sidebarOpen: boolean;
}

const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  onToggleDarkMode,
  darkMode,
  sidebarOpen,
}) => {
  const theme = useTheme();
  const location = useLocation();
  const { botStatus, startBot, stopBot, sessionStats } = useBotContext();

  const getPageTitle = (pathname: string) => {
    switch (pathname) {
      case '/':
      case '/dashboard':
        return 'Dashboard';
      case '/configuration':
        return 'Configuração';
      case '/elements':
        return 'Elementos';
      case '/betting':
        return 'Apostas';
      case '/monitoring':
        return 'Monitoramento';
      case '/logs':
        return 'Logs';
      case '/settings':
        return 'Configurações';
      default:
        return 'Aviator Bot';
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

  const handleBotToggle = async () => {
    if (botStatus?.is_running) {
      await stopBot();
    } else {
      await startBot();
    }
  };

  const isRunning = botStatus?.is_running || false;
  const currentBalance = botStatus?.current_balance;
  const totalProfit = sessionStats?.total_profit || 0;

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        backgroundColor: alpha(theme.palette.background.paper, 0.8),
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        color: theme.palette.text.primary,
      }}
    >
      <Toolbar sx={{ px: { xs: 2, sm: 3 } }}>
        {/* Menu Button */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onToggleSidebar}
          sx={{
            mr: 2,
            transition: 'transform 0.2s ease',
            '&:hover': {
              transform: 'scale(1.1)',
            },
          }}
        >
          <MenuIcon />
        </IconButton>

        {/* Page Title */}
        <Box sx={{ flexGrow: 1 }}>
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Typography
              variant="h6"
              component="h1"
              sx={{
                fontWeight: 600,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              {getPageTitle(location.pathname)}
            </Typography>
          </motion.div>
        </Box>

        {/* Status and Controls */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {/* Balance Display */}
          {currentBalance !== null && currentBalance !== undefined && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              <Box sx={{ textAlign: 'right', display: { xs: 'none', sm: 'block' } }}>
                <Typography variant="caption" color="text.secondary">
                  Saldo
                </Typography>
                <Typography variant="body2" fontWeight={600}>
                  R$ {currentBalance.toFixed(2)}
                </Typography>
              </Box>
            </motion.div>
          )}

          {/* Profit Display */}
          {totalProfit !== 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.1 }}
            >
              <Box sx={{ textAlign: 'right', display: { xs: 'none', sm: 'block' } }}>
                <Typography variant="caption" color="text.secondary">
                  Lucro
                </Typography>
                <Typography
                  variant="body2"
                  fontWeight={600}
                  color={totalProfit >= 0 ? 'success.main' : 'error.main'}
                >
                  {totalProfit >= 0 ? '+' : ''}R$ {totalProfit.toFixed(2)}
                </Typography>
              </Box>
            </motion.div>
          )}

          {/* Bot Status */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Chip
              icon={
                <Box
                  sx={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    backgroundColor: getStatusColor(botStatus?.status || 'stopped'),
                    animation: isRunning ? 'pulse 2s infinite' : 'none',
                  }}
                />
              }
              label={botStatus?.status || 'stopped'}
              size="small"
              variant="outlined"
              sx={{
                borderColor: getStatusColor(botStatus?.status || 'stopped'),
                color: getStatusColor(botStatus?.status || 'stopped'),
                textTransform: 'capitalize',
                fontWeight: 500,
              }}
            />
          </motion.div>

          {/* Bot Control Button */}
          <Tooltip title={isRunning ? 'Parar Bot' : 'Iniciar Bot'}>
            <IconButton
              onClick={handleBotToggle}
              disabled={botStatus?.status === 'starting' || botStatus?.status === 'stopping'}
              sx={{
                backgroundColor: isRunning
                  ? alpha(theme.palette.error.main, 0.1)
                  : alpha(theme.palette.success.main, 0.1),
                color: isRunning ? theme.palette.error.main : theme.palette.success.main,
                border: `1px solid ${alpha(
                  isRunning ? theme.palette.error.main : theme.palette.success.main,
                  0.3
                )}`,
                '&:hover': {
                  backgroundColor: isRunning
                    ? alpha(theme.palette.error.main, 0.2)
                    : alpha(theme.palette.success.main, 0.2),
                  transform: 'scale(1.05)',
                },
                '&:disabled': {
                  opacity: 0.5,
                },
                transition: 'all 0.2s ease',
              }}
            >
              {botStatus?.status === 'starting' || botStatus?.status === 'stopping' ? (
                <RefreshIcon className="spin" />
              ) : isRunning ? (
                <StopIcon />
              ) : (
                <PlayIcon />
              )}
            </IconButton>
          </Tooltip>

          {/* Notifications */}
          <Tooltip title="Notificações">
            <IconButton color="inherit">
              <Badge badgeContent={0} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Tooltip>

          {/* Dark Mode Toggle */}
          <Tooltip title={darkMode ? 'Modo Claro' : 'Modo Escuro'}>
            <IconButton
              onClick={onToggleDarkMode}
              color="inherit"
              sx={{
                transition: 'transform 0.2s ease',
                '&:hover': {
                  transform: 'rotate(180deg)',
                },
              }}
            >
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Tooltip>

          {/* Settings */}
          <Tooltip title="Configurações">
            <IconButton color="inherit">
              <SettingsIcon />
            </IconButton>
          </Tooltip>

          {/* User Avatar */}
          <Avatar
            sx={{
              width: 32,
              height: 32,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              fontSize: '0.875rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'transform 0.2s ease',
              '&:hover': {
                transform: 'scale(1.1)',
              },
            }}
          >
            AB
          </Avatar>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;