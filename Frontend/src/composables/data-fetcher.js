import { getToken } from '@/composables/auth-manager'

export async function fetchData(
  API,
  auth_required = false,
  params = null,
  data = null,
  data_type = null,
  method = 'GET'
) {
  var payload = { method: method }
  var headers = {}
  if (auth_required) headers['Authorization'] = getToken()
  if (params) {
    params = new URLSearchParams(params)
    API += `?${params.toString()}`
  }
  if (data) {
    if (data_type == 'form') {
      payload['body'] = data
    } else if (data_type == 'json') {
      headers['Content-Type'] = 'application/json'
      payload['body'] = JSON.stringify(data)
    }
  }
  if (headers) payload['headers'] = headers
  var response = await fetch(API, payload)
  return await response.json()
}
