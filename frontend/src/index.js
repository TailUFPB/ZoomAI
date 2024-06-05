import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';
import './public/css/style.css';
import './public/css/zoomai_style.css';
import 'react-toastify/dist/ReactToastify.css';

import { ViewsProvider } from './contexts/ViewsContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <ViewsProvider>
        <App />
    </ViewsProvider>
    
);
reportWebVitals();
