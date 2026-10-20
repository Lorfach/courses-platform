// import { useMyContext } from "./MyContext";

export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
}


export async function apiRequest(url, options = {}) {
    const token = getCookie("token"); // Функция для получения куки токена
    const password = getCookie("password");
    // const { subject } = useMyContext();
    const defaultHeaders = {
        "Content-Type": "application/json",
        "token": token ? `Bearer ${token}` : "", // Отправка токена в заголовках (если нужно)
        "Password": password ? password : ""
    };
    // options.subject = subject;
    // options.body
    // http://localhost:5000/api/
    // https://web-production-0b7b0.up.railway.app/api/
    const response = await fetch('http://localhost:5000/api/' + url, {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
        credentials: "include", // Отправка куки
        method: "POST",
        // 'Access-Control-Allow-Credentials': 'true'
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Ошибка запроса");
    }   
    return response.json();
}
