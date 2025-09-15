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
  Divider,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  Visibility as VisibilityIcon,
  RestoreIcon,
  InfoIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useBotContext } from '../../contexts/BotContext';

interface ConfigFormData {
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

interface CredentialsFormData {
  username: string;
  password: string;
}

const Configuration: React.FC = () => {
  const theme = useTheme();
  const { botConfig, updateBotConfig, setCredentials, loading, refreshAll } = useBotContext();
  const [credentialsOpen, setCredentialsOpen] = useState(false);
  const [resetDialogOpen, setResetDialogOpen] = useState(false);

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isDirty },
  } = useForm<ConfigFormData>({
    defaultValues: {
      site_url: '',
      game_url: '',
      headless: false,
      wait_timeout: 30,
      strategy_threshold: 2.0,
      history_size: 10,
      min_strategy_checks: 4,
      update_interval: 2,
      max_retries: 3,
    },
  });

  const {
    control: credentialsControl,
    handleSubmit: handleCredentialsSubmit,
    reset: resetCredentials,
    formState: { errors: credentialsErrors },
  } = useForm<CredentialsFormData>({
    defaultValues: {
      username: '',
      password: '',
    },
  });

  // Update form when config changes
  useEffect(() => {
    if (botConfig) {
      reset({
        site_url: botConfig.site_url,
        game_url: botConfig.game_url,
        headless: botConfig.headless,
        wait_timeout: botConfig.wait_timeout,
        strategy_threshold: botConfig.strategy_threshold,
        history_size: botConfig.history_size,
        min_strategy_checks: botConfig.min_strategy_checks,
        update_interval: botConfig.update_interval,
        max_retries: botConfig.max_retries,
      });
    }
  }, [botConfig, reset]);

  const onSubmit = async (data: ConfigFormData) => {
    try {
      await updateBotConfig(data);
      toast.success('Configuração salva com sucesso!');
    } catch (error) {
      console.error('Erro ao salvar configuração:', error);
    }
  };

  const onCredentialsSubmit = async (data: CredentialsFormData) => {
    try {
      await setCredentials(data.username, data.password);
      setCredentialsOpen(false);
      resetCredentials();
      toast.success('Credenciais definidas com sucesso!');
    } catch (error) {
      console.error('Erro ao definir credenciais:', error);
    }
  };

  const handleReset = () => {
    if (botConfig) {
      reset({
        site_url: botConfig.site_url,
        game_url: botConfig.game_url,
        headless: botConfig.headless,
        wait_timeout: botConfig.wait_timeout,
        strategy_threshold: botConfig.strategy_threshold,
        history_size: botConfig.history_size,
        min_strategy_checks: botConfig.min_strategy_checks,
        update_interval: botConfig.update_interval,
        max_retries: botConfig.max_retries,
      });
      toast.info('Configurações restauradas');
    }
    setResetDialogOpen(false);
  };

  const configSections = [
    {
      title: 'URLs do Sistema',
      icon: <SettingsIcon />,
      color: theme.palette.primary.main,
      fields: ['site_url', 'game_url'],
    },
    {
      title: 'Configurações de Execução',
      icon: <SpeedIcon />,
      color: theme.palette.secondary.main,
      fields: ['headless', 'wait_timeout', 'update_interval', 'max_retries'],
    },
    {
      title: 'Estratégia e Análise',
      icon: <VisibilityIcon />,
      color: theme.palette.info.main,
      fields: ['strategy_threshold', 'history_size', 'min_strategy_checks'],
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              Configuração
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Configure os parâmetros do bot para otimizar o desempenho
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Tooltip title="Atualizar configurações">
              <IconButton onClick={refreshAll} disabled={loading}>
                <RefreshIcon className={loading ? 'spin' : ''} />
              </IconButton>
            </Tooltip>
            
            <Button
              variant="outlined"
              startIcon={<SecurityIcon />}
              onClick={() => setCredentialsOpen(true)}
            >
              Credenciais
            </Button>
            
            <Button
              variant="outlined"
              startIcon={<RestoreIcon />}
              onClick={() => setResetDialogOpen(true)}
              disabled={!isDirty}
            >
              Restaurar
            </Button>
            
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={handleSubmit(onSubmit)}
              disabled={loading || !isDirty}
            >
              Salvar
            </Button>
          </Box>
        </Box>
        
        {isDirty && (
          <Alert severity="warning" sx={{ mb: 2 }}>
            Você tem alterações não salvas. Clique em "Salvar" para aplicar as mudanças.
          </Alert>
        )}
      </Box>

      {/* Configuration Form */}
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={3}>
          {configSections.map((section, sectionIndex) => (
            <Grid item xs={12} key={section.title}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: sectionIndex * 0.1 }}
              >
                <Card
                  sx={{
                    border: `1px solid ${alpha(section.color, 0.2)}`,
                    background: alpha(section.color, 0.02),
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                      <Box
                        sx={{
                          p: 1,
                          borderRadius: 2,
                          backgroundColor: alpha(section.color, 0.1),
                          color: section.color,
                          mr: 2,
                        }}
                      >
                        {section.icon}
                      </Box>
                      <Typography variant="h6" fontWeight={600}>
                        {section.title}
                      </Typography>
                    </Box>
                    
                    <Grid container spacing={3}>
                      {section.fields.map((fieldName) => {
                        switch (fieldName) {
                          case 'site_url':
                            return (
                              <Grid item xs={12} key={fieldName}>
                                <Controller
                                  name="site_url"
                                  control={control}
                                  rules={{ required: 'URL do site é obrigatória' }}
                                  render={({ field }) => (
                                    <TextField
                                      {...field}
                                      fullWidth
                                      label="URL do Site"
                                      placeholder="https://estrelabet.com/ptb/bet/main"
                                      error={!!errors.site_url}
                                      helperText={errors.site_url?.message || 'URL principal do site de apostas'}
                                    />
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'game_url':
                            return (
                              <Grid item xs={12} key={fieldName}>
                                <Controller
                                  name="game_url"
                                  control={control}
                                  rules={{ required: 'URL do jogo é obrigatória' }}
                                  render={({ field }) => (
                                    <TextField
                                      {...field}
                                      fullWidth
                                      label="URL do Jogo"
                                      placeholder="https://estrelabet.com/ptb/games/detail/casino/normal/7787"
                                      error={!!errors.game_url}
                                      helperText={errors.game_url?.message || 'URL específica do jogo Aviator'}
                                    />
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'headless':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="headless"
                                  control={control}
                                  render={({ field }) => (
                                    <Box>
                                      <FormControlLabel
                                        control={
                                          <Switch
                                            checked={field.value}
                                            onChange={field.onChange}
                                            color="primary"
                                          />
                                        }
                                        label="Modo Headless"
                                      />
                                      <Typography variant="caption" display="block" color="text.secondary">
                                        Executar sem interface gráfica (mais rápido)
                                      </Typography>
                                    </Box>
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'wait_timeout':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="wait_timeout"
                                  control={control}
                                  rules={{ min: 5, max: 120 }}
                                  render={({ field }) => (
                                    <Box>
                                      <Typography gutterBottom>
                                        Timeout de Espera: {field.value}s
                                      </Typography>
                                      <Slider
                                        {...field}
                                        min={5}
                                        max={120}
                                        step={5}
                                        marks={[
                                          { value: 5, label: '5s' },
                                          { value: 30, label: '30s' },
                                          { value: 60, label: '60s' },
                                          { value: 120, label: '120s' },
                                        ]}
                                        valueLabelDisplay="auto"
                                      />
                                      <Typography variant="caption" color="text.secondary">
                                        Tempo máximo para aguardar elementos
                                      </Typography>
                                    </Box>
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'update_interval':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="update_interval"
                                  control={control}
                                  rules={{ min: 1, max: 10 }}
                                  render={({ field }) => (
                                    <Box>
                                      <Typography gutterBottom>
                                        Intervalo de Atualização: {field.value}s
                                      </Typography>
                                      <Slider
                                        {...field}
                                        min={1}
                                        max={10}
                                        step={1}
                                        marks={[
                                          { value: 1, label: '1s' },
                                          { value: 5, label: '5s' },
                                          { value: 10, label: '10s' },
                                        ]}
                                        valueLabelDisplay="auto"
                                      />
                                      <Typography variant="caption" color="text.secondary">
                                        Frequência de verificação do jogo
                                      </Typography>
                                    </Box>
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'max_retries':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="max_retries"
                                  control={control}
                                  rules={{ min: 1, max: 10 }}
                                  render={({ field }) => (
                                    <TextField
                                      {...field}
                                      fullWidth
                                      type="number"
                                      label="Máximo de Tentativas"
                                      inputProps={{ min: 1, max: 10 }}
                                      helperText="Número máximo de tentativas em caso de erro"
                                    />
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'strategy_threshold':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="strategy_threshold"
                                  control={control}
                                  rules={{ min: 1.0, max: 10.0 }}
                                  render={({ field }) => (
                                    <Box>
                                      <Typography gutterBottom>
                                        Limite da Estratégia: {field.value}x
                                      </Typography>
                                      <Slider
                                        {...field}
                                        min={1.0}
                                        max={10.0}
                                        step={0.1}
                                        marks={[
                                          { value: 1.0, label: '1.0x' },
                                          { value: 2.0, label: '2.0x' },
                                          { value: 5.0, label: '5.0x' },
                                          { value: 10.0, label: '10.0x' },
                                        ]}
                                        valueLabelDisplay="auto"
                                      />
                                      <Typography variant="caption" color="text.secondary">
                                        Multiplicador máximo para ativar estratégia
                                      </Typography>
                                    </Box>
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'history_size':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="history_size"
                                  control={control}
                                  rules={{ min: 5, max: 50 }}
                                  render={({ field }) => (
                                    <TextField
                                      {...field}
                                      fullWidth
                                      type="number"
                                      label="Tamanho do Histórico"
                                      inputProps={{ min: 5, max: 50 }}
                                      helperText="Número de resultados a manter no histórico"
                                    />
                                  )}
                                />
                              </Grid>
                            );
                          
                          case 'min_strategy_checks':
                            return (
                              <Grid item xs={12} sm={6} key={fieldName}>
                                <Controller
                                  name="min_strategy_checks"
                                  control={control}
                                  rules={{ min: 2, max: 10 }}
                                  render={({ field }) => (
                                    <TextField
                                      {...field}
                                      fullWidth
                                      type="number"
                                      label="Verificações Mínimas"
                                      inputProps={{ min: 2, max: 10 }}
                                      helperText="Número mínimo de resultados para ativar estratégia"
                                    />
                                  )}
                                />
                              </Grid>
                            );
                          
                          default:
                            return null;
                        }
                      })}
                    </Grid>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </form>

      {/* Credentials Dialog */}
      <Dialog
        open={credentialsOpen}
        onClose={() => setCredentialsOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SecurityIcon color="primary" />
            Configurar Credenciais
          </Box>
        </DialogTitle>
        <form onSubmit={handleCredentialsSubmit(onCredentialsSubmit)}>
          <DialogContent>
            <Alert severity="info" sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <InfoIcon fontSize="small" />
                As credenciais são armazenadas de forma segura e criptografada.
              </Box>
            </Alert>
            
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Controller
                  name="username"
                  control={credentialsControl}
                  rules={{ required: 'Nome de usuário é obrigatório' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label="Nome de Usuário"
                      error={!!credentialsErrors.username}
                      helperText={credentialsErrors.username?.message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={12}>
                <Controller
                  name="password"
                  control={credentialsControl}
                  rules={{ required: 'Senha é obrigatória' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      type="password"
                      label="Senha"
                      error={!!credentialsErrors.password}
                      helperText={credentialsErrors.password?.message}
                    />
                  )}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setCredentialsOpen(false)}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained" disabled={loading}>
              Salvar Credenciais
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Reset Dialog */}
      <Dialog
        open={resetDialogOpen}
        onClose={() => setResetDialogOpen(false)}
        maxWidth="sm"
      >
        <DialogTitle>Restaurar Configurações</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja restaurar todas as configurações para os valores salvos?
            Todas as alterações não salvas serão perdidas.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResetDialogOpen(false)}>
            Cancelar
          </Button>
          <Button onClick={handleReset} color="warning" variant="contained">
            Restaurar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Configuration;