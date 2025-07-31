import request from '@/config/axios'

// 商户列表
export const getMerchantListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/merchant/getMerchantList', params })
}

// 根据id获取商户
export const getMerchantByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/merchant/getMerchantById/${dataId}` })
}

// 添加商户
export const addMerchantApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/merchant/createMerchant', data })
}

// 编辑商户
export const editMerchantApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/merchant/editMerchant/${data.id}`, data })
}


// 删除商户
export const delMerchantApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/merchant/removeMerchant', data })
}



