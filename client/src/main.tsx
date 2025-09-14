import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { HashRouter } from "react-router-dom";


createRoot(document.getElementById("root")!).render(<HashRouter basename="/genre_prediction"><App /></HashRouter>);
