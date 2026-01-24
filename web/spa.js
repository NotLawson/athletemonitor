// Custom Single Page Application framework here.
// Essentially, changes a main div element with dynamically loaded content, 
// whilst managing the visibility of the navigation bar, back buttons, etc.
// Routes are stored in routes.js

class SPA {
    constructor(routes, mainElement, navElement, backButton, titleElement, defaultTitle) {
        this.routes = routes;
        this.mainElement = mainElement;
        this.navElement = navElement;
        this.backButton = backButton;
        this.titleElement = titleElement;
        this.defaultTitle = defaultTitle;
        
        window.addEventListener('popstate', (event) => {
            this.loadRoute(window.location.pathname);
        });
    }
    loadRoute(path) {
        const route = this.routes[path];
        if (route) {
            fetch(`./templates/${route.template}`)
                .then(response => response.text())
                .then(html => {
                    var doc = new DOMParser().parseFromString(html, "text/html");
                    this.mainElement.innerHTML = doc.getElementsByTagName('main')[0].innerHTML;
                    doc.getElementsByTagName('script').array.forEach(element => {
                        
                    });
                    try {this.mainElement.appendChild(doc.getElementsByTagName('script')[0]);} catch(e) {}
                    this.titleElement.textContent = route.title || this.defaultTitle;
                    this.navElement.style.display = route.nav ? 'flex' : 'none';
                    this.backButton.style.display = route.back ? 'block' : 'none';
                });
            history.pushState({}, route.title, path);
        } else {
            console.error(`Route for path "${path}" not found.`);
        }
    }
}

export { SPA };