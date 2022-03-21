import Link from "next/link";

export default function Blog({ data }) {
    return (
        <div className="mx-auto w-10/12">
            <div
                className="text-center mt-5">
                <a className="underline color text-orange-700" href="{% url 'blog:blog_form' %}">
                    <i className="bi bi-pencil-square mr-2.5"></i>
                    Tạo một bài viết mới
                </a>
            </div>
            <div
                className="text-red-500 text-xl border-b border-solid border-red-500 mb-12 font-bold mt-12">
                DANH SÁCH TRUYỆN TRANH
            </div>
            {data?.ok && data.data.map((value, index) => {
                return (
                    <div key={index} className="row">
                        <div
                            className="p-2.5 flex py-2.5 border border-solid border-gray-500 rounded-md shadow col mb-4">
                            <img className="w-20 h-32 rounded-md"
                                 src="https://static.khoibut.com/img/kb-novel-cover-default.jpg" alt="img"/>
                            <div className="ml-5">
                                <div className="text-xl font-bold text-orange-300">
                                    <Link className="text-orange-300 underline"
                                       href={ `/blog/${value?.slug}` }>{value?.title}</Link>
                                </div>
                                <div>{value?.content}</div>
                                <div className="flex mt-2.5">
                                    <div
                                        className="mr-1.5 bg-green-100 rounded-md text-green-700 py-0.5 px-2.5">
                                        Tản văn
                                    </div>
                                    <div
                                        className="mr-1.5 bg-green-100 rounded-md text-green-700 py-0.5 px-2.5">
                                        2 chương
                                    </div>
                                    <div
                                        className="bg-green-100 rounded-md text-green-700 py-0.5 px-2.5">
                                        Còn tiếp
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}