export function isAuthenticated() {
    //check for a valid session/token
    if (typeof window !== 'undefined') {
      return localStorage.getItem('isAuthenticated') === 'true';
    }
    return false;
  }
  
  export function login() {
    if (typeof window !== 'undefined') {
      localStorage.setItem('isAuthenticated', 'true');
    }
  }
  
  export function logout() {
    if (typeof window !== 'undefined') {
      localStorage.setItem('isAuthenticated', 'false');
    }
  }