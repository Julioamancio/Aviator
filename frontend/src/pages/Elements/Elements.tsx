import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  IconButton,
  Tooltip,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
  alpha,
  InputAdornment,
} from '@mui/material';
import {
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Code as CodeIcon,
  ExpandMore as ExpandMoreIcon,
  ContentCopy as CopyIcon,
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Help as HelpIcon,
  RestoreIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useBotContext } from '../../contexts/BotContext';

interface ElementFormData {
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

interface ElementInfo {
  name: string;
  label: string;
  description: string;
  example: string;
  type: 'xpath' | 'id' | 'class' | 'css';
  required: boolean;
  category: string;
}

const elementInfos: Record<string, ElementInfo> = {
  cookies_button: {
    name: 'cookies_button',
    label: 'Botão de Cookies',
    description: 'XPath do botão para aceitar cookies',
    example: '//*[@id="cookies-bottom-modal"]/div/div[1]/a',
    type: 'xpath',
    required: true,
    category: 'Navegação',
  },
  username_field: {
    name: 'username_field',
    label: 'Campo de Usuário',
    description: 'XPath do campo de entrada do nome de usuário',
    example: '//*[@id="username"]',
    type: 'xpath',
    required: true,
    category: 'Login',
  },
  password_field: {
    name: 'password_field',
    label: 'Campo de Senha',
    description: 'XPath do campo de entrada da senha',
    example: '//*[@id="password-login"]',
    type: 'xpath',
    required: true,
    category: 'Login',
  },
  login_button: {
    name: 'login_button',
    label: 'Botão de Login',
    description: 'XPath do botão para fazer login',
    example: '//*[@id="header"]/div/div[1]/div/div[2]/app-login/form/div/div/div[2]/button',
    type: 'xpath',
    required: true,
    category: 'Login',
  },
  game_iframe: {
    name: 'game_iframe',
    label: 'Frame do Jogo',
    description: 'ID do iframe que contém o jogo',
    example: 'gm-frm',
    type: 'id',
    required: true,
    category: 'Jogo',
  },
  result_history: {
    name: 'result_history',
    label: 'Histórico de Resultados',
    description: 'Classe do elemento que mostra o histórico',
    example: 'result-history',
    type: 'class',
    required: true,
    category: 'Jogo',
  },
  bet_input: {
    name: 'bet_input',
    label: 'Campo de Aposta',
    description: 'XPath do campo para inserir valor da aposta',
    example: '//*[@id="bet-amount"]',
    type: 'xpath',
    required: false,
    category: 'Apostas',
  },
  bet_button: {
    name: 'bet_button',
    label: 'Botão de Apostar',
    description: 'XPath do botão para realizar aposta',
    example: '//*[@class="bet-button"]',
    type: 'xpath',
    required: false,
    category: 'Apostas',
  },
  cashout_button: {
    name: 'cashout_button',
    label: 'Botão de Cashout',
    description: 'XPath do botão para fazer cashout',
    example: '//*[@class="cashout-button"]',
    type: 'xpath',
    required: false,
    category: 'Apostas',
  },
  multiplier_display: {
    name: 'multiplier_display',
    label: 'Display do Multiplicador',
    description: 'XPath do elemento que mostra o multiplicador atual',
    example: '//*[@class="multiplier"]',
    type: 'xpath',
    required: false,
    category: 'Informações',
  },
  balance_display: {
    name: 'balance_display',
    label: 'Display do Saldo',
    description: 'XPath do elemento que mostra o saldo',
    example: '//*[@class="balance"]',
    type: 'xpath',
    required: false,
    category: 'Informações',
  },
};

const Elements: React.FC = () => {
  const theme = useTheme();
  const { elementConfig, updateElementConfig, loading, refreshAll } = useBotContext();
  const [helpDialogOpen, setHelpDialogOpen] = useState(false);
  const [selectedElement, setSelectedElement] = useState<string | null>(null);
  const [expandedCategory, setExpandedCategory] = useState<string>('Navegação');

  const {
    control,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isDirty },
  } = useForm<ElementFormData>({
    defaultValues: {
      cookies_button: '',
      username_field: '',
      password_field: '',
      login_button: '',
      game_iframe: '',
      result_history: '',
      bet_input: '',
      bet_button: '',
      cashout_button: '',
      multiplier_display: '',
      balance_display: '',
    },
  });

