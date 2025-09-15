import React from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  useTheme,
  alpha,
} from '@mui/material';
import { motion } from 'framer-motion';
import { SmartToy as BotIcon } from '@mui/icons-material';

const LoadingScreen: React.FC = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: theme.palette.mode === 'dark'
          ? 'linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%)'
          : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background Animation */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.1,
          background: `
            radial-gradient(circle at 20% 80%, ${alpha(theme.palette.primary.main, 0.3)} 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, ${alpha(theme.palette.secondary.main, 0.3)} 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, ${alpha(theme.palette.info.main, 0.2)} 0%, transparent 50%)
          `,
        }}
      />

      {/* Main Content */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            zIndex: 1,
          }}
        >
          {/* Logo */}
          <motion.div
            animate={{
              rotate: [0, 360],
              scale: [1, 1.1, 1],
            }}
            transition={{
              rotate: {
                duration: 3,
                repeat: Infinity,
                ease: 'linear',
              },
              scale: {
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              },
            }}
          >
            <Box
              sx={{
                width: 80,
                height: 80,
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 3,
                boxShadow: `0 0 30px ${alpha(theme.palette.primary.main, 0.5)}`,
              }}
            >
              <BotIcon sx={{ fontSize: 40, color: 'white' }} />
            </Box>
          </motion.div>

          {/* Title */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <Typography
              variant="h4"
              sx={{
                fontWeight: 700,
                color: 'white',
                mb: 1,
                textShadow: '0 2px 10px rgba(0, 0, 0, 0.3)',
              }}
            >
              Aviator Bot
            </Typography>
          </motion.div>

          {/* Subtitle */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            <Typography
              variant="h6"
              sx={{
                fontWeight: 400,
                color: alpha('#ffffff', 0.8),
                mb: 4,
                textShadow: '0 1px 5px rgba(0, 0, 0, 0.2)',
              }}
            >
              Sistema Avançado de Automação
            </Typography>
          </motion.div>

          {/* Loading Indicator */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7, duration: 0.5 }}
          >
            <Box sx={{ position: 'relative', mb: 3 }}>
              <CircularProgress
                size={60}
                thickness={4}
                sx={{
                  color: 'white',
                  filter: `drop-shadow(0 0 10px ${alpha('#ffffff', 0.5)})`,
                }}
              />
              <Box
                sx={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  background: alpha('#ffffff', 0.1),
                  backdropFilter: 'blur(10px)',
                }}
              />
            </Box>
          </motion.div>

          {/* Loading Text */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.9, duration: 0.5 }}
          >
            <Typography
              variant="body1"
              sx={{
                color: alpha('#ffffff', 0.9),
                fontWeight: 500,
                letterSpacing: '0.5px',
              }}
            >
              Inicializando sistema...
            </Typography>
          </motion.div>

          {/* Loading Steps */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, duration: 0.5 }}
          >
            <Box sx={{ mt: 3, minHeight: 20 }}>
              <motion.div
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Typography
                  variant="caption"
                  sx={{
                    color: alpha('#ffffff', 0.7),
                    fontSize: '0.75rem',
                  }}
                >
                  Carregando componentes...
                </Typography>
              </motion.div>
            </Box>
          </motion.div>
        </Box>
      </motion.div>

      {/* Floating Particles */}
      {[...Array(6)].map((_, index) => (
        <motion.div
          key={index}
          initial={{
            opacity: 0,
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
          }}
          animate={{
            opacity: [0, 0.6, 0],
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
          }}
          transition={{
            duration: Math.random() * 10 + 10,
            repeat: Infinity,
            ease: 'linear',
          }}
          style={{
            position: 'absolute',
            width: Math.random() * 4 + 2,
            height: Math.random() * 4 + 2,
            borderRadius: '50%',
            background: 'white',
            pointerEvents: 'none',
          }}
        />
      ))}

      {/* Version Info */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 20,
          left: '50%',
          transform: 'translateX(-50%)',
          textAlign: 'center',
        }}
      >
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 0.5 }}
        >
          <Typography
            variant="caption"
            sx={{
              color: alpha('#ffffff', 0.6),
              fontSize: '0.7rem',
            }}
          >
            Versão 1.0.0 • Desenvolvido com ❤️
          </Typography>
        </motion.div>
      </Box>
    </Box>
  );
};

export default LoadingScreen;