export const authClient = {
  getSession: () => {
    const token = localStorage.getItem('token');
    return token ? { token } : null;
  },
  signOut: () => {
    localStorage.removeItem('token');
  },
};

