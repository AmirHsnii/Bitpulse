import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import dayjs from 'dayjs'
import jalaliday from 'jalaliday'
import App from './App'
import './index.css'

// Configure dayjs with Jalali calendar
dayjs.extend(jalaliday)

// Configure i18n
i18n
  .use(initReactI18next)
  .init({
    resources: {
      fa: {
        translation: {
          // Persian translations
          "new": "جدید",
          "read_more": "بیشتر بخوانید",
          "minutes_ago": "{{count}} دقیقه پیش",
          "hours_ago": "{{count}} ساعت پیش",
          "days_ago": "{{count}} روز پیش",
          "search": "جستجو",
          "add_feed": "افزودن خوراک",
          "remove_feed": "حذف خوراک",
          "feed_url": "آدرس خوراک",
          "feed_title": "عنوان خوراک",
          "feed_description": "توضیحات خوراک",
          "no_feeds": "هیچ خوراکی یافت نشد",
          "no_articles": "هیچ مقاله‌ای یافت نشد",
          "loading": "در حال بارگذاری...",
          "error": "خطا",
          "success": "موفق",
        }
      },
      en: {
        translation: {
          // English translations
          "new": "NEW",
          "read_more": "Read More",
          "minutes_ago": "{{count}} minutes ago",
          "hours_ago": "{{count}} hours ago",
          "days_ago": "{{count}} days ago",
          "search": "Search",
          "add_feed": "Add Feed",
          "remove_feed": "Remove Feed",
          "feed_url": "Feed URL",
          "feed_title": "Feed Title",
          "feed_description": "Feed Description",
          "no_feeds": "No feeds found",
          "no_articles": "No articles found",
          "loading": "Loading...",
          "error": "Error",
          "success": "Success",
        }
      }
    },
    lng: "fa", // default language
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    }
  })

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1
    }
  }
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
) 