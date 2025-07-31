import request from '@/config/axios'


export const getSmsListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/yg/sms/getSmsList', params })
}