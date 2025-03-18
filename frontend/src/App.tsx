import { Container, Typography } from '@mui/material';
import { useStore } from './store/store';

function App() {
  return (
    <Container maxWidth="lg">
      <Typography variant="h2" component="h1" gutterBottom>
        SIPPEC Frontend
      </Typography>
    </Container>
  );
}

export default App;
