import request from '@/config/axios'

// 获取银行列表
export const getBankListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/bank/getBankList', params })
}

// 根据id获取银行
export const getBankByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/bank/getBankById/${dataId}` })
}

// 添加银行
export const addBankApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/bank/createBank', data })
}

// 编辑银行配置
export const editBankApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/bank/editBank/${data.id}`, data })
}


// 删除银行配置
export const delBankApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/bank/removeBank', data })
}