  // Update form when config changes
  useEffect(() => {
    if (elementConfig) {
      reset({
        cookies_button: elementConfig.cookies_button,
        username_field: elementConfig.username_field,
        password_field: elementConfig.password_field,
        login_button: elementConfig.login_button,
        game_iframe: elementConfig.game_iframe,
        result_history: elementConfig.result_history,
        bet_input: elementConfig.bet_input,
        bet_button: elementConfig.bet_button,
        cashout_button: elementConfig.cashout_button,
        multiplier_display: elementConfig.multiplier_display,
        balance_display: elementConfig.balance_display,
      });
    }
  }, [elementConfig, reset]);

  const onSubmit = async (data: ElementFormData) => {
    try {
      await updateElementConfig(data);
      toast.success('Elementos salvos com sucesso!');
    } catch (error) {
      console.error('Erro ao salvar elementos:', error);
    }
  };

  const handleReset = () => {
    if (elementConfig) {
      reset({
        cookies_button: elementConfig.cookies_button,
        username_field: elementConfig.username_field,
        password_field: elementConfig.password_field,
        login_button: elementConfig.login_button,
        game_iframe: elementConfig.game_iframe,
        result_history: elementConfig.result_history,
        bet_input: elementConfig.bet_input,
        bet_button: elementConfig.bet_button,
        cashout_button: elementConfig.cashout_button,
        multiplier_display: elementConfig.multiplier_display,
        balance_display: elementConfig.balance_display,
      });
      toast.info('Elementos restaurados');
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copiado para a área de transferência!');
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'xpath':
        return '🎯';
      case 'id':
        return '🆔';
      case 'class':
        return '📝';
      case 'css':
        return '🎨';
      default:
        return '❓';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'xpath':
        return theme.palette.primary.main;
      case 'id':
        return theme.palette.success.main;
      case 'class':
        return theme.palette.info.main;
      case 'css':
        return theme.palette.secondary.main;
      default:
        return theme.palette.grey[500];
    }
  };

  const validateElement = (value: string, info: ElementInfo) => {
    if (info.required && !value) {
      return 'Este campo é obrigatório';
    }
    
    if (value && info.type === 'xpath' && !value.startsWith('/')) {
      return 'XPath deve começar com /';
    }
    
    return true;
  };

  const categories = Array.from(new Set(Object.values(elementInfos).map(info => info.category)));

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              Elementos da Página
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Configure os seletores XPath, IDs e classes dos elementos da página
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Tooltip title="Ajuda sobre elementos">
              <IconButton onClick={() => setHelpDialogOpen(true)}>
                <HelpIcon />
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Atualizar elementos">
              <IconButton onClick={refreshAll} disabled={loading}>
                <RefreshIcon className={loading ? 'spin' : ''} />
              </IconButton>
            </Tooltip>
            
            <Button
              variant="outlined"
              startIcon={<RestoreIcon />}
              onClick={handleReset}
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

