import {useState, useEffect} from "react";
import {getBlogLikeAPI, SLUG, submitBlogLikeAPI} from "./apis";

function App() {
    const [countLike, setCountLike] = useState(null)
    const [isLike, setIsLike] = useState(null)
    const [slug, setSlug] = useState(null)
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
        await submitBlogLikeAPI(
            {
                slug: SLUG
            }
        );
        e.target.className += 'liked';
        setCountLike(countLike + 1);
        setIsLike(true);
    };
    return (
        <div className="App">
            <div onClick={handelCLickLike} className={isLike ? 'like liked': 'like '}> { countLike } Like <i className="bi bi-hand-thumbs-up-fill "></i></div>
        </div>
    );
}

export default App;
