import request from '@/config/axios'


//创建代收订单
export const createCollOrderApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/collorder/createcollorder', data })
}


//创建代付订单
export const createPayOrderApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/createproxypayorder', data })
}


export const queryUtrApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/order/queryUtr', data })
}
