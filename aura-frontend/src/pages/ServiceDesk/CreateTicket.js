import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const CreateTicket = () => {
  return (
    <Box className="fade-in">
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Create New Ticket
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="body1" color="text.secondary">
            Create ticket page is under development. This will provide a form to create new support tickets
            with fields for title, description, priority, category, and file attachments.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CreateTicket;
