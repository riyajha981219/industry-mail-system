import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../services/api'
import './Layout.css'

const Layout = ({ children }) => {
    const [user, setUser] = useState(null)

    const parseStoredUser = (val) => {
        if (!val) return null
        try {
            let parsed = JSON.parse(val)
            // handle double-encoded JSON (string inside string)
            if (typeof parsed === 'string') {
                parsed = JSON.parse(parsed)
            }
            return parsed
        } catch (e) {
            return null
        }
    }

    useEffect(() => {
        try {
            const stored = localStorage.getItem('ims_user')
            const u = parseStoredUser(stored)
            if (u) setUser(u)
        } catch (e) { }
    }, [])

    // Update local user state when localStorage changes in other tabs/windows
    useEffect(() => {
        const onStorage = (e) => {
            if (e.key === 'ims_user') {
                try {
                    if (e.newValue) setUser(parseStoredUser(e.newValue))
                    else setUser(null)
                } catch (err) {
                    setUser(null)
                }
            }
        }

        const onFocus = () => {
            try {
                const stored = localStorage.getItem('ims_user')
                const u = parseStoredUser(stored)
                if (u) setUser(u)
                else setUser(null)
            } catch (e) { setUser(null) }
        }

        window.addEventListener('storage', onStorage)
        window.addEventListener('focus', onFocus)
        return () => {
            window.removeEventListener('storage', onStorage)
            window.removeEventListener('focus', onFocus)
        }
    }, [])

    // OAuth removed: no Google Identity script initialization

    const handleSignOut = () => {
        localStorage.removeItem('ims_user')
        setUser(null)
    }

    return (
        <div className="layout">
            <header className="header">
                <div className="container">
                    <nav className="nav">
                        <Link to="/" className="logo">
                            <h2>📧 Industry Mailer</h2>
                        </Link>
                        <ul className="nav-links">
                            <li><Link to="/">Home</Link></li>
                            <li><Link to="/subscribe">Subscribe</Link></li>
                            <li><Link to="/dashboard">Dashboard</Link></li>
                        </ul>

                        <div className="auth-controls">
                            {user ? (
                                <div className="user-info">
                                    <span className="user-name">{user.full_name || user.email}</span>
                                    <button className="btn" onClick={handleSignOut}>Sign out</button>
                                </div>
                            ) : (
                                <div>
                                    <small style={{ color: '#666' }}>Sign in via email when subscribing</small>
                                </div>
                            )}
                        </div>
                    </nav>
                </div>
            </header>
            <main className="main">
                {children}
            </main>
            <footer className="footer">
                <div className="container">
                    <p>&copy; 2026 Industry Mailer System. All rights reserved.</p>
                </div>
            </footer>
        </div>
    )
}

export default Layout
