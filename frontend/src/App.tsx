import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box,
  useMediaQuery,
} from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

// Components
import Sidebar from './components/Sidebar/Sidebar';
import Header from './components/Header/Header';
import LoadingScreen from './components/LoadingScreen/LoadingScreen';

// Pages
import Dashboard from './pages/Dashboard/Dashboard';
import Configuration from './pages/Configuration/Configuration';
import Elements from './pages/Elements/Elements';
import Betting from './pages/Betting/Betting';
import Monitoring from './pages/Monitoring/Monitoring';
import Logs from './pages/Logs/Logs';
import Settings from './pages/Settings/Settings';

// Contexts
import { WebSocketProvider } from './contexts/WebSocketContext';
import { BotProvider } from './contexts/BotContext';

// Styles
import './App.css';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

// Create Material-UI theme
const createAppTheme = (darkMode: boolean) =>
  createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#667eea',
        light: '#8fa4f3',
        dark: '#4c63d2',
      },
      secondary: {
        main: '#764ba2',
        light: '#9575cd',
        dark: '#512da8',
      },
      background: {
        default: darkMode ? '#0a0e27' : '#f5f7fa',
        paper: darkMode ? '#1a1d3a' : '#ffffff',
      },
      success: {
        main: '#4caf50',
      },
      error: {
        main: '#f44336',
      },
      warning: {
        main: '#ff9800',
      },
      info: {
        main: '#2196f3',
      },
    },
    typography: {
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
      h1: {
        fontWeight: 700,
        fontSize: '2.5rem',
      },
      h2: {
        fontWeight: 600,
        fontSize: '2rem',
      },
      h3: {
        fontWeight: 600,
        fontSize: '1.5rem',
      },
      h4: {
        fontWeight: 600,
        fontSize: '1.25rem',
      },
      h5: {
        fontWeight: 500,
        fontSize: '1.125rem',
      },
      h6: {
        fontWeight: 500,
        fontSize: '1rem',
      },
      body1: {
        fontSize: '0.875rem',
        lineHeight: 1.5,
      },
      body2: {
        fontSize: '0.75rem',
        lineHeight: 1.4,
      },
    },
    shape: {
      borderRadius: 12,
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            fontWeight: 500,
            borderRadius: 8,
            padding: '8px 16px',
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            boxShadow: darkMode
              ? '0 4px 20px rgba(0, 0, 0, 0.3)'
              : '0 4px 20px rgba(0, 0, 0, 0.1)',
            borderRadius: 12,
          },
        },
      },
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: 'none',
          },
        },
      },
    },
  });

const DRAWER_WIDTH = 280;

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : true;
  });
  
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(true);
  
  const isMobile = useMediaQuery('(max-width:768px)');
  const theme = createAppTheme(darkMode);

  // Initialize app
  useEffect(() => {
    const initApp = async () => {
      try {
        // Simulate initialization delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Check backend connection
        const response = await fetch('/health');
        if (!response.ok) {
          console.warn('Backend não está disponível');
        }
      } catch (error) {
        console.error('Erro ao inicializar aplicação:', error);
      } finally {
        setLoading(false);
      }
    };

    initApp();
  }, []);

  // Save dark mode preference
  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  // Handle sidebar on mobile
  useEffect(() => {
    if (isMobile) {
      setSidebarOpen(false);
    } else {
      setSidebarOpen(true);
    }
  }, [isMobile]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <LoadingScreen />
      </ThemeProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <WebSocketProvider>
          <BotProvider>
            <Router>
              <Box sx={{ display: 'flex', minHeight: '100vh' }}>
                {/* Sidebar */}
                <Sidebar
                  open={sidebarOpen}
                  onClose={() => setSidebarOpen(false)}
                  width={DRAWER_WIDTH}
                  isMobile={isMobile}
                />

                {/* Main Content */}
                <Box
                  component="main"
                  sx={{
                    flexGrow: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    minHeight: '100vh',
                    ml: sidebarOpen && !isMobile ? `${DRAWER_WIDTH}px` : 0,
                    transition: theme.transitions.create(['margin'], {
                      easing: theme.transitions.easing.sharp,
                      duration: theme.transitions.duration.leavingScreen,
                    }),
                  }}
                >
                  {/* Header */}
                  <Header
                    onToggleSidebar={toggleSidebar}
                    onToggleDarkMode={toggleDarkMode}
                    darkMode={darkMode}
                    sidebarOpen={sidebarOpen}
                  />

                  {/* Page Content */}
                  <Box
                    sx={{
                      flexGrow: 1,
                      p: 3,
                      backgroundColor: 'background.default',
                      minHeight: 'calc(100vh - 64px)',
                    }}
                  >
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/configuration" element={<Configuration />} />
                      <Route path="/elements" element={<Elements />} />
                      <Route path="/betting" element={<Betting />} />
                      <Route path="/monitoring" element={<Monitoring />} />
                      <Route path="/logs" element={<Logs />} />
                      <Route path="/settings" element={<Settings />} />
                    </Routes>
                  </Box>
                </Box>

                {/* Toast Notifications */}
                <Toaster
                  position="top-right"
                  toastOptions={{
                    duration: 4000,
                    style: {
                      background: darkMode ? '#1a1d3a' : '#ffffff',
                      color: darkMode ? '#ffffff' : '#000000',
                      border: `1px solid ${darkMode ? '#333' : '#e0e0e0'}`,
                      borderRadius: '8px',
                      fontSize: '14px',
                    },
                    success: {
                      iconTheme: {
                        primary: '#4caf50',
                        secondary: '#ffffff',
                      },
                    },
                    error: {
                      iconTheme: {
                        primary: '#f44336',
                        secondary: '#ffffff',
                      },
                    },
                  }}
                />
              </Box>
            </Router>
          </BotProvider>
        </WebSocketProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;