import request from '@/config/axios'

// 机器人列表
export const getBotListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/bot/getBotList', params })
}



// 根据id获取机器人
export const getBotByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/bot/getBotById/${dataId}` })
}

// 添加机器人
export const addBotApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/bot/addBot', data })
}

// 编辑机器人
export const editBotApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/bot/editBot/${data.id}`, data })
}


// 删除机器人
export const delBotApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/bot/removeBot', data })
}



