import axios from "axios";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

export const BLOG_FORM_APIS = window?.BLOG_LIKE_APIS || {}
export const BLOG_FORM_URL = `${BLOG_FORM_APIS?.BASE_URL}${BLOG_FORM_APIS?.GET_BLOG_FORM_API}`
export const BLOG_FORM_EDIT_URL = `${BLOG_FORM_APIS?.BASE_URL}${BLOG_FORM_APIS?.GET_BLOG_FORM_EDIT_API}`
export const SUBMIT_BLOG_FORM_API = `${BLOG_FORM_APIS?.BASE_URL}${BLOG_FORM_APIS?.SUBMIT_BLOG_FORM_API}`
export const SUBMIT_BLOG_FORM_EDIT_API = `${BLOG_FORM_APIS?.BASE_URL}${BLOG_FORM_APIS?.SUBMIT_BLOG_FORM_EDIT_API}`
export const CHECK_LOGIN = BLOG_FORM_APIS?.CHECK_LOGIN
export const BLOG_URL = `${BLOG_FORM_APIS?.BASE_URL}${BLOG_FORM_APIS?.GET_BLOG}`
export const SLUG = BLOG_FORM_APIS?.SLUG

export function getBlogFormAPI () {
    const url =`${BLOG_FORM_URL}`
    return axios.get(url)
}

export function getBlogFormEditAPI () {
    const url =`${BLOG_FORM_EDIT_URL}?slug=${SLUG}`
    return axios.get(url)
}

export function submitBlogFormAPI (body) {
    return axios.post(SUBMIT_BLOG_FORM_API, body)
}

export function submitBlogFormEditAPI (body) {
    return axios.post(SUBMIT_BLOG_FORM_EDIT_API, body)
}
