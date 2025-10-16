import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { useParams } from 'react-router-dom';

const TicketDetail = () => {
  const { ticketId } = useParams();

  return (
    <Box className="fade-in">
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Ticket Details #{ticketId}
      </Typography>
      
      <Card>
        <CardContent>
          <Typography variant="body1" color="text.secondary">
            Ticket detail page is under development. This will show detailed ticket information,
            comments, status updates, and allow ticket management actions.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default TicketDetail;
