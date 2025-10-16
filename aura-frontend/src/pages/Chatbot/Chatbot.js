import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  IconButton,
  Avatar,
  List,
  ListItem,
  Chip,
  Button,
  CircularProgress,
  useTheme,
  Divider,
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Clear as ClearIcon,
  Refresh as RefreshIcon,
  QuestionAnswer as QuestionIcon,
} from '@mui/icons-material';
import { chatbotAPI } from '../../services/api';
import { useSnackbar } from 'notistack';

const Chatbot = () => {
  const theme = useTheme();
  const { enqueueSnackbar } = useSnackbar();
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I'm your AI assistant. I can help you with common IT issues, guide you through troubleshooting steps, and find relevant knowledge base articles. How can I assist you today?",
      timestamp: new Date(),
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  // Sample quick actions/suggestions
  const quickActions = [
    "Password reset help",
    "VPN connection issues",
    "Email setup guide",
    "Software installation",
    "Network troubleshooting",
    "Printer problems"
  ];

  // Scroll to bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize chat session
  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = async () => {
    try {
      // In a real app, this would create a new session with the backend
      setSessionId(`session_${Date.now()}`);
    } catch (error) {
      console.error('Failed to initialize chat session:', error);
    }
  };

  const sendMessage = async (messageContent = inputMessage) => {
    if (!messageContent.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageContent,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Simulate API call - in real app, this would use chatbotAPI.sendMessage
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock bot response based on message content
      const botResponse = generateMockResponse(messageContent);
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: botResponse,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      enqueueSnackbar('Failed to send message', { variant: 'error' });
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Mock response generator (in real app, this would come from the API)
  const generateMockResponse = (message) => {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('password') || lowerMessage.includes('login')) {
      return "I can help you with password issues! Here are some common solutions:\n\n1. **Reset your password**: Go to the company portal and click 'Forgot Password'\n2. **Check caps lock**: Make sure caps lock is off\n3. **Clear browser cache**: Clear your browser's saved passwords\n4. **Contact IT**: If none of these work, I can create a ticket for you\n\nWould you like me to guide you through any of these steps?";
    }
    
    if (lowerMessage.includes('vpn') || lowerMessage.includes('connection')) {
      return "VPN connection problems are common. Let's troubleshoot:\n\n1. **Check your internet**: Make sure you have a stable connection\n2. **Restart VPN client**: Close and reopen your VPN application\n3. **Try different server**: Switch to a different VPN server location\n4. **Update VPN client**: Make sure you have the latest version\n\nIf these don't help, I can escalate this to our network team. Would you like me to create a support ticket?";
    }
    
    if (lowerMessage.includes('email') || lowerMessage.includes('outlook')) {
      return "Email setup issues can be frustrating. Here's what usually works:\n\n1. **Check server settings**: \n   - IMAP: mail.company.com (Port 993)\n   - SMTP: mail.company.com (Port 587)\n2. **Verify credentials**: Double-check username and password\n3. **Enable 2FA**: You might need an app password\n4. **Restart email client**: Close and reopen Outlook\n\nNeed help with any specific email client? I have guides for Outlook, Apple Mail, and others.";
    }
    
    if (lowerMessage.includes('printer') || lowerMessage.includes('print')) {
      return "Printer troubles? Let's get you printing again:\n\n1. **Check connections**: Ensure printer is plugged in and on\n2. **Restart printer**: Turn off for 30 seconds, then back on\n3. **Check print queue**: Clear any stuck print jobs\n4. **Update drivers**: Download latest drivers from manufacturer\n5. **Network printers**: Make sure you're on the right network\n\nWhat type of printer issue are you experiencing?";
    }
    
    // Default response
    return "I understand you're having an issue. While I'm still learning about this specific topic, I can:\n\n1. **Search our knowledge base** for related articles\n2. **Create a support ticket** for you with our IT team\n3. **Connect you with a live agent** if available\n\nWhat would you prefer? Or could you provide more details about your specific problem?";
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: "Chat cleared! How can I help you today?",
        timestamp: new Date(),
      }
    ]);
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Box className="fade-in">
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
            AI Assistant
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Get instant help with common IT issues and troubleshooting
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton onClick={clearChat} title="Clear Chat">
            <ClearIcon />
          </IconButton>
          <IconButton onClick={initializeSession} title="Refresh Session">
            <RefreshIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Quick Actions */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
            Quick Help Topics
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {quickActions.map((action, index) => (
              <Chip
                key={index}
                label={action}
                variant="outlined"
                onClick={() => sendMessage(`Help me with ${action}`)}
                sx={{ cursor: 'pointer' }}
                icon={<QuestionIcon />}
              />
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Chat Interface */}
      <Card sx={{ height: 'calc(100vh - 350px)', display: 'flex', flexDirection: 'column' }}>
        {/* Messages Area */}
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          <List sx={{ py: 0 }}>
            {messages.map((message, index) => (
              <ListItem
                key={message.id}
                sx={{
                  flexDirection: 'column',
                  alignItems: message.type === 'user' ? 'flex-end' : 'flex-start',
                  px: 0,
                  py: 1,
                }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: 1,
                    maxWidth: '80%',
                    flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                  }}
                >
                  <Avatar
                    sx={{
                      width: 32,
                      height: 32,
                      bgcolor: message.type === 'user' ? theme.palette.primary.main : theme.palette.secondary.main,
                    }}
                  >
                    {message.type === 'user' ? <PersonIcon /> : <BotIcon />}
                  </Avatar>
                  
                  <Box
                    sx={{
                      backgroundColor: message.type === 'user' 
                        ? theme.palette.primary.main 
                        : theme.palette.grey[100],
                      color: message.type === 'user' ? 'white' : 'text.primary',
                      borderRadius: 2,
                      px: 2,
                      py: 1.5,
                      maxWidth: '100%',
                    }}
                  >
                    <Typography
                      variant="body2"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word',
                      }}
                    >
                      {message.content}
                    </Typography>
                    <Typography
                      variant="caption"
                      sx={{
                        mt: 0.5,
                        display: 'block',
                        opacity: 0.7,
                        fontSize: '0.7rem',
                      }}
                    >
                      {formatTime(message.timestamp)}
                    </Typography>
                  </Box>
                </Box>
              </ListItem>
            ))}
            
            {/* Typing Indicator */}
            {isLoading && (
              <ListItem sx={{ px: 0, py: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Avatar
                    sx={{
                      width: 32,
                      height: 32,
                      bgcolor: theme.palette.secondary.main,
                    }}
                  >
                    <BotIcon />
                  </Avatar>
                  <Box
                    sx={{
                      backgroundColor: theme.palette.grey[100],
                      borderRadius: 2,
                      px: 2,
                      py: 1.5,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                    }}
                  >
                    <CircularProgress size={16} />
                    <Typography variant="body2" color="text.secondary">
                      Thinking...
                    </Typography>
                  </Box>
                </Box>
              </ListItem>
            )}
          </List>
          <div ref={messagesEndRef} />
        </Box>

        <Divider />

        {/* Input Area */}
        <Box sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={3}
              variant="outlined"
              placeholder="Type your message here... (Press Enter to send)"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              size="small"
            />
            <IconButton
              color="primary"
              onClick={() => sendMessage()}
              disabled={!inputMessage.trim() || isLoading}
              sx={{
                bgcolor: theme.palette.primary.main,
                color: 'white',
                '&:hover': {
                  bgcolor: theme.palette.primary.dark,
                },
                '&.Mui-disabled': {
                  bgcolor: theme.palette.grey[300],
                  color: theme.palette.grey[500],
                },
              }}
            >
              <SendIcon />
            </IconButton>
          </Box>
          
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            💡 Tip: Be specific about your issue for better assistance. I can help with passwords, VPN, email, printers, and more!
          </Typography>
        </Box>
      </Card>
    </Box>
  );
};

export default Chatbot;
