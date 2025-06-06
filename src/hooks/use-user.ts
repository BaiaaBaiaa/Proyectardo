'use client';

import { useEffect, useState } from 'react';

interface User {
  token: string | null;
  email: string | null;
}

export function useUser() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');

    if (token && email) {
      setUser({ token, email });
    } else {
      setUser(null);
    }

    setIsLoading(false);
  }, []);

  return { user, isLoading };
}
