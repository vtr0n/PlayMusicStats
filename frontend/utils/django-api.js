import axios from 'axios';
import {getAccessToken} from './auth';

const BASE_URL = 'http://127.0.0.1:8000';

export {getAuthUrl, confirmCode, getUserInfo, getStats};

function getAuthUrl() {
  const url = `${BASE_URL}/api/v1/get-auth-url`;
  return axios.get(url, {headers: {Authorization: `Bearer ${getAccessToken()}`}}).then(response => response.data);
}

function getUserInfo() {
  const url = `${BASE_URL}/api/v1/user-info`;
  return axios.get(url, {headers: {Authorization: `Bearer ${getAccessToken()}`}}).then(response => response.data);
}

function confirmCode(code) {
  var bodyFormData = new FormData();
  bodyFormData.set('code', code);
  const url = `${BASE_URL}/api/v1/user-info`;
  return axios({
    method: 'PUT',
    url: url,
    headers: {Authorization: `Bearer ${getAccessToken()}`, 'Content-Type': 'application/json',},
    data: bodyFormData
  }).catch(function (error) {
    return error;
  });
}

function getStats() {
  const url = `${BASE_URL}/api/v1/get-stats`;
  return axios.get(url, {headers: {Authorization: `Bearer ${getAccessToken()}`}}).then(response => response.data);
}
