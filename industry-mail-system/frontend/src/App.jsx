import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Subscribe from './pages/Subscribe'
import Dashboard from './pages/Dashboard'
import './App.css'

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/subscribe" element={<Subscribe />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
            </Layout>
        </Router>
    )
}

export default App
