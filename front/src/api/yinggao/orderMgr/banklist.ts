import request from '@/config/axios'



// 获取银行列表
export const getBKListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/bklist/getBKList', params })
}



// // 提交验证码
// export const sumbmitCaptchaApi = (data: any): Promise<IResponse> => {
//   return request.post({ url: '/yg/bklist/manualCaptcha', data})
// }


// // 获取验证码状态
// export const getCaptchaStatusApi = (params: any): Promise<IResponse> => {
//   return request.get({ url: '/yg/bklist/listenErrorMsg', params})
// }

// 上传csv数据
export const imPortCsvDataApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/bklist/importcsv', data})
}


// 获取按钮列表
export const getBtnListApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/btn/getbtnList'})
}

// 根据id获取数据
export const getBtnByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/btn/getBtnById/${dataId}`})
}


// 添加
export const addBtnApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/btn/createbtn', data })
}

// 编辑
export const editBtnApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/btn/editbtn/${data.id}`, data })
}


// 删除
export const delBtnApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/btn/removebtn', data })
}