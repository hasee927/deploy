import request from '@/config/axios'



// 获取订单成功率
export const getOrderstatApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/order/success', params })
}
