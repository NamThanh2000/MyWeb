import Head from 'next/head'
import {getCategoryForumAPI, submitCreatePostAPI} from '../../apis/userAPI'
import "easymde/dist/easymde.min.css";
import {useState} from "react";
import dynamic from "next/dynamic";
import Select from 'react-select';

const SimpleMdeReact = dynamic(() => import('react-simplemde-editor'), {ssr: false})


export default function Home(props) {
    const [valueContent, setValueContent] = useState("");
    const [valueCategory, setValueCategory] = useState(null);
    const [valueTitle, setValueTitle] = useState("");
    const options = props.data.map(value => (
        {value: value, label: value}
    ))
    const onChange = (value) => {
        setValueContent(value);
    }
    const handleSubmit = () => {
        const category = valueCategory.map(value => (
            value.value
        ))
        submitCreatePostAPI({
            content: valueContent,
            title: valueTitle,
            category: category,
        }).then(r => console.log(r))
    }
    return (<>
        <Head>
            <title>Create Next App</title>
            <meta name="description" content="Generated by create next app"/>
            <link rel="icon" href="/favicon.ico"/>
        </Head>
        <div className="mx-auto w-10/12">
            <form className="w-full max-w-3xl mx-auto my-12">
                <div className="md:flex md:items-center mb-6">
                    <div className="md:w-1/6">
                        <label className="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4"
                               htmlFor="inline-full-name">
                            Tiêu đề
                        </label>
                    </div>
                    <div className="md:w-5/6">
                        <input
                            onChange={e => setValueTitle(e.target.value)}
                            value={valueTitle}
                            className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                            id="inline-full-name" type="text" placeholder="Nhập tiêu đề"/>
                    </div>
                </div>
                <div className="md:flex md:items-center mb-6">
                    <div className="md:w-1/6">
                        <label className="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4"
                               htmlFor="inline-password">
                            Chuyên mục
                        </label>
                    </div>
                    <div className="inline-block relative md:w-5/6">
                        <Select
                            isMulti
                            defaultValue={valueCategory}
                            onChange={setValueCategory}
                            options={options}
                            placeholder="Nhập chuyên mục"
                        />
                    </div>
                </div>
                <SimpleMdeReact
                    value={valueContent}
                    onChange={onChange}/>
                <div className="md:flex md:items-center">
                    <div className="mx-auto w-full">
                        <button
                            onClick={handleSubmit}
                            className="w-full shadow bg-purple-500 hover:bg-purple-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded"
                            type="button">
                            Tạo bài viết
                        </button>
                    </div>
                </div>
            </form>

        </div>
    </>)
}


export async function getStaticProps() {
    const data = await getCategoryForumAPI()
    return {props: data.data}
}