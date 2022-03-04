import {useState, useEffect} from "react";
import {CHECK_LOGIN, getBlogLikeAPI, SLUG, submitBlogLikeAPI} from "./apis";
import toast, { Toaster } from 'react-hot-toast';
import tw, { styled } from 'twin.macro';


let Like = styled.div(({color})=>[
    color ?
        tw`ml-5 cursor-pointer border border-blue-800 border-solid inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-blue-600 rounded-lg focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800` :
        tw`ml-5 cursor-pointer inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800`
]);

function App() {
    const likeSuccess = () => toast('You have successfully liked');
    const likeFail = () => toast('You are not logged in');
    const [countLike, setCountLike] = useState(null)
    const [isLike, setIsLike] = useState(null)
    useEffect(async () => {
        getBlogLikeAPI({
            slug: SLUG
        })
            .then(({ data }) => {
                if (data.ok) {
                    setCountLike(data.data.totalLike)
                    setIsLike(data.data.isLiked)
                }
            })
            .catch(() => {
                console.log("err")
            });
    });
    async function handelCLickLike(e) {
        if(isLike){
            return
        };
        if(CHECK_LOGIN){
            const check_submit_like = await submitBlogLikeAPI(
                {
                    slug: SLUG
                }
            );
            if(check_submit_like.data.ok){
                likeSuccess();
                e.target.className += 'liked';
                setCountLike(countLike + 1);
                setIsLike(true);
            }
        }else {
            likeFail();
        }
    };
    return (
        <div className="App">
            <Like
                onClick={handelCLickLike}
                color={isLike}
            >
                { countLike } Like
                <i className="bi bi-hand-thumbs-up-fill "></i>
            </Like>
            <Toaster />
        </div>
    );
}

export default App;
