import React from 'react'
import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const location = useLocation()
  return (
    <nav className="w-full bg-[#23272e] text-white shadow-lg sticky top-0 z-50 font-vazir">
      <div className="container flex items-center justify-between py-3 px-4 mx-auto">
        <Link to="/" className="flex items-center group">
          <img
            src="/bitpulse-logo.png"
            alt="BitPulse Logo"
            className="w-[120px] h-[120px] mr-2 drop-shadow-xl transition-all duration-300 group-hover:scale-105"
            style={{ filter: 'drop-shadow(0 0 32px #00ffe7)' }}
          />
          {/* Optionally, add text next to logo: <span className="ml-2 text-2xl font-extrabold tracking-tight hidden sm:inline">بیت‌پالس</span> */}
        </Link>
        <div className="flex gap-6 text-lg">
          <Link to="/" className={location.pathname === '/' ? 'text-[#00ffe7] font-bold' : 'hover:text-[#00ffe7] transition-colors'}>خانه</Link>
          <Link to="/feeds" className={location.pathname === '/feeds' ? 'text-[#00ffe7] font-bold' : 'hover:text-[#00ffe7] transition-colors'}>خوراک‌ها</Link>
          <Link to="/articles" className={location.pathname === '/articles' ? 'text-[#00ffe7] font-bold' : 'hover:text-[#00ffe7] transition-colors'}>اخبار</Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 