function data_encode(data) {
    return btoa(JSON.stringify(data))
}

function data_decode(data) {
    return JSON.parse(atob(data))
}

function set_cookie(key, value) {
    document.cookie = key + '=' + value + '; path=/;';
}

function delete_cookie(key) {
    document.cookie = key + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function get_cookie(key) {
    return document.cookie.split("; ")
    .find(cookie => cookie.startsWith(key + "="))
    ?.split("=")[1] || null;
}