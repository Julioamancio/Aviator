import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Switch,
  FormControlLabel,
  Slider,
  Alert,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  InputAdornment,
  useTheme,
  alpha,
  LinearProgress,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Casino as CasinoIcon,
  Security as SecurityIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  AttachMoney as MoneyIcon,
  Speed as SpeedIcon,
  Shield as ShieldIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { useBotContext } from '../../contexts/BotContext';

interface BettingFormData {
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

interface StrategyPreset {
  name: string;
  description: string;
  config: Partial<BettingFormData>;
  color: string;
  risk: 'low' | 'medium' | 'high';
}

const strategyPresets: StrategyPreset[] = [
  {
    name: 'Conservadora',
    description: 'Apostas baixas com cashout automático em 2x',
    config: {
      strategy_type: 'conservative',
      auto_cashout: 2.0,
      progressive_betting: false,
      stop_on_loss: true,
      stop_on_win: true,
    },
    color: '#4caf50',
    risk: 'low',
  },
  {
    name: 'Moderada',
    description: 'Equilíbrio entre risco e retorno',
    config: {
      strategy_type: 'moderate',
      auto_cashout: 3.0,
      progressive_betting: true,
      progression_factor: 1.5,
      stop_on_loss: true,
      stop_on_win: false,
    },
    color: '#ff9800',
    risk: 'medium',
  },
  {
    name: 'Agressiva',
    description: 'Alto risco, alto retorno',
    config: {
      strategy_type: 'aggressive',
      auto_cashout: 5.0,
      progressive_betting: true,
      progression_factor: 2.0,
      stop_on_loss: false,
      stop_on_win: false,
    },
    color: '#f44336',
    risk: 'high',
  },
];

const Betting: React.FC = () => {
  const theme = useTheme();
  const { bettingStrategy, startBetting, stopBetting, botStatus, sessionStats, loading } = useBotContext();
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [selectedPreset, setSelectedPreset] = useState<StrategyPreset | null>(null);
  const [pendingFormData, setPendingFormData] = useState<BettingFormData | null>(null);

  const {
    control,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isDirty },
  } = useForm<BettingFormData>({
    defaultValues: {
      amount: 1.0,
      strategy_type: 'conservative',
      auto_cashout: 2.0,
      max_loss: 50.0,
      max_win: 100.0,
      stop_on_loss: true,
      stop_on_win: true,
      progressive_betting: false,
      progression_factor: 1.5,
      reset_on_win: true,
    },
  });

  const watchedValues = watch();
  const isBettingActive = bettingStrategy !== null;
  const canStartBetting = botStatus?.is_running && !isBettingActive;

  // Update form when betting strategy changes
  useEffect(() => {
    if (bettingStrategy) {
      reset({
        amount: bettingStrategy.amount,
        strategy_type: bettingStrategy.strategy_type,
        auto_cashout: bettingStrategy.auto_cashout,
        max_loss: bettingStrategy.max_loss,
        max_win: bettingStrategy.max_win,
        stop_on_loss: bettingStrategy.stop_on_loss,
        stop_on_win: bettingStrategy.stop_on_win,
        progressive_betting: bettingStrategy.progressive_betting,
        progression_factor: bettingStrategy.progression_factor,
        reset_on_win: bettingStrategy.reset_on_win,
      });
    }
  }, [bettingStrategy, reset]);

  const onSubmit = async (data: BettingFormData) => {
    setPendingFormData(data);
    setConfirmDialogOpen(true);
  };

  const confirmStartBetting = async () => {
    if (pendingFormData) {
      try {
        await startBetting(pendingFormData as any);
        setConfirmDialogOpen(false);
        setPendingFormData(null);
        toast.success('Apostas automáticas iniciadas!', { icon: '🎰' });
      } catch (error) {
        console.error('Erro ao iniciar apostas:', error);
      }
    }
  };

  const handleStopBetting = async () => {
    try {
      await stopBetting();
      toast.success('Apostas automáticas paradas');
    } catch (error) {
      console.error('Erro ao parar apostas:', error);
    }
  };

  const applyPreset = (preset: StrategyPreset) => {
    Object.entries(preset.config).forEach(([key, value]) => {
      setValue(key as keyof BettingFormData, value as any);
    });
    setSelectedPreset(preset);
    toast.success(`Preset "${preset.name}" aplicado`);
  };

