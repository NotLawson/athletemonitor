// routes.js
// Example route:
// "/example": {
//     "title": "Example Page",
//     "template": "example.html",
//     "nav": true,
//     "back": true
// }

const routes = {
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
    }
}

export { routes };