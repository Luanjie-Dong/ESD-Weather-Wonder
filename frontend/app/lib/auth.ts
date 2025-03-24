
interface UserProfile {
  city: string;
  country: string;
  created_at: Date; 
  email: string;
  state: string;
  user_id: string;
  username: string | null;
};


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