import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Avatar,
  Chip,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  Code as CodeIcon,
  Casino as CasinoIcon,
  Visibility as VisibilityIcon,
  Description as LogsIcon,
  TuneIcon,
  SmartToy as BotIcon,
  Timeline as TimelineIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useBotContext } from '../../contexts/BotContext';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  width: number;
  isMobile: boolean;
}

interface MenuItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  path: string;
  badge?: string;
  color?: string;
}

const menuItems: MenuItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: <DashboardIcon />,
    path: '/dashboard',
    color: '#667eea',
  },
  {
    id: 'configuration',
    label: 'Configuração',
    icon: <SettingsIcon />,
    path: '/configuration',
    color: '#764ba2',
  },
  {
    id: 'elements',
    label: 'Elementos',
    icon: <CodeIcon />,
    path: '/elements',
    color: '#f093fb',
  },
  {
    id: 'betting',
    label: 'Apostas',
    icon: <CasinoIcon />,
    path: '/betting',
    color: '#4facfe',
    badge: 'Auto',
  },
  {
    id: 'monitoring',
    label: 'Monitoramento',
    icon: <VisibilityIcon />,
    path: '/monitoring',
    color: '#43e97b',
  },
  {
    id: 'logs',
    label: 'Logs',
    icon: <LogsIcon />,
    path: '/logs',
    color: '#fa709a',
  },
  {
    id: 'settings',
    label: 'Configurações',
    icon: <TuneIcon />,
    path: '/settings',
    color: '#ffeaa7',
  },
];

const Sidebar: React.FC<SidebarProps> = ({ open, onClose, width, isMobile }) => {
  const theme = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const { botStatus, sessionStats } = useBotContext();

  const handleItemClick = (path: string) => {
    navigate(path);
    if (isMobile) {
      onClose();
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

  const drawerContent = (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        background: theme.palette.mode === 'dark'
          ? 'linear-gradient(180deg, #1a1d3a 0%, #0a0e27 100%)'
          : 'linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 3,
          borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar
            sx={
              {
                width: 48,
                height: 48,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                mr: 2,
              }
            }
          >
            <BotIcon sx={{ fontSize: 28 }} />
          </Avatar>
          <Box>
            <Typography
              variant="h6"
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Aviator Bot
            </Typography>
            <Typography variant="caption" color="text.secondary">
              v1.0.0
            </Typography>
          </Box>
        </Box>

        {/* Status */}
        <Box
          sx={{
            p: 2,
            borderRadius: 2,
            background: alpha(getStatusColor(botStatus?.status || 'stopped'), 0.1),
            border: `1px solid ${alpha(getStatusColor(botStatus?.status || 'stopped'), 0.2)}`,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Box
              sx={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                backgroundColor: getStatusColor(botStatus?.status || 'stopped'),
                mr: 1,
                animation: botStatus?.is_running ? 'pulse 2s infinite' : 'none',
              }}
            />
            <Typography variant="body2" fontWeight={500}>
              {getStatusText(botStatus?.status || 'stopped')}
            </Typography>
          </Box>
          
          {sessionStats && (
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Chip
                label={`${sessionStats.total_rounds} rodadas`}
                size="small"
                variant="outlined"
                sx={{ fontSize: '0.7rem', height: 20 }}
              />
              {sessionStats.strategies_found > 0 && (
                <Chip
                  label={`${sessionStats.strategies_found} estratégias`}
                  size="small"
                  color="success"
                  variant="outlined"
                  sx={{ fontSize: '0.7rem', height: 20 }}
                />
              )}
            </Box>
          )}
        </Box>
      </Box>

      {/* Navigation */}
      <Box sx={{ flexGrow: 1, py: 1 }}>
        <List sx={{ px: 2 }}>
          <AnimatePresence>
            {menuItems.map((item, index) => {
              const isActive = location.pathname === item.path || 
                (location.pathname === '/' && item.path === '/dashboard');
              
              return (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <ListItem disablePadding sx={{ mb: 0.5 }}>
                    <ListItemButton
                      onClick={() => handleItemClick(item.path)}
                      sx={{
                        borderRadius: 2,
                        py: 1.5,
                        px: 2,
                        transition: 'all 0.2s ease',
                        background: isActive
                          ? alpha(item.color || theme.palette.primary.main, 0.15)
                          : 'transparent',
                        border: isActive
                          ? `1px solid ${alpha(item.color || theme.palette.primary.main, 0.3)}`
                          : '1px solid transparent',
                        '&:hover': {
                          background: alpha(item.color || theme.palette.primary.main, 0.1),
                          transform: 'translateX(4px)',
                        },
                      }}
                    >
                      <ListItemIcon
                        sx={{
                          minWidth: 40,
                          color: isActive
                            ? item.color || theme.palette.primary.main
                            : theme.palette.text.secondary,
                          transition: 'color 0.2s ease',
                        }}
                      >
                        {item.icon}
                      </ListItemIcon>
                      <ListItemText
                        primary={item.label}
                        sx={{
                          '& .MuiListItemText-primary': {
                            fontWeight: isActive ? 600 : 400,
                            color: isActive
                              ? item.color || theme.palette.primary.main
                              : theme.palette.text.primary,
                            fontSize: '0.875rem',
                          },
                        }}
                      />
                      {item.badge && (
                        <Chip
                          label={item.badge}
                          size="small"
                          sx={{
                            height: 20,
                            fontSize: '0.7rem',
                            background: alpha(item.color || theme.palette.primary.main, 0.2),
                            color: item.color || theme.palette.primary.main,
                            border: `1px solid ${alpha(item.color || theme.palette.primary.main, 0.3)}`,
                          }}
                        />
                      )}
                    </ListItemButton>
                  </ListItem>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </List>
      </Box>

      {/* Footer */}
      <Box
        sx={{
          p: 2,
          borderTop: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        }}
      >
        <Box
          sx={{
            p: 2,
            borderRadius: 2,
            background: alpha(theme.palette.info.main, 0.1),
            border: `1px solid ${alpha(theme.palette.info.main, 0.2)}`,
            textAlign: 'center',
          }}
        >
          <SecurityIcon
            sx={{
              fontSize: 20,
              color: theme.palette.info.main,
              mb: 1,
            }}
          />
          <Typography variant="caption" display="block" color="text.secondary">
            Sistema Seguro
          </Typography>
          <Typography variant="caption" display="block" color="info.main" fontWeight={500}>
            Criptografia Ativa
          </Typography>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Drawer
      variant={isMobile ? 'temporary' : 'persistent'}
      anchor="left"
      open={open}
      onClose={onClose}
      sx={{
        width: open ? width : 0,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: width,
          boxSizing: 'border-box',
          border: 'none',
          boxShadow: theme.palette.mode === 'dark'
            ? '4px 0 20px rgba(0, 0, 0, 0.3)'
            : '4px 0 20px rgba(0, 0, 0, 0.1)',
        },
      }}
      ModalProps={{
        keepMounted: true, // Better open performance on mobile
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;