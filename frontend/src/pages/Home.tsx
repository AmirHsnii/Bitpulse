import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import axios from 'axios'
import ArticleCard from '../components/ArticleCard'
import { Article, PaginatedResponse } from '../types'
import { Link } from 'react-router-dom'

// Placeholder icons as SVG components
const icons = {
  refresh: (
    <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582M20 20v-5h-.581M5.635 19A9 9 0 1 0 6 6.35" /></svg>
  ),
  rtl: (
    <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 17V7a2 2 0 0 1 2-2h6" /></svg>
  ),
  search: (
    <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8" /><path d="M21 21l-4.35-4.35" /></svg>
  ),
  live: (
    <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3" /><path d="M19.4 15A7 7 0 0 0 12 5a7 7 0 0 0-7.4 10" /></svg>
  ),
  feed: (
    <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="6" cy="18" r="2" /><path d="M4 4a16 16 0 0 1 16 16" /></svg>
  )
}

function Home() {
  const { t } = useTranslation()
  const [search, setSearch] = useState('')
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(false)
    axios.get<PaginatedResponse<Article>>('/api/articles', {
      params: search ? { search } : {}
    })
      .then(res => {
        setArticles(res.data.items)
        setLoading(false)
      })
      .catch(() => {
        setArticles([])
        setError(true)
        setLoading(false)
      })
  }, [search])

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value)
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background font-vazir text-white">
        <p className="text-center py-8 text-red-600">{t('error')}</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background font-vazir text-white">
      {/* Hero Section */}
      <section className="w-full bg-gradient py-16 text-center rounded-t-3xl rounded-b-3xl shadow-3xl animate-fade-in">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-extrabold text-primary mb-4 drop-shadow-lg animate-slide-in">اخبار رمزارزها را یکجا دنبال کن!</h1>
          <p className="text-xl md:text-2xl text-secondary mb-8 animate-fade-in">جدیدترین اخبار و تحلیل‌های رمزارزی از معتبرترین منابع، همه در یکجا</p>
          <div className="flex justify-center gap-4 mb-8">
            <Link to="/articles" className="btn btn-primary text-lg font-bold animate-pop">مشاهده اخبار</Link>
            <Link to="/feeds" className="btn btn-secondary text-lg font-bold animate-pop">مدیریت خوراک‌ها</Link>
          </div>
          <div className="flex justify-center">
            <img src="/crypto-news.gif" alt="Crypto News Animation" className="w-[100px] h-[100px] rounded-2xl shadow-3xl animate-fade-in" />
          </div>
        </div>
      </section>

      {/* Latest Articles */}
      <section className="w-full py-12 bg-background">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-2xl font-bold text-primary">آخرین اخبار رمزارزها</h2>
            <input
              type="text"
              placeholder="جستجو در اخبار..."
              value={search}
              onChange={handleSearch}
              className="input bg-background border-primary text-white placeholder-secondary max-w-xs shadow-md"
              style={{ fontFamily: 'Vazir' }}
            />
          </div>
          {loading ? (
            <p className="text-center text-secondary">در حال بارگذاری...</p>
          ) : error ? (
            <p className="text-center text-red-400">خطا در دریافت اخبار</p>
          ) : (
            <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
              {articles.slice(0, 12).map(article => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          )}
          <div className="flex justify-center mt-8">
            <Link to="/articles" className="btn btn-primary text-lg font-bold animate-pop">
              مشاهده همه اخبار
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home 