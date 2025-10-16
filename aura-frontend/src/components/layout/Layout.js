import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Box, useMediaQuery, useTheme } from '@mui/material';
import Header from './Header';
import Sidebar from './Sidebar';

const Layout = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [sidebarOpen, setSidebarOpen] = useState(!isMobile);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const location = useLocation();

  const handleSidebarToggle = () => {
    if (isMobile) {
      setSidebarOpen(!sidebarOpen);
    } else {
      setSidebarCollapsed(!sidebarCollapsed);
    }
  };

  const handleSidebarClose = () => {
    if (isMobile) {
      setSidebarOpen(false);
    }
  };

  return (
    <Box className="app-layout" sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <Sidebar
        open={sidebarOpen}
        collapsed={sidebarCollapsed}
        isMobile={isMobile}
        onClose={handleSidebarClose}
        currentPath={location.pathname}
      />
      
      {/* Main Content Area */}
      <Box className="app-main" sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Header
          onSidebarToggle={handleSidebarToggle}
          sidebarCollapsed={sidebarCollapsed}
          isMobile={isMobile}
        />
        
        {/* Page Content */}
        <Box
          className="app-content"
          component="main"
          sx={{
            flex: 1,
            p: 3,
            backgroundColor: theme.palette.background.default,
            overflow: 'auto',
            [theme.breakpoints.down('md')]: {
              p: 2,
            },
          }}
        >
          {children}
        </Box>
      </Box>
      
      {/* Mobile Overlay */}
      {isMobile && sidebarOpen && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: 1199,
          }}
          onClick={handleSidebarClose}
        />
      )}
    </Box>
  );
};

export default Layout;
