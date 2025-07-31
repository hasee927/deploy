import request from '@/config/axios'

// 通道列表
export const getChannelListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/channel/getChannelList', params })
}

// 大额代收通道选择项
export const getBigInChannelOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/channel/bigInOptions' })
}

// 小额代收通道选择项
export const getSmallInChannelOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/channel/smallInOptions' })
}

// 大额代付通道选择项
export const getBigPayChannelOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/channel/bigPayOptions' })
}

// 小额代付通道选择项
export const getSmallPayChannelOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/yg/channel/smallPayOptions' })
}


// 根据id获取通道
export const getChannelByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/channel/getChannelById/${dataId}` })
}

// 添加通道
export const addChannelApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/channel/createChannel', data })
}

// 编辑通道
export const editChannelApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/channel/editChannel/${data.id}`, data })
}


// 删除通道
export const delChannelApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/channel/removeChannel', data })
}



