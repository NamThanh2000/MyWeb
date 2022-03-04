import {useState, useEffect} from "react";
import {CHECK_LOGIN, getBlogLikeAPI, SLUG, submitBlogLikeAPI} from "./apis";
import toast, { Toaster } from 'react-hot-toast';

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
            <div
                onClick={handelCLickLike}
                className={isLike ? 'like liked': 'like '}
            >
                { countLike } Like
                <i className="bi bi-hand-thumbs-up-fill "></i>
            </div>
            <Toaster />
        </div>
    );
}

export default App;
