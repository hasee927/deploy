import request from '@/config/axios'



// 获取商户资金列表
export const getFinanceApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/finance/getFinanceList', params })
}


// 获取单个商户资金
export const getFinanceByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/finance/getFinanceById/${dataId}` })
}


// 调账
export const editFinanceApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/finance/editFinance/${data.id}` , data})
}

