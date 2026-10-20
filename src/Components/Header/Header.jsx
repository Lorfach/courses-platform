import { useCallback } from "react";
import { useNavigate } from "react-router-dom";

const Header = () => {
    let navigate = useNavigate()
    const logout = useCallback(() => {
        document.cookie = 'password=; Max-Age=-99999999;';  
        document.cookie = 'token=; Max-Age=-99999999;';
        navigate('/login')
    }, [])

    const gotoCourses = useCallback(() => {
        navigate('/')
    }, [])
    return (
        <header className="w-full bg-[#1e1e1f]">
            <div className="max-w-[1280px] mx-auto h-16 flex items-center px-6 sm:px-10 md:px-16">
               <div className="h-full flex items-center hover:rotate-[15deg] transition cursor-pointer" onClick={gotoCourses}>
                <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg"><g clipPath="url(#clip0_1480_4696)"><path d="M40.5666 22.8519V20.4095H46.6698V17.3046H36.627V32.5073H42.397C46.0035 32.5073 47.2799 30.6208 47.2799 28.1784V27.179C47.2799 24.8489 46.0035 22.85 42.397 22.85H40.5666V22.8519ZM43.286 28.2345C43.286 29.0674 42.8967 29.4548 42.12 29.4548H40.5666V25.9044H42.12C42.8967 25.9044 43.286 26.2376 43.286 27.0143V28.2345Z" fill="white"></path><path d="M6.65177 17.3196C4.94677 19.0246 3.96233 19.8331 2.27979 20.971V23.55C3.63293 22.6854 4.5107 21.976 5.4652 20.9654C4.45642 25.0716 3.93425 27.9519 3.24177 32.6234L5.88817 32.4456C6.6761 26.4996 7.17581 23.3105 8.42227 17.3196H6.65177Z" fill="white"></path><path d="M28.0347 30.6339C30.3966 30.6339 32.0791 27.31 32.0791 22.5656C32.0791 20.3347 31.1602 19.2417 29.3017 19.2417C27.0053 19.2417 25.2348 22.7172 25.2348 27.2651C25.2348 29.2976 25.9553 30.632 28.0328 30.632L28.0347 30.6339ZM27.9261 32.7113C24.4057 32.7113 22.8317 30.6994 22.8317 27.2894C22.8317 21.2761 25.5211 17.1006 29.4121 17.1006C32.6481 17.1006 34.4841 19.0676 34.4841 22.545C34.4841 28.6238 31.8601 32.7113 27.9242 32.7113H27.9261ZM14.8944 30.6339C17.2563 30.6339 18.9388 27.31 18.9388 22.5656C18.9388 20.3347 18.0199 19.2417 16.1614 19.2417C13.865 19.2417 12.0945 22.7172 12.0945 27.2651C12.0945 29.2976 12.8151 30.632 14.8925 30.632H14.8944V30.6339ZM14.7858 32.7113C11.2654 32.7113 9.69141 30.6994 9.69141 27.2894C9.69141 21.2761 12.3809 17.1006 16.2718 17.1006C19.5078 17.1006 21.3438 19.0676 21.3438 22.545C21.3438 28.6238 18.7199 32.7113 14.7839 32.7113H14.7858Z" fill="white"></path></g><defs><clipPath id="clip0_1480_4696"><rect width="45" height="15.6108" fill="white" transform="translate(2.27979 17.1006)"></rect></clipPath></defs></svg>
               </div>

               <div className="ml-auto h-8 w-8 hover:rotate-[-15deg] hover:cursor-pointer transition" onClick={logout}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="currentColor" className="fill-red-400" viewBox="0 0 16 16">
                        <path fillRule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
                        <path fillRule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
                    </svg>
               </div>
            </div>
        </header>
    )
};

export default Header;
