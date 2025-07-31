import request from '@/config/axios'


export const senderMsgApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/yg/bot/sendmsg', data })
}