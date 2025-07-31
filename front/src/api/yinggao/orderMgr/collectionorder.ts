import request from '@/config/axios'



// 获取代收订单列表
export const getCollOrderListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/collorder/getcollorderList', params })
}


// 补单
export const supOrderByIdApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/collorder/suporder`, data })
}



// 通知商户
export const noticeMerchantApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/yg/collorder/notice`, data })
}


// 导出数据
export const exportDataApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/yg/collorder/exportexcel`, data })
}
