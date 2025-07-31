import request from '@/config/axios'

// 打款明细列表
export const getPayDetailListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/paydetail/getPayDetailList', params })
}



// 根据id获取打款明细
export const getPayDetailByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/paydetail/getPayDetailById/${dataId}` })
}

// 添加打款明细
export const addPayDetailApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/paydetail/createPayDetail', data })
}

// 编辑打款明细
export const editPayDetailApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/paydetail/editPayDetail/${data.id}`, data })
}


// 删除打款明细
export const delPayDetailApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/paydetail/removePayDetail', data })
}



// 导出数据
export const exportDatalApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/yg/paydetail/exportexcel`, data })
}
