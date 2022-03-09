import {CKEditor} from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import {useEffect, useState} from "react";
import {SLUG, BLOG_URL, CHECK_LOGIN, getBlogFormAPI, submitBlogFormEditAPI, getBlogFormEditAPI} from "./apis";
import toast, {Toaster} from 'react-hot-toast';
import Select from "./Select";

function AppBlogFormEdit() {
    const [categoryItems, setCategoryItems] = useState([]);
    const [dataTitle, setDataTitle] = useState('');
    const [dataContent, setDataContent] = useState('<p>Viết nội dung tại đây</p>');
    const [dataCategory, setDataCategory] = useState({
        id: 0,
        label: 'Chuyên mục',
        value: 'Category'
    });
    const [dataInitial, setDataInitial] = useState({});
    const [checkSubmit, setCheckSubmit] = useState(false);
    const [isEdit, setIsEdit] = useState(null);
    const submitSuccess = () => toast.success('Chỉnh sửa Blog thành công');
    const submitFailedLogin = () => toast.error("Chỉnh sửa Blog thất bại, vui lòng đăng nhập");
    const submitFailedTitleErr = () => toast.error("Chỉnh sửa Blog thất bại, tiêu đề phải nhiều hơn 3 ký tự và it hơn 200 ký tự");
    const submitFailedContentErr = () => toast.error("Chỉnh sửa Blog thất bại, nội dung không thể để trống");
    const submitFailedCategoryErr = () => toast.error("Chỉnh sửa Blog thất bại, vui lòng chọn chuyên mục");
    const submitFailedTimeOut = () => toast.error("Chỉnh sửa Blog thất bại, Server chưa phản hồi");
    const submitFailedNotChangeInfo = () => toast.error("Chưa có nội dung thay đổi");

    useEffect(() => {
        if (CHECK_LOGIN) {
            getBlogFormEditAPI()
                .then(({data}) => {
                    if (data.ok) {
                        const dataItems = data.data.cate.map((value, key) => {
                            return {
                                id: key + 1,
                                label: value,
                                value: value
                            }
                        })
                        setCategoryItems(dataItems);
                        setDataInitial(data.data.blog);
                        setDataTitle(data.data.blog.title)
                        setDataContent(data.data.blog.content)
                        setDataCategory({
                            id: 0,
                            label: data.data.blog.category,
                            value: data.data.blog.category
                        })
                        setIsEdit(true);
                    } else {
                        setIsEdit(false);
                    }
                })
                .catch(() => {
                    console.log("err")
                });
        }
    }, []);

    useEffect(() => {
        if (dataTitle !== dataInitial.title || dataContent !== dataInitial.content || dataCategory.label !== dataInitial.category)
            setCheckSubmit(true);
        else
            setCheckSubmit(false);
    }, [dataTitle, dataContent, dataCategory]);

    function handleSubmit(e) {
        e.preventDefault();
        if (CHECK_LOGIN) {
            if (!checkSubmit) {
                submitFailedNotChangeInfo();
                return;
            }
            if (dataTitle.trim().length < 3 || dataTitle.trim().length > 200) {
                submitFailedTitleErr();
                return
            }
            if (dataContent.length === 0 || dataContent === '<p>Viết nội dung tại đây</p>') {
                submitFailedContentErr();
                return;
            }
            if(dataCategory.label === 0){
                submitFailedCategoryErr();
                return;
            }
            submitBlogFormEditAPI({
                title: dataTitle,
                category: dataCategory.label,
                content: dataContent,
                slug: SLUG
            }).then(({data}) => {
                if (data.ok) {
                    submitSuccess()
                    setTimeout(() => {
                        window.location.href = `${BLOG_URL}${SLUG}/?page=1`;
                    }, 2000)
                } else
                    submitFailedTimeOut()
            })
        } else
            submitFailedLogin();
    };
    return (
        <div className="AppBlogForm">
            {isEdit === true && (
                <>
                    <div className="w-5/12 m-auto mt-20">
                        <div className="text-center mb-10 italic">Hãy chỉnh sửa nội dung theo ý của bạn</div>
                        <form>
                            <div className="flex justify-end">
                                <Select
                                    //className="flex-1"
                                    options={categoryItems}
                                    selectedOption={dataCategory}
                                    handelChange={(event, id, value) => {
                                        setDataCategory(event);
                                    }}
                                />
                            </div>
                            <div className="relative z-0 mb-6 w-full group mt-10">
                                <input
                                    onChange={(e) => {
                                        setDataTitle(e.target.value)
                                    }}
                                    value={dataTitle}
                                    type="text"
                                    name="floating_email"
                                    className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                                    placeholder=" "
                                    required/>
                                <label
                                    htmlFor="floating_email"
                                    className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">
                                    Tiêu đề
                                </label>
                            </div>
                            <div className="mt-3">
                                <label className="text-gray-500 text-sm">Nội dung</label>
                                <div className="mt-3">
                                    <CKEditor
                                        editor={ClassicEditor}
                                        data={dataContent}
                                        onChange={(event, editor) => {
                                            const data = editor.getData();
                                            setDataContent(data);
                                        }}
                                        onFocus={() => {
                                            if (dataContent === '<p>Viết nội dung tại đây</p>') {
                                                setDataContent('');
                                            }
                                        }}
                                        onBlur={() => {
                                            if (dataContent === '')
                                                setDataContent('<p>Viết nội dung tại đây</p>');
                                        }}
                                    />
                                </div>
                            </div>
                            <div className="flex justify-center mt-10">
                                <button onClick={handleSubmit}
                                        className="text-white bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600 hover:bg-gradient-to-br focus:ring-4 focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2">
                                    Chỉnh sửa Blog
                                </button>
                            </div>
                        </form>
                    </div>
                    <Toaster/>
                </>
            )}
            {isEdit === false && (
                <div className="text-center mt-52">
                    <div id="alert-additional-content-2" className="w-5/12 m-auto p-4 mb-4 bg-red-100 rounded-lg dark:bg-red-200"
                         role="alert">
                        <div className="flex items-center justify-center">
                            <svg className="mr-2 w-5 h-5 text-red-700 dark:text-red-800" fill="currentColor"
                                 viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd"
                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                      clip-rule="evenodd"></path>
                            </svg>
                            <h3 className="text-lg font-medium text-red-700 dark:text-red-800">Bạn không có quyền chỉnh sửa Blog này</h3>
                        </div>
                        <div className="mt-2 mb-4 text-sm text-red-700 dark:text-red-800">
                            Vui vòng đăng nhập tài khoản đã tạo bài viết
                        </div>
                        <div className="flex justify-center">
                            <button onClick={() => {
                                window.location.href = `${BLOG_URL}${SLUG}/?page=1`;
                            }} type="button"
                                    className="text-red-700 bg-transparent border border-red-700 hover:bg-red-800 hover:text-white focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-xs px-3 py-1.5 text-center dark:border-red-800 dark:text-red-800 dark:hover:text-white"
                                    data-collapse-toggle="alert-additional-content-2" aria-label="Close">
                                Quay lại trang bài viết
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default AppBlogFormEdit;
