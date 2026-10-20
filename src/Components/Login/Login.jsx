import { useState } from "react";
import { apiRequest } from "../../api";
import { useNavigate } from "react-router-dom";
import './login.css';

export default function Login() {
    const navigate = useNavigate();
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleLogin = async () => {
        setError("");
        setIsLoading(true);

        try {
            const data = await apiRequest("login", {
                body: JSON.stringify({ password }),
            });

            // Сохраняем токен и пароль в куки
            // console.log(dt);
            console.log(data);
            
            if(data.token){
                document.cookie = `token=${data.token}; Path=/; Secure; Max-Age=1209600`;
                document.cookie = `password=${encodeURIComponent(password)}; Path=/; Secure; Max-Age=1209600`;
                navigate('/');
            }else{
                setError('Пароль неверный');
            }
            
            // console.log("Успешная авторизация", dt);
            // if(data.status == 200){
            //     // localStorage.setItem('token', dt.token)
            //     document.cookie = `token=${dt.token}; Path=/; Secure; Max-Age=1209600`;
            //     document.cookie = `password=${encodeURIComponent(password)}; Path=/; Secure; Max-Age=1209600`;
            //     navigate('/');
            // }else if(data.status == 404){
            //     setError('Пароль неверный');
            // }
        } catch (err) {
            if (err.message === 'User not found' || err.message === 'Пользователь не найден') {
                setError('Пароль неверный');
            } else {
                setError(err.message);
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="h-screen -mb-10 flex flex-col justify-center items-center">
            <div>
                <div className="text-4xl mx-auto font-medium">
                    Вход в аккаунт
                </div>

                <div className="w-80 h-auto m-auto mt-14">
                    <input
                        className="w-full h-full outline-0 text-xl text-center border-[#8e74ff] border hover:contrast-[0.9] transition-all rounded-xl font-medium py-3 px-6 text-[#8e74ff] bg-[#1e1e1f]"
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                {error && <div className="mt-4 text-red-500 text-center">{error}</div>}

                <button
                    className={`mt-16 py-3 px-24 text-base ${
                        isLoading ? "bg-gray-500" : "bg-[#8e74ff36] hover:bg-[#8e74ff70]"
                    } transition-all`}
                    onClick={handleLogin}
                    disabled={isLoading}
                >
                    {isLoading ? "Загрузка..." : "Войти"}
                </button>
            </div>
        </div>
    );
}
