import React from 'react';
import { Routes, Route } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Home from './pages/Home'
import FeedManager from './pages/FeedManager'
import AllArticles from './pages/AllArticles'
import Navbar from './components/Navbar'
import Footer from './components/Footer'

function App() {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-background font-vazir">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/feeds" element={<FeedManager />} />
          <Route path="/articles" element={<AllArticles />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App 