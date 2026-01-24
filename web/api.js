// API Wrapper

class API {
    constructor(token) {
        this.token = token;
        if (!this.authenticate()) {
            throw new Error("Authentication failed");
        } else {
            console.log("Authentication successful");
        }
    }

    authenticate() {
        resp = fetch('/api/authenticate', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        if (resp.status == 200) {
            return true;
        } else {
            return false;
        }
    }

    async get(endpoint, body=null) {
        if (body) {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
        } else {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
        }
        return await resp.json();
    }

    async post(endpoint, body=null) {
        if (body) {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
        } else {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
        }
        return await resp.json();
    }

    async put(endpoint, body=null) {
        if (body) {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
        } else {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
        }
        return await resp.json();
    }

    async delete(endpoint, body=null) {
        if (body) {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
        } else {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
        }
        return await resp.json();
    }
    
    async patch(endpoint, body=null) {
        if (body) {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
        } else {
            resp = await fetch(`/api/${endpoint}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
        }
        return await resp.json();
    }
}

class Me {
    constructor(api) {
        this.api = api;
    }

    async getUserData() {
        data = await this.api.get('iden/user/me')
        this.data = {
            id: data[0],
            username: data[1],
            pname: data[2],
            fname: data[3],
            lname: data[4],
            email: data[5],
            groups: data[6],
            type: data[7],
            ftue_complete: data[8],
            created_at: data[9],
            last_login: data[10]
        }
    }
}

export { API, Me };