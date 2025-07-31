import request from '@/config/axios'

// 群列表
export const getGrouplistApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/group/getGroupList', params })
}



// 根据id获取群
export const getGroupByIdApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/yg/group/getGroupById/${dataId}` })
}

// 添加群
export const addGroupApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/group/addgroup', data })
}

// 编辑群
export const editGroupApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/yg/group/editGroup/${data.id}`, data })
}


// 删除群
export const delGroupApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/yg/group/removeGroup', data })
}



