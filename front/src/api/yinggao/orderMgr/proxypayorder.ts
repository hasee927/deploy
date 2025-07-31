import request from '@/config/axios'



// 获取代付订单列表
export const getPPOrderListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/pporder/getpporderList', params })
}


// 计算出款和批量出款的金额
export const batchPayOutAmountApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/payoutamount', data })
}

// 批量出款
export const batchPayOutApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/payout', data })
}


// 批量重新提交
export const batchRevertPayOutApi = (data: any): Promise<IResponse> => {
  // return request.post({ url: '/yg/pporder/revertpayout', data })
  return request.post({ url: '/yg/pporder/payout', data })
}

// 批量状态检查
export const batchCheckStatusApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/batchcheckstatus', data })
}



// 批量成功
export const batchSuccessApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/batchsuccess', data })
}


// 批量失败
export const batchFailerApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/batchfailer', data })
}


// 批量冲正
export const batchChongZhengApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/batchchongzheng', data })
}



// 补发通知
export const reissueNoticeApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/reissuenotice', data })
}

// 银行出款导出
export const bankExportApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/bankpayexport',  data })
}


// 导入银行代付流水数据
export const importBankDataApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/pporder/importpayout',  data })
}




// 导出数据
export const exportDataApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/yg/pporder/exportexcel`, data })
}

