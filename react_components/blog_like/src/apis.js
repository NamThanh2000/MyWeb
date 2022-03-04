import axios from "axios";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

export const BLOG_LIKE_APIS = window.BLOG_LIKE_APIS || {}
export const BLOG_LIKE_INFO_URL = `${BLOG_LIKE_APIS?.BASE_URL}${BLOG_LIKE_APIS?.GET_BLOG_LIKE_INFO_API}`
export const SUBMIT_BLOG_LIKE_INFO_API = `${BLOG_LIKE_APIS?.BASE_URL}${BLOG_LIKE_APIS?.SUBMIT_BLOG_LIKE_INFO_API}`
export const SLUG = BLOG_LIKE_APIS?.SLUG
export const CHECK_LOGIN = BLOG_LIKE_APIS?.CHECK_LOGIN

export function getBlogLikeAPI (params) {
    return axios.get(`${BLOG_LIKE_INFO_URL}?slug=${params.slug}`)
}

export function submitBlogLikeAPI (body) {
    return axios.post(SUBMIT_BLOG_LIKE_INFO_API, body)
}
