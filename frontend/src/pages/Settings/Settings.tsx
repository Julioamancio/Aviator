import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Button,
  Grid,
  Divider,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  useTheme,
  alpha,
} from '@mui/material';
import {
  DarkMode as DarkModeIcon,
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Backup as BackupIcon,
  RestoreIcon,
  Delete as DeleteIcon,
  Info as InfoIcon,
  Update as UpdateIcon,
  BugReport as BugReportIcon,
  Help as HelpIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

interface SettingsSection {
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
}

const Settings: React.FC = () => {
  const theme = useTheme();
  const [settings, setSettings] = useState({
    darkMode: true,
    notifications: true,
    soundAlerts: false,
    autoStart: false,
    saveHistory: true,
    debugMode: false,
    autoUpdate: true,
    telemetry: false,
  });
  
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const [backupDialogOpen, setBackupDialogOpen] = useState(false);

  const handleSettingChange = (setting: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setSettings(prev => ({
      ...prev,
      [setting]: event.target.checked,
    }));
    
    toast.success(`${setting} ${event.target.checked ? 'ativado' : 'desativado'}`);
  };

  const handleExportSettings = () => {
    const settingsData = {
      settings,
      exportDate: new Date().toISOString(),
      version: '1.0.0',
    };
    
    const blob = new Blob([JSON.stringify(settingsData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `aviator-bot-settings-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast.success('Configurações exportadas com sucesso!');
  };

  const handleImportSettings = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            const data = JSON.parse(e.target?.result as string);
            if (data.settings) {
              setSettings(data.settings);
              toast.success('Configurações importadas com sucesso!');
            } else {
              toast.error('Arquivo de configuração inválido');
            }
          } catch (error) {
            toast.error('Erro ao importar configurações');
          }
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  const handleResetSettings = () => {
    setSettings({
      darkMode: true,
      notifications: true,
      soundAlerts: false,
      autoStart: false,
      saveHistory: true,
      debugMode: false,
      autoUpdate: true,
      telemetry: false,
    });
    setResetDialogOpen(false);
    toast.success('Configurações restauradas para o padrão');
  };

  const settingsSections: SettingsSection[] = [
    {
      title: 'Aparência',
      description: 'Personalize a interface do usuário',
      icon: <DarkModeIcon />,
      color: theme.palette.primary.main,
    },
    {
      title: 'Notificações',
      description: 'Configure alertas e notificações',
      icon: <NotificationsIcon />,
      color: theme.palette.secondary.main,
    },
    {
      title: 'Sistema',
      description: 'Configurações avançadas do sistema',
      icon: <SecurityIcon />,
      color: theme.palette.info.main,
    },
    {
      title: 'Dados',
      description: 'Backup e restauração de dados',
      icon: <BackupIcon />,
      color: theme.palette.success.main,
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Configurações
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Personalize o comportamento e aparência do Aviator Bot
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Appearance Settings */}
        <Grid item xs={12} lg={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card
              sx={{
                border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                background: alpha(theme.palette.primary.main, 0.02),
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 2,
                      backgroundColor: alpha(theme.palette.primary.main, 0.1),
                      color: theme.palette.primary.main,
                      mr: 2,
                    }}
                  >
                    <DarkModeIcon />
                  </Box>
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      Aparência
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Personalize a interface do usuário
                    </Typography>
                  </Box>
                </Box>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <DarkModeIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Modo Escuro"
                      secondary="Usar tema escuro na interface"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.darkMode}
                        onChange={handleSettingChange('darkMode')}
                        color="primary"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Notification Settings */}
        <Grid item xs={12} lg={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card
              sx={{
                border: `1px solid ${alpha(theme.palette.secondary.main, 0.2)}`,
                background: alpha(theme.palette.secondary.main, 0.02),
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 2,
                      backgroundColor: alpha(theme.palette.secondary.main, 0.1),
                      color: theme.palette.secondary.main,
                      mr: 2,
                    }}
                  >
                    <NotificationsIcon />
                  </Box>
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      Notificações
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Configure alertas e notificações
                    </Typography>
                  </Box>
                </Box>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <NotificationsIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Notificações Push"
                      secondary="Receber notificações do sistema"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.notifications}
                        onChange={handleSettingChange('notifications')}
                        color="secondary"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <NotificationsIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Alertas Sonoros"
                      secondary="Reproduzir sons para eventos importantes"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.soundAlerts}
                        onChange={handleSettingChange('soundAlerts')}
                        color="secondary"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* System Settings */}
        <Grid item xs={12} lg={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Card
              sx={{
                border: `1px solid ${alpha(theme.palette.info.main, 0.2)}`,
                background: alpha(theme.palette.info.main, 0.02),
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 2,
                      backgroundColor: alpha(theme.palette.info.main, 0.1),
                      color: theme.palette.info.main,
                      mr: 2,
                    }}
                  >
                    <SecurityIcon />
                  </Box>
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      Sistema
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Configurações avançadas do sistema
                    </Typography>
                  </Box>
                </Box>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <UpdateIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Início Automático"
                      secondary="Iniciar bot automaticamente ao abrir"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.autoStart}
                        onChange={handleSettingChange('autoStart')}
                        color="info"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <UpdateIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Atualizações Automáticas"
                      secondary="Verificar e instalar atualizações automaticamente"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.autoUpdate}
                        onChange={handleSettingChange('autoUpdate')}
                        color="info"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <BugReportIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Modo Debug"
                      secondary="Ativar logs detalhados para depuração"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.debugMode}
                        onChange={handleSettingChange('debugMode')}
                        color="info"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Data Settings */}
        <Grid item xs={12} lg={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3 }}
          >
            <Card
              sx={{
                border: `1px solid ${alpha(theme.palette.success.main, 0.2)}`,
                background: alpha(theme.palette.success.main, 0.02),
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 2,
                      backgroundColor: alpha(theme.palette.success.main, 0.1),
                      color: theme.palette.success.main,
                      mr: 2,
                    }}
                  >
                    <BackupIcon />
                  </Box>
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      Dados
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Backup e restauração de dados
                    </Typography>
                  </Box>
                </Box>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <BackupIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Salvar Histórico"
                      secondary="Manter histórico de resultados e apostas"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.saveHistory}
                        onChange={handleSettingChange('saveHistory')}
                        color="success"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <InfoIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Telemetria"
                      secondary="Enviar dados anônimos para melhorias"
                    />
                    <ListItemSecondaryAction>
                      <Switch
                        checked={settings.telemetry}
                        onChange={handleSettingChange('telemetry')}
                        color="success"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Actions */}
        <Grid item xs={12}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Ações
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<BackupIcon />}
                      onClick={handleExportSettings}
                      sx={{ py: 1.5 }}
                    >
                      Exportar Configurações
                    </Button>
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<RestoreIcon />}
                      onClick={handleImportSettings}
                      sx={{ py: 1.5 }}
                    >
                      Importar Configurações
                    </Button>
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      color="warning"
                      startIcon={<RestoreIcon />}
                      onClick={() => setResetDialogOpen(true)}
                      sx={{ py: 1.5 }}
                    >
                      Restaurar Padrão
                    </Button>
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<HelpIcon />}
                      sx={{ py: 1.5 }}
                    >
                      Ajuda
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* System Info */}
        <Grid item xs={12}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Informações do Sistema
                </Typography>
                
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Versão
                    </Typography>
                    <Typography variant="body1" fontWeight={600}>
                      1.0.0
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Última Atualização
                    </Typography>
                    <Typography variant="body1" fontWeight={600}>
                      {new Date().toLocaleDateString('pt-BR')}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Status
                    </Typography>
                    <Typography variant="body1" fontWeight={600} color="success.main">
                      Ativo
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Licença
                    </Typography>
                    <Typography variant="body1" fontWeight={600}>
                      MIT
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      {/* Reset Dialog */}
      <Dialog
        open={resetDialogOpen}
        onClose={() => setResetDialogOpen(false)}
        maxWidth="sm"
      >
        <DialogTitle>Restaurar Configurações Padrão</DialogTitle>
        <DialogContent>
          <Alert severity="warning" sx={{ mb: 2 }}>
            Esta ação irá restaurar todas as configurações para os valores padrão.
            Esta ação não pode ser desfeita.
          </Alert>
          <Typography>
            Tem certeza que deseja continuar?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResetDialogOpen(false)}>
            Cancelar
          </Button>
          <Button onClick={handleResetSettings} color="warning" variant="contained">
            Restaurar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Settings;