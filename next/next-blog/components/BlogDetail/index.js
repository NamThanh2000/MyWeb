import dayjs from "dayjs";
import Link from "next/link";
import {STATIC_SITE_BASE_URL} from "../../constants";
import parse from 'html-react-parser';

export default function Blog(props) {
    return (<>
        <div className="mx-auto w-10/12">
            <div
                className="text-blue-400 mt-24 text-xs">
                <span className="font-bold">ĐANG TRUYEN SANG TAC</span>
                <i className="bi bi-pen"></i>
            </div>
            <div>
                <h1 className="text-3xl mb-5">{props.data.blogDetail.data.title}</h1>
                <div className="border-t border-solid border-gray-500 flex justify-between items-center mb-12">
                    <div className="my-auto mx-2.5 flex justify-center items-center">
                        <div>
                            <div className="font-bold text-lg">{props.data.blogDetail.data.username}</div>
                            <div id="created">{dayjs(props.data.blogDetail.data.created_at).format('DD/MM/YYYY')}</div>
                        </div>
                        <div id="root"></div>
                    </div>
                    <div>
                        <a className="underline"
                           href="">Chỉnh sửa nội dung</a>
                    </div>
                </div>
                <img className="w-full"
                     src="https://blog.vietnovel.com/content/images/size/w2000/2022/02/Pink-and-Green-Elegant-Flower-Shop-Delivery-Instagram-Post.png"
                     alt="img"/>
                <div className="my-12 mx-0">
                    <div id="content">{props.data.blogDetail.data.content}</div>
                </div>
            </div>
            <div
                className="text-red-500 text-xl border-b border-solid border-red-500 mb-12 font-bold">
                DANH
                SÁCH NHỮNG TRUYỆN KHÁC
            </div>
            {props.data.blogDetailList.map((value, index) => {
                return (
                    <div key={index} className="row">
                        <div
                            className="col p-2.5 flex my-2.5 mx-0 border border-solid border-gray-500 rounded-md shadow">
                            <img className="w-20 h-32 rounded-md"
                                 src="https://static.khoibut.com/img/kb-novel-cover-default.jpg" alt="img"/>
                            <div className="ml-5">
                                <div className="text-xl font-bold text-orange-300">
                                    <Link className="text-orange-300 underline"
                                       href={ `${STATIC_SITE_BASE_URL}blog/${value.slug}`}>{value.title}</Link>
                                </div>
                                <div>{ parse(value.content) }</div>
                                <div className="flex mt-2.5">
                                    <div
                                        className="mr-1.5 bg-green-100 rounded-md text text-green-700 py-0.5 px-2.5">
                                        Tản văn
                                    </div>
                                    <div
                                        className="mr-1.5 bg-green-100 rounded-md text text-green-700 py-0.5 px-2.5">
                                        2 chương
                                    </div>
                                    <div
                                        className="bg-green-100 rounded-md text text-green-700 py-0.5 px-2.5">
                                        Còn tiếp
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    </>)
}