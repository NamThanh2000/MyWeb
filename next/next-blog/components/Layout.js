export default function Layout(props) {
    return (
        <div>
            <main>
                <nav className="bg-amber-300">
                    <div className="mx-auto flex justify-between px-2.5 py-2.5 w-10/12">
                        <div className="flex items-center">
                            <a className="no-underline text-gray-600 text-xl ml-5" href="http://127.0.0.1:8000/">
                                <img className="w-24" src="https://static.vietnovel.com/img/svg/origin-logo-black.svg"
                                     alt="img"/>
                            </a>
                        </div>
                        <div className="flex items-center">
                            <div className="mr-2.5">Dark mode</div>
                            <label className="switch mr-2.5">
                                <input type="checkbox" id="darkmode"/>
                                <span className="slider round"></span>
                            </label>
                            <div className="border border-solid border-white rounded-md text-gray-600 py-0.5 px-2.5 flex items-center justify-between">
                                <div>

                                </div>
                            </div>
                            {/*<a className="no-underline text-white bg-amber-500 rounded-md px-5 py-1.5 ml-2.5"*/}
                            {/*   href="">*/}
                            {/*    LOG OUT*/}
                            {/*</a>*/}
                            <a className="no-underline text-white bg-amber-500 rounded-md px-5 py-1.5"
                               href="/login">
                                LOG IN
                            </a>
                            <a className="no-underline text-white bg-amber-500 rounded-md px-5 py-1.5 ml-2.5"
                               href="/register">
                                REGISTER
                            </a>
                        </div>
                    </div>
                </nav>
                {props.children}
            </main>
        </div>
    )
}
