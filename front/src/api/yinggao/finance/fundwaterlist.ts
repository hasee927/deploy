import request from '@/config/axios'

// 资金流水列表
export const getFundWaterListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/fund/getfundwater', params })
}


// 导出数据
export const exportDataApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/yg/fund/exportexcel`, data })
}