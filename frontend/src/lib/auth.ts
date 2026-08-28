export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
}

export const setToken = (token: string, user: User) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('agro_access_token', token);
    localStorage.setItem('agro_user', JSON.stringify(user));
  }
};

export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('agro_access_token');
  }
  return null;
};

export const getUser = (): User | null => {
  if (typeof window !== 'undefined') {
    const user = localStorage.getItem('agro_user');
    if (user) {
      try {
        return JSON.parse(user) as User;
      } catch (e) {
        return null;
      }
    }
  }
  return null;
};

export const removeToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('agro_access_token');
    localStorage.removeItem('agro_user');
  }
};
