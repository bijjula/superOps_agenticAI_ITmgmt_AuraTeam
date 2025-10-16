import { createTheme } from '@mui/material/styles';

// SAP Fiori Color Palette
const fioriColors = {
  // Primary Colors
  sapBlue: '#0070f3',
  sapOrange: '#ff5722',
  sapGreen: '#4caf50',
  sapRed: '#f44336',
  
  // Neutral Colors
  sapGray1: '#f7f7f7',
  sapGray2: '#ededed',
  sapGray3: '#d5d5d5',
  sapGray4: '#bfbfbf',
  sapGray5: '#8c8c8c',
  sapGray6: '#666666',
  sapGray7: '#333333',
  
  // Semantic Colors
  sapPositive: '#4caf50',
  sapNegative: '#f44336',
  sapCritical: '#ff9800',
  sapNeutral: '#2196f3',
  
  // Background Colors
  sapBackgroundShell: '#354a5f',
  sapBackgroundPage: '#f7f7f7',
  sapBackgroundCard: '#ffffff',
};

// Create SAP Fiori Theme
export const fioriTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: fioriColors.sapBlue,
      light: '#4d94ff',
      dark: '#0056cc',
      contrastText: '#ffffff',
    },
    secondary: {
      main: fioriColors.sapOrange,
      light: '#ff8a50',
      dark: '#e64a19',
      contrastText: '#ffffff',
    },
    error: {
      main: fioriColors.sapNegative,
      light: '#f66',
      dark: '#d32f2f',
    },
    warning: {
      main: fioriColors.sapCritical,
      light: '#ffb74d',
      dark: '#f57c00',
    },
    info: {
      main: fioriColors.sapNeutral,
      light: '#64b5f6',
      dark: '#1976d2',
    },
    success: {
      main: fioriColors.sapPositive,
      light: '#81c784',
      dark: '#388e3c',
    },
    background: {
      default: fioriColors.sapBackgroundPage,
      paper: fioriColors.sapBackgroundCard,
    },
    text: {
      primary: fioriColors.sapGray7,
      secondary: fioriColors.sapGray6,
      disabled: fioriColors.sapGray5,
    },
    divider: fioriColors.sapGray3,
    grey: {
      50: fioriColors.sapGray1,
      100: fioriColors.sapGray2,
      200: fioriColors.sapGray3,
      300: fioriColors.sapGray4,
      400: fioriColors.sapGray5,
      500: fioriColors.sapGray6,
      600: fioriColors.sapGray7,
    },
  },
  typography: {
    fontFamily: '"Inter", "Helvetica Neue", Arial, sans-serif',
    fontSize: 14,
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 600,
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      lineHeight: 1.2,
      color: fioriColors.sapGray7,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
      color: fioriColors.sapGray7,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
      lineHeight: 1.4,
      color: fioriColors.sapGray7,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
      lineHeight: 1.4,
      color: fioriColors.sapGray7,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
      lineHeight: 1.5,
      color: fioriColors.sapGray7,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.6,
      color: fioriColors.sapGray7,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.75,
      color: fioriColors.sapGray6,
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.57,
      color: fioriColors.sapGray6,
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.5,
      color: fioriColors.sapGray7,
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: 1.43,
      color: fioriColors.sapGray6,
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.75,
      textTransform: 'none',
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: 1.66,
      color: fioriColors.sapGray5,
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: 2.66,
      textTransform: 'uppercase',
      color: fioriColors.sapGray5,
    },
  },
  shape: {
    borderRadius: 4,
  },
  spacing: 8,
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },
  shadows: [
    'none',
    '0px 1px 3px rgba(0, 0, 0, 0.12), 0px 1px 2px rgba(0, 0, 0, 0.24)',
    '0px 3px 6px rgba(0, 0, 0, 0.16), 0px 3px 6px rgba(0, 0, 0, 0.23)',
    '0px 10px 20px rgba(0, 0, 0, 0.19), 0px 6px 6px rgba(0, 0, 0, 0.23)',
    '0px 14px 28px rgba(0, 0, 0, 0.25), 0px 10px 10px rgba(0, 0, 0, 0.22)',
    '0px 19px 38px rgba(0, 0, 0, 0.30), 0px 15px 12px rgba(0, 0, 0, 0.22)',
    // ... extend as needed
  ],
  components: {
    // Button customizations
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          textTransform: 'none',
          fontWeight: 500,
          padding: '8px 16px',
          minHeight: 36,
        },
        contained: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.12)',
          '&:hover': {
            boxShadow: '0px 3px 6px rgba(0, 0, 0, 0.16)',
          },
        },
        outlined: {
          borderWidth: 1,
          '&:hover': {
            borderWidth: 1,
          },
        },
      },
    },
    // Card customizations
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.12), 0px 1px 2px rgba(0, 0, 0, 0.24)',
          border: `1px solid ${fioriColors.sapGray2}`,
        },
      },
    },
    // Paper customizations
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
        elevation1: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.12), 0px 1px 2px rgba(0, 0, 0, 0.24)',
        },
      },
    },
    // AppBar customizations
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: fioriColors.sapBackgroundShell,
          color: '#ffffff',
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.12), 0px 1px 2px rgba(0, 0, 0, 0.24)',
        },
      },
    },
    // Drawer customizations
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: fioriColors.sapBackgroundShell,
          color: '#ffffff',
          borderRight: 'none',
        },
      },
    },
    // Chip customizations
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          fontSize: '0.75rem',
          height: 24,
        },
        filled: {
          backgroundColor: fioriColors.sapGray2,
          color: fioriColors.sapGray7,
          '&:hover': {
            backgroundColor: fioriColors.sapGray3,
          },
        },
      },
    },
    // TextField customizations
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 4,
            backgroundColor: fioriColors.sapBackgroundCard,
            '& fieldset': {
              borderColor: fioriColors.sapGray3,
            },
            '&:hover fieldset': {
              borderColor: fioriColors.sapGray4,
            },
            '&.Mui-focused fieldset': {
              borderColor: fioriColors.sapBlue,
              borderWidth: 2,
            },
          },
        },
      },
    },
    // DataGrid customizations
    MuiDataGrid: {
      styleOverrides: {
        root: {
          border: `1px solid ${fioriColors.sapGray2}`,
          borderRadius: 8,
          '& .MuiDataGrid-cell': {
            borderBottom: `1px solid ${fioriColors.sapGray2}`,
          },
          '& .MuiDataGrid-columnHeaders': {
            backgroundColor: fioriColors.sapGray1,
            borderBottom: `2px solid ${fioriColors.sapGray3}`,
          },
          '& .MuiDataGrid-row:hover': {
            backgroundColor: fioriColors.sapGray1,
          },
        },
      },
    },
    // Badge customizations
    MuiBadge: {
      styleOverrides: {
        badge: {
          fontSize: '0.75rem',
          height: 20,
          minWidth: 20,
        },
      },
    },
    // Tabs customizations
    MuiTabs: {
      styleOverrides: {
        root: {
          borderBottom: `1px solid ${fioriColors.sapGray2}`,
          minHeight: 48,
        },
        indicator: {
          backgroundColor: fioriColors.sapBlue,
          height: 3,
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          fontSize: '0.875rem',
          minHeight: 48,
          '&.Mui-selected': {
            color: fioriColors.sapBlue,
          },
        },
      },
    },
  },
});

// Custom theme variants for specific use cases
export const fioriDarkTheme = createTheme({
  ...fioriTheme,
  palette: {
    ...fioriTheme.palette,
    mode: 'dark',
    background: {
      default: '#1a1a1a',
      paper: '#2a2a2a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#cccccc',
    },
  },
});

export default fioriTheme;
