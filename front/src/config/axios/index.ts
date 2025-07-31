import { service } from './service'

import { config } from './config'

const { default_headers } = config

const request = (option: any) => {
  const { url, method, params, data, headersType, responseType } = option
  // let tmpUrl = url
  // const substr = tmpUrl.substring(0,8)
  // if(substr == 'facespay') {
  //   tmpUrl = "https://pay.faces-pay.com/api"+tmpUrl.substring(8,100)
  //   return service({
  //     url: tmpUrl,
  //     method,
  //     params,
  //     data,
  //     headers: {
  //       'Content-Type': 'application/json'
  //     }
  //   })
  // }

  return service({
    url: url,
    method,
    params,
    data,
    responseType: responseType,
    headers: {
      'Content-Type': headersType || default_headers
    }
  })
}
export default {
  get: <T = any>(option: any) => {
    return request({ method: 'get', ...option }) as unknown as T
  },
  post: <T = any>(option: any) => {
    return request({ method: 'post', ...option }) as unknown as T
  },
  delete: <T = any>(option: any) => {
    return request({ method: 'delete', ...option }) as unknown as T
  },
  put: <T = any>(option: any) => {
    return request({ method: 'put', ...option }) as unknown as T
  }
}
