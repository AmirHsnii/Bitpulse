import React from 'react'
import { useTranslation } from 'react-i18next'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { Article } from '../types'

dayjs.extend(relativeTime)

function stripHtml(html: string = '', maxLength = 120) {
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  const text = tmp.textContent || tmp.innerText || '';
  return text.length > maxLength ? text.slice(0, maxLength) + '...' : text;
}

function getRelativeTime(date: string) {
  return dayjs(date).fromNow();
}

interface ArticleCardProps {
  article: Article
}

function isEnglish(text: string) {
  // Count Latin letters vs. non-ASCII
  const latin = (text.match(/[A-Za-z]/g) || []).length;
  const nonLatin = (text.match(/[^\x00-\x7F]/g) || []).length;
  return latin > nonLatin;
}

const ArticleCard = ({ article }: ArticleCardProps) => {
  const { t } = useTranslation()
  const ltr = isEnglish(article.title)
  return (
    <article
      className={`card p-6 flex flex-col h-full bg-white/90 text-gray-900 ${ltr ? 'text-left' : 'text-right'}`}
      dir={ltr ? 'ltr' : 'rtl'}
    >
      <h2 className="font-bold text-lg md:text-xl mb-2 leading-snug line-clamp-2">{article.title}</h2>
      <div className={`flex flex-wrap items-center gap-2 mb-2 text-xs text-gray-500 ${ltr ? 'justify-start' : 'justify-end'}`}
        dir={ltr ? 'ltr' : 'rtl'}>
        <span>{getRelativeTime(article.published_at)}</span>
        {article.feed?.title && (
          <span className="badge badge-source">{article.feed.title}</span>
        )}
        <span className="badge badge-new">{t('جدید')}</span>
      </div>
      <hr className="my-2 border-gray-200" />
      <p className="mt-2 text-sm text-gray-700 line-clamp-3" dir={ltr ? 'ltr' : 'rtl'}>
        {stripHtml(article.description || '')}
      </p>
      <a
        href={article.link}
        target="_blank"
        rel="noopener noreferrer"
        className={`block text-primary mt-4 font-medium hover:underline ${ltr ? 'text-left' : 'text-right'}`}
        dir={ltr ? 'ltr' : 'rtl'}
      >
        بیشتر بخوانید →
      </a>
    </article>
  )
}

export default ArticleCard 