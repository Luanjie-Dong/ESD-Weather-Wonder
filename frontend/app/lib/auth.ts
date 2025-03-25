"use client"

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
  if (typeof window === 'undefined') return false; 
  return localStorage.getItem('isAuthenticated') === 'true';
}

export function login(profile: UserProfile) {
  if (typeof window === 'undefined') return; 
  localStorage.setItem('isAuthenticated', 'true');
  localStorage.setItem('user_profile', JSON.stringify(profile));
}

export function logout() {
  if (typeof window === 'undefined') return; 
  localStorage.setItem('isAuthenticated', 'false');
  localStorage.removeItem('user_profile'); 
}