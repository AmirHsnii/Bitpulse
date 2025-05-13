export interface Feed {
  id: number
  url: string
  title: string
  description?: string
  last_updated?: string
  created_at: string
  is_active: boolean
}

export interface Article {
  id: number
  feed_id: number
  feed: Feed
  title: string
  link: string
  description?: string
  content?: string
  author?: string
  published_at: string
  created_at: string
  updated_at?: string
  is_new: boolean
}

export interface PaginatedResponse<T> {
  total: number
  page: number
  size: number
  pages: number
  items: T[]
}

export interface ArticleQueryParams {
  page?: number
  size?: number
  feed_id?: number
  search?: string
  start_date?: string
  end_date?: string
  is_new?: boolean
} 