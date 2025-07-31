import request from '@/config/axios'
import type { Project, Dynamic, Team, RadarData, Shortcuts } from './types'



// 获取今日和昨天的统计数据
export const getCollectionDataApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/order/todaycollection' })
}

// 代收排行榜
export const getCollectionRankingApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/order/collectionranking', params })
}



// 获取今日和昨天的代付数据
export const getPayOutDataApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/order/todaypayout' })
}

// 代付排行榜
export const getPayRankingApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/order/payoutranking', params })
}


// 代付排行榜
export const getPayPendingApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/order/paypending' })
}