  const calculatePotentialProfit = () => {
    const amount = watchedValues.amount || 0;
    const cashout = watchedValues.auto_cashout || 2;
    return (amount * cashout) - amount;
  };

  const calculateRiskLevel = () => {
    const cashout = watchedValues.auto_cashout || 2;
    const progressive = watchedValues.progressive_betting;
    const factor = watchedValues.progression_factor || 1;
    
    let risk = 0;
    if (cashout > 5) risk += 3;
    else if (cashout > 3) risk += 2;
    else risk += 1;
    
    if (progressive) risk += factor > 2 ? 2 : 1;
    
    if (risk <= 2) return { level: 'Baixo', color: theme.palette.success.main };
    if (risk <= 4) return { level: 'Médio', color: theme.palette.warning.main };
    return { level: 'Alto', color: theme.palette.error.main };
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return theme.palette.success.main;
      case 'medium': return theme.palette.warning.main;
      case 'high': return theme.palette.error.main;
      default: return theme.palette.grey[500];
    }
  };

  const riskLevel = calculateRiskLevel();
  const potentialProfit = calculatePotentialProfit();

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              Apostas Automáticas
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Configure estratégias de aposta com controles de segurança avançados
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            {/* Status */}
            <Chip
              icon={
                <Box
                  sx={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    backgroundColor: isBettingActive ? theme.palette.success.main : theme.palette.error.main,
                    animation: isBettingActive ? 'pulse 2s infinite' : 'none',
                  }}
                />
              }
              label={isBettingActive ? 'Ativo' : 'Inativo'}
              color={isBettingActive ? 'success' : 'default'}
              variant="outlined"
            />
            
            {/* Control Button */}
            {isBettingActive ? (
              <Button
                variant="contained"
                color="error"
                startIcon={<StopIcon />}
                onClick={handleStopBetting}
                disabled={loading}
              >
                Parar Apostas
              </Button>
            ) : (
              <Button
                variant="contained"
                color="success"
                startIcon={<PlayIcon />}
                onClick={handleSubmit(onSubmit)}
                disabled={!canStartBetting || loading}
              >
                Iniciar Apostas
              </Button>
            )}
          </Box>
        </Box>
        
        {/* Status Alerts */}
        {!botStatus?.is_running && (
          <Alert severity="warning" sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <WarningIcon fontSize="small" />
              O bot deve estar em execução para iniciar apostas automáticas.
            </Box>
          </Alert>
        )}
        
        {isBettingActive && (
          <Alert severity="success" sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CasinoIcon fontSize="small" />
              Apostas automáticas ativas com estratégia {bettingStrategy?.strategy_type}
            </Box>
          </Alert>
        )}
      </Box>

      <Grid container spacing={3}>
        {/* Strategy Presets */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Estratégias Pré-definidas
              </Typography>
              <Grid container spacing={2}>
                {strategyPresets.map((preset, index) => (
                  <Grid item xs={12} sm={4} key={preset.name}>
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card
                        sx={{
                          cursor: 'pointer',
                          border: selectedPreset?.name === preset.name
                            ? `2px solid ${preset.color}`
                            : `1px solid ${alpha(preset.color, 0.3)}`,
                          background: alpha(preset.color, 0.05),
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            transform: 'translateY(-2px)',
                            boxShadow: `0 4px 20px ${alpha(preset.color, 0.2)}`,
                          },
                        }}
                        onClick={() => applyPreset(preset)}
                      >
                        <CardContent>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                            <Typography variant="h6" fontWeight={600}>
                              {preset.name}
                            </Typography>
                            <Chip
                              label={preset.risk}
                              size="small"
                              sx={{
                                backgroundColor: alpha(getRiskColor(preset.risk), 0.1),
                                color: getRiskColor(preset.risk),
                                border: `1px solid ${alpha(getRiskColor(preset.risk), 0.3)}`,
                              }}
                            />
                          </Box>
                          <Typography variant="body2" color="text.secondary">
                            {preset.description}
                          </Typography>
                        </CardContent>
                      </Card>
                    </motion.div>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Configuration Form */}
        <Grid item xs={12} lg={8}>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configuração da Estratégia
                </Typography>
                
                <Grid container spacing={3}>
                  {/* Basic Settings */}
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="amount"
                      control={control}
                      rules={{ required: 'Valor é obrigatório', min: 0.1 }}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          type="number"
                          label="Valor da Aposta"
                          inputProps={{ min: 0.1, step: 0.1 }}
                          InputProps={{
                            startAdornment: <InputAdornment position="start">R$</InputAdornment>,
                          }}
                          error={!!errors.amount}
                          helperText={errors.amount?.message || 'Valor base para cada aposta'}
                        />
                      )}
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="strategy_type"
                      control={control}
                      render={({ field }) => (
                        <FormControl fullWidth>
                          <InputLabel>Tipo de Estratégia</InputLabel>
                          <Select {...field} label="Tipo de Estratégia">
                            <MenuItem value="conservative">Conservadora</MenuItem>
                            <MenuItem value="moderate">Moderada</MenuItem>
                            <MenuItem value="aggressive">Agressiva</MenuItem>
                            <MenuItem value="custom">Personalizada</MenuItem>
                          </Select>
                        </FormControl>
                      )}
                    />
                  </Grid>
                  
                  {/* Auto Cashout */}
                  <Grid item xs={12}>
                    <Controller
                      name="auto_cashout"
                      control={control}
                      render={({ field }) => (
                        <Box>
                          <Typography gutterBottom>
                            Cashout Automático: {field.value?.toFixed(1)}x
                          </Typography>
                          <Slider
                            {...field}
                            min={1.1}
                            max={10.0}
                            step={0.1}
                            marks={[
                              { value: 1.1, label: '1.1x' },
                              { value: 2.0, label: '2.0x' },
                              { value: 5.0, label: '5.0x' },
                              { value: 10.0, label: '10.0x' },
                            ]}
                            valueLabelDisplay="auto"
                          />
                          <Typography variant="caption" color="text.secondary">
                            Multiplicador para cashout automático
                          </Typography>
                        </Box>
                      )}
                    />
                  </Grid>
                  
                  {/* Safety Limits */}
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="max_loss"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          type="number"
                          label="Perda Máxima"
                          inputProps={{ min: 0, step: 1 }}
                          InputProps={{
                            startAdornment: <InputAdornment position="start">R$</InputAdornment>,
                          }}
                          helperText="Parar apostas ao atingir esta perda"
                        />
                      )}
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="max_win"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          type="number"
                          label="Ganho Máximo"
                          inputProps={{ min: 0, step: 1 }}
                          InputProps={{
                            startAdornment: <InputAdornment position="start">R$</InputAdornment>,
                          }}
                          helperText="Parar apostas ao atingir este ganho"
                        />
                      )}
                    />
                  </Grid>
                  
                  {/* Progressive Betting */}
                  <Grid item xs={12}>
                    <Controller
                      name="progressive_betting"
                      control={control}
                      render={({ field }) => (
                        <FormControlLabel
                          control={
                            <Switch
                              checked={field.value}
                              onChange={field.onChange}
                              color="primary"
                            />
                          }
                          label="Aposta Progressiva"
                        />
                      )}
                    />
                    <Typography variant="caption" display="block" color="text.secondary">
                      Aumentar valor da aposta após perdas consecutivas
                    </Typography>
                  </Grid>
                  
                  {watchedValues.progressive_betting && (
                    <Grid item xs={12}>
                      <Controller
                        name="progression_factor"
                        control={control}
                        render={({ field }) => (
                          <Box>
                            <Typography gutterBottom>
                              Fator de Progressão: {field.value?.toFixed(1)}x
                            </Typography>
                            <Slider
                              {...field}
                              min={1.1}
                              max={3.0}
                              step={0.1}
                              marks={[
                                { value: 1.1, label: '1.1x' },
                                { value: 1.5, label: '1.5x' },
                                { value: 2.0, label: '2.0x' },
                                { value: 3.0, label: '3.0x' },
                              ]}
                              valueLabelDisplay="auto"
                            />
                            <Typography variant="caption" color="text.secondary">
                              Multiplicador para aumentar aposta após perda
                            </Typography>
                          </Box>
                        )}
                      />
                    </Grid>
                  )}
                  
                  {/* Stop Conditions */}
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="stop_on_loss"
                      control={control}
                      render={({ field }) => (
                        <FormControlLabel
                          control={
                            <Switch
                              checked={field.value}
                              onChange={field.onChange}
                              color="error"
                            />
                          }
                          label="Parar ao Atingir Perda Máxima"
                        />
                      )}
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="stop_on_win"
                      control={control}
                      render={({ field }) => (
                        <FormControlLabel
                          control={
                            <Switch
                              checked={field.value}
                              onChange={field.onChange}
                              color="success"
                            />
                          }
                          label="Parar ao Atingir Ganho Máximo"
                        />
                      )}
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </form>
        </Grid>

        {/* Risk Analysis */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: 'fit-content' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Análise de Risco
              </Typography>
              
              {/* Risk Level */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="body2">Nível de Risco</Typography>
                  <Chip
                    label={riskLevel.level}
                    size="small"
                    sx={{
                      backgroundColor: alpha(riskLevel.color, 0.1),
                      color: riskLevel.color,
                      border: `1px solid ${alpha(riskLevel.color, 0.3)}`,
                    }}
                  />
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={riskLevel.level === 'Baixo' ? 33 : riskLevel.level === 'Médio' ? 66 : 100}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: alpha(riskLevel.color, 0.2),
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: riskLevel.color,
                    },
                  }}
                />
              </Box>
              
              {/* Potential Profit */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Lucro Potencial por Aposta
                </Typography>
                <Typography variant="h5" color="success.main" fontWeight={600}>
                  +R$ {potentialProfit.toFixed(2)}
                </Typography>
              </Box>
              
              {/* Current Session */}
              {sessionStats && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Sessão Atual
                  </Typography>
                  <Grid container spacing={1}>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Apostas
                      </Typography>
                      <Typography variant="body2" fontWeight={600}>
                        {sessionStats.bets_placed}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Taxa de Vitória
                      </Typography>
                      <Typography variant="body2" fontWeight={600}>
                        {sessionStats.bets_placed > 0 
                          ? ((sessionStats.wins / sessionStats.bets_placed) * 100).toFixed(1)
                          : 0}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Lucro Total
                      </Typography>
                      <Typography 
                        variant="body2" 
                        fontWeight={600}
                        color={sessionStats.total_profit >= 0 ? 'success.main' : 'error.main'}
                      >
                        {sessionStats.total_profit >= 0 ? '+' : ''}R$ {sessionStats.total_profit.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Saldo
                      </Typography>
                      <Typography variant="body2" fontWeight={600}>
                        R$ {(sessionStats.current_balance || 0).toFixed(2)}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              )}
              
              {/* Safety Features */}
              <Alert severity="info" icon={<ShieldIcon />}>
                <Typography variant="body2">
                  <strong>Recursos de Segurança:</strong>
                  <br />• Limites de perda e ganho
                  <br />• Parada automática
                  <br />• Monitoramento em tempo real
                </Typography>
              </Alert>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Confirmation Dialog */}
      <Dialog
        open={confirmDialogOpen}
        onClose={() => setConfirmDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SecurityIcon color="warning" />
            Confirmar Início das Apostas
          </Box>
        </DialogTitle>
        <DialogContent>
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Typography variant="body2">
              <strong>Atenção:</strong> Você está prestes a iniciar apostas automáticas.
              Certifique-se de que todas as configurações estão corretas.
            </Typography>
          </Alert>
          
          {pendingFormData && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Resumo da Configuração:
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Valor da Aposta:
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    R$ {pendingFormData.amount.toFixed(2)}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Cashout Automático:
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    {pendingFormData.auto_cashout?.toFixed(1)}x
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Perda Máxima:
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    R$ {pendingFormData.max_loss?.toFixed(2) || 'Sem limite'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Ganho Máximo:
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    R$ {pendingFormData.max_win?.toFixed(2) || 'Sem limite'}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDialogOpen(false)}>
            Cancelar
          </Button>
          <Button 
            onClick={confirmStartBetting} 
            variant="contained" 
            color="success"
            disabled={loading}
          >
            Confirmar e Iniciar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Betting;