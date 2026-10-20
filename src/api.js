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
        "token": token ? `Bearer ${token}` : "",
        "Password": password ? password : ""
    };

    const apiBase = import.meta.env.VITE_API_URL || '/api';
    const endpoint = url.startsWith('/') ? url.slice(1) : url;
    const response = await fetch(`${apiBase}/${endpoint}`, {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
        credentials: "include",
        method: "POST",
    });

    if (!response.ok) {
        let errorMessage = `Ошибка ${response.status}`;
        try {
            const errorText = await response.text();
            try {
                const errorData = JSON.parse(errorText);
                errorMessage = errorData.message || errorData.error || errorMessage;
            } catch {
                errorMessage = errorText || errorMessage;
            }
        } catch {
            // keep default status message
        }
        throw new Error(errorMessage);
    }   
    return response.json();
}
