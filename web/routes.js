// routes.js
// Example route:
// "/example": {
//     "title": "Example Page",
//     "template": "example.html",
//     "nav": true,
//     "back": true
// }

const routes = {
    'init': {
        "title": "Initializing...",
        "template": "init.html",
        "nav": false,
        "back": false
    },
    '/': {
        "title": "Home",
        "template": "home.html",
        "nav": true,
        "back": false
    },
    '/settings': {
        "title": "Settings",
        "template": "settings.html",
        "nav": false,
        "back": true
    },
    'login': {
        "title": "Login",
        "template": "login.html",
        "nav": false,
        "back": false
    }
}

export { routes };