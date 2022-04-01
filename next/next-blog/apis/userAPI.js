import axios from 'axios'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

import {
    CURRENT_USER_API,
    BLOG_LIST_API,
    BLOG_DETAIL_API,
    BLOG_DETAIL_LIST_API,
    GET_LOGIN_API,
    SUBMIT_LOGIN_API, GET_CATEGORY_FORUM, SUBMIT_CREATE_POST, SUBMIT_CREATE_POST_FORUM, GET_LIST_POST_FORUM
} from '../constants'

export function currentUserAPI () {
    return axios.get(CURRENT_USER_API)
}

export function getBlogListAPI () {
    return axios.get(`${BLOG_LIST_API}`)
}

export function getBlogDetailAPI (slug) {
    return axios.get(`${BLOG_DETAIL_API}?slug=${slug}`)
}

export function getBlogDetailListAPI (slug) {
    return axios.get(`${BLOG_DETAIL_LIST_API}?slug=${slug}`)
}

export function getLoginAPI () {
    return axios.get(`${GET_LOGIN_API}`)
}

export function submitLoginAPI (data) {
    return axios.post(`${SUBMIT_LOGIN_API}`, data)
}

export function getCategoryForumAPI () {
    return axios.get(`${GET_CATEGORY_FORUM}`)
}

export function submitCreatePostForumAPI (data) {
    return axios.post(`${SUBMIT_CREATE_POST_FORUM}`, data)
}

export function getListPostForumAPI (page) {
    return axios.get(`${GET_LIST_POST_FORUM}?page=${page}`)
}