      {/* Elements Form */}
      <form onSubmit={handleSubmit(onSubmit)}>
        {categories.map((category, categoryIndex) => {
          const categoryElements = Object.values(elementInfos).filter(
            info => info.category === category
          );
          
          return (
            <motion.div
              key={category}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: categoryIndex * 0.1 }}
            >
              <Accordion
                expanded={expandedCategory === category}
                onChange={() => setExpandedCategory(expandedCategory === category ? '' : category)}
                sx={{
                  mb: 2,
                  border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                  '&:before': { display: 'none' },
                }}
              >
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <CodeIcon color="primary" />
                    <Typography variant="h6" fontWeight={600}>
                      {category}
                    </Typography>
                    <Chip
                      label={`${categoryElements.length} elementos`}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                </AccordionSummary>
                
                <AccordionDetails>
                  <Grid container spacing={3}>
                    {categoryElements.map((info) => {
                      const fieldValue = watch(info.name as keyof ElementFormData);
                      const hasValue = Boolean(fieldValue);
                      
                      return (
                        <Grid item xs={12} key={info.name}>
                          <Card
                            sx={{
                              border: `1px solid ${alpha(
                                hasValue ? theme.palette.success.main : theme.palette.grey[300],
                                0.3
                              )}`,
                              background: hasValue
                                ? alpha(theme.palette.success.main, 0.02)
                                : 'transparent',
                            }}
                          >
                            <CardContent sx={{ p: 3 }}>
                              <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 2 }}>
                                <Box sx={{ flex: 1 }}>
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                    <Typography variant="h6" fontWeight={600}>
                                      {info.label}
                                    </Typography>
                                    <Chip
                                      label={`${getTypeIcon(info.type)} ${info.type.toUpperCase()}`}
                                      size="small"
                                      sx={{
                                        backgroundColor: alpha(getTypeColor(info.type), 0.1),
                                        color: getTypeColor(info.type),
                                        border: `1px solid ${alpha(getTypeColor(info.type), 0.3)}`,
                                      }}
                                    />
                                    {info.required && (
                                      <Chip
                                        label="Obrigatório"
                                        size="small"
                                        color="error"
                                        variant="outlined"
                                      />
                                    )}
                                    {hasValue && (
                                      <CheckIcon sx={{ color: theme.palette.success.main, fontSize: 20 }} />
                                    )}
                                  </Box>
                                  <Typography variant="body2" color="text.secondary" gutterBottom>
                                    {info.description}
                                  </Typography>
                                </Box>
                              </Box>
                              
                              <Controller
                                name={info.name as keyof ElementFormData}
                                control={control}
                                rules={{
                                  validate: (value) => validateElement(value, info),
                                }}
                                render={({ field }) => (
                                  <TextField
                                    {...field}
                                    fullWidth
                                    label={`${info.type.toUpperCase()} do ${info.label}`}
                                    placeholder={info.example}
                                    error={!!errors[info.name as keyof ElementFormData]}
                                    helperText={
                                      errors[info.name as keyof ElementFormData]?.message ||
                                      `Exemplo: ${info.example}`
                                    }
                                    InputProps={{
                                      startAdornment: (
                                        <InputAdornment position="start">
                                          <SearchIcon color="action" />
                                        </InputAdornment>
                                      ),
                                      endAdornment: (
                                        <InputAdornment position="end">
                                          <Tooltip title="Copiar exemplo">
                                            <IconButton
                                              size="small"
                                              onClick={() => copyToClipboard(info.example)}
                                            >
                                              <CopyIcon fontSize="small" />
                                            </IconButton>
                                          </Tooltip>
                                        </InputAdornment>
                                      ),
                                    }}
                                    sx={{
                                      '& .MuiOutlinedInput-root': {
                                        '&.Mui-focused fieldset': {
                                          borderColor: getTypeColor(info.type),
                                        },
                                      },
                                    }}
                                  />
                                )}
                              />
                            </CardContent>
                          </Card>
                        </Grid>
                      );
                    })}
                  </Grid>
                </AccordionDetails>
              </Accordion>
            </motion.div>
          );
        })}
      </form>

      {/* Help Dialog */}
      <Dialog
        open={helpDialogOpen}
        onClose={() => setHelpDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <HelpIcon color="primary" />
            Ajuda - Configuração de Elementos
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="h6" gutterBottom>
            Tipos de Seletores
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6}>
              <Card sx={{ p: 2, border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}` }}>
                <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                  🎯 XPath
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Caminho completo para o elemento. Exemplo: //*[@id="username"]
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Card sx={{ p: 2, border: `1px solid ${alpha(theme.palette.success.main, 0.2)}` }}>
                <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                  🆔 ID
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Identificador único do elemento. Exemplo: username
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Card sx={{ p: 2, border: `1px solid ${alpha(theme.palette.info.main, 0.2)}` }}>
                <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                  📝 Class
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Nome da classe CSS. Exemplo: login-button
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Card sx={{ p: 2, border: `1px solid ${alpha(theme.palette.secondary.main, 0.2)}` }}>
                <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                  🎨 CSS
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Seletor CSS completo. Exemplo: .login-form input[type="text"]
                </Typography>
              </Card>
            </Grid>
          </Grid>
          
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              <strong>Dica:</strong> Use as ferramentas de desenvolvedor do navegador (F12) para
              encontrar os seletores corretos. Clique com o botão direito no elemento e
              selecione "Inspecionar" para ver o código HTML.
            </Typography>
          </Alert>
          
          <Alert severity="warning">
            <Typography variant="body2">
              <strong>Importante:</strong> Elementos marcados como "Obrigatório" são essenciais
              para o funcionamento básico do bot. Certifique-se de configurá-los corretamente.
            </Typography>
          </Alert>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setHelpDialogOpen(false)} variant="contained">
            Entendi
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Elements;