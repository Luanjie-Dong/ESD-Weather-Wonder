
interface UserProfile {
  id?: string;
  name?: string;
  email?: string;
}

export function isAuthenticated() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('isAuthenticated') === 'true';
    }
    return false;
  }
  
  export function login(profile: UserProfile) {
    if (typeof window !== 'undefined') {
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('user_profile', JSON.stringify(profile));
    }
  }

  export function logout() {
    if (typeof window !== 'undefined') {
      localStorage.setItem('isAuthenticated', 'false');
      localStorage.removeItem('user_profile'); 
    }
  }