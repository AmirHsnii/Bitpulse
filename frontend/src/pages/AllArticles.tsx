import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from 'react-query'
import axios from 'axios'
import ArticleCard from '../components/ArticleCard'
import { Article, PaginatedResponse } from '../types'

function AllArticles() {
  const { t } = useTranslation()
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const pageSize = 15

  const fetchArticles = async () => {
    const res = await axios.get<PaginatedResponse<Article>>('/api/articles', {
      params: { page, size: pageSize, search }
    })
    return res.data
  }

  const { data, isLoading, isError } = useQuery(['all-articles', page, search], fetchArticles, { keepPreviousData: true })

  const totalPages = data ? data.pages : 1

  return (
    <section className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6 text-green-700">{t('همه اخبار')}</h1>
      <input
        type="text"
        className="input mb-6"
        placeholder={t('جستجو در اخبار...')}
        value={search}
        onChange={e => { setSearch(e.target.value); setPage(1); }}
      />
      {isLoading ? (
        <p className="text-center text-gray-400">در حال بارگذاری...</p>
      ) : isError ? (
        <p className="text-center text-red-500">{t('خطا در بارگذاری اخبار')}</p>
      ) : (
        <>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {data?.items.map(article => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
          {/* Pagination Controls */}
          <div className="flex justify-center items-center gap-2 mt-8">
            <button
              className="btn btn-secondary"
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              قبلی
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
              <button
                key={p}
                className={`btn ${p === page ? 'btn-primary' : 'btn-secondary'} px-3`}
                onClick={() => setPage(p)}
              >
                {p}
              </button>
            ))}
            <button
              className="btn btn-secondary"
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
            >
              بعدی
            </button>
          </div>
        </>
      )}
    </section>
  )
}

export default AllArticles 