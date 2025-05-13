import React from 'react'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import axios from 'axios'
import { Feed } from '../types'

function FeedManager() {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [newFeedUrl, setNewFeedUrl] = useState('')
  const [newFeedTitle, setNewFeedTitle] = useState('')

  const { data: feeds, isLoading, error } = useQuery<Feed[]>(
    'feeds',
    async () => {
      const response = await axios.get('/api/feeds')
      return response.data
    }
  )

  const addFeedMutation = useMutation(
    async ({ url, title }: { url: string; title: string }) => {
      const response = await axios.post('/api/feeds', { url, title })
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('feeds')
        setNewFeedUrl('')
        setNewFeedTitle('')
      }
    }
  )

  const deleteFeedMutation = useMutation(
    async (id: number) => {
      await axios.delete(`/api/feeds/${id}`)
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('feeds')
      }
    }
  )

  const handleAddFeed = (e: React.FormEvent) => {
    e.preventDefault()
    if (newFeedUrl && newFeedTitle) {
      addFeedMutation.mutate({ url: newFeedUrl, title: newFeedTitle })
    }
  }

  const handleDeleteFeed = (id: number) => {
    if (window.confirm(t('confirm_delete_feed'))) {
      deleteFeedMutation.mutate(id)
    }
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{t('error')}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">{t('add_feed')}</h2>
        <form onSubmit={handleAddFeed} className="space-y-4">
          <div>
            <label htmlFor="feed-url" className="block text-sm font-medium text-gray-700 mb-1">
              {t('feed_url')}
            </label>
            <input
              type="url"
              id="feed-url"
              value={newFeedUrl}
              onChange={(e) => setNewFeedUrl(e.target.value)}
              placeholder="https://example.com/feed.xml"
              className="input"
              required
            />
          </div>
          <div>
            <label htmlFor="feed-title" className="block text-sm font-medium text-gray-700 mb-1">
              {t('feed_title')}
            </label>
            <input
              type="text"
              id="feed-title"
              value={newFeedTitle}
              onChange={(e) => setNewFeedTitle(e.target.value)}
              placeholder="عنوان خوراک"
              className="input"
              required
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={addFeedMutation.isLoading}
          >
            {addFeedMutation.isLoading ? t('adding') : t('add_feed')}
          </button>
        </form>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">{t('manage_feeds')}</h2>
        {isLoading ? (
          <p>{t('loading')}</p>
        ) : feeds?.length === 0 ? (
          <p className="text-gray-500">{t('no_feeds')}</p>
        ) : (
          <div className="space-y-4">
            {feeds?.map(feed => (
              <div
                key={feed.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div>
                  <h3 className="font-medium">{feed.title}</h3>
                  <p className="text-sm text-gray-500">{feed.url}</p>
                </div>
                <button
                  onClick={() => handleDeleteFeed(feed.id)}
                  className="btn btn-secondary"
                  disabled={deleteFeedMutation.isLoading}
                >
                  {t('remove_feed')}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default FeedManager 